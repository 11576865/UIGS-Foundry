#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_knowledge_health_report as g


class KnowledgeHealthTests(unittest.TestCase):
    def write_json(self, root: Path, rel: str, data) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_text(self, root: Path, rel: str, text: str) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def fixture(self) -> Path:
        root = Path(tempfile.mkdtemp())
        self.write_json(
            root,
            "catalog/index.json",
            {
                "patterns": [{"id": "A", "status": "validated", "path": "x"}],
                "records": [{"id": "B", "status": "experimental", "path": "y"}],
            },
        )
        self.write_text(
            root,
            "inbox/bugs/one.md",
            "# Bug: one\n\nStatus: Bug\nLifecycle: repair-evidenced\n",
        )
        self.write_text(
            root,
            "inbox/bugs/two.md",
            "# Bug: two\n\nStatus: Bug\n",
        )
        self.write_text(root, "inbox/candidates/c.md", "# Candidate\n")
        self.write_text(root, "inbox/observations/o.md", "# Observation\n")
        self.write_text(root, "inbox/cases/case.md", "# Case\n")
        self.write_json(
            root,
            "outbox/pending/repo/p1.json",
            {
                "packet_id": "p1",
                "source_repository": "owner/repo",
                "status": "pending",
            },
        )
        self.write_json(
            root,
            "outbox/pending/repo/p2.json",
            {
                "packet_id": "p2",
                "source_repository": "owner/repo",
                "status": "pending",
            },
        )
        self.write_json(
            root,
            "outbox/reviews/p2.json",
            {"packet_id": "p2", "decision": "reject"},
        )
        self.write_json(
            root,
            "outbox/triage/repo/p1.json",
            {"packet_id": "p1"},
        )
        self.write_json(
            root,
            "outbox/proposals/repo/p1.json",
            {"packet_id": "p1", "source_repository": "owner/repo"},
        )
        self.write_json(
            root,
            "outbox/proposals/repo/p2.json",
            {"packet_id": "p2", "source_repository": "owner/repo"},
        )
        self.write_json(root, "intake/records/bug/b.json", {"id": "BUG.X"})
        self.write_json(
            root,
            "prevention/registry.json",
            {
                "schema_version": 1,
                "entries": [
                    {
                        "id": "PREVENT.ONE",
                        "knowledge_refs": ["inbox/bugs/one.md"],
                        "enforcement": [{"status": "enforced-main"}],
                        "recurrence_count": 1,
                    },
                    {
                        "id": "PREVENT.TWO",
                        "knowledge_refs": ["inbox/bugs/two.md"],
                        "enforcement": [{"status": "submitted"}],
                        "recurrence_count": 0,
                    },
                    {
                        "id": "PREVENT.THREE",
                        "knowledge_refs": [],
                        "enforcement": [],
                        "recurrence_count": 0,
                    },
                ],
            },
        )
        return root

    def test_snapshot_separates_record_count_from_lifecycle_and_prevention(self):
        root = self.fixture()
        snapshot = g.build_snapshot(root)

        self.assertEqual(snapshot["inbox"]["bugs"], 2)
        self.assertEqual(snapshot["bug_lifecycle"]["counts"]["repair-evidenced"], 1)
        self.assertEqual(snapshot["bug_lifecycle"]["counts"]["unclassified"], 1)
        self.assertEqual(len(snapshot["bug_lifecycle"]["unclassified"]), 1)

        self.assertEqual(snapshot["intake"]["pending_total"], 2)
        self.assertEqual(snapshot["intake"]["pending_unreviewed"], 1)
        self.assertEqual(snapshot["intake"]["triaged_pending"], 1)
        self.assertEqual(snapshot["intake"]["untriaged_pending"], 1)
        self.assertEqual(snapshot["intake"]["proposals_total"], 2)
        self.assertEqual(snapshot["intake"]["proposals_open"], 1)

        self.assertEqual(snapshot["prevention"]["entries"], 3)
        self.assertEqual(snapshot["prevention"]["enforced_entries"], 1)
        self.assertEqual(snapshot["prevention"]["submitted_entries"], 1)
        self.assertEqual(snapshot["prevention"]["unguarded_entries"], 1)
        self.assertEqual(snapshot["prevention"]["recurring_entries"], 1)
        self.assertEqual(snapshot["prevention"]["recurrence_total"], 1)

    def test_markdown_states_interpretation_boundary(self):
        root = self.fixture()
        rendered = g.render_markdown(g.build_snapshot(root))
        self.assertIn("not** the count of unresolved product defects", rendered)
        self.assertIn("Pending packets not yet triaged | 1", rendered)
        self.assertIn("Submitted but not yet main-enforced: 1", rendered)
        self.assertIn("Rules with recorded recurrence: 1", rendered)


if __name__ == "__main__":
    unittest.main()
