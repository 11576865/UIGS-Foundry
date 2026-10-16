#!/usr/bin/env python3
"""Compare two pinned Code Atlas runtime traces; differences are not causes.

The output contains bounded evidence summaries and omits raw exception messages,
snapshot values, absolute paths, and run timestamps.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from itertools import zip_longest
from pathlib import Path

MAX_INPUT_BYTES = 6_000_000
MAX_DETAILS = 50
VALID_STATUS = {"completed", "failed"}


def load_trace(path: Path) -> dict:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("trace exceeds size limit")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_pair(a: dict, b: dict) -> tuple[str, str]:
    for item in (a, b):
        if item.get("schema_version") != 1 or item.get("kind") != "python_runtime_trace":
            raise ValueError("unsupported runtime evidence")
        if item.get("status") not in VALID_STATUS:
            raise ValueError("trace execution outcome missing")
        if not isinstance(item.get("repository"), str) or not item["repository"]:
            raise ValueError("repository identity missing")
        if not isinstance(item.get("revision"), str) or not re.fullmatch(r"[0-9a-f]{40}", item["revision"]):
            raise ValueError("commit-pinned trace required")
        if item.get("stats", {}).get("truncated") or item.get("annotations", {}).get("truncated"):
            raise ValueError("truncated trace is not comparable")
        if not isinstance(item.get("operation_calls"), list) or not isinstance(item.get("annotations", {}).get("events"), list):
            raise ValueError("operation evidence missing")
    if (a["repository"], a["revision"]) != (b["repository"], b["revision"]):
        raise ValueError("repository or revision mismatch")
    return a["repository"], a["revision"]


def scoped(trace: dict, operation_name: str) -> tuple[list[dict], Counter]:
    events = trace["annotations"]["events"]
    roots = [e for e in events if e.get("kind") == "operation_begin"
             and e.get("parent_id") is None and e.get("name") == operation_name]
    if len(roots) != 1:
        raise ValueError("expected exactly one matching top-level operation")
    root_id = roots[0].get("operation_id")
    if not isinstance(root_id, str) or not root_id:
        raise ValueError("missing operation identity")
    ids = {root_id}
    for e in events:
        if e.get("kind") == "operation_begin" and e.get("parent_id") in ids:
            ids.add(e.get("operation_id"))
    normalized = []
    for e in events:
        if e.get("operation_id") not in ids:
            continue
        detail = e.get("detail") or {}
        normalized.append({
            "kind": e.get("kind"), "name": e.get("name"),
            "subject": e.get("subject"),
            "verdict": detail.get("verdict"),
            "operation": "root" if e.get("operation_id") == root_id else "nested",
        })
    calls = Counter()
    for e in trace["operation_calls"]:
        if e.get("operation_id") not in ids:
            continue
        count = e.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            raise ValueError("invalid observed call count")
        key = (e.get("from"), e.get("to"), e.get("path"), e.get("line"))
        if not isinstance(key[0], str) or not isinstance(key[1], str):
            raise ValueError("invalid source symbols")
        calls[key] += count
    return normalized, calls


def compare(a: dict, b: dict, operation_name: str) -> dict:
    repo, rev = validate_pair(a, b)
    left_events, left_calls = scoped(a, operation_name)
    right_events, right_calls = scoped(b, operation_name)
    first = None
    for pos, (left, right) in enumerate(zip_longest(left_events, right_events)):
        if left != right:
            first = {"index": pos, "baseline": left, "candidate": right}
            break
    changed = []
    for key in sorted(left_calls.keys() | right_calls.keys(), key=str):
        before = left_calls[key]
        after = right_calls[key]
        if before != after:
            src, dst, path, line = key
            changed.append({"from": src, "to": dst, "path": path,
                            "line": line, "baseline_count": before,
                            "candidate_count": after})
    return {
        "schema_version": 1, "kind": "code_atlas_runtime_comparison",
        "repository": repo, "revision": rev, "operation_name": operation_name,
        "baseline_status": a["status"], "candidate_status": b["status"],
        "baseline_exception_type": a.get("exception_type"),
        "candidate_exception_type": b.get("exception_type"),
        "status_changed": a["status"] != b["status"],
        "first_observed_event_difference": first,
        "changed_call_sites": changed[:MAX_DETAILS],
        "changed_call_sites_total": len(changed),
        "changed_call_sites_truncated": len(changed) > MAX_DETAILS,
        "baseline_event_count": len(left_events),
        "candidate_event_count": len(right_events),
        "scope": "one named top-level operation; call-site counts and explicit annotations",
        "interpretation": "observed differences, not earliest causal divergence or proof of defect origin",
        "limitations": [
            "Both inputs must be pinned to identical clean-repository commits",
            "Only explicitly annotated operation trees and captured Python calls are compared",
            "Events from concurrent tasks may interleave; ordering is observational",
            "The first observed event difference is not the first cause",
            "Profile sampling can omit C calls, subprocess effects, earlier threads and unexecuted paths",
            "Exception class and operation status do not prove full correctness",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two pinned Code Atlas operation traces")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = compare(load_trace(args.baseline), load_trace(args.candidate), args.operation)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.error(f"invalid comparison evidence: {type(exc).__name__}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Compared {args.operation}: status_changed={report['status_changed']}, "
          f"changed_call_sites={report['changed_call_sites_total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
