#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intake_state

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "reports" / "generated" / "review-queue.json"
OUT_MD = ROOT / "reports" / "generated" / "review-queue.md"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json_records(base: Path) -> list[tuple[Path, dict[str, Any]]]:
    out: list[tuple[Path, dict[str, Any]]] = []
    if not base.exists():
        return out
    for path in sorted(base.rglob("*.json")):
        try:
            item = load(path)
        except Exception:
            continue
        if isinstance(item, dict):
            out.append((path, item))
    return out


def pending_by_id(root: Path) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("packet_id", "")): item
        for _, item in intake_state.pending_packets(root, open_only=False)
        if str(item.get("packet_id", ""))
    }


def proposals_by_packet(root: Path) -> dict[str, dict[str, Any]]:
    result = {}
    for _, item in load_json_records(root / "outbox" / "proposals"):
        packet_id = str(item.get("packet_id", ""))
        if packet_id:
            result[packet_id] = item
    return result


def triage_records(root: Path) -> list[dict[str, Any]]:
    return [item for _, item in load_json_records(root / "outbox" / "triage")]


def review_family_key(triage: dict[str, Any], packet: dict[str, Any]) -> tuple[str, ...]:
    red = triage.get("red_reason") if isinstance(triage.get("red_reason"), dict) else {}
    evidence = packet.get("evidence") if isinstance(packet.get("evidence"), dict) else {}
    workflow = str(evidence.get("workflow", "")).strip() or "unknown-workflow"
    category = str(red.get("category", "unknown")).strip() or "unknown"
    matched = ",".join(sorted(str(x) for x in red.get("matched_rules", []) if str(x))) or "no-rule"
    related = ",".join(sorted(str(x) for x in triage.get("related_records", []) if str(x))) or "no-related-record"
    return (
        str(triage.get("source_repository", "unknown")),
        workflow,
        category,
        matched,
        related,
    )


def build_snapshot(root: Path = ROOT) -> dict[str, Any]:
    pending = pending_by_id(root)
    reviewed = intake_state.reviewed_packet_ids(root)
    proposals = proposals_by_packet(root)
    triage = triage_records(root)

    triage_status_counts = Counter(str(item.get("triage_status", "unknown")) for item in triage)
    open_proposals = [
        item for packet_id, item in proposals.items()
        if packet_id not in reviewed
    ]

    families: dict[tuple[str, ...], list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    orphan_needs_review: list[str] = []

    for item in triage:
        packet_id = str(item.get("packet_id", ""))
        if packet_id in reviewed:
            continue
        if str(item.get("triage_status", "")) != "needs-review":
            continue
        packet = pending.get(packet_id)
        if not packet:
            orphan_needs_review.append(packet_id)
            continue
        families[review_family_key(item, packet)].append((item, packet))

    family_rows = []
    for key, members in families.items():
        repo, workflow, category, matched, related = key
        created = sorted(
            str(packet.get("created_at", ""))
            for _, packet in members
            if str(packet.get("created_at", ""))
        )
        confidences = []
        for triage_item, _ in members:
            red = triage_item.get("red_reason") if isinstance(triage_item.get("red_reason"), dict) else {}
            value = red.get("confidence")
            if isinstance(value, (int, float)):
                confidences.append(float(value))
        packet_ids = sorted(str(packet.get("packet_id", "")) for _, packet in members)
        family_rows.append({
            "source_repository": repo,
            "workflow": workflow,
            "category": category,
            "matched_rules": [] if matched == "no-rule" else matched.split(","),
            "related_records": [] if related == "no-related-record" else related.split(","),
            "count": len(members),
            "confidence_min": min(confidences) if confidences else None,
            "confidence_max": max(confidences) if confidences else None,
            "oldest_at": created[0] if created else "",
            "latest_at": created[-1] if created else "",
            "sample_packet_ids": packet_ids[:5],
        })
    family_rows.sort(key=lambda x: (-int(x["count"]), x["source_repository"], x["workflow"], x["category"]))

    proposal_rows = []
    for proposal in sorted(
        open_proposals,
        key=lambda x: (str(x.get("source_repository", "")), str(x.get("packet_id", ""))),
    ):
        suggested = proposal.get("suggested_record") if isinstance(proposal.get("suggested_record"), dict) else {}
        proposal_rows.append({
            "packet_id": str(proposal.get("packet_id", "")),
            "source_repository": str(proposal.get("source_repository", "")),
            "suggested_type": str(suggested.get("type", "")),
            "suggested_id": str(suggested.get("id", "")),
            "title": str(suggested.get("title", "")),
            "dedupe_candidates": proposal.get("dedupe_candidates", []),
        })

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": {
            "pending_packets": len(pending),
            "triage_records": len(triage),
            "needs_review_packets": sum(row["count"] for row in family_rows) + len(orphan_needs_review),
            "needs_review_families": len(family_rows),
            "open_proposals": len(proposal_rows),
            "reviewed_packets": len(reviewed),
            "orphan_needs_review": len(orphan_needs_review),
        },
        "triage_status_counts": dict(sorted(triage_status_counts.items())),
        "needs_review_families": family_rows,
        "open_proposals": proposal_rows,
        "orphan_needs_review_packet_ids": sorted(orphan_needs_review),
    }


