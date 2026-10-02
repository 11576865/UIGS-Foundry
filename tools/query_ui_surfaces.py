#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,unicodedata
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1];INDEX=ROOT/"domains"/"interface-grammar"/"inventory"/"index.json"
def norm(v:str)->str:return re.sub(r"\s+"," ",unicodedata.normalize("NFKC",v).lower()).strip()
def features(v:str)->set[str]:
    v=norm(v);out=set(re.findall(r"[a-z0-9._-]+",v))
    for seq in re.findall(r"[\u3400-\u9fff]+",v):
        if len(seq)==1:out.add(seq)
        else:out.update(seq[i:i+2] for i in range(len(seq)-1))
    return out
def jaccard(a:set[str],b:set[str])->float:return len(a&b)/len(a|b) if a and b else 0.0
def score(text:str,s:dict[str,Any])->tuple[float,list[str]]:
    q=norm(text);qf=features(text);reasons=[];value=0.0
    if q==norm(str(s.get("id",""))):value+=130;reasons.append("exact-id")
    if q==norm(str(s.get("name",""))):value+=110;reasons.append("exact-name")
    fields=[str(s.get("name","")),str(s.get("kind","")),str(s.get("group","")),str(s.get("intent","")),str(s.get("implementation_effect",""))," ".join(str(x) for x in s.get("patterns",[]))]
    best=0.0
    for field in fields:
        nf=norm(field)
        if q and q in nf:value+=18
        if nf and nf in q:value+=10
        best=max(best,jaccard(qf,features(field)))
    value+=best*55
    if best>=0.3:reasons.append("token/bigram-overlap")
    return round(value,3),sorted(set(reasons))
def query(text:str,index:dict[str,Any],limit:int=8)->list[dict[str,Any]]:
    rows=[]
    for s in index.get("surfaces",[]):
        value,reasons=score(text,s)
        if value<=0:continue
        rows.append({"id":s["id"],"name":s["name"],"kind":s["kind"],"project":s["project"],"repository":s["repository"],"platform":s["platform"],"score":value,"reasons":reasons,"implementation_effect":s.get("implementation_effect",""),"patterns":s.get("patterns",[]),"source_refs":s.get("source_refs",[]),"visual_evidence":s.get("visual_evidence",[]),"source_head":s.get("source_head","")})
    rows.sort(key=lambda x:(-x["score"],x["id"]));return rows[:limit]
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("query");p.add_argument("--limit",type=int,default=8);p.add_argument("--json",action="store_true");a=p.parse_args()
    result=query(a.query,json.loads(INDEX.read_text(encoding="utf-8")),max(1,a.limit))
    if a.json:print(json.dumps({"query":a.query,"results":result},ensure_ascii=False,indent=2));return 0
    for i,row in enumerate(result,1):
        print(f"{i}. {row['id']} — {row['name']} [{row['project']}] score={row['score']}");print(f"   {row['implementation_effect']}")
    return 0
if __name__=="__main__":raise SystemExit(main())
