#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATTERNS=ROOT/"domains"/"interface-grammar"/"registry"/"patterns"
MANIFESTS=ROOT/"domains"/"interface-grammar"/"showcases"/"manifests"

class ShowcaseTests(unittest.TestCase):
    def docs(self):
        result={}
        for p in PATTERNS.glob("*.json"):
            d=json.loads(p.read_text(encoding="utf-8"));result[d["id"]]=d
        return result

    def test_entrypoints_exist_and_pattern_ids_resolve(self):
        patterns=self.docs()
        for m in MANIFESTS.glob("*.json"):
            d=json.loads(m.read_text(encoding="utf-8"))
            self.assertTrue((ROOT/d["entrypoint"]).is_file(),d["entrypoint"])
            for pid in d["patterns"]:self.assertIn(pid,patterns)

    def test_reference_demo_links_are_reciprocal(self):
        patterns=self.docs()
        for m in MANIFESTS.glob("*.json"):
            d=json.loads(m.read_text(encoding="utf-8"))
            if d.get("type")!="reference-demo":continue
            rel=m.relative_to(ROOT).as_posix()
            for pid in d["patterns"]:self.assertIn(rel,patterns[pid].get("showcases",[]))

    def test_pattern_showcase_paths_exist(self):
        for p in PATTERNS.glob("*.json"):
            d=json.loads(p.read_text(encoding="utf-8"))
            for ref in d.get("showcases",[]):self.assertTrue((ROOT/ref).is_file(),ref)

    def test_visual_baseline_hashes(self):
        for m in MANIFESTS.glob("*.json"):
            d=json.loads(m.read_text(encoding="utf-8"))
            if d.get("type")!="visual-baseline":continue
            entry=ROOT/d["entrypoint"]
            self.assertIn("viewport",d)
            self.assertIn("browser",d)
            self.assertIn("source_showcase",d)
            digest=hashlib.sha256(entry.read_bytes()).hexdigest()
            self.assertEqual(d.get("sha256"),digest)

if __name__=="__main__":unittest.main()
