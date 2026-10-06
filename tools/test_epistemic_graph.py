#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from datetime import datetime
from pathlib import Path

from evaluate_epistemic_graph import evaluate

NOW = "2026-10-07T00:00:00+00:00"

def write(root: Path, rel: str, data: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def claim(cid: str, *, maturity: str="canonical", evidence_refs=None, depends_on=None, min_support:int=2, minimum_directness:str="runtime") -> dict:
    return {
        "schema_version":1,"id":cid,"statement":cid,"kind":"normative",
        "maturity":maturity,"authority":"active","epistemic_state":"supported",
        "scope":{},"assumptions":[],"evidence_refs":evidence_refs or [],"depends_on":depends_on or [],
        "support_policy":{
            "minimum_independent_support":min_support,
            "minimum_directness":minimum_directness,
            "quarantine_on_active_contradiction":True,
            "quarantine_on_broken_dependency":True,
            "max_evidence_age_days":None
        },
        "review":{"last_reviewed_at":NOW,"next_review_due":None,"approved_by":"test","rationale":"test fixture"},
        "created_at":NOW,"updated_at":NOW
    }

def evidence(eid:str, claim_id:str, result:str, independence_key:str, *, directness:str="runtime", scope_relation:str="within_scope") -> dict:
    return {
        "schema_version":1,"id":eid,"status":"active",
        "source":{"type":"test_run","locator":eid,"revision":None,"environment_fingerprint":None},
        "observed_at":NOW,"valid_until":None,"independence_key":independence_key,
        "provenance":{"entity_id":eid,"activity_id":"test","agent_id":"test","was_derived_from":[],"was_attributed_to":"test"},
        "relations":[{
            "claim_id":claim_id,"result":result,
            "defeater_type":"rebutting" if result=="contradicts" else "none",
            "directness":directness,"scope_relation":scope_relation,"assumption_context":[],"notes":None
        }]
    }

def test_same_lineage_counts_once() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.TEST.LINEAGE"; e1="EVID.TEST.LINEAGE.A"; e2="EVID.TEST.LINEAGE.B"
        write(root,"knowledge/claims/c.json",claim(cid,evidence_refs=[e1,e2]))
        write(root,"knowledge/evidence/e1.json",evidence(e1,cid,"supports","origin.same"))
        write(root,"knowledge/evidence/e2.json",evidence(e2,cid,"supports","origin.same"))
        state=evaluate(root,datetime.fromisoformat(NOW))["claims"][0]
        assert len(state["support_groups"])==1
        assert state["effective_authority"]=="quarantined"

def test_contradiction_quarantines_without_demoting() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.TEST.CONTRADICTION"; e1="EVID.TEST.SUPPORT.A"; e2="EVID.TEST.SUPPORT.B"; e3="EVID.TEST.CONTRADICT"
        write(root,"knowledge/claims/c.json",claim(cid,evidence_refs=[e1,e2,e3]))
        write(root,"knowledge/evidence/e1.json",evidence(e1,cid,"supports","origin.a"))
        write(root,"knowledge/evidence/e2.json",evidence(e2,cid,"supports","origin.b"))
        write(root,"knowledge/evidence/e3.json",evidence(e3,cid,"contradicts","origin.c"))
        state=evaluate(root,datetime.fromisoformat(NOW))["claims"][0]
        assert state["maturity"]=="canonical"
        assert state["effective_authority"]=="quarantined"
        assert state["effective_epistemic_state"]=="mixed"

def test_out_of_scope_contradiction_does_not_quarantine() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.TEST.SCOPE"; e1="EVID.TEST.S1"; e2="EVID.TEST.S2"; ex="EVID.TEST.OUTSIDE"
        write(root,"knowledge/claims/c.json",claim(cid,evidence_refs=[e1,e2,ex]))
        write(root,"knowledge/evidence/e1.json",evidence(e1,cid,"supports","s.1"))
        write(root,"knowledge/evidence/e2.json",evidence(e2,cid,"supports","s.2"))
        outside=evidence(ex,cid,"inconclusive","outside",scope_relation="outside_scope")
        write(root,"knowledge/evidence/ex.json",outside)
        state=evaluate(root,datetime.fromisoformat(NOW))["claims"][0]
        assert state["effective_authority"]=="active"
        assert state["effective_epistemic_state"]=="supported"

def test_weak_evidence_does_not_satisfy_directness_policy() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.TEST.DIRECTNESS"; e1="EVID.TEST.W1"; e2="EVID.TEST.W2"
        write(root,"knowledge/claims/c.json",claim(cid,evidence_refs=[e1,e2],minimum_directness="runtime"))
        write(root,"knowledge/evidence/e1.json",evidence(e1,cid,"supports","w.1",directness="static"))
        write(root,"knowledge/evidence/e2.json",evidence(e2,cid,"supports","w.2",directness="inferred"))
        state=evaluate(root,datetime.fromisoformat(NOW))["claims"][0]
        assert state["effective_authority"]=="quarantined"
        assert not state["support_groups"]

def test_dependency_invalidation_propagates() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); a="CLAIM.TEST.A"; b="CLAIM.TEST.B"
        a1,a2,ax="EVID.TEST.A1","EVID.TEST.A2","EVID.TEST.AX"; b1,b2="EVID.TEST.B1","EVID.TEST.B2"
        write(root,"knowledge/claims/a.json",claim(a,evidence_refs=[a1,a2,ax]))
        write(root,"knowledge/claims/b.json",claim(b,evidence_refs=[b1,b2],depends_on=[a]))
        write(root,"knowledge/evidence/a1.json",evidence(a1,a,"supports","a.1"))
        write(root,"knowledge/evidence/a2.json",evidence(a2,a,"supports","a.2"))
        write(root,"knowledge/evidence/ax.json",evidence(ax,a,"contradicts","a.x"))
        write(root,"knowledge/evidence/b1.json",evidence(b1,b,"supports","b.1"))
        write(root,"knowledge/evidence/b2.json",evidence(b2,b,"supports","b.2"))
        states={x["id"]:x for x in evaluate(root,datetime.fromisoformat(NOW))["claims"]}
        assert states[a]["effective_authority"]=="quarantined"
        assert states[b]["effective_authority"]=="quarantined"
        assert a in states[b]["broken_dependencies"]

def test_automation_cannot_permanently_demote() -> None:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); cid="CLAIM.TEST.CHANGE"; e1,e2="EVID.TEST.C1","EVID.TEST.C2"
        write(root,"knowledge/claims/c.json",claim(cid,evidence_refs=[e1,e2]))
        write(root,"knowledge/evidence/e1.json",evidence(e1,cid,"supports","c.1"))
        write(root,"knowledge/evidence/e2.json",evidence(e2,cid,"supports","c.2"))
        write(root,"knowledge/changes/x.json",{
            "schema_version":1,"id":"CHANGE.TEST.BAD","target_claim":cid,"operation":"demote",
            "reason":"test","evidence_refs":[],"decided_by":"automation","decided_at":NOW,
            "reversible":True,"replacement_claim":None
        })
        report=evaluate(root,datetime.fromisoformat(NOW))
        assert any("automation cannot perform permanent operation demote" in x for x in report["validation_errors"])

if __name__=="__main__":
    test_same_lineage_counts_once()
    test_contradiction_quarantines_without_demoting()
    test_out_of_scope_contradiction_does_not_quarantine()
    test_weak_evidence_does_not_satisfy_directness_policy()
    test_dependency_invalidation_propagates()
    test_automation_cannot_permanently_demote()
    print("epistemic graph tests passed")
