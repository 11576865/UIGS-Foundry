#!/usr/bin/env python3
from __future__ import annotations
import json, sys, tempfile, unittest
from unittest import mock
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


    def test_dry_run_does_not_write_pending_receipts_or_report(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources = root / "sources.json"
            receipts = root / "outbox" / "receipts.json"
            sources.write_text(json.dumps({"sources": [{"repository": "owner/repo"}]}), encoding="utf-8")
            tree = [{"type": "blob", "path": "packets/ci-dry-run.json", "sha": "one"}]
            with mock.patch.object(c, "fetch_source_tree", return_value=tree), mock.patch.object(
                c, "fetch_blob_json", return_value=packet("ci-dry-run", "incident:dry")
            ):
                changed, errors = c.collect(sources, receipts, dry_run=True, root=root)
            self.assertEqual((changed, errors), (1, []))
            self.assertFalse((root / "outbox").exists())
            self.assertFalse((root / "reports").exists())

    def test_dry_run_simulates_duplicate_receipts_in_memory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources = root / "sources.json"
            receipts = root / "outbox" / "receipts.json"
            sources.write_text(json.dumps({"sources": [{"repository": "owner/repo"}]}), encoding="utf-8")
            tree = [{"type": "blob", "path": "packets/ci-first.json", "sha": "first"},
                    {"type": "blob", "path": "packets/ci-second.json", "sha": "second"}]
            payloads = {"first": packet("ci-first", "incident:shared"),
                        "second": packet("ci-second", "incident:shared")}
            with mock.patch.object(c, "fetch_source_tree", return_value=tree), mock.patch.object(
                c, "fetch_blob_json", side_effect=lambda repo, sha, token: payloads[sha]
            ):
                changed, errors = c.collect(sources, receipts, dry_run=True, root=root)
            self.assertEqual((changed, errors), (2, []))
            self.assertFalse((root / "outbox").exists())

    def test_invalid_packet_does_not_block_valid_sibling_and_retry(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources = root / "sources.json"
            receipts = root / "outbox" / "receipts.json"
            sources.write_text(json.dumps({"sources": [{"repository": "owner/repo"}]}), encoding="utf-8")
            tree = [{"type": "blob", "path": "packets/ci-bad.json", "sha": "bad"},
                    {"type": "blob", "path": "packets/ci-good.json", "sha": "good"}]
            payloads = {"bad": {"wrong": "schema"}, "good": packet("ci-good", "incident:good")}
            with mock.patch.object(c, "fetch_source_tree", return_value=tree), mock.patch.object(
                c, "fetch_blob_json", side_effect=lambda repo, sha, token: payloads[sha]
            ):
                changed, errors = c.collect(sources, receipts, root=root)
                self.assertEqual(changed, 1)
                self.assertEqual(len(errors), 1)
                self.assertIn("packets/ci-bad.json", errors[0])
                self.assertTrue((root / "outbox" / "pending" / "owner__repo" / "ci-good.json").exists())
                self.assertIn("owner/repo#ci-good", c.load_receipts(receipts)["items"])
                payloads["bad"] = packet("ci-bad", "incident:bad")
                changed2, errors2 = c.collect(sources, receipts, root=root)
            self.assertEqual((changed2, errors2), (1, []))
            self.assertEqual(len(c.load_receipts(receipts)["items"]), 2)

    def test_identical_orphan_pending_is_adopted_without_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = packet("ci-recover", "incident:recover")
            pending = root / "outbox" / "pending" / "owner__repo" / "ci-recover.json"
            pending.parent.mkdir(parents=True)
            pending.write_text(json.dumps(source), encoding="utf-8")
            original = pending.read_bytes()
            receipts = {"version": 1, "items": {}}
            result, key = c.apply_packet(source, "owner/repo", "source", receipts, root)
            self.assertEqual(result, "pending")
            self.assertEqual(pending.read_bytes(), original)
            self.assertEqual(receipts["items"][key]["disposition"], "pending")

    def test_orphan_pending_collision_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pending = root / "outbox" / "pending" / "owner__repo" / "ci-collision.json"
            pending.parent.mkdir(parents=True)
            pending.write_text(json.dumps(packet("ci-collision", "incident:first")), encoding="utf-8")
            receipts = {"version": 1, "items": {}}
            with self.assertRaises(c.PacketError):
                c.apply_packet(packet("ci-collision", "incident:second"), "owner/repo", "source", receipts, root)
            self.assertEqual(receipts["items"], {})

    def test_receipt_without_pending_is_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sources = root / "sources.json"
            receipts = root / "outbox" / "receipts.json"
            sources.write_text(json.dumps({"sources": [{"repository": "owner/repo"}]}), encoding="utf-8")
            c.write_json(receipts, {"version": 1, "items": {
                "owner/repo#ci-missing": {"disposition": "pending", "pending_path": "outbox/pending/owner__repo/ci-missing.json"}
            }})
            tree = [{"type": "blob", "path": "packets/ci-missing.json", "sha": "unused"}]
            with mock.patch.object(c, "fetch_source_tree", return_value=tree), mock.patch.object(
                c, "fetch_blob_json", side_effect=AssertionError("blob already received")
            ):
                changed, errors = c.collect(sources, receipts, root=root)
            self.assertEqual(changed, 0)
            self.assertEqual(len(errors), 1)
            self.assertIn("no persisted Pending packet", errors[0])

    def test_duplicate_receipt_requires_persisted_canonical_owner(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            receipts = {"version": 1, "items": {}}
            c.apply_packet(packet("ci-original", "incident:shared"), "owner/repo", "source", receipts, root)
            c.apply_packet(packet("ci-duplicate", "incident:shared"), "owner/repo", "source", receipts, root)
            (root / receipts["items"]["owner/repo#ci-original"]["pending_path"]).unlink()
            with self.assertRaises(c.PacketError):
                c.check_receipt_storage(receipts, "owner/repo#ci-duplicate", root)

if __name__ == "__main__":
    unittest.main()
