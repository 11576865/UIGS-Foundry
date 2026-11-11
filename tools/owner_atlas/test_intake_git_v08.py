"""No GitHub network; real local git history using temporary repository."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import intake_git_v08 as intake


def cmd(root,*args):
    cp=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True)
    if cp.returncode: raise RuntimeError(cp.stderr)
    return cp.stdout.strip()


class GitIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        cmd(self.root,'init','-q');cmd(self.root,'config','user.email','fixture@example.invalid')
        cmd(self.root,'config','user.name','Fixture')
        for p,t in {'src/a.py':'\n'.join('a'+str(i) for i in range(1,16))+'\n',
                    'src/b.py':'hello\nworld\n',
                    'docs/theory.md':'First\nSecond\nThird\n'}.items():
            f=self.root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t)
        cmd(self.root,'add','.');cmd(self.root,'commit','-qm','base'); self.base=cmd(self.root,'rev-parse','HEAD')
        self.snapshot={'schema_version':2,'project':{'repository':'11576865/HSR-Voice-Archive-Builder','pinned_sha':self.base},
          'capabilities':[{'id':'A','name':'visible feature A','evidence':[{'path':'src/a.py','start':9,'end':12,'label':'A handler'}]},
                          {'id':'B','name':'visible feature B','evidence':[{'path':'src/b.py','start':1,'end':2,'label':'B entry'}]},
                          {'id':'C','name':'same file unrelated handler','evidence':[{'path':'src/a.py','start':1,'end':2,'label':'unrelated'}]}],
          'goal_ledger':{'goals':[{'id':'DOC.1','title':'documented expectation','source':[{'path':'docs/theory.md','start':2,'end':2}]}]}}

    def commit(self):
        cmd(self.root,'add','.');cmd(self.root,'commit','-qm','change')
        return cmd(self.root,'rev-parse','HEAD')

    def test_zero_delta_and_immutable_baseline(self):
        r=intake.build_intake(self.root,self.snapshot)
        self.assertEqual(r['summary']['changed_files'],0)
        self.assertEqual(r['head_sha'],self.base)
        self.assertEqual(r['mapping'],[])
        self.assertFalse(r['semantic_change_proven'])

    def test_direct_overlap_and_unrelated_function_same_file(self):
        p=self.root/'src/a.py';txt=p.read_text().replace('a10\n','A10_CHANGED\n');p.write_text(txt)
        head=self.commit();r=intake.build_intake(self.root,self.snapshot)
        self.assertEqual(r['head_sha'],head)
        x={m['id']:m for m in r['mapping']}
        self.assertEqual(x['A']['strongest_overlap'],'anchor-overlap')
        self.assertEqual(x['C']['strongest_overlap'],'file-only')
        self.assertNotIn('B',x)
        self.assertFalse(r['owner_accepted'])
        self.assertEqual(intake.agent_packet(r)['authority'],'analysis-only-no-product-change-authorization')

    def test_line_shift_is_not_direct_semantic_change(self):
        p=self.root/'src/a.py';p.write_text('inserted\n'+p.read_text())
        self.commit();r=intake.build_intake(self.root,self.snapshot)
        x={m['id']:m for m in r['mapping']}
        self.assertEqual(x['A']['strongest_overlap'],'anchor-line-shift-risk')
        self.assertEqual(x['C']['strongest_overlap'],'adjacent-insertion')

    def test_documented_goal_source_impact(self):
        f=self.root/'docs/theory.md';f.write_text('First\nRevised second\nThird\n')
        self.commit();r=intake.build_intake(self.root,self.snapshot)
        self.assertEqual(r['mapping'][0]['id'],'DOC.1')
        self.assertEqual(r['mapping'][0]['object_type'],'documented_goal')
        self.assertFalse(r['theory_approved'])

    def test_changed_file_without_known_anchor_is_discovery_queue(self):
        p=self.root/'src/new.py';p.write_text('new feature?\n');self.commit()
        r=intake.build_intake(self.root,self.snapshot)
        self.assertIn('src/new.py',r['unmapped_paths'])
        self.assertFalse(r['mapping'])

    def test_dirty_worktree_not_confused_with_commit(self):
        (self.root/'src/a.py').write_text('uncommitted\n')
        r=intake.build_intake(self.root,self.snapshot)
        self.assertTrue(r['source']['worktree_dirty_ignored_for_commit_comparison'])
        self.assertEqual(r['summary']['changed_files'],0)

    def test_non_descendant_rejected(self):
        self.commit() if False else None
        cmd(self.root,'checkout','--orphan','second-root')
        cmd(self.root,'rm','-rf','.');(self.root/'alien').write_text('unrelated')
        self.commit()
        with self.assertRaisesRegex(intake.IntakeError,'NOT descended'):
            intake.build_intake(self.root,self.snapshot)

    def test_repository_remote_mismatch_rejected(self):
        cmd(self.root,'remote','add','origin','https://github.com/other/wrong.git')
        with self.assertRaisesRegex(intake.IntakeError,'does not match'):
            intake.build_intake(self.root,self.snapshot)

    def test_repeated_output_deterministic(self):
        (self.root/'src/a.py').write_text('new\n');self.commit()
        r1=intake.build_intake(self.root,self.snapshot)
        r2=intake.build_intake(self.root,self.snapshot)
        self.assertEqual(json.dumps(r1,sort_keys=True),json.dumps(r2,sort_keys=True))

if __name__=='__main__': unittest.main()
