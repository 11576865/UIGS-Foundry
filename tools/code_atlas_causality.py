#!/usr/bin/env python3
"""Explicit, bounded operation annotations for Code Atlas runtime evidence.

Annotation means the running program emitted this event; it does not prove
that a state or effect was independently verified.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from threading import Lock, get_ident
from time import monotonic_ns
from typing import Iterator

_ACTIVE: ContextVar["Recorder | None"] = ContextVar("uigs_atlas_recorder", default=None)
_OPERATION: ContextVar[str | None] = ContextVar("uigs_atlas_operation", default=None)
KINDS = frozenset({"action", "state_write", "side_effect", "checkpoint"})


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

    def emit(self, kind: str, name: str, operation_id: str | None, parent_id: str | None = None, *, subject: str | None = None):
        with self._lock:
            if len(self.events) >= self.max_events:
                self.truncated = True
                return False
            item = {"seq": len(self.events) + 1, "kind": kind, "name": name,
                    "operation_id": operation_id, "parent_id": parent_id,
                    "monotonic_ns": monotonic_ns(), "thread_id": get_ident()}
            if subject is not None:
                item["subject"] = subject
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
