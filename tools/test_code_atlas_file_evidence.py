#!/usr/bin/env python3
"""Exact-scope filesystem side-effect probe tests; no product files modified."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from code_atlas_causality import collect, observe_file, operation


class FileEvidenceTests(unittest.TestCase):
    def test_create_modify_unchanged_remove_and_absent(self):
        with tempfile.TemporaryDirectory() as folder, collect() as rec:
            target = Path(folder) / "artifact.bin"
            with operation("safe fixture"):
                with observe_file("artifact", target):
                    target.write_bytes(b"alpha")
                with observe_file("artifact", target):
                    target.write_bytes(b"omega")
                with observe_file("artifact", target):
                    target.write_bytes(b"omega")
                with observe_file("artifact", target):
                    target.unlink()
                with observe_file("artifact", target):
                    pass
            events = [e for e in rec.events if e["kind"] == "file_delta"]
            self.assertEqual([e["detail"]["verdict"] for e in events],
                             ["created", "modified", "unchanged", "removed", "unchanged"])
            self.assertEqual(len({e["operation_id"] for e in events}), 1)
            self.assertFalse(any("alpha" in str(e) or "omega" in str(e) or folder in str(e) for e in events))

    def test_symlink_and_directory_are_unknown_not_traversed(self):
        with tempfile.TemporaryDirectory() as folder, collect() as rec:
            base = Path(folder)
            hidden = base / "secret.bin"
            hidden.write_bytes(b"secret")
            link = base / "shortcut"
            try:
                link.symlink_to(hidden)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable in test environment")
            with operation("inspection"):
                with observe_file("link", link):
                    pass
                with observe_file("directory", base):
                    pass
            results = [e for e in rec.events if e["kind"] == "file_delta"]
            self.assertEqual([e["detail"]["verdict"] for e in results], ["unknown", "unknown"])
            self.assertEqual(results[0]["detail"]["before_status"], "symlink")
            self.assertEqual(results[1]["detail"]["before_status"], "not_regular")
            self.assertNotIn(str(hidden), str(rec.report()))

    def test_unknown_on_large_file_or_size_race(self):
        with tempfile.TemporaryDirectory() as folder, collect() as rec:
            target = Path(folder) / "large.bin"
            target.write_bytes(b"x" * 32)
            with operation("inspection"):
                with observe_file("big", target, max_bytes=8):
                    pass
            result = [e for e in rec.events if e["kind"] == "file_delta"][0]
            self.assertEqual(result["detail"]["verdict"], "unknown")
            self.assertEqual(result["detail"]["before_status"], "size_limit")

    def test_exception_still_records_observation(self):
        with tempfile.TemporaryDirectory() as folder, collect() as rec:
            target = Path(folder) / "a"
            with self.assertRaisesRegex(RuntimeError, "test stop"):
                with operation("failure"):
                    with observe_file("out", target):
                        target.write_bytes(b"value")
                        raise RuntimeError("test stop")
            result = [e for e in rec.events if e["kind"] == "file_delta"][0]
            self.assertEqual(result["detail"]["verdict"], "created")
            self.assertTrue(any(e["kind"] == "operation_error" for e in rec.events))

    def test_limit_validation_and_no_recorder(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "not-touched"
            with self.assertRaises(ValueError):
                with observe_file("file", target, max_bytes=0):
                    pass
            with self.assertRaises(ValueError):
                with observe_file("file", target, max_bytes=1024*1024+1):
                    pass
            with observe_file("file", target):
                pass
            self.assertFalse(target.exists())

    def test_same_length_different_content_detected(self):
        with tempfile.TemporaryDirectory() as folder, collect() as rec:
            target = Path(folder) / "same-length"
            target.write_bytes(b"abc")
            with operation("overwrite"):
                with observe_file("file", target):
                    target.write_bytes(b"xyz")
            delta = [e for e in rec.events if e["kind"] == "file_delta"]
            self.assertEqual(delta[0]["detail"]["verdict"], "modified")

    def test_record_limit_flags_truncation(self):
        with tempfile.TemporaryDirectory() as folder, collect(max_events=1) as rec:
            with operation("limited"):
                with observe_file("file", Path(folder) / "none"):
                    pass
            self.assertTrue(rec.truncated)
            self.assertEqual(len(rec.events), 1)


if __name__ == "__main__":
    unittest.main()
