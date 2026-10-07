#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

BUG_LIFECYCLES={"recorded","repair-evidenced","validation-pending","regression-verified","recurring","superseded"}
ENFORCEMENT_STATUSES={"submitted","enforced-main","deprecated"}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None

seen_ids: dict[str,str] = {}
for path in sorted(ROOT.rglob("*.json")):
    data=load(path)
    if data is None:
        continue
    rel=path.relative_to(ROOT).as_posix()
    record_id=data.get("id") if isinstance(data,dict) else None
    if record_id and rel != "catalog/index.json":
        if record_id in seen_ids:
            errors.append(f"duplicate id {record_id}: {seen_ids[record_id]} and {rel}")
        else:
            seen_ids[record_id]=rel
    if "/registry/patterns/" in f"/{rel}":
        for key in ("id","type","status","name","intent","constraints","provenance"):
            if key not in data:
                errors.append(f"{rel}: missing {key}")
        if data.get("type") != "pattern":
            errors.append(f"{rel}: type must be pattern")
        if not str(data.get("id","")).startswith("UIGS."):
            errors.append(f"{rel}: id must start UIGS.")
    if "/bug-museum/" in f"/{rel}":
        for key in ("id","type","status","title","symptom","root_cause","resolution","regression_guard","provenance"):
            if key not in data:
                errors.append(f"{rel}: missing bug field {key}")
        if data.get("type") != "bug":
            errors.append(f"{rel}: bug type must be bug")
    if rel.startswith("projects/") and rel.endswith(".project.json"):
        for key in ("project","repository","authority","intake"):
            if key not in data:
                errors.append(f"{rel}: missing project manifest field {key}")
    if rel.startswith("outbox/pending/"):
        for key in ("packet_version","packet_id","status","record_type","title","summary","source_repository","source_event","created_at","dedupe_key"):
            if key not in data:
                errors.append(f"{rel}: missing intake packet field {key}")
        if data.get("status") != "pending":
            errors.append(f"{rel}: imported outbox packet must remain pending")


claim_ids: set[str] = set()
for path in sorted((ROOT/"knowledge"/"claims").glob("*.json")) if (ROOT/"knowledge"/"claims").exists() else []:
    data=load(path)
    if not isinstance(data,dict):
        continue
    rel=path.relative_to(ROOT).as_posix()
    for key in ("schema_version","id","statement","kind","maturity","authority","epistemic_state","scope","assumptions","evidence_refs","depends_on","support_policy","created_at","updated_at"):
        if key not in data:
            errors.append(f"{rel}: missing Claim field {key}")
    cid=str(data.get("id",""))
    if not cid.startswith("CLAIM."):
        errors.append(f"{rel}: Claim id must start CLAIM.")
    if cid:
        claim_ids.add(cid)

for path in sorted((ROOT/"knowledge"/"evidence").glob("*.json")) if (ROOT/"knowledge"/"evidence").exists() else []:
    data=load(path)
    if not isinstance(data,dict):
        continue
    rel=path.relative_to(ROOT).as_posix()
    for key in ("schema_version","id","status","source","observed_at","independence_key","relations"):
        if key not in data:
            errors.append(f"{rel}: missing Evidence field {key}")
    if not str(data.get("id","")).startswith("EVID."):
        errors.append(f"{rel}: Evidence id must start EVID.")

for path in sorted((ROOT/"knowledge"/"changes").glob("*.json")) if (ROOT/"knowledge"/"changes").exists() else []:
    data=load(path)
    if not isinstance(data,dict):
        continue
    rel=path.relative_to(ROOT).as_posix()
    for key in ("schema_version","id","target_claim","operation","reason","evidence_refs","decided_by","decided_at"):
        if key not in data:
            errors.append(f"{rel}: missing Knowledge Change field {key}")
    if not str(data.get("id","")).startswith("CHANGE."):
        errors.append(f"{rel}: Knowledge Change id must start CHANGE.")

for path in sorted((ROOT/"domains"/"interface-grammar"/"registry"/"patterns").glob("*.json")) if (ROOT/"domains"/"interface-grammar"/"registry"/"patterns").exists() else []:
    data=load(path)
    if not isinstance(data,dict):
        continue
    for ref in data.get("claim_refs",[]) if isinstance(data.get("claim_refs",[]),list) else []:
        if str(ref) not in claim_ids:
            errors.append(f"{path.relative_to(ROOT)}: missing Claim reference {ref}")

for path in sorted((ROOT/"inbox"/"bugs").glob("*.md")) if (ROOT/"inbox"/"bugs").exists() else []:
    text=path.read_text(encoding="utf-8")
    rel=path.relative_to(ROOT).as_posix()
    lifecycle=None
    for line in text.splitlines():
        if line.startswith("Lifecycle:"):
            lifecycle=line.split(":",1)[1].strip()
            break
    if not lifecycle:
        errors.append(f"{rel}: missing Lifecycle")
    elif lifecycle not in BUG_LIFECYCLES:
        errors.append(f"{rel}: invalid Lifecycle {lifecycle}")

