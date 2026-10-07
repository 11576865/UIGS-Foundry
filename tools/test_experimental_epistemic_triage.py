#!/usr/bin/env python3
from __future__ import annotations
import json
import tempfile
from pathlib import Path

from generate_experimental_epistemic_triage import generate

NOW="2026-10-07T00:00:00+00:00"

def write(root:Path,path:str,obj:dict):
    p=root/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def claim(cid:str,maturity:str,minimum:int,evidence_refs:list[str],state:str="supported"):
    return {
        "schema_version":1,"id":cid,"statement":cid,"kind":"heuristic",
        "maturity":maturity,"authority":"active","epistemic_state":state,
        "scope":{},"assumptions":[],"evidence_refs":evidence_refs,"depends_on":[],
        "support_policy":{"minimum_independent_support":minimum,"minimum_directness":"static","quarantine_on_active_contradiction":True,"quarantine_on_broken_dependency":True,"max_evidence_age_days":None},
        "review":{"last_reviewed_at":NOW,"next_review_due":None,"approved_by":"test","rationale":"test"},
        "created_at":NOW,"updated_at":NOW
    }

def evidence(eid:str,cid:str,key:str):
    return {
        "schema_version":1,"id":eid,"status":"active",
        "source":{"type":"file","locator":eid,"revision":None,"environment_fingerprint":None},
        "observed_at":NOW,"valid_until":None,"independence_key":key,
        "provenance":{"entity_id":eid,"activity_id":"test","agent_id":"test","was_derived_from":[],"was_attributed_to":"test"},
        "relations":[{"claim_id":cid,"result":"supports","defeater_type":"none","directness":"runtime","scope_relation":"within_scope","assumption_context":[],"notes":None}]
    }

def run():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        entries=[
            {"id":"REC.AGG","status":"experimental","path":"records/a.json"},
            {"id":"REC.PROMOTE","status":"experimental","path":"records/b.json"},
            {"id":"REC.MISSION","status":"experimental","path":"records/c.json"},
            {"id":"REC.CHALLENGE","status":"experimental","path":"records/d.json"},
        ]
        write(root,"catalog/index.json",{"patterns":[],"records":entries})
        write(root,"prevention/registry.json",{"schema_version":1,"entries":[{"id":"PREVENT.X","knowledge_refs":["records/d.json"],"enforcement":[],"recurrence_count":1}]})

        write(root,"records/a.json",{"claim_refs":["CLAIM.AGG"],"provenance":[]})
        write(root,"records/b.json",{"claim_refs":["CLAIM.PROMOTE"],"provenance":[]})
        write(root,"records/c.json",{"claim_refs":["CLAIM.MISSION"],"provenance":[]})
        write(root,"records/d.json",{"claim_refs":["CLAIM.CHALLENGE"],"provenance":[]})

        write(root,"knowledge/claims/agg.json",claim("CLAIM.AGG","validated",1,["EVID.AGG"]))
        write(root,"knowledge/evidence/agg.json",evidence("EVID.AGG","CLAIM.AGG","agg"))

        write(root,"knowledge/claims/promote.json",claim("CLAIM.PROMOTE","experimental",1,["EVID.PROMOTE"]))
        write(root,"knowledge/evidence/promote.json",evidence("EVID.PROMOTE","CLAIM.PROMOTE","promote"))

        write(root,"knowledge/claims/mission.json",claim("CLAIM.MISSION","experimental",2,["EVID.MISSION"],"challenged"))
        write(root,"knowledge/evidence/mission.json",evidence("EVID.MISSION","CLAIM.MISSION","mission"))

        write(root,"knowledge/claims/challenge.json",claim("CLAIM.CHALLENGE","experimental",1,["EVID.CHALLENGE"]))
        write(root,"knowledge/evidence/challenge.json",evidence("EVID.CHALLENGE","CLAIM.CHALLENGE","challenge"))

        report=generate(root,NOW)
        got={x["record_id"]:x["classification"] for x in report["items"]}
        assert got["REC.AGG"]=="aggregate_view"
        assert got["REC.PROMOTE"]=="promotion_candidate"
        assert got["REC.MISSION"]=="validation_mission"
        assert got["REC.CHALLENGE"]=="challenge_or_narrow"
        assert report["summary"]=={
            "experimental_records":4,
            "promotion_candidate":1,
            "validation_mission":1,
            "challenge_or_narrow":1,
            "aggregate_view":1
        }
    print("experimental epistemic triage tests passed")

if __name__=="__main__":
    run()
