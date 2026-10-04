#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intake_state

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "generated"

BUG_LIFECYCLES = {
    "recorded",
    "repair-evidenced",
    "validation-pending",
    "regression-verified",
    "recurring",
    "superseded",
}
ENFORCEMENT_STATUSES = {"submitted", "enforced-main", "deprecated"}


def load_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_files(root: Path, name: str) -> list[Path]:
    base = root / "inbox" / name
    return sorted(base.glob("*.md")) if base.exists() else []


def parse_bug_lifecycle(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^Lifecycle:\s*([^\s]+)\s*$", text)
    return match.group(1) if match else "unclassified"


def count_json_files(path: Path) -> int:
    return sum(1 for _ in path.rglob("*.json")) if path.exists() else 0


def triage_coverage(root: Path, pending: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    records = []
    base = root / "outbox" / "triage"
    if base.exists():
        for path in sorted(base.rglob("*.json")):
            try:
                item = load_json(path, {})
            except Exception:
                continue
            if isinstance(item, dict):
                records.append(item)

    pending_ids = {
        str(item.get("packet_id", ""))
        for _, item in pending
        if str(item.get("packet_id", ""))
    }
    triaged_ids = {
        str(item.get("packet_id", ""))
        for item in records
        if str(item.get("packet_id", ""))
    }
    statuses = Counter(
        str(item.get("triage_status", "unknown"))
        for item in records
        if str(item.get("packet_id", "")) in pending_ids
    )
    return {
        "records": len(records),
        "triaged_pending": len(pending_ids & triaged_ids),
        "untriaged_pending": len(pending_ids - triaged_ids),
        "status_counts": dict(sorted(statuses.items())),
    }


def open_proposals(root: Path) -> tuple[int, int]:
    base = root / "outbox" / "proposals"
    proposals = []
    if base.exists():
        for path in sorted(base.rglob("*.json")):
            try:
                proposals.append(load_json(path, {}))
            except Exception:
                continue
    reviewed = intake_state.reviewed_packet_ids(root)
    open_count = sum(
        1 for item in proposals
        if str(item.get("packet_id", "")) not in reviewed
    )
    return len(proposals), open_count


def catalog_statuses(root: Path) -> tuple[int, Counter[str]]:
    catalog = load_json(root / "catalog" / "index.json", {}) or {}
    entries = list(catalog.get("patterns", [])) + list(catalog.get("records", []))
    return len(entries), Counter(str(item.get("status", "unknown")) for item in entries)


def prevention_state(root: Path) -> dict[str, Any]:
    registry = load_json(root / "prevention" / "registry.json", {"entries": []}) or {"entries": []}
    entries = list(registry.get("entries", []))
    status_counts: Counter[str] = Counter()
    enforced_entries = 0
    submitted_entries = 0
    unguarded_entries = 0
    recurring_entries = 0
    recurrence_total = 0

    for entry in entries:
        controls = entry.get("enforcement", []) if isinstance(entry, dict) else []
        statuses = {
            str(control.get("status", "unknown"))
            for control in controls
            if isinstance(control, dict)
        }
        for status in statuses:
            status_counts[status] += 1
        if "enforced-main" in statuses:
            enforced_entries += 1
        elif "submitted" in statuses:
            submitted_entries += 1
        else:
            unguarded_entries += 1
        recurrence = int(entry.get("recurrence_count", 0) or 0)
        recurrence_total += recurrence
        if recurrence > 0:
            recurring_entries += 1

    return {
        "entries": len(entries),
        "enforced_entries": enforced_entries,
        "submitted_entries": submitted_entries,
        "unguarded_entries": unguarded_entries,
        "recurring_entries": recurring_entries,
        "recurrence_total": recurrence_total,
        "control_status_counts": dict(sorted(status_counts.items())),
    }


def build_snapshot(root: Path = ROOT) -> dict[str, Any]:
    bug_paths = markdown_files(root, "bugs")
    lifecycle_counts = Counter(parse_bug_lifecycle(path) for path in bug_paths)
    unclassified = [
        path.relative_to(root).as_posix()
        for path in bug_paths
        if parse_bug_lifecycle(path) == "unclassified"
    ]

    pending_packets = intake_state.pending_packets(root, open_only=False)
    pending_total = len(pending_packets)
    pending_unreviewed = len(intake_state.pending_packets(root, open_only=True))
    triage = triage_coverage(root, pending_packets)
    proposals_total, proposals_open = open_proposals(root)
    catalog_total, status_counts = catalog_statuses(root)

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "inbox": {
            "bugs": len(bug_paths),
            "candidates": len(markdown_files(root, "candidates")),
            "observations": len(markdown_files(root, "observations")),
            "cases": len(markdown_files(root, "cases")),
            "tests": len(markdown_files(root, "tests")),
        },
        "bug_lifecycle": {
            "counts": dict(sorted(lifecycle_counts.items())),
            "unclassified": unclassified,
            "note": "Bug records are durable evidence and are not an unresolved-product-bug count.",
        },
        "intake": {
            "pending_total": pending_total,
            "pending_unreviewed": pending_unreviewed,
            "triage_records": triage["records"],
            "triaged_pending": triage["triaged_pending"],
            "untriaged_pending": triage["untriaged_pending"],
            "triage_status_counts": triage["status_counts"],
            "proposals_total": proposals_total,
            "proposals_open": proposals_open,
            "reviews": len(intake_state.review_items(root)),
            "typed_records": count_json_files(root / "intake" / "records"),
        },
        "catalog": {
            "total": catalog_total,
            "status_counts": dict(sorted(status_counts.items())),
        },
        "prevention": prevention_state(root),
    }


def render_markdown(snapshot: dict[str, Any]) -> str:
    inbox = snapshot["inbox"]
    bug = snapshot["bug_lifecycle"]
    intake = snapshot["intake"]
    catalog = snapshot["catalog"]
    prevention = snapshot["prevention"]

    lines = [
        "# UIGS Knowledge Health",
        "",
        f"Generated: {snapshot['generated_at']}",
        "",
        "## Intake and knowledge inventory",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Bug records | {inbox['bugs']} |",
        f"| Candidates | {inbox['candidates']} |",
        f"| Observations | {inbox['observations']} |",
        f"| Cases | {inbox['cases']} |",
        f"| Durable Pending packets | {intake['pending_total']} |",
        f"| Pending packets without review decision | {intake['pending_unreviewed']} |",
        f"| Pending packets with triage record | {intake['triaged_pending']} |",
        f"| Pending packets not yet triaged | {intake['untriaged_pending']} |",
        f"| Triage records total | {intake['triage_records']} |",
        f"| Promotion proposals (total / open) | {intake['proposals_total']} / {intake['proposals_open']} |",
        f"| Typed intake records | {intake['typed_records']} |",
        f"| Catalog entries | {catalog['total']} |",
        "",
        "## Bug evidence lifecycle",
        "",
        "Bug records are historical/reusable evidence. Their count is **not** the count of unresolved product defects.",
        "",
    ]
    counts = bug["counts"]
    lines += [f"- {key}: {value}" for key, value in sorted(counts.items())] or ["- none"]
    if bug["unclassified"]:
        lines += [
            "",
            "Unclassified Bug records:",
            *[f"- {path}" for path in bug["unclassified"]],
        ]

    lines += [
        "",
        "## Prevention coverage",
        "",
        f"- Registered prevention rules: {prevention['entries']}",
        f"- Enforced on source main: {prevention['enforced_entries']}",
        f"- Submitted but not yet main-enforced: {prevention['submitted_entries']}",
        f"- No executable guard registered: {prevention['unguarded_entries']}",
        f"- Rules with recorded recurrence: {prevention['recurring_entries']}",
        f"- Total recorded recurrences: {prevention['recurrence_total']}",
        "",
        "Prevention coverage tracks executable controls separately from prose knowledge. A Bug or Candidate document alone is not counted as enforcement.",
        "",
        "## Catalog maturity",
        "",
    ]
    lines += [f"- {key}: {value}" for key, value in sorted(catalog["status_counts"].items())] or ["- none"]
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "- A high Bug/Candidate count can reflect stronger observation and capture rather than lower product quality.",
        "- The Pending directory is durable intake storage: a packet may already be triaged while remaining under Pending.",
        "- Untriaged Pending and open review proposals are stronger backlog signals than the raw Pending count.",
        "- Review/proposal backlog measures governance debt, not source-product defect count.",
        "- `submitted` prevention controls are not counted as enforced until the source main contains the control.",
        "- Recurrence is tracked separately because repeated failure after prior knowledge is evidence of prevention/enforcement debt.",
        "",
    ]
    return "\n".join(lines)


def write_reports(root: Path = ROOT) -> dict[str, Any]:
    snapshot = build_snapshot(root)
    out = root / "reports" / "generated"
    out.mkdir(parents=True, exist_ok=True)
    (out / "knowledge-health.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "knowledge-health.md").write_text(render_markdown(snapshot), encoding="utf-8")
    return snapshot


def main() -> int:
    snapshot = write_reports(ROOT)
    print(
        "knowledge-health: "
        f"bugs={snapshot['inbox']['bugs']} "
        f"untriaged={snapshot['intake']['untriaged_pending']} "
        f"prevention={snapshot['prevention']['entries']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
