#!/usr/bin/env python3
"""Explicit, bounded operation annotations for Code Atlas runtime evidence.

Annotation means the running program emitted this event; it does not prove
that a state or effect was independently verified.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import os
import stat
from pathlib import Path
import json
from collections.abc import Callable
from contextvars import ContextVar
from threading import Lock, get_ident
from time import monotonic_ns
from typing import Iterator

_ACTIVE: ContextVar["Recorder | None"] = ContextVar("uigs_atlas_recorder", default=None)
_OPERATION: ContextVar[str | None] = ContextVar("uigs_atlas_operation", default=None)
KINDS = frozenset({"action", "state_write", "side_effect", "checkpoint"})
MAX_SNAPSHOT_BYTES = 65536


class Recorder:
    def __init__(self, max_events: int = 2000):
        if max_events < 1:
            raise ValueError("max_events must be positive")
        self.max_events = max_events
        self.events: list[dict] = []
        self.truncated = False
        self._next_id = 0
        self._lock = Lock()

    def start(self, name: str, parent: str | None) -> str:
        with self._lock:
            self._next_id += 1
            ident = f"op-{self._next_id}"
        self.emit("operation_begin", name, ident, parent)
        return ident

    def emit(self, kind: str, name: str, operation_id: str | None, parent_id: str | None = None, *, subject: str | None = None, detail: dict | None = None):
        with self._lock:
            if len(self.events) >= self.max_events:
                self.truncated = True
                return False
            item = {"seq": len(self.events) + 1, "kind": kind, "name": name,
                    "operation_id": operation_id, "parent_id": parent_id,
                    "monotonic_ns": monotonic_ns(), "thread_id": get_ident()}
            if subject is not None:
                item["subject"] = subject
            if detail is not None:
                item["detail"] = detail
            self.events.append(item)
            return True

    def report(self) -> dict:
        return {"collector": "explicit_contextvars_annotations", "events": list(self.events),
                "truncated": self.truncated, "event_limit": self.max_events,
                "limitations": [
                    "Annotations are claims emitted by the instrumented code, not independently verified state changes",
                    "Async tasks inherit context at creation; threads do not inherit context automatically",
                    "Only explicitly instrumented operations and events appear; missing events do not imply absent effects",
                    "Timestamps are monotonic within one process and are not globally synchronized clocks",
                    "Only chosen JSON values are compared; no system-wide state/cause proof",
                ]}


@contextmanager
def collect(max_events: int = 2000) -> Iterator[Recorder]:
    rec = Recorder(max_events)
    token = _ACTIVE.set(rec)
    parent = _OPERATION.set(None)
    try:
        yield rec
    finally:
        _OPERATION.reset(parent)
        _ACTIVE.reset(token)


def current_operation() -> str | None:
    return _OPERATION.get()


@contextmanager
def operation(name: str):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("operation name must not be empty")
    recorder = _ACTIVE.get()
    if recorder is None:
        yield None
        return
    parent_id = current_operation()
    ident = recorder.start(name, parent_id)
    token = _OPERATION.set(ident)
    try:
        yield ident
    except BaseException as exc:
        recorder.emit("operation_error", type(exc).__name__, ident, parent_id)
        raise
    else:
        recorder.emit("operation_end", name, ident, parent_id)
    finally:
        _OPERATION.reset(token)


def mark(kind: str, name: str, *, subject: str | None = None) -> bool:
    if kind not in KINDS:
        raise ValueError(f"unsupported annotation kind: {kind}")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("event name must not be empty")
    if subject is not None and not isinstance(subject, str):
        raise ValueError("subject must be a string")
    recorder = _ACTIVE.get()
    if recorder is None:
        return False
    return recorder.emit(kind, name, current_operation(), subject=subject)


@contextmanager
def observe_state(subject: str, read_state: Callable[[], object]):
    """Compare two snapshots; emit verdict only (no raw values in evidence)."""
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("state subject must be non-empty")
    if not callable(read_state):
        raise TypeError("read_state must be callable")
    recorder = _ACTIVE.get()
    if recorder is None:
        yield None
        return
    ident = current_operation()

    def snapshot():
        try:
            payload = json.dumps(read_state(), sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":"), allow_nan=False)
            if len(payload.encode("utf-8")) > MAX_SNAPSHOT_BYTES:
                return None, "size_limit"
            return payload, None
        except Exception:
            return None, "probe_error"

    before, before_error = snapshot()
    try:
        yield None
    finally:
        after, after_error = snapshot()
        verdict = "unknown" if before_error or after_error else ("changed" if before != after else "unchanged")
        detail = {"verdict": verdict, "method": "json_before_after"}
        if before_error:
            detail["before_status"] = before_error
        if after_error:
            detail["after_status"] = after_error
        recorder.emit("state_delta", "probe comparison", ident, subject=subject, detail=detail)



MAX_FILE_PROBE_BYTES = 1024 * 1024


def _sample_file(path: Path, max_bytes: int):
    """Read a selected ordinary file without exporting its content or digest.

    The snapshot is a short-lived internal value; unknown covers unsafe types,
    races, changed-during-read files and inspection errors.
    """
    try:
        initial = os.lstat(path)
    except FileNotFoundError:
        return ("absent", None), None
    except OSError:
        return None, "access_error"
    if stat.S_ISLNK(initial.st_mode):
        return None, "symlink"
    if not stat.S_ISREG(initial.st_mode):
        return None, "not_regular"
    if initial.st_size > max_bytes:
        return None, "size_limit"
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError:
        return None, "access_error"
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or (before.st_dev, before.st_ino) != (initial.st_dev, initial.st_ino):
            return None, "file_replaced"
        if before.st_size > max_bytes:
            return None, "size_limit"
        digest = hashlib.sha256()
        size = 0
        while True:
            block = os.read(fd, min(65536, max_bytes + 1 - size))
            if not block:
                break
            size += len(block)
            if size > max_bytes:
                return None, "size_limit"
            digest.update(block)
        after = os.fstat(fd)
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_size, after.st_mtime_ns, after.st_ctime_ns) or size != after.st_size:
            return None, "changed_during_read"
        return ("file", size, digest.digest()), None
    except OSError:
        return None, "access_error"
    finally:
        os.close(fd)


@contextmanager
def observe_file(subject: str, path: os.PathLike[str] | str, *, max_bytes: int = MAX_FILE_PROBE_BYTES):
    """Record a bounded before/after file-content verdict for an explicit path.

    This observer does not write the target file, run it, follow initial
    symlinks, or export its path, bytes, hashes, or error messages.
    It cannot prove why a change occurred.
    """
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("file subject must not be empty")
    target = Path(path)
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or not 1 <= max_bytes <= MAX_FILE_PROBE_BYTES:
        raise ValueError("max_bytes must be between 1 and 1048576")
    recorder = _ACTIVE.get()
    if recorder is None:
        yield None
        return
    operation_id = current_operation()
    first, first_error = _sample_file(target, max_bytes)
    try:
        yield None
    finally:
        second, second_error = _sample_file(target, max_bytes)
        if first_error or second_error:
            verdict = "unknown"
        elif first[0] == "absent" and second[0] == "file":
            verdict = "created"
        elif first[0] == "file" and second[0] == "absent":
            verdict = "removed"
        else:
            verdict = "unchanged" if first == second else "modified"
        detail = {"verdict": verdict, "method": "bounded_sha256_before_after",
                  "max_bytes": max_bytes}
        if first_error:
            detail["before_status"] = first_error
        if second_error:
            detail["after_status"] = second_error
        recorder.emit("file_delta", "file content comparison", operation_id,
                      subject=subject, detail=detail)
