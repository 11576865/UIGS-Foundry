#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT/"catalog/index.json").read_text(encoding="utf-8"))
projects = sorted(ROOT.glob("projects/*.project.json"))
candidates = sorted((ROOT/"inbox/candidates").glob("*.md")) if (ROOT/"inbox/candidates").exists() else []
print("# UIGS-Foundry inventory\n")
print(f"Generated: {datetime.now(timezone.utc).isoformat()}")
print(f"Domains: {len(catalog.get('domains', []))}")
print(f"Registered patterns: {len(catalog.get('patterns', []))}")
print(f"Project manifests: {len(projects)}")
print(f"Candidate documents: {len(candidates)}\n")
print("## Patterns")
for item in catalog.get("patterns", []):
    print(f"- {item['id']} [{item['status']}] -> {item['path']}")
