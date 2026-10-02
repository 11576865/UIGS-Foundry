#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

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
