#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import evaluate_epistemic_graph as epistemic

OUT_JSON=ROOT/"reports"/"generated"/"validation-missions.json"
OUT_MD=ROOT/"reports"/"generated"/"validation-missions.md"


def load(path:Path)->dict[str,Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def claims(root:Path)->dict[str,dict[str,Any]]:
    out={}
    base=root/"knowledge"/"claims"
    if not base.exists(): return out
    for path in sorted(base.glob("*.json")):
        data=load(path)
        out[str(data.get("id",""))]=data
    return out


def slug(cid:str)->str:
    return re.sub(r"[^A-Za-z0-9._-]+","_",cid).strip("_")


def priority(state:dict[str,Any])->str:
    maturity=str(state.get("maturity",""))
    quarantined=state.get("effective_authority")=="quarantined"
    if quarantined and maturity=="canonical": return "critical"
    if quarantined or maturity=="validated": return "high"
    if maturity in {"experimental","candidate"}: return "medium"
    return "low"


def mission_for(
    state:dict[str,Any],
    claim:dict[str,Any],
    generated_at:str,
)->dict[str,Any]|None:
    if state.get("effective_authority") in {"deprecated","superseded"}:
        return None
    trigger=""
    objective=""
    desired:list[str]=[]
    broken=state.get("broken_dependencies",[])
    ep=str(state.get("effective_epistemic_state",""))
    minimum=int(claim.get("support_policy",{}).get("minimum_independent_support",0))
    support=len(state.get("support_groups",[]))

    if state.get("active_contradiction_count",0):
        trigger="mixed_evidence" if state.get("active_support_count",0) else "contradiction"
        objective="Resolve the active contradiction with evidence that directly discriminates between the competing explanations under the Claim's declared scope and assumptions."
        desired=[
            "independent reproduction of the contradicting result",
            "independent reproduction of the supporting result under the same scope",
            "environment/version evidence sufficient to determine whether the conflict is contextual"
        ]
    elif broken:
        trigger="broken_dependency"
        objective="Revalidate the dependencies this Claim relies on before restoring default authority."
        desired=[
            "current evidence for each challenged dependency",
            "evidence that the dependent Claim remains valid if the dependency is narrowed or replaced"
        ]
    elif ep=="stale":
        trigger="stale_evidence"
        objective="Refresh time/version-sensitive evidence for the Claim's declared scope."
        desired=[
            "current runtime or final-path evidence",
            "version/environment fingerprint for the refreshed observation"
        ]
    elif support < minimum:
        trigger="insufficient_independent_support"
        objective=f"Acquire independent support sufficient to meet the Claim policy ({support}/{minimum} independent support groups currently active)."
        desired=[
            "evidence from a causally independent implementation, experiment, or source",
            "provenance showing the new evidence is not derived from existing support"
        ]
    elif ep=="unknown":
        trigger="unknown_state"
        objective="Establish whether the Claim is supported, contradicted, or should remain explicitly unknown."
        desired=[
            "direct test or observation within the declared scope",
            "provenance and assumptions for the observation"
        ]
    else:
        return None

    cid=str(state["id"])
    return {
        "schema_version":1,
        "id":f"MISSION.{slug(cid)}.{trigger.upper()}",
        "claim_id":cid,
        "status":"proposed",
        "priority":priority(state),
        "trigger":trigger,
        "objective":objective,
        "desired_evidence":desired,
        "independence_requirement":"New support must use a distinct causal/provenance lineage unless the mission is explicitly testing replication from the same lineage.",
        "constraints":[
            "Do not infer independent confirmation from copied UIGS guidance.",
            "Preserve assumptions, versions, environment, and source revision.",
            "Do not automatically restore, demote, deprecate, or supersede the Claim; submit evidence for governed review."
        ],
        "created_at":generated_at
    }


def prevention_provenance_missions(root:Path, generated_at:str)->list[dict[str,Any]]:
    path=root/"prevention"/"registry.json"
    if not path.is_file():
        return []
    registry=load(path)
    out=[]
    for entry in registry.get("entries",[]):
        legacy=int(entry.get("legacy_unattributed_recurrence_count",0) or 0)
        if legacy <= 0:
            continue
        cid=str(entry.get("effectiveness_claim_ref",""))
        if not cid.startswith("CLAIM."):
            continue
        out.append({
            "schema_version":1,
            "id":f"MISSION.{slug(cid)}.RECURRENCE_PROVENANCE_GAP",
            "claim_id":cid,
            "status":"proposed",
            "priority":"medium",
            "trigger":"recurrence_provenance_gap",
            "objective":f"Attribute {legacy} legacy recurrence count(s) for {entry.get('id')} to concrete source events before using them as counter-evidence.",
            "desired_evidence":[
                "a dated Bug/incident/workflow/source record identifying each recurrence",
                "the enforcement generation active when each recurrence occurred",
                "an Evidence record relating that event to the generation-specific effectiveness Claim"
            ],
            "independence_requirement":"Do not infer a recurrence event from the aggregate counter alone; each attributed event needs its own source provenance.",
            "constraints":[
                "Do not convert legacy_unattributed_recurrence_count into contradiction Evidence without a source event.",
                "Do not rewrite historical generation boundaries to make the count fit."
            ],
            "created_at":generated_at
        })
    return out


def generate(root:Path=ROOT)->dict[str,Any]:
    as_of=datetime.now(timezone.utc).replace(microsecond=0)
    report=epistemic.evaluate(root,as_of)
    source=claims(root)
    missions=[]
    for state in report.get("claims",[]):
        claim=source.get(str(state.get("id")),{})
        m=mission_for(state,claim,report["generated_at"])
        if m: missions.append(m)
    missions.extend(prevention_provenance_missions(root,report["generated_at"]))
    order={"critical":0,"high":1,"medium":2,"low":3}
    missions.sort(key=lambda x:(order[x["priority"]],x["claim_id"],x["trigger"]))
    return {
        "schema_version":1,
        "generated_at":report["generated_at"],
        "mission_count":len(missions),
        "missions":missions
    }


def markdown(data:dict[str,Any])->str:
    lines=[
        "# UIGS Validation Missions","",
        f"Generated: {data['generated_at']}","",
        f"Proposed missions: {data['mission_count']}","",
        "These are evidence-acquisition proposals, not automatically executed work.",""
    ]
    for m in data["missions"]:
        lines.extend([
            f"## {m['id']}","",
            f"- Claim: `{m['claim_id']}`",
            f"- Priority: **{m['priority']}**",
            f"- Trigger: `{m['trigger']}`",
            f"- Objective: {m['objective']}",
            f"- Independence: {m['independence_requirement']}",
            ""
        ])
    if not data["missions"]:
        lines.append("No current Claim requires an automatically proposed validation mission.")
        lines.append("")
    return "\n".join(lines)


def main()->int:
    data=generate(ROOT)
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    OUT_MD.write_text(markdown(data),encoding="utf-8")
    print(f"validation missions: {data['mission_count']}")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
