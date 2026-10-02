#!/usr/bin/env python3
from __future__ import annotations
import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATTERNS=ROOT/"domains"/"interface-grammar"/"registry"/"patterns"
MANIFESTS=ROOT/"domains"/"interface-grammar"/"showcases"/"manifests"

class ShowcaseTests(unittest.TestCase):
    def test_references_are_reciprocal_and_entrypoints_exist(self):
        pattern_docs={}
        for p in PATTERNS.glob("*.json"):
            d=json.loads(p.read_text(encoding="utf-8")); pattern_docs[d["id"]]=d
        for m in MANIFESTS.glob("*.json"):
            d=json.loads(m.read_text(encoding="utf-8"))
            self.assertTrue((ROOT/d["entrypoint"]).is_file(),d["entrypoint"])
            for pid in d["patterns"]:
                self.assertIn(pid,pattern_docs)
                self.assertIn(m.relative_to(ROOT).as_posix(),pattern_docs[pid].get("showcases",[]))

    def test_pattern_showcase_paths_exist(self):
        for p in PATTERNS.glob("*.json"):
            d=json.loads(p.read_text(encoding="utf-8"))
            for ref in d.get("showcases",[]):
                self.assertTrue((ROOT/ref).is_file(),ref)

if __name__=="__main__":
    unittest.main()