def render_markdown(snapshot: dict[str, Any]) -> str:
    s = snapshot["summary"]
    lines = [
        "# UIGS Review Queue",
        "",
        f"Generated: {snapshot['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Durable Pending packets: {s['pending_packets']}",
        f"- Triage records: {s['triage_records']}",
        f"- Needs-review packets: {s['needs_review_packets']}",
        f"- Needs-review families after grouping: {s['needs_review_families']}",
        f"- Open promotion proposals: {s['open_proposals']}",
        f"- Reviewed packets: {s['reviewed_packets']}",
        "",
        "Raw Pending count is durable storage. This report narrows review work to unresolved triage families and explicit open promotion proposals.",
        "",
        "## Needs-review CI families",
        "",
    ]

    families = snapshot["needs_review_families"]
    if not families:
        lines.append("- none")
    else:
        lines += [
            "| Count | Repository | Workflow | Category | Matched rules | Related knowledge |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
        for row in families:
            rules = ", ".join(row["matched_rules"]) or "—"
            related = ", ".join(row["related_records"]) or "—"
            lines.append(
                f"| {row['count']} | {row['source_repository']} | {row['workflow']} | "
                f"{row['category']} | {rules} | {related} |"
            )

    lines += ["", "## Open promotion proposals", ""]
    proposals = snapshot["open_proposals"]
    if not proposals:
        lines.append("- none")
    else:
        for row in proposals:
            dedupe = row["dedupe_candidates"]
            suffix = f"; dedupe candidates: {len(dedupe)}" if dedupe else ""
            lines.append(
                f"- `{row['packet_id']}` — {row['suggested_type']} — {row['title']}{suffix}"
            )

    if snapshot["orphan_needs_review_packet_ids"]:
        lines += ["", "## Integrity warning", ""]
        lines += [
            f"- needs-review triage without Pending packet: `{packet_id}`"
            for packet_id in snapshot["orphan_needs_review_packet_ids"]
        ]

    lines += [
        "",
        "## Review boundary",
        "",
        "- Grouping is operational deduplication only; it does not assert identical root cause.",
        "- A family count is not a Bug count and does not create reusable knowledge automatically.",
        "- Promotion still requires explicit accept/reject review.",
        "- Canonical promotion remains governed separately by `governance/PROMOTION.md`.",
        "",
    ]
    return "\n".join(lines)


def write_reports(root: Path = ROOT) -> dict[str, Any]:
    snapshot = build_snapshot(root)
    out = root / "reports" / "generated"
    out.mkdir(parents=True, exist_ok=True)
    (out / "review-queue.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "review-queue.md").write_text(render_markdown(snapshot), encoding="utf-8")
    return snapshot


def main() -> int:
    snapshot = write_reports(ROOT)
    summary = snapshot["summary"]
    print(
        "review-queue: "
        f"needs_review_packets={summary['needs_review_packets']} "
        f"families={summary['needs_review_families']} "
        f"open_proposals={summary['open_proposals']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
