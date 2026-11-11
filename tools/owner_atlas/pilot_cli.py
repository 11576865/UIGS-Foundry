#!/usr/bin/env python3
"""Read-only HSR historical semantic replay with persistent unapproved candidate ledger.

Run in a GitHub Actions manual replay job or locally where an actual full HSR Git
checkout containing both commits exists. Never modifies product source or policy.
"""
from pathlib import Path
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from reconcile_semantics_v09 import review,store_in_ledger,read_limited,atomic_json
from export_semantic_ledger_v09 import bundle

def replay(repo:Path, fixture:Path, out:Path)->dict:
    snapshot=read_limited(fixture/'snapshot.json')
    proposal=read_limited(fixture/'proposal.json')
    result=review(repo,snapshot,proposal)
    out.mkdir(parents=True,exist_ok=True)
    atomic_json(out/'review.json',result)
    ledger=out/'ledger'
    item=store_in_ledger(ledger,result)
    packet=bundle(ledger)
    atomic_json(out/'handoff.json',packet)
    return {'source_quote_checked':result['source_quote_checked'],
      'review_state':result['authority'],'candidate_digest':item['digest'],
      'handoff':str(out/'handoff.json'),'product_tests_executed':False,
      'semantic_correctness_proven':False,'owner_approved':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root',required=True,type=Path)
    p.add_argument('--fixture',type=Path,default=ROOT/'fixtures'/'hsr-pr194')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    x=replay(a.repo_root,a.fixture,a.out)
    print(json.dumps(x,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
