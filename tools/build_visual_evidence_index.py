#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
MANIFESTS=ROOT/"domains"/"interface-grammar"/"visual-evidence"/"manifests"
INDEX=ROOT/"domains"/"interface-grammar"/"visual-evidence"/"index.json"
COVERAGE=ROOT/"domains"/"interface-grammar"/"visual-evidence"/"coverage.json"
SURFACES=ROOT/"domains"/"interface-grammar"/"inventory"/"index.json"
def load(p:Path)->Any:return json.loads(p.read_text(encoding="utf-8"))
def build()->tuple[dict[str,Any],dict[str,Any]]:
    rows=[];by_surface={}
    for p in sorted(MANIFESTS.glob("*.json")) if MANIFESTS.exists() else []:
        d=load(p);row={"id":d["id"],"evidence_level":d["evidence_level"],"platform":d["platform"],"capture_id":d["capture_id"],"surface_ids":d["surface_ids"],"patterns":d.get("patterns",[]),"entrypoint":d["entrypoint"],"source_repository":d["source_repository"],"source_revision":d["source_revision"],"sha256":d["sha256"],"image":d["image"],"change_status":d.get("change_status"),"path":p.relative_to(ROOT).as_posix()}
        rows.append(row)
        for sid in d["surface_ids"]:by_surface.setdefault(sid,[]).append(row)
    surface_index=load(SURFACES) if SURFACES.is_file() else {"surfaces":[]}
    all_ids=[s["id"] for s in surface_index.get("surfaces",[])]
    covered=sorted(sid for sid in all_ids if by_surface.get(sid))
    index={"version":1,"evidence_count":len(rows),"evidence":rows,"by_surface":{sid:by_surface.get(sid,[]) for sid in all_ids}}
    coverage={"version":1,"total_surfaces":len(all_ids),"with_production_visual_evidence":len(covered),"missing_production_visual_evidence":[sid for sid in all_ids if sid not in covered],"evidence_records":len(rows)}
    return index,coverage
def write(p:Path,v:Any):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");a=ap.parse_args();i,c=build()
    if a.check:
        if (load(INDEX) if INDEX.exists() else None)!=i or (load(COVERAGE) if COVERAGE.exists() else None)!=c:
            print("production visual evidence index is stale");return 1
        print(f"production visual evidence current: {i['evidence_count']} records");return 0
    write(INDEX,i);write(COVERAGE,c);print(f"production visual evidence indexed: {i['evidence_count']} records; surface coverage={c['with_production_visual_evidence']}/{c['total_surfaces']}");return 0
if __name__=="__main__":raise SystemExit(main())
