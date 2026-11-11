"""Require content-addressed receipts and reject forged completion in ledger export."""
from pathlib import Path
import copy
import json
import unittest
from test_reconcile_semantics_v09 import SemanticReviewTests
from reconcile_semantics_v09 import review,store_in_ledger,SemanticError
from export_semantic_ledger_v09 import bundle

class LedgerExportTests(SemanticReviewTests):
 def test_export_clean_bundle(self):
  r=review(self.repo,self.snapshot,self.prop)
  dest=self.root/'ledger';store_in_ledger(dest,r)
  b=bundle(dest)
  self.assertEqual(len(b['records']),1)
  self.assertFalse(b['owner_accepted'])
  self.assertEqual(b['records'][0]['head_sha'],self.new)
 def test_export_conflict_bundle_preserves_both(self):
  r=review(self.repo,self.snapshot,self.prop);dest=self.root/'ledger';store_in_ledger(dest,r)
  second=copy.deepcopy(r);second['claims'][0]['user_effect']='第二位 AI 对同一次修改给出另一种可能用户影响，需要独立验证之后才能确定哪种正确'
  store_in_ledger(dest,second)
  b=bundle(dest)
  self.assertEqual(len(b['records']),2)
  self.assertTrue(all(e['review_status']=='parallel-interpretations-review-required' for e in b['index']['entries']))
 def test_export_rejects_tampered_receipt(self):
  r=review(self.repo,self.snapshot,self.prop);dest=self.root/'ledger';m=store_in_ledger(dest,r)
  p=Path(m['receipt_path']);x=json.loads(p.read_text('utf-8'))
  x['owner_accepted']=True;p.write_text(json.dumps(x),'utf-8')
  with self.assertRaises(SemanticError):bundle(dest)
 def test_export_rejects_forged_index_approval(self):
  r=review(self.repo,self.snapshot,self.prop);dest=self.root/'ledger';store_in_ledger(dest,r)
  p=dest/'index.json';x=json.loads(p.read_text('utf-8'))
  x['entries'][0]['review_status']='approved';p.write_text(json.dumps(x),'utf-8')
  with self.assertRaises(SemanticError):bundle(dest)
 def test_export_rejects_nonexistent_conflict_reference(self):
  r=review(self.repo,self.snapshot,self.prop);dest=self.root/'ledger';store_in_ledger(dest,r)
  p=dest/'index.json';x=json.loads(p.read_text('utf-8'))
  x['entries'][0]['conflicts_with']=['e'*64];p.write_text(json.dumps(x),'utf-8')
  with self.assertRaises(SemanticError):bundle(dest)

if __name__=='__main__':unittest.main()
