#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"catalog/index.json").read_text(encoding="utf-8"))
projects=sorted(ROOT.glob("projects/*.project.json"))
candidates=sorted((ROOT/"inbox/candidates").glob("*.md")) if (ROOT/"inbox/candidates").exists() else []
pending=sorted((ROOT/"outbox/pending").rglob("*.json")) if (ROOT/"outbox/pending").exists() else []
patterns=catalog.get("patterns",[])
records=catalog.get("records",[])
statuses=Counter(item.get("status","unknown") for item in patterns+records)

print("# UIGS-Foundry inventory\n")
print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
print(f"Domains: {len(catalog.get('domains',[]))}")
print(f"Registered UI patterns: {len(patterns)}")
print(f"Other structured records: {len(records)}")
print(f"Project manifests: {len(projects)}")
print(f"Candidate documents: {len(candidates)}")
print(f"Durable pending intake packets: {len(pending)}")
print("Statuses: "+", ".join(f"{k}={v}" for k,v in sorted(statuses.items())))
print()
print("## UI Patterns")
for item in patterns:
    print(f"- {item['id']} [{item['status']}] -> {item['path']}")
print()
print("## Knowledge Records")
for item in records:
    print(f"- {item['id']} [{item['status']}] -> {item['path']}")
