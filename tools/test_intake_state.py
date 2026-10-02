#!/usr/bin/env python3
from __future__ import annotations
import json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import intake_state

class IntakeStateTests(unittest.TestCase):
    def test_review_closes_open_pending_without_deleting_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"outbox/pending").mkdir(parents=True)
            (root/"outbox/reviews").mkdir(parents=True)
            packet={"packet_id":"p1","source_repository":"owner/repo"}
            (root/"outbox/pending/p1.json").write_text(json.dumps(packet),encoding="utf-8")
            self.assertEqual(len(intake_state.pending_packets(root,True)),1)
            review={"packet_id":"p1","decision":"accept"}
            (root/"outbox/reviews/p1.json").write_text(json.dumps(review),encoding="utf-8")
            self.assertEqual(len(intake_state.pending_packets(root,True)),0)
            self.assertEqual(len(intake_state.pending_packets(root,False)),1)

    def test_nonfinal_review_does_not_close(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"outbox/pending").mkdir(parents=True)
            (root/"outbox/reviews").mkdir(parents=True)
            (root/"outbox/pending/p1.json").write_text(json.dumps({"packet_id":"p1"}),encoding="utf-8")
            (root/"outbox/reviews/p1.json").write_text(json.dumps({"packet_id":"p1","decision":"defer"}),encoding="utf-8")
            self.assertEqual(len(intake_state.pending_packets(root,True)),1)

if __name__=="__main__":
    unittest.main()
