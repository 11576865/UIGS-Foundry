#!/usr/bin/env python3
from __future__ import annotations
import json,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"tools"))
from record_prevention_recurrence import record_recurrence
from evaluate_epistemic_graph import evaluate
from generate_validation_missions import generate
NOW="2026-10-07T00:00:00+00:00"
def write(root,path,obj):
    p=root/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(obj if isinstance(obj,str) else json.dumps(obj,indent=2)+"\n",encoding="utf-8")
def mkclaim(cid):
    return {"schema_version":1,"id":cid,"statement":"current prevention generation covers the failure family","kind":"capability","maturity":"experimental","authority":"active","epistemic_state":"supported","scope":{},"assumptions":[],"evidence_refs":["EVID.SUPPORT"],"depends_on":[],"supersedes":[],"superseded_by":None,"support_policy":{"minimum_independent_support":1,"minimum_directness":"runtime","quarantine_on_active_contradiction":True,"quarantine_on_broken_dependency":True,"max_evidence_age_days":None},"review":{"last_reviewed_at":NOW,"next_review_due":None,"approved_by":"test","rationale":"test"},"created_at":NOW,"updated_at":NOW}
def support(cid):
    return {"schema_version":1,"id":"EVID.SUPPORT","status":"active","source":{"type":"test_run","locator":"test","revision":None,"environment_fingerprint":None},"observed_at":NOW,"valid_until":None,"independence_key":"support","relations":[{"claim_id":cid,"result":"supports","defeater_type":"none","directness":"runtime","scope_relation":"within_scope","assumption_context":[],"notes":None}]}
def run():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.PREVENT.X.G1"; write(root,"knowledge/claims/"+cid+".json",mkclaim(cid)); write(root,"knowledge/evidence/EVID.SUPPORT.json",support(cid)); write(root,"incident.md","# recurrence")
        write(root,"prevention/registry.json",{"schema_version":2,"entries":[{"id":"PREVENT.X","title":"x","knowledge_refs":["incident.md"],"effectiveness_claim_ref":cid,"enforcement_generation":1,"enforcement":[],"recurrence_events":[],"legacy_unattributed_recurrence_count":0,"recurrence_count":0}]})
        record_recurrence(root,"PREVENT.X","RECURRENCE.X.1",NOW,"incident.md","o/r",1)
        state=next(x for x in evaluate(root)["claims"] if x["id"]==cid); assert state["effective_epistemic_state"]=="mixed"; assert state["effective_authority"]=="quarantined"
        assert any(m["claim_id"]==cid and m["trigger"]=="mixed_evidence" for m in generate(root)["missions"])
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.PREVENT.Y.G1"; write(root,"knowledge/claims/"+cid+".json",mkclaim(cid)); write(root,"knowledge/evidence/EVID.SUPPORT.json",support(cid))
        write(root,"prevention/registry.json",{"schema_version":2,"entries":[{"id":"PREVENT.Y","title":"y","knowledge_refs":[],"effectiveness_claim_ref":cid,"enforcement_generation":1,"enforcement":[],"recurrence_events":[],"legacy_unattributed_recurrence_count":1,"recurrence_count":1}]})
        ms=generate(root)["missions"]; assert any(m["claim_id"]==cid and m["trigger"]=="recurrence_provenance_gap" for m in ms)
        state=next(x for x in evaluate(root)["claims"] if x["id"]==cid); assert state["effective_epistemic_state"]=="supported"
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.PREVENT.Z.G1"; c=mkclaim(cid); c["authority"]="superseded"; c["epistemic_state"]="mixed"
        write(root,"knowledge/claims/"+cid+".json",c); write(root,"knowledge/evidence/EVID.SUPPORT.json",support(cid)); write(root,"incident.md","# recurrence")
        record={"schema_version":1,"id":"EVID.RECUR","status":"active","source":{"type":"file","locator":"incident.md","revision":None,"environment_fingerprint":None},"observed_at":NOW,"valid_until":None,"independence_key":"recur","relations":[{"claim_id":cid,"result":"contradicts","defeater_type":"rebutting","directness":"runtime","scope_relation":"within_scope","assumption_context":[],"notes":None}]}
        write(root,"knowledge/evidence/EVID.RECUR.json",record); c["evidence_refs"].append("EVID.RECUR"); write(root,"knowledge/claims/"+cid+".json",c)
        write(root,"prevention/registry.json",{"schema_version":2,"entries":[]})
        assert not any(m["claim_id"]==cid for m in generate(root)["missions"]), "superseded historical generations do not generate missions"
    print("prevention recurrence epistemics tests passed")
if __name__=="__main__": run()
