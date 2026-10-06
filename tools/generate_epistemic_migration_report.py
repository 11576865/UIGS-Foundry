#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT_JSON=ROOT/"reports"/"generated"/"epistemic-migration.json"
OUT_MD=ROOT/"reports"/"generated"/"epistemic-migration.md"

def load(path:Path)->Any:
    return json.loads(path.read_text(encoding="utf-8"))

def generate(root:Path=ROOT)->dict[str,Any]:
    catalog=load(root/"catalog"/"index.json")
    items=[]
    for section in ("patterns","records"):
        for entry in catalog.get(section,[]):
            path=root/str(entry.get("path",""))
            refs=[]
            if path.is_file():
                data=load(path)
                if isinstance(data,dict):
                    refs=[str(x) for x in data.get("claim_refs",[]) if str(x)]
            items.append({
                "id":str(entry.get("id","")),
                "section":section,
                "status":str(entry.get("status","")),
                "path":str(entry.get("path","")),
                "claim_refs":refs,
                "mapped":bool(refs)
            })
    unmapped=[x for x in items if not x["mapped"]]
    return {
        "schema_version":1,
        "generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary":{
            "catalog_items":len(items),
            "mapped":len(items)-len(unmapped),
            "unmapped":len(unmapped),
            "validated_or_canonical_unmapped":sum(1 for x in unmapped if x["status"] in {"validated","canonical"})
        },
        "items":items
    }

def markdown(data:dict[str,Any])->str:
    s=data["summary"]
    lines=[
        "# UIGS Epistemic Migration","",
        f"Generated: {data['generated_at']}","",
        f"- Catalog items: {s['catalog_items']}",
        f"- Claim-mapped: {s['mapped']}",
        f"- Legacy/unmapped: {s['unmapped']}",
        f"- Validated/Canonical but unmapped: {s['validated_or_canonical_unmapped']}","",
        "## Priority migration debt",""
    ]
    high=[x for x in data["items"] if not x["mapped"] and x["status"] in {"validated","canonical"}]
    lines.extend([f"- {x['id']} ({x['status']}) — {x['path']}" for x in high] or ["- None"])
    lines.extend(["","Unmapped does not mean invalid. It means the aggregate record has not yet gained claim-level truth-maintenance coverage.",""])
    return "\n".join(lines)

def main()->int:
    data=generate(ROOT)
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT_MD.write_text(markdown(data),encoding="utf-8")
    print(f"epistemic migration: mapped={data['summary']['mapped']} unmapped={data['summary']['unmapped']}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
