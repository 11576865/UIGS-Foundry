#!/usr/bin/env python3
"""Opt-in, bounded in-process Python call observation for UIGS Code Atlas.

Only observed Python->Python calls with both endpoints inside the supplied root
are recorded. This tool executes the selected script with its usual side effects.
It cannot establish complete execution coverage or correctness.
"""
from __future__ import annotations

import argparse
import json
import re
import runpy
import subprocess
import sys
import threading
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

MAX_EVENTS = 100_000


def clean_revision(root: Path) -> str | None:
    try:
        sha = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL, timeout=4, text=True,
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"],
            stderr=subprocess.DEVNULL, timeout=4,
        )
        return sha if re.fullmatch(r"[0-9a-f]{40}", sha) and not dirty else None
    except (OSError, subprocess.SubprocessError):
        return None


def frame_symbol(frame, root: Path) -> str | None:
    code = frame.f_code
    qual = code.co_qualname
    if code.co_name == "<module>" or "<locals>" in qual or "<" in qual:
        return None
    try:
        path = Path(code.co_filename).resolve().relative_to(root)
    except (ValueError, OSError):
        return None
    if path.suffix != ".py":
        return None
    return f"fn:{path.as_posix()}:{qual}"


def observe(root: Path, action: Callable[[], object], *, repo: str | None = None,
            max_events: int = MAX_EVENTS) -> dict:
    """Observe one explicit callable, restoring profiling hooks even on error.

    Captures current thread and new Python threads only; previous threads,
    C-level calls, subprocesses, and unidentifiable nested functions are out of scope.
    """
    root = root.resolve()
    if not root.is_dir() or max_events < 1:
        raise ValueError("root must exist and max_events must be positive")
    revision_before = clean_revision(root)
    counts: Counter[tuple[str, str, str, int]] = Counter()
    n_events = 0
    unmapped = 0
    truncated = False
    previous = sys.getprofile()
    previous_threads = threading.getprofile()

    def collector(frame, event, arg):
        nonlocal n_events, unmapped, truncated
        if event != "call":
            return
        if n_events >= max_events:
            truncated = True
            return
        n_events += 1
        caller = frame.f_back
        if caller is None:
            unmapped += 1
            return
        source = frame_symbol(caller, root)
        target = frame_symbol(frame, root)
        if source is None or target is None:
            unmapped += 1
            return
        rel = source.removeprefix("fn:").rsplit(":", 1)[0]
        counts[(source, target, rel, caller.f_lineno)] += 1

    try:
        sys.setprofile(collector)
        threading.setprofile(collector)
        action()
    finally:
        sys.setprofile(previous)
        threading.setprofile(previous_threads)

    revision_after = clean_revision(root)
    revision = revision_before if revision_before == revision_after else None
    calls = [
        {"from": src, "to": dst, "kind": "runtime_calls",
         "evidence": "python_profile_observed", "path": path,
         "line": line, "count": count}
        for (src, dst, path, line), count in sorted(counts.items())
    ]
    return {
        "schema_version": 1, "kind": "python_runtime_trace",
        "repository": repo, "revision": revision,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "collector": "sys.setprofile", "status": "completed",
        "limitations": [
            "Only calls executed during this explicit run are observed",
            "Existing threads, subprocesses and C calls are not traced",
            "Nested/local functions are not mapped to current static graph",
            "Observed calls are not evidence of correctness or full coverage",
        ],
        "calls": calls,
        "stats": {"profile_calls": n_events, "mapped_sites": len(calls),
                  "unmapped_events": unmapped, "truncated": truncated},
    }


def enrich_static(graph: dict, trace: dict) -> dict:
    """Add scoped observed call edges only where both AST symbols exist."""
    if graph.get("schema_version") != 1 or trace.get("schema_version") != 1:
        raise ValueError("unsupported Code Atlas graph or trace version")
    if trace.get("kind") != "python_runtime_trace":
        raise ValueError("unsupported trace kind")
    if graph.get("repository") != trace.get("repository"):
        raise ValueError("repository mismatch between graph and trace")
    if graph.get("revision") != trace.get("revision"):
        raise ValueError("revision mismatch between graph and trace")
    ids = {n["id"] for n in graph["nodes"]}
    known = []
    missing = []
    for edge in trace.get("calls", []):
        if edge.get("from") in ids and edge.get("to") in ids:
            known.append(edge)
        else:
            missing.append({"from": edge.get("from"), "to": edge.get("to")})
    result = {**graph, "nodes": list(graph["nodes"]),
              "edges": list(graph["edges"]) + known,
              "runtime_trace": {
                  "observed_at": trace.get("observed_at"),
                  "collector": trace.get("collector"),
                  "anchored": bool(graph.get("revision")),
                  "mapped_edges": len(known),
                  "unmatched_edges": len(missing),
                  "unmatched_samples": missing[:20],
                  "truncated": bool(trace.get("stats", {}).get("truncated")),
              }}
    result["stats"] = {**graph["stats"], "runtime_edges": len(known),
                       "runtime_unmatched_edges": len(missing)}
    result["limitations"] = list(graph.get("limitations", [])) + list(trace.get("limitations", []))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Opt-in Python runtime evidence for UIGS Code Atlas")
    parser.add_argument("--root", type=Path, required=True, help="Root of checked-out repository")
    parser.add_argument("--repo", default=None)
    parser.add_argument("--script", type=Path, required=True,
                        help="Explicit Python entrypoint to RUN (may have side effects)")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-events", type=int, default=MAX_EVENTS)
    args, script_args = parser.parse_known_args()
    script_args = script_args[1:] if script_args[:1] == ["--"] else script_args
    root = args.root.resolve()
    script = (root / args.script).resolve()
    if not script.is_relative_to(root) or not script.is_file() or script.suffix != ".py":
        parser.error("--script must be a Python file inside --root")
    original_argv = sys.argv[:]
    original_path = sys.path[:]

    def action():
        sys.argv = [str(script), *script_args]
        sys.path.insert(0, str(script.parent))
        try:
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    raise
        finally:
            sys.argv = original_argv
            sys.path[:] = original_path

    report = observe(root, action, repo=args.repo, max_events=args.max_events)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"runtime evidence: {report['stats']}; written {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
