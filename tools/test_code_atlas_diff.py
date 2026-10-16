#!/usr/bin/env python3
"""Falsification gates for bounded same-revision operation evidence comparison."""
from __future__ import annotations

import importlib.util
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from code_atlas_causality import mark, operation

SPEC = importlib.util.spec_from_file_location("atlas_trace", Path(__file__).with_name("code_atlas_trace.py"))
trace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace)

DIFF_SPEC = importlib.util.spec_from_file_location("atlas_diff", Path(__file__).with_name("code_atlas_diff.py"))
diff = importlib.util.module_from_spec(DIFF_SPEC)
DIFF_SPEC.loader.exec_module(diff)
TOOLS = Path(__file__).resolve().parent
SHA = "a" * 40


def fixture(status="completed", operation_id="op-1", *, revision=SHA):
    event_kind = "operation_error" if status == "failed" else "operation_end"
    return {
        "schema_version": 1, "kind": "python_runtime_trace", "repository": "owner/repo",
        "revision": revision, "status": status,
        "exception_type": "RuntimeError" if status == "failed" else None,
        "stats": {"truncated": False},
        "annotations": {"truncated": False, "events": [
            {"kind": "operation_begin", "name": "Test operation", "parent_id": None,
             "operation_id": operation_id},
            {"kind": "action", "name": "do test", "operation_id": operation_id},
            {"kind": event_kind, "name": "RuntimeError" if status == "failed" else "Test operation",
             "operation_id": operation_id},
        ]},
        "operation_calls": [{"operation_id": operation_id,
                             "from": "fn:task.py:run", "to": "fn:task.py:work",
                             "path": "task.py", "line": 7, "count": 1}],
    }


class ComparisonTests(unittest.TestCase):
    def test_same_operation_different_run_ids_compare(self):
        result = diff.compare(fixture(), fixture("failed", "op-27"), "Test operation")
        self.assertTrue(result["status_changed"])
        self.assertEqual(result["candidate_exception_type"], "RuntimeError")
        self.assertEqual(result["changed_call_sites_total"], 0)
        self.assertEqual(result["first_observed_event_difference"]["index"], 2)
        self.assertIn("not earliest causal divergence", result["interpretation"])

    def test_call_count_difference_is_explicit(self):
        a, b = fixture(), fixture()
        b["operation_calls"][0]["count"] = 4
        report = diff.compare(a, b, "Test operation")
        self.assertEqual(report["changed_call_sites_total"], 1)
        self.assertEqual(report["changed_call_sites"][0]["baseline_count"], 1)
        self.assertEqual(report["changed_call_sites"][0]["candidate_count"], 4)
        self.assertIsNone(report["first_observed_event_difference"])

    def test_mismatch_and_unanchored_rejected(self):
        for bad in (fixture(revision="b"*40), fixture(revision=None)):
            with self.assertRaisesRegex(ValueError, "revision|commit-pinned"):
                diff.compare(fixture(), bad, "Test operation")
        different_repo = fixture()
        different_repo["repository"] = "other/repo"
        with self.assertRaisesRegex(ValueError, "repository"):
            diff.compare(fixture(), different_repo, "Test operation")

    def test_truncation_and_missing_scope_rejected(self):
        for key in ("annotations", "stats"):
            bad = fixture()
            bad[key]["truncated"] = True
            with self.assertRaisesRegex(ValueError, "truncated"):
                diff.compare(fixture(), bad, "Test operation")
        with self.assertRaisesRegex(ValueError, "top-level operation"):
            diff.compare(fixture(), fixture(), "not present")

    def test_invalid_counts_and_repeated_roots_rejected(self):
        bad = fixture()
        bad["operation_calls"][0]["count"] = -1
        with self.assertRaisesRegex(ValueError, "count"):
            diff.compare(fixture(), bad, "Test operation")
        bad = fixture()
        bad["annotations"]["events"].append({
            "kind": "operation_begin", "name": "Test operation",
            "parent_id": None, "operation_id": "op-2",
        })
        with self.assertRaisesRegex(ValueError, "exactly one"):
            diff.compare(fixture(), bad, "Test operation")

    def test_default_observer_keeps_exception_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            script = root / "sample.py"
            script.write_text("def explode():\n    raise RuntimeError('private message')\nexplode()\n")
            before = sys.getprofile()
            with self.assertRaisesRegex(RuntimeError, "private message"):
                trace.observe(root, lambda: runpy.run_path(str(script)))
            self.assertIs(sys.getprofile(), before)

    def test_opt_in_failure_collects_sanitized_trace_and_restores_hooks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            script = root / "sample.py"
            script.write_text("def explode():\n    raise RuntimeError('private message')\nexplode()\n")
            previous = sys.getprofile()
            report = trace.observe(root, lambda: runpy.run_path(str(script)),
                                   repo="owner/repo", capture_failure=True)
            self.assertIs(sys.getprofile(), previous)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["exception_type"], "RuntimeError")
            self.assertNotIn("private message", json.dumps(report))
            self.assertGreater(report["stats"]["profile_calls"], 0)

    def test_cli_failure_retains_report_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            script = root / "fail.py"
            script.write_text("from sys import exit\nexit(9)\n")
            report_path = root / "trace.json"
            cmd = [sys.executable, str(TOOLS / "code_atlas_trace.py"),
                   "--root", str(root), "--script", "fail.py", "--repo", "owner/repo",
                   "--record-failure", "--output", str(report_path)]
            run = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            data = json.loads(report_path.read_text())
            self.assertEqual(data["status"], "failed")
            self.assertEqual(data["exception_type"], "SystemExit")

    def test_comparison_cli_success_and_bad_revision(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "good.json"
            b = root / "bad.json"
            output = root / "diff.json"
            a.write_text(json.dumps(fixture()), encoding="utf-8")
            b.write_text(json.dumps(fixture("failed")), encoding="utf-8")
            cmd = [sys.executable, str(TOOLS / "code_atlas_diff.py"), "--baseline", str(a),
                   "--candidate", str(b), "--operation", "Test operation", "--output", str(output)]
            good = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertTrue(json.loads(output.read_text())["status_changed"])
            b.write_text(json.dumps(fixture("failed", revision="b"*40)))
            fail = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(fail.returncode, 0)
            self.assertIn("invalid comparison evidence", fail.stderr)


if __name__ == "__main__":
    unittest.main()
