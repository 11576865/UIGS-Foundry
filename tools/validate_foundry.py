#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors = []

def load(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None

for path in sorted(ROOT.rglob("*.json")):
    data = load(path)
    if data is None: continue
    rel = path.relative_to(ROOT).as_posix()
    if "/registry/patterns/" in f"/{rel}":
        for key in ("id","type","status","name","intent","constraints","provenance"):
            if key not in data: errors.append(f"{rel}: missing {key}")
        if data.get("type") != "pattern": errors.append(f"{rel}: type must be pattern")
        if not str(data.get("id","")).startswith("UIGS."): errors.append(f"{rel}: id must start UIGS.")
    if rel.startswith("projects/") and rel.endswith(".project.json"):
        for key in ("project","repository","authority","intake"):
            if key not in data: errors.append(f"{rel}: missing {key}")

catalog = load(ROOT / "catalog/index.json")
if catalog:
    for item in catalog.get("patterns", []):
        if not (ROOT / item.get("path","")).is_file():
            errors.append(f"catalog/index.json: missing target {item.get('path')}")

if errors:
    print("Foundry validation failed:", file=sys.stderr)
    for e in errors: print(f"- {e}", file=sys.stderr)
    raise SystemExit(1)
print("Foundry validation passed")
