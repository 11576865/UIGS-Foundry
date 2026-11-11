"""End-to-end pilot uses real temporary git objects without network or authorisation."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from pilot_cli import replay

class PilotEndToEnd(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.repo=self.root/'repo';self.repo.mkdir()
        def git(*args):
            p=subprocess.run(['git','-C',str(self.repo),*args],capture_output=True,text=True)
            if p.returncode:raise AssertionError(p.stderr)
            return p.stdout.strip()
        git('init','-q');git('config','user.email','fixture@example.test');git('config','user.name','Fixture')
        (self.repo/'app').mkdir()
        f=self.repo/'app'/'controller.py';f.write_text('def submit():\n    return "OLD_VERIFIED_CALL"\n','utf-8')
        git('add','.');git('commit','-qm','before');self.before=git('rev-parse','HEAD')
        f.write_text('def submit():\n    return "NEW_VERIFIED_PREFLIGHT"\n','utf-8')
        git('add','.');git('commit','-qm','after');self.after=git('rev-parse','HEAD')
        self.fixture=self.root/'fixture';self.fixture.mkdir()
        snapshot={'schema_version':2,'project':{'repository':'fixture/test','pinned_sha':self.before},
          'capabilities':[{'id':'ass-in','name':'source gate','evidence':[{'path':'app/controller.py','start':2,'end':2}]}],
          'goal_ledger':{'goals':[{'id':'DOC.1','title':'doc note', 'source':[],'implementation_evidence':[]}]}}
        proposal={'schema':'uigs-owner-atlas-semantic-proposal/1','authority':'ai-proposed-not-approved',
          'repository':'fixture/test','base_sha':self.before,'head_sha':self.after,
          'theory_approved':False,'owner_accepted':False,'tests_verified':False,'runtime_verified':False,
          'semantic_verified':False,'authorized_to_edit':False,'claims':[{
            'id':'TEST.1','capability_id':'ass-in','goal_ids':['DOC.1'],'relationship':'add',
            'before':'The previous version used an old callback for this fixture.',
            'after':'The new version uses a different callback for this fixture.',
            'user_effect':'This could change what the user sees during execution.',
            'rationale':'This is source anchored but not runtime proven and needs review.',
            'open_questions':['Does the actual product execution use the new code path?'],
            'before_evidence':[{'path':'app/controller.py','start':2,'end':2,'quote':'OLD_VERIFIED_CALL'}],
            'after_evidence':[{'path':'app/controller.py','start':2,'end':2,'quote':'NEW_VERIFIED_PREFLIGHT'}]
          }]}
        (self.fixture/'snapshot.json').write_text(json.dumps(snapshot),'utf-8')
        (self.fixture/'proposal.json').write_text(json.dumps(proposal),'utf-8')
    def test_real_git_to_candidate_ledger_handoff(self):
        r=replay(self.repo,self.fixture,self.root/'out')
        self.assertTrue(r['source_quote_checked'])
        self.assertFalse(r['owner_approved'])
        handoff=json.loads((self.root/'out'/'handoff.json').read_text('utf-8'))
        self.assertEqual(len(handoff['records']),1)
        self.assertFalse(handoff['semantic_correctness_proven'])
        again=replay(self.repo,self.fixture,self.root/'out')
        self.assertEqual(again['candidate_digest'],r['candidate_digest'])
        self.assertEqual(len(json.loads((self.root/'out'/'ledger'/'index.json').read_text())['entries']),1)
    def test_wrong_after_source_fails_closed(self):
        fixture=json.loads((self.fixture/'proposal.json').read_text())
        fixture['claims'][0]['after_evidence'][0]['quote']='FAKE_NEVER_EXISTS_IN_THE_SOURCE'
        (self.fixture/'proposal.json').write_text(json.dumps(fixture),'utf-8')
        with self.assertRaises(ValueError):replay(self.repo,self.fixture,self.root/'fail')

if __name__=='__main__':unittest.main()
