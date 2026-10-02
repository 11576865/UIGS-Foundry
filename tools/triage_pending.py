#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PENDING_ROOT = ROOT / "outbox" / "pending"
TRIAGE_ROOT = ROOT / "outbox" / "triage"
RULES_PATH = ROOT / "triage" / "red-reason-rules.json"
LINK_RULES_PATH = ROOT / "triage" / "related-knowledge-rules.json"

FIELD_WEIGHT = {
    "conclusion": 1.0,
    "step": 1.0,
    "job": 0.82,
    "workflow": 0.58,
    "text": 0.42,
}

def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def packet_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def text_fields(packet: dict[str,Any]) -> dict[str,list[str]]:
    evidence = packet.get("evidence") if isinstance(packet.get("evidence"),dict) else {}
    failed_jobs = evidence.get("failed_jobs") if isinstance(evidence.get("failed_jobs"),list) else []
    failed_steps = evidence.get("failed_steps") if isinstance(evidence.get("failed_steps"),list) else []
    return {
        "conclusion":[str(evidence.get("conclusion",""))],
        "workflow":[str(evidence.get("workflow",""))],
        "job":[str(x.get("name","")) if isinstance(x,dict) else str(x) for x in failed_jobs],
        "step":[str(x.get("name","")) if isinstance(x,dict) else str(x) for x in failed_steps],
        "text":[str(packet.get("title","")),str(packet.get("summary",""))],
    }

def classify_ci(packet: dict[str,Any], rules: dict[str,Any]) -> dict[str,Any]:
    fields = text_fields(packet)
    scores: dict[str,float] = {}
    signals: dict[str,list[str]] = {}
    matched: dict[str,list[str]] = {}

    for rule in rules.get("rules",[]):
        try:
            regex = re.compile(str(rule["pattern"]), re.IGNORECASE)
        except re.error:
            continue
        category = str(rule.get("category","unknown"))
        for field in rule.get("fields",[]):
            for value in fields.get(field,[]):
                if value and regex.search(value):
                    weight = FIELD_WEIGHT.get(field,0.3)
                    scores[category] = scores.get(category,0.0) + weight
                    signals.setdefault(category,[]).append(f"{field}:{value}")
                    matched.setdefault(category,[]).append(str(rule.get("id","rule")))
                    break

    if not scores:
        return {"category":"unknown","confidence":0.0,"needs_review":True,"signals":[],"matched_rules":[]}

    ordered = sorted(scores.items(), key=lambda kv:(-kv[1],kv[0]))
    category, top = ordered[0]
    second = ordered[1][1] if len(ordered)>1 else 0.0
    ambiguous = second > 0 and (top-second) < 0.20

    if top >= 1.0:
        confidence = 0.92
    elif top >= 0.82:
        confidence = 0.82
    elif top >= 0.58:
        confidence = 0.68
    else:
        confidence = 0.56
    if ambiguous:
        confidence = min(confidence,0.50)

    return {
        "category":category,
        "confidence":round(confidence,2),
        "needs_review": bool(ambiguous or confidence < 0.75),
        "signals": sorted(set(signals.get(category,[]))),
        "matched_rules": sorted(set(matched.get(category,[]))),
    }

def related_records(packet: dict[str,Any], category: str | None, rules: dict[str,Any]) -> list[str]:
    if not category or category == "unknown":
        return []
    repo = str(packet.get("source_repository",""))
    result: list[str] = []
    for rule in rules.get("rules",[]):
        if rule.get("repository") != repo:
            continue
        if category not in rule.get("categories",[]):
            continue
        for record in rule.get("records",[]):
            if record not in result:
                result.append(record)
    return result

def triage_packet(packet: dict[str,Any], packet_hash: str, rules: dict[str,Any], links: dict[str,Any]) -> dict[str,Any]:
    record_type = str(packet.get("record_type",""))
    if record_type == "ci_failure":
        red = classify_ci(packet,rules)
        status = "auto-classified" if not red["needs_review"] and red["category"]!="unknown" else "needs-review"
        category = red["category"]
    else:
        red = None
        status = "ready-for-record"
        category = None

    return {
        "schema_version":1,
        "packet_id":str(packet.get("packet_id","")),
        "source_repository":str(packet.get("source_repository","")),
        "packet_sha256":packet_hash,
        "triage_status":status,
        "record_type":record_type,
        "routing_hints":sorted(set(str(x) for x in packet.get("routing_hints",[]) if str(x))),
        "red_reason":red,
        "related_records":related_records(packet,category,links),
        "created_at":str(packet.get("created_at","")),
        "triaged_at":now(),
    }

def output_path(packet_path: Path, packet: dict[str,Any], root: Path = ROOT) -> Path:
    repo = re.sub(r"[^A-Za-z0-9._-]+","__",str(packet.get("source_repository","unknown"))).strip("._-") or "unknown"
    return root / "outbox" / "triage" / repo / f"{packet.get('packet_id','unknown')}.json"

def run(root: Path = ROOT) -> tuple[int,int]:
    pending_root = root/"outbox"/"pending"
    rules = load(root/"triage"/"red-reason-rules.json")
    links = load(root/"triage"/"related-knowledge-rules.json")
    changed=0; total=0
    if not pending_root.exists():
        return 0,0
    for path in sorted(pending_root.rglob("*.json")):
        total += 1
        packet = load(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        out = output_path(path,packet,root)
        if out.is_file():
            old = load(out)
            if old.get("packet_sha256") == digest:
                continue
        record = triage_packet(packet,digest,rules,links)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        changed += 1
    return total,changed

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.parse_args()
    total,changed=run()
    print(f"triage pending: packets={total}, changed={changed}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
