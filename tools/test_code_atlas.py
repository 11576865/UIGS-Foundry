#!/usr/bin/env python3
"""Code Atlas contract tests: static evidence, false positives and self-observation."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("code_atlas", Path(__file__).with_name("code_atlas.py"))
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)


class AtlasTests(unittest.TestCase):
    def test_import_and_direct_call(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.py").write_text("def run():\n    return 1\n", encoding="utf-8")
            (root / "b.py").write_text("from a import run as go\ndef wrapper():\n    return go()\n", encoding="utf-8")
            graph = atlas.index(root)
            links = {(e["from"], e["to"], e["kind"]) for e in graph["edges"]}
            self.assertIn(("file:b.py", "file:a.py", "imports"), links)
            self.assertIn(("fn:b.py:wrapper", "fn:a.py:run", "calls"), links)
            self.assertIsNone(next(n for n in graph["nodes"] if n["id"] == "fn:a.py:run")["url"])

    def test_shadowed_import_not_misattributed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.py").write_text("def run():\n    pass\n", encoding="utf-8")
            (root / "b.py").write_text("from a import run\ndef wrapper(run):\n    run()\n", encoding="utf-8")
            graph = atlas.index(root)
            calls = {(e["from"], e["to"]) for e in graph["edges"] if e["kind"] == "calls"}
            self.assertNotIn(("fn:b.py:wrapper", "fn:a.py:run"), calls)
            self.assertGreater(graph["stats"]["unresolved_calls"], 0)

    def test_nested_call_not_counted_as_parent_call(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "x.py").write_text(
                "def target():\n    pass\ndef outer():\n    def inner():\n        target()\n    return inner\n",
                encoding="utf-8",
            )
            graph = atlas.index(root)
            calls = {(e["from"], e["to"]) for e in graph["edges"] if e["kind"] == "calls"}
            self.assertNotIn(("fn:x.py:outer", "fn:x.py:target"), calls)

    def test_parse_error_and_unverified_commit_anchor(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "broken.py").write_text("def (", encoding="utf-8")
            (root / "ok.py").write_text("def fine():\n    pass\n", encoding="utf-8")
            graph = atlas.index(root, repo="owner/repo", revision="not-a-sha")
            self.assertEqual(len(graph["parse_errors"]), 1)
            self.assertTrue(all(n["url"] is None for n in graph["nodes"]))

    def test_offline_html_export(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "example.py").write_text("def target():\n    return 1\n", encoding="utf-8")
            dest = root / "standalone.html"
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("code_atlas.py")),
                 "--root", str(root), "--repo", "owner/repo",
                 "--export-html", str(dest)],
                check=True, stdout=subprocess.DEVNULL,
            )
            html = dest.read_text(encoding="utf-8")
            self.assertIn("window.__UIGS_ATLAS_GRAPH__", html)
            self.assertIn("fn:example.py:target", html)

    def test_reflexive_index_and_cross_file_link(self):
        root = Path(__file__).resolve().parents[1]
        graph = atlas.index(root)
        ids = {n["id"] for n in graph["nodes"]}
        self.assertIn("fn:tools/code_atlas.py:index", ids)
        self.assertIn("fn:tools/code_atlas.py:serve", ids)
        self.assertIn("fn:tools/test_code_atlas.py:AtlasTests.test_reflexive_index_and_cross_file_link", ids)
        self.assertEqual(len(ids), len(graph["nodes"]))
        calls = {(e["from"], e["to"]) for e in graph["edges"] if e["kind"] == "calls"}
        self.assertIn(("fn:tools/code_atlas.py:serve", "fn:tools/code_atlas.py:index"), calls)
        self.assertIn(("fn:tools/generate_validation_missions.py:generate",
                       "fn:tools/evaluate_epistemic_graph.py:evaluate"), calls)
        self.assertIn(("fn:tools/test_epistemic_graph.py:test_same_lineage_counts_once",
                       "fn:tools/evaluate_epistemic_graph.py:evaluate"), calls)


if __name__ == "__main__":
    unittest.main()
