#!/usr/bin/env python3
"""Source-grounded explicit annotations must not be mistaken for causal proof."""
import asyncio
import importlib.util
import runpy
import tempfile
import unittest
from pathlib import Path

from code_atlas_causality import collect, current_operation, mark, operation, observe_state

SPEC = importlib.util.spec_from_file_location("atlas_trace", Path(__file__).with_name("code_atlas_trace.py"))
trace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace)


class CausalityTests(unittest.TestCase):
    def test_explicit_nested_operation_and_state_annotation(self):
        with collect() as rec:
            with operation("save parameters") as outer:
                self.assertEqual(current_operation(), outer)
                mark("action", "click-save")
                with operation("persist draft") as inner:
                    mark("state_write", "replace draft", subject="subtitle:draft")
                mark("side_effect", "request preview")
        ev = rec.events
        self.assertEqual([x["kind"] for x in ev], [
            "operation_begin", "action", "operation_begin", "state_write", "operation_end", "side_effect", "operation_end"])
        self.assertEqual(ev[2]["parent_id"], outer)
        self.assertEqual(ev[3]["operation_id"], inner)
        self.assertEqual(ev[3]["subject"], "subtitle:draft")
        self.assertIsNone(current_operation())
        self.assertFalse(mark("checkpoint", "outside collector"))

    def test_exception_and_limit_are_explicit(self):
        with collect(max_events=2) as rec:
            with self.assertRaisesRegex(RuntimeError, "boom"):
                with operation("failing task"):
                    mark("action", "entry")
                    raise RuntimeError("boom")
        self.assertEqual(len(rec.events), 2)
        self.assertTrue(rec.truncated)
        self.assertIsNone(current_operation())

    def test_async_tasks_inherit_operation_context(self):
        async def child():
            mark("checkpoint", "async child")
        async def run():
            with operation("async parent") as ident:
                await asyncio.create_task(child())
                return ident
        with collect() as rec:
            ident = asyncio.run(run())
        matching = [x for x in rec.events if x["name"] == "async child"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["operation_id"], ident)

    def test_runtime_observation_correlates_to_operation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "flow.py").write_text("def finish():\n    return 1\ndef start():\n    return finish()\n", encoding="utf-8")
            def action():
                with operation("Save"):
                    mark("action", "save clicked")
                    ns = runpy.run_path(str(root / "flow.py"))
                    ns["start"]()
                    mark("checkpoint", "done")
            report = trace.observe(root, action, repo="owner/repo")
            self.assertEqual(report["annotations"]["events"][0]["kind"], "operation_begin")
            calls = report["operation_calls"]
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["from"], "fn:flow.py:start")
            self.assertEqual(calls[0]["to"], "fn:flow.py:finish")
            self.assertEqual(calls[0]["operation_id"], report["annotations"]["events"][0]["operation_id"])
            static = {"schema_version": 1, "repository": "owner/repo", "revision": None,
                      "nodes": [{"id": "fn:flow.py:start"}, {"id": "fn:flow.py:finish"}],
                      "edges": [], "stats": {}, "limitations": []}
            combined = trace.enrich_static(static, report)
            self.assertEqual(combined["stats"]["operation_runtime_calls"], 1)
            self.assertEqual(combined["operation_evidence"]["unmatched_calls"], 0)

    def test_annotation_rejects_invalid_kinds(self):
        with self.assertRaises(ValueError):
            mark("automatically_proven_correct", "false")
        with self.assertRaises(ValueError):
            with operation(""):
                pass


    def test_probe_changed_and_unchanged(self):
        state = {"value": [1]}
        with collect() as rec:
            with operation("edit"):
                with observe_state("document", lambda: state):
                    state["value"].append(2)
                with observe_state("document", lambda: state):
                    pass
        events = [e for e in rec.events if e["kind"] == "state_delta"]
        self.assertEqual([e["detail"]["verdict"] for e in events], ["changed", "unchanged"])
        self.assertNotIn("[1,2]", str(rec.report()))

    def test_probe_failure_and_privacy(self):
        reads = [0]
        def reader():
            reads[0] += 1
            if reads[0] == 2:
                raise RuntimeError("secret error")
            return {"secret": "secret value"}
        with collect() as rec:
            with operation("task"):
                with observe_state("doc", reader):
                    pass
        delta = [e for e in rec.events if e["kind"] == "state_delta"][0]
        self.assertEqual(delta["detail"]["verdict"], "unknown")
        self.assertEqual(delta["detail"]["after_status"], "probe_error")
        self.assertNotIn("secret", str(rec.report()))

    def test_probe_serialization_and_size_limit(self):
        with collect() as rec:
            with operation("task"):
                with observe_state("unsupported", lambda: object()):
                    pass
                with observe_state("oversize", lambda: "x"*70000):
                    pass
        results = [e for e in rec.events if e["kind"] == "state_delta"]
        self.assertEqual([e["detail"]["verdict"] for e in results], ["unknown", "unknown"])
        self.assertEqual(results[1]["detail"]["before_status"], "size_limit")

    def test_probe_records_after_exception(self):
        state = {"value": 1}
        with collect() as rec:
            with self.assertRaisesRegex(RuntimeError, "stop"):
                with operation("failure"):
                    with observe_state("doc", lambda: state):
                        state["value"] = 2
                        raise RuntimeError("stop")
        self.assertTrue(any(e["kind"] == "state_delta" and e["detail"]["verdict"] == "changed" for e in rec.events))
        self.assertIsNone(current_operation())

    def test_probe_dormant_without_collector(self):
        def forbidden():
            raise AssertionError("reader must not run")
        with observe_state("doc", forbidden):
            pass
        with self.assertRaises(TypeError):
            with observe_state("doc", None):
                pass


if __name__ == "__main__":
    unittest.main()