prevention=load(ROOT/"prevention"/"registry.json") if (ROOT/"prevention"/"registry.json").is_file() else None
if prevention:
    if prevention.get("schema_version") != 2:
        errors.append("prevention/registry.json: schema_version must be 2")
    seen_prevention=set()
    seen_recurrence=set()
    for entry in prevention.get("entries",[]):
        pid=str(entry.get("id",""))
        if not pid.startswith("PREVENT."):
            errors.append(f"prevention/registry.json: invalid prevention id {pid}")
        if pid in seen_prevention:
            errors.append(f"prevention/registry.json: duplicate prevention id {pid}")
        seen_prevention.add(pid)
        refs=entry.get("knowledge_refs",[])
        if not isinstance(refs,list):
            errors.append(f"{pid}: knowledge_refs must be a list")
            refs=[]
        for ref in refs:
            if not (ROOT/str(ref)).is_file():
                errors.append(f"{pid}: missing knowledge ref {ref}")
        generation=entry.get("enforcement_generation")
        if not isinstance(generation,int) or generation < 1:
            errors.append(f"{pid}: enforcement_generation must be a positive integer")
            generation=0
        effectiveness=str(entry.get("effectiveness_claim_ref",""))
        if effectiveness not in claim_ids:
            errors.append(f"{pid}: missing effectiveness Claim {effectiveness}")
        if effectiveness and not effectiveness.endswith(f".G{generation}"):
            errors.append(f"{pid}: effectiveness_claim_ref must target current generation {generation}")
        controls=entry.get("enforcement",[])
        if not isinstance(controls,list):
            errors.append(f"{pid}: enforcement must be a list")
            controls=[]
        for control in controls:
            if not isinstance(control,dict):
                errors.append(f"{pid}: enforcement item must be an object")
                continue
            status=str(control.get("status",""))
            if status not in ENFORCEMENT_STATUSES:
                errors.append(f"{pid}: invalid enforcement status {status}")
            if not str(control.get("project","")):
                errors.append(f"{pid}: enforcement item missing project")
            if not str(control.get("kind","")):
                errors.append(f"{pid}: enforcement item missing kind")
            cg=control.get("generation")
            if not isinstance(cg,int) or cg < 1 or cg > generation:
                errors.append(f"{pid}: enforcement item has invalid generation {cg}")
        events=entry.get("recurrence_events",[])
        if not isinstance(events,list):
            errors.append(f"{pid}: recurrence_events must be a list")
            events=[]
        for event in events:
            if not isinstance(event,dict):
                errors.append(f"{pid}: recurrence event must be an object")
                continue
            rid=str(event.get("id",""))
            if not rid.startswith("RECURRENCE."):
                errors.append(f"{pid}: invalid recurrence event id {rid}")
            if rid in seen_recurrence:
                errors.append(f"{pid}: duplicate recurrence event id {rid}")
            seen_recurrence.add(rid)
            eg=event.get("generation")
            if not isinstance(eg,int) or eg < 1 or eg > generation:
                errors.append(f"{pid}: recurrence {rid} has invalid generation {eg}")
            source_ref=str(event.get("source_ref",""))
            if not source_ref or not (ROOT/source_ref).is_file():
                errors.append(f"{pid}: recurrence {rid} missing source_ref {source_ref}")
            evid=str(event.get("evidence_ref",""))
            evidence_path=ROOT/"knowledge"/"evidence"/f"{evid}.json"
            if not evid.startswith("EVID.PREVENT.") or not evidence_path.is_file():
                errors.append(f"{pid}: recurrence {rid} missing Evidence {evid}")
            status=str(event.get("status",""))
            if status not in {"active","addressed"}:
                errors.append(f"{pid}: recurrence {rid} invalid status {status}")
            resolved=event.get("resolved_by_generation")
            if status=="active" and resolved is not None:
                errors.append(f"{pid}: active recurrence {rid} cannot have resolved_by_generation")
            if status=="addressed" and (not isinstance(resolved,int) or not isinstance(eg,int) or resolved <= eg or resolved > generation):
                errors.append(f"{pid}: addressed recurrence {rid} requires a later valid resolved_by_generation")
        legacy=entry.get("legacy_unattributed_recurrence_count",0)
        recurrence=entry.get("recurrence_count",0)
        if not isinstance(legacy,int) or legacy < 0:
            errors.append(f"{pid}: legacy_unattributed_recurrence_count must be a non-negative integer")
            legacy=0
        if not isinstance(recurrence,int) or recurrence < 0:
            errors.append(f"{pid}: recurrence_count must be a non-negative integer")
        elif recurrence != legacy + len(events):
            errors.append(f"{pid}: recurrence_count must equal attributed events + legacy unattributed count")

catalog=load(ROOT/"catalog/index.json")
if catalog:
    ids=set()
    for section in ("patterns","records"):
        for item in catalog.get(section,[]):
            item_id=item.get("id",""); target=item.get("path","")
            if item_id in ids:
                errors.append(f"catalog/index.json: duplicate catalog id {item_id}")
            ids.add(item_id)
            if not (ROOT/target).is_file():
                errors.append(f"catalog/index.json: missing target {target}")
    for target in catalog.get("projects",[]):
        if not (ROOT/target).is_file():
            errors.append(f"catalog/index.json: missing project {target}")
    for target in catalog.get("schemas",[]):
        if not (ROOT/target).is_file():
            errors.append(f"catalog/index.json: missing schema {target}")

sources=load(ROOT/"outbox"/"sources.json")
if sources:
    seen=set()
    for item in sources.get("sources",[]):
        repo=str(item.get("repository",""))
        if not repo or "/" not in repo:
            errors.append("outbox/sources.json: invalid repository")
        if repo in seen:
            errors.append(f"outbox/sources.json: duplicate source {repo}")
        seen.add(repo)

if errors:
    print("Foundry validation failed:",file=sys.stderr)
    for err in errors:
        print(f"- {err}",file=sys.stderr)
    raise SystemExit(1)
print(f"Foundry validation passed ({len(seen_ids)} indexed JSON ids)")
