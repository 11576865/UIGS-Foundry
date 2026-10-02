#!/usr/bin/env python3
from __future__ import annotations
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import generate_project_state_report as g

class ProjectStateTests(unittest.TestCase):
    def test_latest_run_selected_per_name(self):
        runs=[
            {"name":"A","created_at":"2026-10-01T00:00:00Z","run_number":1,"head_sha":"old","status":"completed","conclusion":"success"},
            {"name":"A","created_at":"2026-10-02T00:00:00Z","run_number":2,"head_sha":"new","status":"completed","conclusion":"failure"},
        ]
        out=g.latest_by_name(runs,["A"])
        self.assertEqual(out[0]["conclusion"],"failure")
        self.assertEqual(out[0]["head_sha"],"new")

    def test_missing_workflow_remains_unknown(self):
        out=g.latest_by_name([],["Never ran"])
        self.assertFalse(out[0]["found"])
        self.assertEqual(out[0]["status"],"unknown")

if __name__=="__main__":
    unittest.main()
