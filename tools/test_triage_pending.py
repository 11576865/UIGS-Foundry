#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import triage_pending as t

RULES = json.loads((t.ROOT/"triage"/"red-reason-rules.json").read_text(encoding="utf-8"))
LINKS = json.loads((t.ROOT/"triage"/"related-knowledge-rules.json").read_text(encoding="utf-8"))

def packet(repo="11576865/ASS-Workbench-Android", conclusion="failure", workflow="Android CI", jobs=None, steps=None, record_type="ci_failure"):
    return {
        "packet_version":1,"packet_id":"p1","status":"pending","record_type":record_type,
        "title":f"{workflow}: {conclusion}","summary":"Tracked CI workflow failed.",
        "source_repository":repo,"source_event":"workflow_run","created_at":"2026-10-02T00:00:00+00:00",
        "dedupe_key":"k","routing_hints":["reliability"],
        "evidence":{"workflow":workflow,"conclusion":conclusion,"failed_jobs":jobs or [],"failed_steps":steps or []}
    }

class TriageTests(unittest.TestCase):
    def classify(self,p):
        raw=json.dumps(p,sort_keys=True).encode()
        return t.triage_packet(p,hashlib.sha256(raw).hexdigest(),RULES,LINKS)

    def test_policy_step(self):
        r=self.classify(packet(steps=[{"name":"Validate Actions artifact policy"}]))
        self.assertEqual(r["red_reason"]["category"],"policy")
        self.assertFalse(r["red_reason"]["needs_review"])

    def test_release_step_beats_build_workflow(self):
        r=self.classify(packet(workflow="Build Android and Deploy Frontend",steps=[{"name":"Deploy to GitHub Pages"}]))
        self.assertEqual(r["red_reason"]["category"],"release-publication")

    def test_timeout_is_resource_budget(self):
        r=self.classify(packet(conclusion="timed_out",workflow="Some workflow"))
        self.assertEqual(r["red_reason"]["category"],"resource-budget")

    def test_unknown_stays_reviewable(self):
        r=self.classify(packet(workflow="Mystery",steps=[{"name":"Do something"}]))
        self.assertEqual(r["red_reason"]["category"],"unknown")
        self.assertTrue(r["red_reason"]["needs_review"])

    def test_manual_semantic_packet_is_ready(self):
        r=self.classify(packet(record_type="bug"))
        self.assertEqual(r["triage_status"],"ready-for-record")
        self.assertIsNone(r["red_reason"])

if __name__=="__main__":
    unittest.main()
