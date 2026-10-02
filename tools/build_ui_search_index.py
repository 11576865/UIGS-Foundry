#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PATTERNS=ROOT/"domains"/"interface-grammar"/"registry"/"patterns"
INDEX=ROOT/"domains"/"interface-grammar"/"search"/"index.json"
COVERAGE=ROOT/"domains"/"interface-grammar"/"showcases"/"coverage.json"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def flatten(value: Any, out: list[str] | None=None) -> list[str]:
    if out is None: out=[]
    if isinstance(value,str): out.append(value)
    elif isinstance(value,list):
        for x in value: flatten(x,out)
    elif isinstance(value,dict):
        for x in value.values(): flatten(x,out)
    return out

def build(root: Path=ROOT) -> tuple[dict[str,Any],dict[str,Any]]:
    pattern_dir=root/"domains"/"interface-grammar"/"registry"/"patterns"
    rows=[]
    digest=hashlib.sha256()
    for path in sorted(pattern_dir.glob("*.json")):
        raw=path.read_bytes()
        digest.update(path.name.encode("utf-8")+b"\0"+raw+b"\0")
        d=json.loads(raw.decode("utf-8"))
        terms=flatten({
            "id":d.get("id",""),"name":d.get("name",{}),"aliases":d.get("aliases",[]),
            "intent":d.get("intent",""),"use_when":d.get("use_when",[]),"anatomy":d.get("anatomy",[]),
            "visual_contract":d.get("visual_contract",{}),"interaction_contract":d.get("interaction_contract",{})
        })
        seen=set(); unique=[]
        for t in terms:
            if t not in seen:
                seen.add(t); unique.append(t)
        showcases=d.get("showcases",[]) if isinstance(d.get("showcases",[]),list) else []
        rows.append({
            "id":d["id"],"status":d.get("status",""),"name":d.get("name",{}),
            "aliases":d.get("aliases",[]),"intent":d.get("intent",""),
            "use_when":d.get("use_when",[]),"do_not_use_when":d.get("do_not_use_when",[]),
            "anatomy":d.get("anatomy",[]),"realizations":d.get("realizations",{}),
            "validation":d.get("validation",[]),"showcases":showcases,
            "showcase_status":"available" if showcases else "missing",
            "source_path":path.relative_to(root).as_posix(),"search_terms":unique
        })
    index={"version":1,"source_digest":digest.hexdigest(),"pattern_count":len(rows),"patterns":rows}
    coverage={
        "version":1,"source_digest":index["source_digest"],"total_patterns":len(rows),
        "with_realization":sum(bool(x["realizations"]) for x in rows),
        "with_validation":sum(bool(x["validation"]) for x in rows),
        "with_visual_showcase":sum(x["showcase_status"]=="available" for x in rows),
        "missing_visual_showcase":[x["id"] for x in rows if x["showcase_status"]!="available"]
    }
    return index,coverage

def write(path: Path,value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    index,coverage=build()
    if args.check:
        current_index=load(INDEX) if INDEX.is_file() else None
        current_coverage=load(COVERAGE) if COVERAGE.is_file() else None
        if current_index!=index or current_coverage!=coverage:
            print("UI search index is stale")
            return 1
        print(f"UI search index current: {index['pattern_count']} patterns")
        return 0
    write(INDEX,index); write(COVERAGE,coverage)
    print(f"UI search index built: {index['pattern_count']} patterns")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
