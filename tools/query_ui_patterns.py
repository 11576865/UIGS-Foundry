#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, unicodedata
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"domains"/"interface-grammar"/"search"/"index.json"

def norm(s: str) -> str:
    return re.sub(r"\s+"," ",unicodedata.normalize("NFKC",s).lower()).strip()

def compact(s: str) -> str:
    return re.sub(r"[\s\-_/—–]+","",norm(s))

def features(s: str) -> set[str]:
    s=norm(s)
    out=set(re.findall(r"[a-z0-9.]+",s))
    for seq in re.findall(r"[\u3400-\u9fff]+",s):
        if len(seq)==1: out.add(seq)
        else:
            out.update(seq[i:i+2] for i in range(len(seq)-1))
    return out

def jaccard(a: set[str],b: set[str]) -> float:
    return len(a&b)/len(a|b) if a and b else 0.0

def score(query: str,row: dict[str,Any]) -> tuple[float,list[str]]:
    q=norm(query); qc=compact(query); qf=features(query)
    pid=norm(str(row.get("id","")))
    name=row.get("name",{}) if isinstance(row.get("name"),dict) else {}
    names=[str(name.get("zh","")),str(name.get("en",""))]
    aliases=[str(x) for x in row.get("aliases",[])]
    reasons=[]; total=0.0
    if q==pid:
        total+=120; reasons.append("exact-id")
    for n in names:
        if q and q==norm(n):
            total+=100; reasons.append("exact-name")
    for a in aliases:
        if q and q==norm(a):
            total+=95; reasons.append("exact-alias")
    strong=names+aliases
    for t in strong:
        tc=compact(t)
        if len(qc)>=2 and qc and qc in tc:
            total+=55; reasons.append("query-in-name/alias")
        elif len(tc)>=3 and tc and tc in qc:
            total+=28; reasons.append("name/alias-in-query")
    all_terms=[str(x) for x in row.get("search_terms",[])]
    best=0.0
    for t in all_terms:
        best=max(best,jaccard(qf,features(t)))
        tc=compact(t)
        if len(qc)>=4 and qc in tc:
            total+=14
    total+=best*45
    if best>=0.35: reasons.append("token/bigram-overlap")
    return round(total,3),sorted(set(reasons))

def query(text: str,index: dict[str,Any],limit: int=5) -> list[dict[str,Any]]:
    ranked=[]
    for row in index.get("patterns",[]):
        s,reasons=score(text,row)
        if s<=0: continue
        ranked.append({
            "id":row["id"],"score":s,"reasons":reasons,"status":row.get("status",""),
            "name":row.get("name",{}),"intent":row.get("intent",""),
            "realizations":row.get("realizations",{}),"validation":row.get("validation",[]),
            "showcase_status":row.get("showcase_status","missing"),"production_realizations":row.get("production_realizations",[]),"source_path":row.get("source_path","")
        })
    ranked.sort(key=lambda x:(-x["score"],x["id"]))
    return ranked[:limit]

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit",type=int,default=5)
    p.add_argument("--json",action="store_true")
    args=p.parse_args()
    index=json.loads(INDEX.read_text(encoding="utf-8"))
    results=query(args.query,index,max(1,args.limit))
    if args.json:
        print(json.dumps({"query":args.query,"results":results},ensure_ascii=False,indent=2))
    else:
        for i,r in enumerate(results,1):
            name=r.get("name",{})
            print(f"{i}. {r['id']} [{r['status']}] score={r['score']}")
            print(f"   {name.get('zh','')} / {name.get('en','')}")
            print(f"   {r['intent']}")
            print(f"   realizations={','.join(sorted(r['realizations'])) or 'none'}; production={len(r.get('production_realizations',[]))}; showcase={r['showcase_status']}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
