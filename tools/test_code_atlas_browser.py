#!/usr/bin/env python3
"""Chromium rendering tests over synthetic Code Atlas evidence, not source truth."""
from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(__file__).with_name("code_atlas_web") / "index.html"


def example_graph():
    pre = "fn:tools/code_atlas_causality_demo.py:"
    source = "https://github.com/11576865/UIGS-Foundry/blob/" + "a" * 40
    return {
        "schema_version": 1, "repository": "11576865/UIGS-Foundry",
        "revision": "a" * 40, "stats": {"python_files": 1, "nodes": 2, "edges": 1, "unresolved_calls": 0},
        "nodes": [
            {"id": pre + "calculate", "kind": "function", "label": "calculate()",
             "path": "tools/code_atlas_causality_demo.py", "line": 10,
             "url": source + "/tools/code_atlas_causality_demo.py#L10"},
            {"id": pre + "compute_value", "kind": "function", "label": "compute_value()",
             "path": "tools/code_atlas_causality_demo.py", "line": 5, "url": None},
        ],
        "edges": [
            {"from": pre + "calculate", "to": pre + "compute_value",
             "kind": "runtime_calls", "evidence": "python_profile_observed", "line": 12, "count": 1},
        ],
        "operation_evidence": {
            "annotations": {"truncated": False, "events": [
                {"seq": 1, "kind": "operation_begin", "name": "Example calculation", "operation_id": "op-1"},
                {"seq": 2, "kind": "state_delta", "name": "probe comparison", "operation_id": "op-1",
                 "subject": "example:result", "detail": {"verdict": "changed"}},
                {"seq": 3, "kind": "state_delta", "name": "probe comparison", "operation_id": "op-1",
                 "subject": "example:untouched", "detail": {"verdict": "unchanged"}},
                {"seq": 4, "kind": "state_delta", "name": "probe comparison", "operation_id": "op-1",
                 "subject": "example:error", "detail": {"verdict": "unknown"}},
                {"seq": 5, "kind": "file_delta", "name": "file content comparison", "operation_id": "op-1",
                 "subject": "example:output-file", "detail": {"verdict": "created", "method": "bounded_sha256_before_after"}},
            ]},
            "calls": [{"operation_id": "op-1", "from": pre + "calculate",
                       "to": pre + "compute_value", "count": 1}],
            "unmatched_calls": 0,
        },
        "runtime_trace": {"mapped_edges": 1},
    }


class BrowserContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="uigs-atlas-browser-")
        html = WEB.read_text(encoding="utf-8")
        marker = "<script>\n(()=>"
        if marker not in html:
            raise AssertionError("HTML injection marker changed")
        payload = json.dumps(example_graph(), ensure_ascii=True).replace("<", "\\u003c")
        html = html.replace(marker, "<script>window.__UIGS_ATLAS_GRAPH__=" + payload +
                            ";</script>\n" + marker, 1)
        Path(cls.temp.name, "fixture.html").write_text(html, encoding="utf-8")
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, fmt, *args):
                pass
        cls.http = ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=cls.temp.name))
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.http.server_port}/fixture.html"
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join(timeout=5)
        cls.temp.cleanup()

    def open_selected(self, width, height):
        page = self.browser.new_page(viewport={"width": width, "height": height})
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.goto(self.url)
        self.assertEqual(page.title(), "UIGS · Code Atlas")
        page.locator("#search").fill("calculate")
        self.assertEqual(page.locator(".item").count(), 1)
        page.locator(".item").first.click()
        self.assertEqual(page.locator("#name").inner_text(), "calculate()")
        self.assertFalse(errors, "browser JavaScript exception: " + repr(errors))
        return page

    def screenshot(self, page, name):
        folder = Path(os.environ.get("UIGS_ATLAS_BROWSER_ARTIFACT_DIR", "/tmp/uigs-atlas-browser"))
        folder.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(folder / name), full_page=False)

    def test_desktop_source_and_state_evidence(self):
        page = self.open_selected(1440, 900)
        try:
            self.assertTrue(page.locator("#operationEvidence").is_visible())
            rows = page.locator("#operationEvents [data-kind=\"state_delta\"][data-verdict]")
            self.assertEqual(rows.count(), 3)
            self.assertEqual(
                [rows.nth(i).get_attribute("data-verdict") for i in range(3)],
                ["changed", "unchanged", "unknown"],
            )
            self.assertIn("状态探针：有变化", page.locator("#operationEvents").inner_text())
            self.assertIn("文件探针：已创建", page.locator("#operationEvents").inner_text())
            self.assertEqual(page.locator('#operationEvents [data-kind="file_delta"][data-verdict="created"]').count(), 1)
            self.assertIn("python_profile_observed", page.locator("#relations").inner_text())
            self.assertIn("blob/" + "a" * 40, page.locator("#source").get_attribute("href"))
            page.locator("#bigger").click()
            self.screenshot(page, "code-atlas-desktop.png")
        finally:
            page.close()

    def test_narrow_view_retains_operation_evidence(self):
        page = self.open_selected(390, 780)
        try:
            self.assertTrue(page.locator(".inspector").first.is_visible())
            self.assertTrue(page.locator("#operationEvidence").is_visible())
            self.assertTrue(page.locator('#operationEvents [data-kind="state_delta"][data-verdict="unknown"]').is_visible())
            self.assertTrue(page.locator('#operationEvents [data-kind="file_delta"][data-verdict="created"]').is_visible())
            self.screenshot(page, "code-atlas-narrow.png")
        finally:
            page.close()


if __name__ == "__main__":
    unittest.main()
