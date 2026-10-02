#!/usr/bin/env python3
from __future__ import annotations
import json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect_outboxes as c

def packet(packet_id: str, dedupe_key: str, repo: str = "owner/repo") -> dict:
    return {
        "packet_version":1,"packet_id":packet_id,"status":"pending","record_type":"ci_failure",
        "title":"CI failed","summary":"A tracked workflow failed and requires triage.",
        "source_repository":repo,"source_event":"workflow_run","source_ref":"refs/heads/main",
        "source_sha":"abc123","source_url":"https://github.com/owner/repo/actions/runs/1",
        "created_at":"2026-10-02T00:00:00+00:00","dedupe_key":dedupe_key,
        "routing_hints":["reliability","red-reason"]
    }

class CollectorTests(unittest.TestCase):
    def test_new_packet_becomes_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); receipts={"version":1,"items":{}}
            disposition,key=c.apply_packet(packet("ci-owner-repo-1-1","workflow:owner/repo:1:1"),"owner/repo","uigs-outbox:packets/x.json",receipts,root)
            self.assertEqual(disposition,"pending")
            pending=root/receipts["items"][key]["pending_path"]
            self.assertTrue(pending.is_file())
            self.assertEqual(json.loads(pending.read_text(encoding="utf-8"))["packet_id"],"ci-owner-repo-1-1")

    def test_dedupe_key_does_not_create_second_pending_copy(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); receipts={"version":1,"items":{}}
            c.apply_packet(packet("manual-owner-repo-a","incident:stable"),"owner/repo","a",receipts,root)
            disposition,key=c.apply_packet(packet("manual-owner-repo-b","incident:stable"),"owner/repo","b",receipts,root)
            self.assertEqual(disposition,"duplicate")
            self.assertEqual(receipts["items"][key]["disposition"],"duplicate")
            self.assertEqual(len(list((root/"outbox"/"pending").rglob("*.json"))),1)

    def test_repository_spoof_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(c.PacketError):
                c.apply_packet(packet("ci-owner-repo-2-1","x","other/repo"),"owner/repo","x",{"version":1,"items":{}},Path(td))

if __name__ == "__main__":
    unittest.main()
