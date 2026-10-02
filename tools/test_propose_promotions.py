#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import propose_promotions as p

class ProposalTests(unittest.TestCase):
    def test_candidate_never_exceeds_candidate_status(self):
        packet={"packet_id":"x","record_type":"candidate","title":"A reusable thing","summary":"Summary","source_repository":"owner/repo","source_sha":"abc","routing_hints":["reliability"],"evidence":{},"metadata":{}}
        r=p.suggested_record(packet)
        self.assertEqual(r["status"],"candidate")

    def test_bug_starts_observed_even_when_fix_evidence_exists(self):
        packet={"packet_id":"x","record_type":"bug","title":"Startup failure","summary":"Summary","source_repository":"owner/repo","source_sha":"abc","routing_hints":["reliability"],"evidence":{"fix_commit":"1","ci_run":"2"},"metadata":{"root_cause_status":"resolved","fix_merged":True}}
        r=p.suggested_record(packet)
        self.assertEqual(r["status"],"observed")
        self.assertTrue(r["evidence_summary"]["fix_present"])
        self.assertTrue(r["evidence_summary"]["regression_evidence_present"])

    def test_similarity_finds_close_title(self):
        records=[{"id":"REL.X","title":"Hidden startup failure visibility","summary":"Windows launcher hides startup failure"}]
        found=p.dedupe_candidates("Hidden Windows startup failure","launcher hides failure",[],records)
        self.assertEqual(found[0]["id"],"REL.X")

if __name__=="__main__":
    unittest.main()
