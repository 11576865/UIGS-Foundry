#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_review_queue_report as g


class ReviewQueueTests(unittest.TestCase):
    def write_json(self, root: Path, rel: str, data) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def fixture(self) -> Path:
        root = Path(tempfile.mkdtemp())

        for packet_id, workflow, category in [
            ("p1", "Android CI", "unit-test"),
            ("p2", "Android CI", "unit-test"),
            ("p3", "Android Emulator Regression", "runtime-smoke"),
        ]:
            self.write_json(
                root,
                f"outbox/pending/repo/{packet_id}.json",
                {
                    "packet_id": packet_id,
                    "source_repository": "owner/repo",
                    "status": "pending",
                    "record_type": "ci_failure",
                    "created_at": f"2026-10-04T00:0{packet_id[-1]}:00+00:00",
                    "evidence": {"workflow": workflow},
                },
            )
            self.write_json(
                root,
                f"outbox/triage/repo/{packet_id}.json",
                {
                    "packet_id": packet_id,
                    "source_repository": "owner/repo",
                    "triage_status": "needs-review",
                    "record_type": "ci_failure",
                    "red_reason": {
                        "category": category,
                        "confidence": 0.5,
                        "needs_review": True,
                        "matched_rules": ["unit"] if category == "unit-test" else ["runtime"],
                    },
                    "related_records": [],
                },
            )

        self.write_json(
            root,
            "outbox/pending/repo/chat1.json",
            {
                "packet_id": "chat1",
                "source_repository": "owner/repo",
                "status": "pending",
                "record_type": "bug",
                "created_at": "2026-10-04T01:00:00+00:00",
            },
        )
        self.write_json(
            root,
            "outbox/triage/repo/chat1.json",
            {
                "packet_id": "chat1",
                "source_repository": "owner/repo",
                "triage_status": "ready-for-record",
                "record_type": "bug",
            },
        )
        self.write_json(
            root,
            "outbox/proposals/repo/chat1.json",
            {
                "packet_id": "chat1",
                "source_repository": "owner/repo",
                "suggested_record": {
                    "type": "bug",
                    "id": "BUG.TEST",
                    "title": "Example",
                },
                "dedupe_candidates": [],
            },
        )
        return root

    def test_needs_review_packets_group_by_repo_workflow_category_and_rules(self):
        root = self.fixture()
        snapshot = g.build_snapshot(root)

        self.assertEqual(snapshot["summary"]["pending_packets"], 4)
        self.assertEqual(snapshot["summary"]["needs_review_packets"], 3)
        self.assertEqual(snapshot["summary"]["needs_review_families"], 2)

        counts = sorted(row["count"] for row in snapshot["needs_review_families"])
        self.assertEqual(counts, [1, 2])

    def test_reviewed_packet_is_removed_from_open_work(self):
        root = self.fixture()
        self.write_json(
            root,
            "outbox/reviews/chat1.json",
            {"packet_id": "chat1", "decision": "accept"},
        )
        self.write_json(
            root,
            "outbox/reviews/p1.json",
            {"packet_id": "p1", "decision": "reject"},
        )

        snapshot = g.build_snapshot(root)

        self.assertEqual(snapshot["summary"]["needs_review_packets"], 2)
        self.assertEqual(snapshot["summary"]["open_proposals"], 0)
        self.assertEqual(snapshot["summary"]["reviewed_packets"], 2)

    def test_markdown_warns_that_grouping_is_not_root_cause_deduplication(self):
        root = self.fixture()
        rendered = g.render_markdown(g.build_snapshot(root))

        self.assertIn("operational deduplication only", rendered)
        self.assertIn("Open promotion proposals: 1", rendered)


if __name__ == "__main__":
    unittest.main()
