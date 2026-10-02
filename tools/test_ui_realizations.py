#!/usr/bin/env python3
from __future__ import annotations
import json, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ui_realization_index as builder

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "domains" / "interface-grammar" / "realizations" / "manifests"
PATTERNS = ROOT / "domains" / "interface-grammar" / "registry" / "patterns"

class RealizationTests(unittest.TestCase):
    def test_manifest_pattern_links_resolve(self):
        pattern_ids = {json.loads(path.read_text(encoding="utf-8"))["id"] for path in PATTERNS.glob("*.json")}
        for path in MANIFESTS.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["record_type"], "ui-realization")
            self.assertIn(data["implementation_kind"], {"production", "reference"})
            self.assertTrue(data["source_files"])
            for link in data["patterns"]:
                self.assertIn(link["id"], pattern_ids)

    def test_blob_ids_are_git_sha1s(self):
        for path in MANIFESTS.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data["source_files"] + data.get("validation_files", []):
                self.assertRegex(item["blob_sha"], r"^[0-9a-f]{40}$")

    def test_seed_covers_all_registered_patterns(self):
        _, coverage = builder.build()
        self.assertEqual(coverage["with_production_implementation"], coverage["total_patterns"])
        self.assertEqual(coverage["missing_production_implementation"], [])

if __name__ == "__main__":
    unittest.main()
