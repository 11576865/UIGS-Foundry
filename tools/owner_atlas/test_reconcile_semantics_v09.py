"""Real local Git fixtures for v0.9 semantic evidence receipts."""
from pathlib import Path
import copy
import json
import subprocess
import tempfile
import unittest
from reconcile_semantics_v09 import (review,store_in_ledger,SemanticError,digest,source_anchor)
from intake_git_v08 import IntakeError

class SemanticReviewTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir()
  def git(*args):
   p=subprocess.run(['git','-C',str(self.repo),*args],capture_output=True,text=True)
   if p.returncode: raise AssertionError(p.stderr)
   return p.stdout.strip()
  self.git=git
  git('init','-q');git('config','user.email','test@example.com');git('config','user.name','Test')
  (self.repo/'app').mkdir()
  (self.repo/'app'/'engine.py').write_text('def do_thing():\n    return "OLD_ASS_BEHAVIOR"\n','utf-8')
  git('add','.');git('commit','-qm','Before');self.old=git('rev-parse','HEAD')
  (self.repo/'app'/'engine.py').write_text('def do_thing():\n    return "NEW_ASS_BEHAVIOR"\n','utf-8')
  git('add','.');git('commit','-qm','After');self.new=git('rev-parse','HEAD')
  self.snapshot={'schema_version':2,'project':{'repository':'demo/HSR','pinned_sha':self.old},
       'capabilities':[{'id':'ass-in','name':'内部 ASS','evidence':[{'path':'app/engine.py','start':2,'end':2}]}],
       'goal_ledger':{'goals':[{'id':'DEMO.DOC.01','title':'身份验证','source':[],'implementation_evidence':[]}]}}
  self.prop={'schema':'uigs-owner-atlas-semantic-proposal/1','authority':'ai-proposed-not-approved',
    'repository':'demo/HSR','base_sha':self.old,'head_sha':self.new,
    'theory_approved':False,'owner_accepted':False,'tests_verified':False,
    'runtime_verified':False,'semantic_verified':False,'authorized_to_edit':False,
    'claims':[{'id':'CLAIM.1','capability_id':'ass-in','goal_ids':['DEMO.DOC.01'],
      'relationship':'replace','before':'旧代码返回 OLD_ASS_BEHAVIOR 标识','after':'新代码返回 NEW_ASS_BEHAVIOR 标识',
      'user_effect':'可能影响用户看到的 ASS 状态名称','rationale':'这一变化可能反映内部输出状态命名的重新设计，需要运行验证',
      'open_questions':['实际用户界面能否显示新的标识'],
      'before_evidence':[{'path':'app/engine.py','start':2,'end':2,'quote':'OLD_ASS_BEHAVIOR'}],
      'after_evidence':[{'path':'app/engine.py','start':2,'end':2,'quote':'NEW_ASS_BEHAVIOR'}]}]}
 def test_success_requires_two_git_revisions_and_quotes(self):
  x=review(self.repo,self.snapshot,self.prop)
  self.assertEqual(x['claimed_count'],1)
  self.assertTrue(x['source_quote_checked'])
  self.assertEqual(x['claims'][0]['after_source_checked'][0]['git_revision'],self.new)
  self.assertFalse(x['semantic_correctness_proven']);self.assertFalse(x['owner_accepted'])
 def reject(self,cb):
  p=copy.deepcopy(self.prop);cb(p)
  with self.assertRaises((SemanticError,ValueError,IntakeError)):review(self.repo,self.snapshot,p)
 def test_refuses_forged_authority(self):self.reject(lambda x:x.update(owner_accepted=True))
 def test_refuses_forged_implementation_rights(self):self.reject(lambda x:x.update(authorized_to_edit=True))
 def test_refuses_unsupported_after_quote(self):self.reject(lambda x:x['claims'][0]['after_evidence'][0].update(quote='SPOOFED_FUNCTION_BODY'))
 def test_refuses_wrong_source_line(self):self.reject(lambda x:x['claims'][0]['after_evidence'][0].update(start=1,end=1))
 def test_refuses_traversal(self):self.reject(lambda x:x['claims'][0]['after_evidence'][0].update(path='../secret.txt'))
 def test_refuses_unknown_capability(self):self.reject(lambda x:x['claims'][0].update(capability_id='phantom'))
 def test_refuses_unapproved_goal_becoming_approved(self):self.reject(lambda x:x.update(theory_approved=True))
 def test_refuses_non_descendant(self):self.reject(lambda x:x.update(head_sha='f'*40))
 def test_refuses_wrong_baseline(self):self.reject(lambda x:x.update(base_sha='0'*40))
 def test_refuses_malformed_claim(self):self.reject(lambda x:x['claims'][0].update(open_questions=[]))
 def test_ledger_is_idempotent_and_unapproved(self):
  data=review(self.repo,self.snapshot,self.prop)
  path=self.root/'ledger'
  a=store_in_ledger(path,data);b=store_in_ledger(path,data)
  self.assertEqual(a,b)
  idx=json.loads((path/'index.json').read_text('utf-8'))
  self.assertEqual(len(idx['entries']),1)
  self.assertEqual(idx['entries'][0]['review_status'],'semantic-owner-review-pending')
  self.assertEqual(json.loads(Path(a['receipt_path']).read_text('utf-8')),data)
 def test_ledger_does_not_trust_corruption(self):
  data=review(self.repo,self.snapshot,self.prop);p=self.root/'ledger';a=store_in_ledger(p,data)
  Path(a['receipt_path']).write_text('{"x":1}','utf-8')
  with self.assertRaises(SemanticError):store_in_ledger(p,data)
 def test_concurrent_writer_fails_closed(self):
  data=review(self.repo,self.snapshot,self.prop);path=self.root/'ledger';path.mkdir()
  (path/'.writer-lock').write_text('another worker','utf-8')
  with self.assertRaises(SemanticError):store_in_ledger(path,data)
 def test_parallel_agents_create_conflict_not_silent_overwrite(self):
  data=review(self.repo,self.snapshot,self.prop);path=self.root/'ledger'
  a=store_in_ledger(path,data)
  other=copy.deepcopy(data)
  other['claims'][0]['user_effect']='另一条 AI 提供了完全不同且未经验证的行为解释，这一解释可能与第一个线程相冲突'
  b=store_in_ledger(path,other)
  self.assertNotEqual(a['digest'],b['digest'])
  index=json.loads((path/'index.json').read_text('utf-8'))
  self.assertEqual(len(index['entries']),2)
  self.assertTrue(all(e['review_status']=='parallel-interpretations-review-required' for e in index['entries']))
  self.assertTrue(all(e['conflicts_with'] for e in index['entries']))
 def test_cli_end_to_end_creates_shareable_receipt(self):
  snap=self.root/'snapshot.json';snap.write_text(json.dumps(self.snapshot),'utf-8')
  prop=self.root/'proposal.json';prop.write_text(json.dumps(self.prop),'utf-8')
  receipt=self.root/'receipt.json';ledger=self.root/'ledger'
  script=Path(__file__).with_name('reconcile_semantics_v09.py')
  run=subprocess.run(['python',str(script),'--repo-root',str(self.repo),
      '--snapshot',str(snap),'--proposal',str(prop),'--out',str(receipt),
      '--ledger-dir',str(ledger)],capture_output=True,text=True,check=False)
  self.assertEqual(run.returncode,0,run.stderr)
  result=json.loads(receipt.read_text('utf-8'))
  self.assertEqual(result['claimed_count'],1)
  bundle_out=self.root/'bundle.json'
  run2=subprocess.run(['python',str(Path(__file__).with_name('export_semantic_ledger_v09.py')),
      '--ledger-dir',str(ledger),'--out',str(bundle_out)],capture_output=True,text=True,check=False)
  self.assertEqual(run2.returncode,0,run2.stderr)
  assembled=json.loads(bundle_out.read_text('utf-8'))
  self.assertEqual(assembled['records'][0],result)
  self.assertFalse(assembled['semantic_correctness_proven'])
 def test_diff_summary_does_not_approve_behavior(self):
  data=review(self.repo,self.snapshot,self.prop)
  self.assertGreater(data['git_diff_summary']['changed_files'],0)
  self.assertFalse(data['tests_verified'])

if __name__=='__main__':unittest.main()
