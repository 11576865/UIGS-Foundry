#!/usr/bin/env python3
from __future__ import annotations
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import verify_ui_realizations as v
class Tests(unittest.TestCase):
    def test_unrelated_head_commit_keeps_source_current(self):
        data={"id":"R","project":"P","platform":"web","repository":"o/r","revision":"old","default_branch":"main","source_files":[{"path":"src/a","blob_sha":"same"}],"validation_files":[{"path":"test/a","blob_sha":"testsame"}]}
        def fake(url):
            if "/branches/main" in url:return {"commit":{"sha":"new"}}
            if "src/a" in url:return {"sha":"same"}
            if "test/a" in url:return {"sha":"testsame"}
            raise AssertionError(url)
        row=v.verify_one(data,True,fake);self.assertFalse(row["head_matches_revision"]);self.assertTrue(row["source_verified"]);self.assertTrue(row["source_content_current"])
    def test_changed_current_source_preserves_history_but_marks_current_false(self):
        data={"id":"R","project":"P","platform":"web","repository":"o/r","revision":"old","default_branch":"main","source_files":[{"path":"src/a","blob_sha":"oldblob"}],"validation_files":[]}
        def fake(url):
            if "/branches/main" in url:return {"commit":{"sha":"new"}}
            if "ref=old" in url:return {"sha":"oldblob"}
            if "ref=new" in url:return {"sha":"newblob"}
            raise AssertionError(url)
        row=v.verify_one(data,True,fake);self.assertTrue(row["source_verified"]);self.assertFalse(row["source_content_current"])
if __name__=="__main__":unittest.main()
