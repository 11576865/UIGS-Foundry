#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
PATTERNS=ROOT/"domains"/"interface-grammar"/"registry"/"patterns"
MANIFESTS=ROOT/"domains"/"interface-grammar"/"showcases"/"manifests"
INDEX=ROOT/"domains"/"interface-grammar"/"search"/"index.json"
COVERAGE=ROOT/"domains"/"interface-grammar"/"showcases"/"coverage.json"

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def flatten(value:Any,out:list[str]|None=None)->list[str]:
    if out is None:out=[]
    if isinstance(value,str):out.append(value)
    elif isinstance(value,list):
        for x in value:flatten(x,out)
    elif isinstance(value,dict):
        for x in value.values():flatten(x,out)
    return out

def discovered_showcases(root:Path)->dict[str,list[str]]:
    manifests=root/"domains"/"interface-grammar"/"showcases"/"manifests"
    result:dict[str,list[str]]={}
    if not manifests.exists():return result
    for p in sorted(manifests.glob("*.json")):
        try:d=load(p)
        except Exception:continue
        rel=p.relative_to(root).as_posix()
        for pid in d.get("patterns",[]) if isinstance(d.get("patterns"),list) else []:
            result.setdefault(str(pid),[]).append(rel)
    return result

def discovered_realizations(root:Path)->dict[str,list[dict[str,Any]]]:
    result:dict[str,list[dict[str,Any]]]={}
    base=root/"domains"/"interface-grammar"/"realizations"/"manifests"
    if not base.exists():return result
    for path in sorted(base.glob("*.json")):
        try:data=load(path)
        except Exception:continue
        for link in data.get("patterns",[]) if isinstance(data.get("patterns"),list) else []:
            pid=str(link.get("id",""))
            if not pid:continue
            result.setdefault(pid,[]).append({
                "id":data.get("id",""),
                "platform":data.get("platform",""),
                "project":data.get("project",""),
                "repository":data.get("repository",""),
                "revision":data.get("revision",""),
                "role":link.get("role",""),
                "verification_status":data.get("verification_status",""),
                "path":path.relative_to(root).as_posix(),
            })
    return result

def showcase_types(root:Path,refs:list[str])->list[str]:
    types=[]
    for ref in refs:
        p=root/ref
        if not p.is_file():continue
        try:t=str(load(p).get("type",""))
        except Exception:continue
        if t and t not in types:types.append(t)
    return sorted(types)

def build(root:Path=ROOT)->tuple[dict[str,Any],dict[str,Any]]:
    pattern_dir=root/"domains"/"interface-grammar"/"registry"/"patterns";rows=[];digest=hashlib.sha256()
    discovered=discovered_showcases(root)
    realization_map=discovered_realizations(root)
    for path in sorted(pattern_dir.glob("*.json")):
        raw=path.read_bytes();digest.update(path.name.encode()+b"\0"+raw+b"\0");d=json.loads(raw.decode())
        terms=flatten({"id":d.get("id",""),"name":d.get("name",{}),"aliases":d.get("aliases",[]),"intent":d.get("intent",""),"use_when":d.get("use_when",[]),"anatomy":d.get("anatomy",[]),"visual_contract":d.get("visual_contract",{}),"interaction_contract":d.get("interaction_contract",{})})
        unique=[];seen=set()
        for t in terms:
            if t not in seen:seen.add(t);unique.append(t)
        explicit=d.get("showcases",[]) if isinstance(d.get("showcases",[]),list) else []
        refs=sorted(set(explicit+discovered.get(str(d["id"]),[])))
        types=showcase_types(root,refs)
        rows.append({"id":d["id"],"status":d.get("status",""),"name":d.get("name",{}),"aliases":d.get("aliases",[]),"intent":d.get("intent",""),"use_when":d.get("use_when",[]),"do_not_use_when":d.get("do_not_use_when",[]),"anatomy":d.get("anatomy",[]),"realizations":d.get("realizations",{}),"validation":d.get("validation",[]),"showcases":refs,"showcase_types":types,"showcase_status":"available" if refs else "missing","source_path":path.relative_to(root).as_posix(),"search_terms":unique,"production_realizations":realization_map.get(str(d["id"]),[])})
    manifest_digest=hashlib.sha256()
    manifests=root/"domains"/"interface-grammar"/"showcases"/"manifests"
    if manifests.exists():
        for p in sorted(manifests.glob("*.json")):
            manifest_digest.update(p.name.encode()+b"\0"+p.read_bytes()+b"\0")
    idx={"version":3,"source_digest":digest.hexdigest(),"showcase_digest":manifest_digest.hexdigest(),"pattern_count":len(rows),"patterns":rows}
    has=lambda x,t:t in x["showcase_types"]
    coverage={"version":3,"source_digest":idx["source_digest"],"showcase_digest":idx["showcase_digest"],"total_patterns":len(rows),"with_realization":sum(bool(x["realizations"]) for x in rows),"with_validation":sum(bool(x["validation"]) for x in rows),"with_visual_showcase":sum(bool(x["showcases"]) for x in rows),"with_reference_demo":sum(has(x,"reference-demo") for x in rows),"with_production_evidence":sum(has(x,"production-evidence") or has(x,"interaction-recording") for x in rows),"with_visual_baseline":sum(has(x,"visual-baseline") for x in rows),"missing_visual_showcase":[x["id"] for x in rows if not x["showcases"]],"missing_production_evidence":[x["id"] for x in rows if not(has(x,"production-evidence") or has(x,"interaction-recording"))],"missing_visual_baseline":[x["id"] for x in rows if not has(x,"visual-baseline")]}
    return idx,coverage
def write(path:Path,value:Any):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");a=p.parse_args();i,c=build()
    if a.check:
        if (load(INDEX) if INDEX.is_file() else None)!=i or (load(COVERAGE) if COVERAGE.is_file() else None)!=c:print("UI search index is stale");return 1
        print(f"UI search index current: {i['pattern_count']} patterns");return 0
    write(INDEX,i);write(COVERAGE,c);print(f"UI search index built: {i['pattern_count']} patterns");return 0
if __name__=="__main__":raise SystemExit(main())
