#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "knowledge" / "claims"
EVIDENCE = ROOT / "knowledge" / "evidence"
CHANGES = ROOT / "knowledge" / "changes"
OUT_JSON = ROOT / "reports" / "generated" / "epistemic-state.json"
OUT_MD = ROOT / "reports" / "generated" / "epistemic-state.md"

HIGH_MATURITY = {"validated", "canonical"}
PERMANENT_OPS = {"revise", "contract", "demote", "deprecate", "supersede"}


def load_json_files(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    out: list[tuple[Path, dict[str, Any]]] = []
    if not root.exists():
        return out
    for path in sorted(root.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
        out.append((path, data))
    return out


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def validate_graph(
    claims: dict[str, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
    changes: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []

    for cid, claim in claims.items():
        if claim.get("id") != cid:
            errors.append(f"{cid}: key/id mismatch")
        deps = [str(x) for x in claim.get("depends_on", [])]
        if cid in deps:
            errors.append(f"{cid}: claim cannot depend on itself")
        for dep in deps:
            if dep not in claims:
                errors.append(f"{cid}: missing dependency {dep}")
        for eid in claim.get("evidence_refs", []):
            if eid not in evidence:
                errors.append(f"{cid}: missing evidence {eid}")
        replacement = claim.get("superseded_by")
        if replacement and replacement not in claims:
            errors.append(f"{cid}: missing superseding claim {replacement}")
        if claim.get("authority") == "superseded" and not replacement:
            errors.append(f"{cid}: superseded authority requires superseded_by")
        policy = claim.get("support_policy", {})
        minimum = int(policy.get("minimum_independent_support", 0))
        maturity = str(claim.get("maturity", ""))
        if maturity == "canonical" and minimum < 2:
            errors.append(f"{cid}: canonical claim must require >=2 independent support groups")
        if maturity == "validated" and minimum < 1:
            errors.append(f"{cid}: validated claim must require >=1 independent support group")
        review = claim.get("review") if isinstance(claim.get("review"), dict) else {}
        if maturity == "canonical":
            if not review.get("approved_by"):
                errors.append(f"{cid}: canonical claim missing review.approved_by")
            if not review.get("rationale"):
                errors.append(f"{cid}: canonical claim missing review.rationale")

    for eid, item in evidence.items():
        if item.get("id") != eid:
            errors.append(f"{eid}: key/id mismatch")
        for rel in item.get("relations", []):
            cid = str(rel.get("claim_id", ""))
            if cid not in claims:
                errors.append(f"{eid}: relation references missing claim {cid}")
            elif eid not in claims[cid].get("evidence_refs", []):
                errors.append(f"{eid}: {cid} relation is not listed in claim.evidence_refs")
            result = rel.get("result")
            defeater = rel.get("defeater_type")
            if result == "contradicts" and defeater == "none":
                errors.append(f"{eid}: contradiction must declare rebutting or undercutting defeater")
            if result != "contradicts" and defeater != "none":
                errors.append(f"{eid}: non-contradiction evidence must use defeater_type=none")
        prov = item.get("provenance") if isinstance(item.get("provenance"), dict) else {}
        for parent in prov.get("was_derived_from", []):
            if parent == eid:
                errors.append(f"{eid}: evidence cannot derive from itself")
            elif parent not in evidence:
                errors.append(f"{eid}: missing provenance ancestor {parent}")

    for change_id, change in changes.items():
        if change.get("id") != change_id:
            errors.append(f"{change_id}: key/id mismatch")
        target = str(change.get("target_claim", ""))
        if target not in claims:
            errors.append(f"{change_id}: missing target claim {target}")
        for eid in change.get("evidence_refs", []):
            if eid not in evidence:
                errors.append(f"{change_id}: missing evidence {eid}")
        operation = str(change.get("operation", ""))
        decided_by = str(change.get("decided_by", ""))
        if operation in PERMANENT_OPS and decided_by == "automation":
            errors.append(f"{change_id}: automation cannot perform permanent operation {operation}")
        replacement = change.get("replacement_claim")
        if replacement and replacement not in claims:
            errors.append(f"{change_id}: missing replacement claim {replacement}")

    return errors


def relation_rows(
    claim_id: str,
    evidence: dict[str, dict[str, Any]],
    as_of: datetime,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    for eid, item in evidence.items():
        valid_until = parse_time(item.get("valid_until"))
        effective_stale = item.get("status") != "active" or (valid_until is not None and valid_until < as_of)
        for rel in item.get("relations", []):
            if rel.get("claim_id") != claim_id:
                continue
            row = {
                "evidence_id": eid,
                "independence_key": str(item.get("independence_key", eid)),
                "result": str(rel.get("result", "")),
                "defeater_type": str(rel.get("defeater_type", "none")),
                "directness": str(rel.get("directness", "")),
                "status": str(item.get("status", "")),
            }
            (stale if effective_stale else active).append(row)
    return active, stale


def base_state(
    cid: str,
    claim: dict[str, Any],
    evidence: dict[str, dict[str, Any]],
    as_of: datetime,
) -> dict[str, Any]:
    active, stale = relation_rows(cid, evidence, as_of)
    supports = [x for x in active if x["result"] == "supports"]
    contradicts = [x for x in active if x["result"] == "contradicts"]
    support_groups = sorted({x["independence_key"] for x in supports})
    contradiction_groups = sorted({x["independence_key"] for x in contradicts})
    minimum = int(claim.get("support_policy", {}).get("minimum_independent_support", 0))
    assumption_challenge = any(
        str(a.get("status")) == "challenged"
        for a in claim.get("assumptions", [])
        if isinstance(a, dict)
    )

    reasons: list[str] = []
    if contradicts and supports:
        epistemic = "mixed"
        reasons.append("active supporting and contradicting evidence coexist")
    elif contradicts:
        epistemic = "contradicted"
        reasons.append("active contradicting evidence exists")
    elif assumption_challenge:
        epistemic = "challenged"
        reasons.append("one or more assumptions are challenged")
    elif len(support_groups) >= minimum and (support_groups or minimum == 0):
        epistemic = "supported"
    elif stale and not supports:
        epistemic = "stale"
        reasons.append("referenced evidence is stale/retracted/superseded or expired")
    elif supports:
        epistemic = "challenged"
        reasons.append(
            f"independent support below policy minimum ({len(support_groups)}/{minimum})"
        )
    else:
        epistemic = "unknown"
        reasons.append("no active supporting evidence")

    declared_authority = str(claim.get("authority", "active"))
    effective_authority = declared_authority
    policy = claim.get("support_policy", {})

    if declared_authority == "active":
        if contradicts and bool(policy.get("quarantine_on_active_contradiction", False)):
            effective_authority = "quarantined"
            reasons.append("automatic quarantine: active contradiction")
        elif assumption_challenge:
            effective_authority = "quarantined"
            reasons.append("automatic quarantine: challenged assumption")
        elif (
            str(claim.get("maturity")) in HIGH_MATURITY
            and minimum > 0
            and len(support_groups) < minimum
            and bool(claim.get("evidence_refs"))
        ):
            effective_authority = "quarantined"
            reasons.append("automatic quarantine: high-maturity support requirement no longer met")

    return {
        "id": cid,
        "statement": claim.get("statement"),
        "maturity": claim.get("maturity"),
        "declared_authority": declared_authority,
        "effective_authority": effective_authority,
        "stored_epistemic_state": claim.get("epistemic_state"),
        "effective_epistemic_state": epistemic,
        "support_groups": support_groups,
        "contradiction_groups": contradiction_groups,
        "active_support_count": len(supports),
        "active_contradiction_count": len(contradicts),
        "stale_relation_count": len(stale),
        "broken_dependencies": [],
        "review_required": bool(
            effective_authority != declared_authority
            or epistemic != claim.get("epistemic_state")
        ),
        "reasons": reasons,
    }


def evaluate(root: Path = ROOT, as_of: datetime | None = None) -> dict[str, Any]:
    as_of = as_of or now_utc()
    claim_files = load_json_files(root / "knowledge" / "claims")
    evidence_files = load_json_files(root / "knowledge" / "evidence")
    change_files = load_json_files(root / "knowledge" / "changes")

    claims = {str(data.get("id")): data for _, data in claim_files}
    evidence = {str(data.get("id")): data for _, data in evidence_files}
    changes = {str(data.get("id")): data for _, data in change_files}

    errors = validate_graph(claims, evidence, changes)
    states = {cid: base_state(cid, claim, evidence, as_of) for cid, claim in claims.items()}

    changed = True
    passes = 0
    while changed and passes <= max(1, len(states)):
        changed = False
        passes += 1
        for cid, claim in claims.items():
            state = states[cid]
            broken: list[str] = []
            for dep in claim.get("depends_on", []):
                dep_state = states.get(dep)
                if not dep_state:
                    continue
                if dep_state["effective_authority"] in {"quarantined", "deprecated", "superseded"}:
                    broken.append(dep)
                elif dep_state["effective_epistemic_state"] in {
                    "challenged",
                    "contradicted",
                    "stale",
                }:
                    broken.append(dep)
            broken = sorted(set(broken))
            if broken != state["broken_dependencies"]:
                state["broken_dependencies"] = broken
                changed = True
            if broken:
                if state["effective_epistemic_state"] not in {"contradicted", "mixed"}:
                    if state["effective_epistemic_state"] != "challenged":
                        state["effective_epistemic_state"] = "challenged"
                        changed = True
                if (
                    state["declared_authority"] == "active"
                    and bool(claim.get("support_policy", {}).get("quarantine_on_broken_dependency", False))
                    and state["effective_authority"] != "quarantined"
                ):
                    state["effective_authority"] = "quarantined"
                    changed = True
                reason = "dependency requires review: " + ", ".join(broken)
                if reason not in state["reasons"]:
                    state["reasons"].append(reason)
                state["review_required"] = True

    return {
        "schema_version": 1,
        "generated_at": as_of.isoformat(),
        "summary": {
            "claims": len(claims),
            "evidence": len(evidence),
            "changes": len(changes),
            "validation_errors": len(errors),
            "review_required": sum(1 for x in states.values() if x["review_required"]),
            "effectively_quarantined": sum(
                1 for x in states.values() if x["effective_authority"] == "quarantined"
            ),
        },
        "validation_errors": errors,
        "claims": [states[cid] for cid in sorted(states)],
    }


def markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        "# UIGS Epistemic State",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Claims: {s['claims']}",
        f"- Evidence records: {s['evidence']}",
        f"- Knowledge changes: {s['changes']}",
        f"- Validation errors: {s['validation_errors']}",
        f"- Review required: {s['review_required']}",
        f"- Effectively quarantined: {s['effectively_quarantined']}",
        "",
        "## Claims",
        "",
        "| Claim | Maturity | Declared authority | Effective authority | Epistemic state | Support groups | Contradiction groups | Review |",
        "| --- | --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in report["claims"]:
        lines.append(
            "| {id} | {maturity} | {declared_authority} | {effective_authority} | "
            "{effective_epistemic_state} | {supports} | {contradicts} | {review} |".format(
                id=item["id"],
                maturity=item["maturity"],
                declared_authority=item["declared_authority"],
                effective_authority=item["effective_authority"],
                effective_epistemic_state=item["effective_epistemic_state"],
                supports=len(item["support_groups"]),
                contradicts=len(item["contradiction_groups"]),
                review="yes" if item["review_required"] else "no",
            )
        )
    if report["validation_errors"]:
        lines.extend(["", "## Validation errors", ""])
        lines.extend(f"- {x}" for x in report["validation_errors"])
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- Maturity is governance history, not current truth.",
            "- Effective authority is the value consumers must use.",
            "- Automatic quarantine is reversible and does not silently demote maturity.",
            "- Raw artifact count is not independent evidence count.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--as-of", default="")
    args = parser.parse_args()

    as_of = parse_time(args.as_of) if args.as_of else None
    report = evaluate(ROOT, as_of)
    if args.check:
        if report["validation_errors"]:
            for error in report["validation_errors"]:
                print(f"epistemic graph error: {error}")
            return 1
        print(
            "epistemic graph passed: "
            f"claims={report['summary']['claims']} "
            f"evidence={report['summary']['evidence']} "
            f"review_required={report['summary']['review_required']} "
            f"quarantined={report['summary']['effectively_quarantined']}"
        )
        return 0

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(report), encoding="utf-8")
    print(OUT_JSON.relative_to(ROOT))
    print(OUT_MD.relative_to(ROOT))
    return 1 if report["validation_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
