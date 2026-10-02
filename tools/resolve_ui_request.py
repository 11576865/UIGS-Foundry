#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from typing import Any
sys.path.insert(0,str(Path(__file__).resolve().parent))
import query_ui_composition as composition
import query_ui_surfaces as surfaces_query

ROOT=Path(__file__).resolve().parents[1]
PATTERN_INDEX=ROOT/"domains"/"interface-grammar"/"search"/"index.json"
SURFACE_INDEX=ROOT/"domains"/"interface-grammar"/"inventory"/"index.json"
VISUAL_INDEX=ROOT/"domains"/"interface-grammar"/"visual-evidence"/"index.json"

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))

def _pattern_row(row:dict[str,Any],source:str)->dict[str,Any]:
    return {
        "id":row["id"],"status":row.get("status",""),"name":row.get("name",{}),"intent":row.get("intent",""),
        "realizations":row.get("realizations",{}),"validation":row.get("validation",[]),
        "showcases":row.get("showcases",[]),"showcase_types":row.get("showcase_types",[]),
        "showcase_status":row.get("showcase_status","missing"),
        "production_realizations":row.get("production_realizations",[]),
        "source_path":row.get("source_path",""),"selection_source":source,"score":0.0,"reasons":[source]
    }

def resolve(text:str,pattern_index:dict[str,Any],surface_index:dict[str,Any],recipes:list[dict[str,Any]],visual_index:dict[str,Any]|None=None)->dict[str,Any]:
    visual_index=visual_index or {"by_surface":{}}
    plan=composition.plan(text,pattern_index,recipes)
    pattern_map={row["id"]:row for row in pattern_index.get("patterns",[])}
    selected={row["id"]:dict(row) for row in plan.get("patterns",[])}

    direct=surfaces_query.query(text,surface_index,10)
    strong=[]
    if direct:
        threshold=max(40.0,float(direct[0]["score"])*0.55)
        strong=[row for row in direct if float(row["score"])>=threshold]

    for surface in strong:
        for pid in surface.get("patterns",[]):
            if pid not in selected and pid in pattern_map:
                selected[pid]=_pattern_row(pattern_map[pid],"surface-link")

    selected_ids=set(selected)
    ranked=composition.rank_recipes(text,recipes,selected_ids)
    clean_recipes=[]
    for item in ranked[:3]:
        item=dict(item);item.pop("_recipe",None);clean_recipes.append(item)

    concrete={}
    for row in direct:
        item=dict(row);item["selection_source"]="direct-query";item["matched_patterns"]=sorted(selected_ids&set(row.get("patterns",[])))
        concrete[row["id"]]=item
    for surface in surface_index.get("surfaces",[]):
        matches=sorted(selected_ids&set(surface.get("patterns",[])))
        if not matches:continue
        sid=surface["id"]
        if sid in concrete:
            concrete[sid]["matched_patterns"]=sorted(set(concrete[sid].get("matched_patterns",[]))|set(matches))
            continue
        concrete[sid]={
            "id":sid,"name":surface["name"],"kind":surface["kind"],"project":surface["project"],
            "repository":surface["repository"],"platform":surface["platform"],"score":0.0,
            "reasons":["pattern-link"],"selection_source":"pattern-link","matched_patterns":matches,
            "implementation_effect":surface.get("implementation_effect",""),"patterns":surface.get("patterns",[]),
            "source_refs":surface.get("source_refs",[]),"visual_evidence":surface.get("visual_evidence",[]),
            "source_head":surface.get("source_head","")
        }
    concrete_rows=sorted(concrete.values(),key=lambda x:(0 if x.get("selection_source")=="direct-query" else 1,-float(x.get("score",0)),x["id"]))

    realization_seen=set();realizations=[]
    showcase_seen=set();showcases=[]
    patterns=[]
    gaps=[]
    for pid,item in sorted(selected.items(),key=lambda kv:(0 if kv[1].get("selection_source")=="query" else 1,-float(kv[1].get("score",0)),kv[0])):
        base=pattern_map.get(pid,{})
        merged=dict(item)
        merged["production_realizations"]=base.get("production_realizations",item.get("production_realizations",[]))
        merged["showcases"]=base.get("showcases",item.get("showcases",[]))
        merged["showcase_types"]=base.get("showcase_types",item.get("showcase_types",[]))
        patterns.append(merged)
        for r in merged["production_realizations"]:
            rid=r.get("id") or r.get("realization_id")
            if rid and rid not in realization_seen:realization_seen.add(rid);realizations.append(r)
        for ref in merged["showcases"]:
            if ref not in showcase_seen:showcase_seen.add(ref);showcases.append(ref)
        if not merged["production_realizations"]:gaps.append({"subject":pid,"kind":"production-realization"})
        if not merged.get("showcases"):gaps.append({"subject":pid,"kind":"showcase"})
        if not merged.get("validation"):gaps.append({"subject":pid,"kind":"pattern-validation"})

    visual_records=[];visual_seen=set()
    for surface in concrete_rows:
        evidence=visual_index.get("by_surface",{}).get(surface["id"],[])
        surface["production_visual_evidence"]=evidence
        if not evidence:gaps.append({"subject":surface["id"],"kind":"production-visual-evidence"})
        for item in evidence:
            eid=item.get("id")
            if eid and eid not in visual_seen:visual_seen.add(eid);visual_records.append(item)

    return {
        "query":text,
        "intent_segments":composition.split_intents(text),
        "patterns":patterns,
        "recipes":clean_recipes,
        "concrete_surfaces":concrete_rows,
        "production_realizations":realizations,
        "showcases":showcases,
        "production_visual_evidence":visual_records,
        "evidence_gaps":gaps
    }

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("query");p.add_argument("--json",action="store_true");args=p.parse_args()
    result=resolve(args.query,load(PATTERN_INDEX),load(SURFACE_INDEX),composition.load_recipes(),load(VISUAL_INDEX) if VISUAL_INDEX.is_file() else None)
    if args.json:print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    print("Patterns:")
    for row in result["patterns"]:print(f"- {row['id']} source={row.get('selection_source','query')}")
    print("Concrete surfaces:")
    for row in result["concrete_surfaces"][:10]:print(f"- {row['id']} [{row['project']}] source={row['selection_source']}")
    print("Production realizations:")
    for row in result["production_realizations"]:print(f"- {row.get('id') or row.get('realization_id')} [{row.get('project','')}]")
    print("Evidence gaps:")
    for row in result["evidence_gaps"][:12]:print(f"- {row['subject']}: {row['kind']}")
    return 0
if __name__=="__main__":raise SystemExit(main())
