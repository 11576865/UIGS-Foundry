#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,sys,unicodedata
from pathlib import Path
from typing import Any
sys.path.insert(0,str(Path(__file__).resolve().parent))
import query_ui_patterns as qp

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"domains"/"interface-grammar"/"search"/"index.json"
RECIPES=ROOT/"domains"/"interface-grammar"/"compositions"/"recipes"

def norm(s:str)->str:
    return re.sub(r"\s+"," ",unicodedata.normalize("NFKC",s).lower()).strip()

def load_recipes()->list[dict[str,Any]]:
    out=[]
    for p in sorted(RECIPES.glob("*.json")):
        d=json.loads(p.read_text(encoding="utf-8"));d["_path"]=p.relative_to(ROOT).as_posix();out.append(d)
    return out

def pattern_candidates(text:str,index:dict[str,Any],limit:int=8)->list[dict[str,Any]]:
    ranked=qp.query(text,index,limit)
    if not ranked:return []
    top=ranked[0]["score"]
    floor=max(14.0,min(42.0,top*0.24))
    selected=[r for r in ranked if r["score"]>=floor]
    return selected[:limit]

def recipe_score(text:str,recipe:dict[str,Any],selected_ids:set[str])->tuple[float,list[str]]:
    q=norm(text);reasons=[];score=0.0
    names=recipe.get("name",{}) if isinstance(recipe.get("name"),dict) else {}
    aliases=[str(x) for x in recipe.get("aliases",[])]
    for term in [str(names.get("zh","")),str(names.get("en",""))]+aliases:
        nt=norm(term)
        if q==nt and q: score+=100;reasons.append("exact-recipe-name/alias")
        elif nt and (nt in q or q in nt): score+=30;reasons.append("recipe-phrase-overlap")
    members=recipe.get("patterns",[])
    required={x["id"] for x in members if x.get("role")=="required"}
    recommended={x["id"] for x in members if x.get("role")=="recommended"}
    optional={x["id"] for x in members if x.get("role")=="optional"}
    req_hit=len(required&selected_ids);rec_hit=len(recommended&selected_ids);opt_hit=len(optional&selected_ids)
    score+=req_hit*28+rec_hit*15+opt_hit*8
    if required and req_hit==len(required):reasons.append("all-required-patterns-covered")
    elif req_hit:reasons.append("partial-required-pattern-coverage")
    if rec_hit:reasons.append("recommended-pattern-coverage")
    return score,sorted(set(reasons))

def plan(text:str,index:dict[str,Any],recipes:list[dict[str,Any]])->dict[str,Any]:
    selected=pattern_candidates(text,index)
    selected_ids={x["id"] for x in selected}
    ranked=[]
    for recipe in recipes:
        s,reasons=recipe_score(text,recipe,selected_ids)
        if s<=0:continue
        members=recipe.get("patterns",[])
        coverage=[]
        for x in members:
            coverage.append({"id":x["id"],"role":x.get("role"),"matched":x["id"] in selected_ids,"purpose":x.get("purpose","")})
        ranked.append({"id":recipe["id"],"score":round(s,2),"reasons":reasons,"status":recipe.get("status"),"name":recipe.get("name"),"coverage":coverage,"composition_contract":recipe.get("composition_contract",[]),"showcases":recipe.get("showcases",[]),"_path":recipe["_path"]})
    ranked.sort(key=lambda x:(-x["score"],x["id"]))
    missing=[]
    for p in selected:
        if not p.get("realizations"): missing.append({"pattern":p["id"],"kind":"realization"})
        if p.get("showcase_status")!="available": missing.append({"pattern":p["id"],"kind":"showcase"})
        if not p.get("validation"): missing.append({"pattern":p["id"],"kind":"validation"})
    return {"query":text,"patterns":selected,"recipes":ranked[:3],"evidence_gaps":missing}

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("query");ap.add_argument("--json",action="store_true");args=ap.parse_args()
    index=json.loads(INDEX.read_text(encoding="utf-8"));result=plan(args.query,index,load_recipes())
    if args.json:print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    print("Patterns:")
    for x in result["patterns"]:print(f"- {x['id']} [{x['status']}] score={x['score']}")
    print("Recipes:")
    for x in result["recipes"]:print(f"- {x['id']} [{x['status']}] score={x['score']}")
    if result["evidence_gaps"]:
        print("Evidence gaps:")
        for x in result["evidence_gaps"]:print(f"- {x['pattern']}: missing {x['kind']}")
    return 0
if __name__=="__main__":raise SystemExit(main())
