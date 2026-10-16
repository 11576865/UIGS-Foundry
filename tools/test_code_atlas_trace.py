#!/usr/bin/env python3
"""Runtime evidence tests: observation is not self-certification."""
import importlib.util
import json
import runpy
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("atlas_trace", Path(__file__).with_name("code_atlas_trace.py"))
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class RuntimeTraceTests(unittest.TestCase):
    def fixture(self, root):
        (root / "flow.py").write_text(
            "def finish():\n    return 3\n"
            "def start():\n    return finish()\n"
            "start()\n", encoding="utf-8")

    def test_observed_edges_and_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            before, thread_before = sys.getprofile(), threading.getprofile()
            evidence = mod.observe(root, lambda: runpy.run_path(str(root / "flow.py")), repo="owner/repo")
            self.assertEqual(before, sys.getprofile())
            self.assertEqual(thread_before, threading.getprofile())
            self.assertEqual(evidence["kind"], "python_runtime_trace")
            calls = evidence["calls"]
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["from"], "fn:flow.py:start")
            self.assertEqual(calls[0]["to"], "fn:flow.py:finish")
            self.assertEqual(calls[0]["evidence"], "python_profile_observed")
            self.assertEqual(calls[0]["line"], 4)

    def test_restore_hooks_after_exception(self):
        with tempfile.TemporaryDirectory() as td:
            def fail():
                raise RuntimeError("deliberate")
            before, thread_before = sys.getprofile(), threading.getprofile()
            with self.assertRaisesRegex(RuntimeError, "deliberate"):
                mod.observe(Path(td), fail)
            self.assertIs(before, sys.getprofile())
            self.assertIs(thread_before, threading.getprofile())

    def test_merge_revision_mismatch_fails_closed(self):
        original = {"schema_version": 1, "repository": "owner/repo", "revision": "a"*40,
                    "nodes": [], "edges": [], "stats": {}, "limitations": []}
        evidence = {"schema_version": 1, "kind": "python_runtime_trace", "repository": "owner/repo",
                    "revision": "b"*40, "calls": [], "stats": {}}
        with self.assertRaisesRegex(ValueError, "revision mismatch"):
            mod.enrich_static(original, evidence)

    def test_known_and_unknown_runtime_edges_are_separated(self):
        original = {"schema_version": 1, "repository": None, "revision": None,
                    "nodes": [{"id": "fn:flow.py:start"}, {"id": "fn:flow.py:finish"}],
                    "edges": [], "stats": {"nodes": 2}, "limitations": []}
        evidence = {"schema_version": 1, "kind": "python_runtime_trace", "repository": None,
                    "revision": None, "observed_at": "2026-10-16", "collector": "sys.setprofile",
                    "calls": [
                        {"from": "fn:flow.py:start", "to": "fn:flow.py:finish", "kind": "runtime_calls", "count": 1},
                        {"from": "fn:flow.py:start", "to": "fn:flow.py:nested", "kind": "runtime_calls", "count": 1},
                    ], "stats": {"truncated": False}}
        merged = mod.enrich_static(original, evidence)
        self.assertEqual(merged["stats"]["runtime_edges"], 1)
        self.assertEqual(merged["stats"]["runtime_unmatched_edges"], 1)
        self.assertEqual(len(merged["runtime_trace"]["unmatched_samples"]), 1)
        self.assertFalse(merged["runtime_trace"]["anchored"])

    def test_cli_requires_explicit_execution(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            evidence_path = root / "result.json"
            cmd = [sys.executable, str(Path(__file__).with_name("code_atlas_trace.py")),
                   "--root", str(root), "--script", "flow.py", "--output", str(evidence_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            content = json.loads(evidence_path.read_text())
            self.assertEqual(content["calls"][0]["to"], "fn:flow.py:finish")
            outside = root.parent / "out-of-root.py"
            invalid = subprocess.run(
                cmd[:cmd.index("--script")+1] + [str(outside), "--output", str(evidence_path)],
                capture_output=True, text=True)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("inside --root", invalid.stderr)

    def test_truncation_does_not_claim_full_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            evidence = mod.observe(root, lambda: runpy.run_path(str(root / "flow.py")), max_events=1)
            self.assertTrue(evidence["stats"]["truncated"])
            self.assertEqual(evidence["stats"]["profile_calls"], 1)


if __name__ == "__main__":
    unittest.main()
