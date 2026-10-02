#!/usr/bin/env python3
from __future__ import annotations
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=(ROOT/"tools"/"push_with_rebase_retry.sh").read_text(encoding="utf-8")
WORKFLOWS=[
 "capture-ui-reference-baselines.yml","collect-uigs-outboxes.yml","generate-project-state.yml",
 "propose-uigs-promotions.yml","refresh-ui-search-index.yml","review-uigs-promotion.yml","triage-uigs-pending.yml"
]

class PushRetryContractTests(unittest.TestCase):
    def test_retry_script_fetches_rebases_and_retries_push(self):
        self.assertIn('git fetch origin "$branch"',SCRIPT)
        self.assertIn('git rebase "origin/$branch"',SCRIPT)
        self.assertIn('git push origin "HEAD:$branch"',SCRIPT)
        self.assertIn('for ((attempt=1;',SCRIPT)

    def test_all_writer_workflows_use_retry_helper(self):
        for name in WORKFLOWS:
            text=(ROOT/".github"/"workflows"/name).read_text(encoding="utf-8")
            self.assertIn("push_with_rebase_retry.sh",text,name)
            self.assertNotIn("git pull --rebase origin main",text,name)

if __name__=="__main__":unittest.main()
