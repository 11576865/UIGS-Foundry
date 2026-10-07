#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import evaluate_epistemic_graph as epistemic

OUT_JSON=ROOT/"reports"/"generated"/"experimental-epistemic-triage.json"
OUT_MD=ROOT/"reports"/"generated"/"experimental-epistemic-triage.md"

IMPLEMENTATION_TOKENS=(
    "production implementation","implemented architecture","implemented hardening",
    "implemented product behavior","implemented release hardening","implemented ci check",
    "machine enforcement","production thermal probe","production job evidence",
    "production classification","source-owned ui inventory","implemented control-plane",
    "implemented registry","implemented retrieval","implemented correction",
    "implemented test harness","implemented actions cache","path-filtered production ci",
    "production fix","implemented migration","implemented ui refactor"
)
VALIDATION_TOKENS=(
    "automated test","automated supervisor test","automated checkpoint",
    "unit contract","ui contract test","regression contract","regression test",
    "browser e2e","workflow smoke coverage","successful production visual capture",
    "successful corrected","observed workflow","observed no downstream",
    "failure proving","validated historical failure","clone contract test",
    "delete/active-job safety test","destructive-operation guard"
)

def load(path:Path)->Any:
    return json.loads(path.read_text(encoding="utf-8"))

def source_group(source:str, source_type:str)->str:
    source=source.strip()
    m=re.search(r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",source)
    if m:
        return m.group(1)
    if source.startswith("http://") or source.startswith("https://"):
        return urlparse(source).netloc or source
    if source_type=="manual_decision":
        return "manual-decision"
    if "UIGS-Foundry GitHub Actions" in source:
        return "11576865/UIGS-Foundry"
    return source or source_type or "unknown"

def recurrence_for(path:str, record_id:str, related:list[str], prevention:dict[str,Any])->int:
    refs={path,record_id,*[str(x) for x in related]}
    total=0
    for entry in prevention.get("entries",[]):
        knowledge={str(x) for x in entry.get("knowledge_refs",[])}
        if refs & knowledge:
            total+=int(entry.get("recurrence_count",0) or 0)
    return total

def classify_record(
    entry:dict[str,Any],
    data:dict[str,Any],
    prevention:dict[str,Any],
    claim_states:dict[str,dict[str,Any]],
)->dict[str,Any]:
    provenance=data.get("provenance",[]) if isinstance(data.get("provenance"),list) else []
    claim_refs=[str(x) for x in data.get("claim_refs",[]) if str(x)] if isinstance(data.get("claim_refs"),list) else []
    related=data.get("related_records",data.get("related",[]))
    related=[str(x) for x in related] if isinstance(related,list) else []
    groups=[]
    implementation=0
    validation=0
    for p in provenance:
        if not isinstance(p,dict):
            continue
        st=str(p.get("source_type",""))
        src=str(p.get("source",""))
        group=source_group(src,st)
        if group!="manual-decision" and group not in groups:
            groups.append(group)
        level=str(p.get("evidence_level","")).lower()
        if any(token in level for token in IMPLEMENTATION_TOKENS):
            implementation+=1
        if any(token in level for token in VALIDATION_TOKENS):
            validation+=1

    recurrence=recurrence_for(str(entry.get("path","")),str(entry.get("id","")),related,prevention)
    reasons=[]
    linked=[claim_states[x] for x in claim_refs if x in claim_states]
    experimental=[x for x in linked if str(x.get("maturity"))=="experimental"]

    if recurrence>0:
        classification="challenge_or_narrow"
        reasons.append(f"prevention recurrence signal={recurrence}")
        action="Review the linked Claim as counter-evidence/scope debt before any promotion."
    elif experimental:
        if any(
            int(x.get("qualifying_contradiction_count",0))>0
            or bool(x.get("broken_dependencies"))
            for x in experimental
        ):
            classification="challenge_or_narrow"
            reasons.append("linked Experimental Claim has contradiction or broken dependency")
            action="Resolve contradiction/dependency scope before promotion."
        elif all(
            str(x.get("effective_epistemic_state"))=="supported"
            and str(x.get("effective_authority"))=="active"
            and len(x.get("support_groups",[]))>=int(x.get("required_independent_support",0))
            for x in experimental
        ):
            classification="promotion_candidate"
            reasons.append("linked Experimental Claim currently satisfies its declared support policy")
            action="Perform governed Validated-promotion review; do not auto-promote."
        else:
            classification="validation_mission"
            reasons.append("linked Experimental Claim does not yet satisfy its declared support policy")
            action="Acquire the missing independent/direct evidence requested by the Claim support policy."
    elif claim_refs:
        classification="aggregate_view"
        reasons.append("record projects non-Experimental Claim state")
        action="Keep this record as a view; govern truth/authority at the linked Claim level."
    elif (implementation>=1 and validation>=1) or (len(groups)>=2 and (implementation+validation)>=2):
        classification="promotion_candidate"
        reasons.append("existing provenance includes both implementation/production and validation signals, or multiple source groups")
        action="Create/attach an atomic Claim and Evidence records, then perform a governed Validated-promotion review; do not auto-promote."
    else:
        classification="validation_mission"
        if not provenance:
            reasons.append("no provenance recorded")
        elif len(groups)<2:
            reasons.append("independent evidence coverage is limited")
        if validation==0:
            reasons.append("no explicit validation/test/failure-reproduction signal")
        action="Define the atomic Claim first, then acquire discriminating independent evidence before promotion."

    return {
        "record_id":str(entry.get("id","")),
        "path":str(entry.get("path","")),
        "current_status":"experimental",
        "classification":classification,
        "reasons":reasons,
        "claim_refs":claim_refs,
        "provenance_count":len(provenance),
        "independent_source_groups":sorted(groups),
        "implementation_signals":implementation,
        "validation_signals":validation,
        "recurrence_count":recurrence,
        "recommended_action":action
    }

def generate(root:Path=ROOT, generated_at:str|None=None)->dict[str,Any]:
    catalog=load(root/"catalog"/"index.json")
    prevention=load(root/"prevention"/"registry.json") if (root/"prevention"/"registry.json").is_file() else {"entries":[]}
    state_report=epistemic.evaluate(root)
    claim_states={str(x["id"]):x for x in state_report.get("claims",[])}
    entries=[*(catalog.get("patterns",[]) or []),*(catalog.get("records",[]) or [])]
    items=[]
    for entry in entries:
        if str(entry.get("status",""))!="experimental":
            continue
        path=root/str(entry.get("path",""))
        if not path.is_file():
            continue
        data=load(path)
        if not isinstance(data,dict):
            continue
        items.append(classify_record(entry,data,prevention,claim_states))
    order={"challenge_or_narrow":0,"promotion_candidate":1,"validation_mission":2,"aggregate_view":3}
    items.sort(key=lambda x:(order[x["classification"]],x["record_id"]))
    summary={"experimental_records":len(items),"promotion_candidate":0,"validation_mission":0,"challenge_or_narrow":0,"aggregate_view":0}
    for item in items:
        summary[item["classification"]]+=1
    return {
        "schema_version":1,
        "generated_at":generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary":summary,
        "items":items
    }

def markdown(data:dict[str,Any])->str:
    s=data["summary"]
    lines=[
        "# Experimental Epistemic Triage","",
        f"Generated: {data['generated_at']}","",
        "This report recommends governance actions. It does not automatically change maturity or authority.","",
        "## Summary","",
        f"- Experimental records: {s['experimental_records']}",
        f"- Promotion candidates: {s['promotion_candidate']}",
        f"- Validation missions needed: {s['validation_mission']}",
        f"- Challenge / narrow review: {s['challenge_or_narrow']}",
        f"- Aggregate views over existing Claims: {s['aggregate_view']}",""
    ]
    for category,title in (
        ("challenge_or_narrow","Challenge / narrow"),
        ("promotion_candidate","Promotion candidates"),
        ("validation_mission","Validation missions"),
        ("aggregate_view","Aggregate views"),
    ):
        lines.extend([f"## {title}",""])
        rows=[x for x in data["items"] if x["classification"]==category]
        if not rows:
            lines.append("- None")
        else:
            for item in rows:
                reasons="; ".join(item["reasons"]) or "classified by current evidence policy"
                lines.append(f"- `{item['record_id']}` — {reasons}. Next: {item['recommended_action']}")
        lines.append("")
    return "\n".join(lines)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    data=generate(ROOT)
    text=markdown(data)
    if args.check:
        if not OUT_JSON.is_file() or not OUT_MD.is_file():
            print("experimental epistemic triage report is missing")
            return 1
        current=load(OUT_JSON)
        current.pop("generated_at",None)
        expected=dict(data)
        expected.pop("generated_at",None)
        if current!=expected:
            print("experimental epistemic triage report is stale")
            return 1
        print(f"experimental epistemic triage current: {data['summary']}")
        return 0
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT_MD.write_text(text,encoding="utf-8")
    print(json.dumps(data["summary"],sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
