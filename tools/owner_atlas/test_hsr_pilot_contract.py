"""The real historical HSR case is a fixture, not an owner-approved specification."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'fixtures' / 'hsr-pr194'

class HsrPilotContract(unittest.TestCase):
    def test_historical_case_pinned_and_unapproved(self):
        snapshot=json.loads((FIXTURES/'snapshot.json').read_text('utf-8'))
        prop=json.loads((FIXTURES/'proposal.json').read_text('utf-8'))
        self.assertEqual(prop['base_sha'], snapshot['project']['pinned_sha'])
        self.assertEqual(prop['repository'], snapshot['project']['repository'])
        self.assertEqual(prop['head_sha'], 'dea5411312ed3e819864f1915f4f2008f938cba3')
        self.assertEqual(snapshot['goal_ledger']['goals'][0]['status'], 'documented-not-owner-approved')
        for flag in ('theory_approved','owner_accepted','tests_verified','runtime_verified','semantic_verified','authorized_to_edit'):
            self.assertIs(prop[flag], False)
    def test_preserves_exact_old_and_new_quote_ids(self):
        prop=json.loads((FIXTURES/'proposal.json').read_text('utf-8'))
        case=prop['claims'][0]
        self.assertEqual(case['before_evidence'][0]['start'], 5804)
        self.assertEqual(case['after_evidence'][0]['start'], 5807)
        self.assertEqual(case['before_evidence'][0]['path'], case['after_evidence'][0]['path'])
        self.assertIn('audio-integrity',case['after_evidence'][0]['quote'])

if __name__=='__main__':unittest.main()
