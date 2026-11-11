#!/usr/bin/env python3
"""Export bounded owner-atlas candidate ledger for offline browser handoff.

The exported JSON is unsigned; source SHA checks MUST be repeated after import.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from reconcile_semantics_v09 import (read_limited,check,digest,atomic_json,
    REVIEW_SCHEMA,LEDGER_SCHEMA,SemanticError)

BUNDLE_SCHEMA='uigs-owner-atlas-semantic-bundle/1'

def bundle(directory:Path)->dict:
    index=read_limited(directory/'index.json')
    check(index.get('schema')==LEDGER_SCHEMA and index.get('authority')=='candidate-only-not-approved','Ledger index authority invalid')
    entries=index.get('entries')
    check(type(entries) is list and len(entries)<=100,'Ledger too large; paginate via separate bundles')
    records=[];digests=set()
    for entry in entries:
        key=entry.get('digest')
        check(isinstance(key,str) and len(key)==64 and key not in digests,'Missing/duplicate record digest')
        digests.add(key)
        check(entry.get('review_status') in ('semantic-owner-review-pending','parallel-interpretations-review-required'),'Invalid review state')
        p=directory/'candidates'/f'{key}.json'
        record=read_limited(p)
        check(record.get('schema')==REVIEW_SCHEMA and digest(record)==key,'Digest mismatch or altered semantic review')
        check(entry.get('repository')==record['repository'] and entry.get('base_sha')==record['base_sha'] and entry.get('head_sha')==record['head_sha'],'Record/index identity mismatch')
        check(entry.get('receipt_path')==f'candidates/{key}.json','Unsafe/counterfeit receipt path')
        check(record.get('semantic_correctness_proven') is False and record.get('owner_accepted') is False,'Promoted records cannot be exported as candidate')
        records.append(record)
    for entry in entries:
        check(set(entry.get('conflicts_with',[])).issubset(digests),'Conflict references unknown records')
    return {'schema':BUNDLE_SCHEMA,'authority':'unsigned-candidate-archive-not-product-acceptance',
        'index':index,'records':records,'source_authenticity':'requires-independent-local-git-recheck',
        'owner_approved_theory':False,'owner_accepted':False,
        'semantic_correctness_proven':False,'implementation_authorized':False}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--ledger-dir',required=True,type=Path);a.add_argument('--out',required=True,type=Path)
    opt=a.parse_args()
    try:
        result=bundle(opt.ledger_dir)
        atomic_json(opt.out,result)
        print('Exported',len(result['records']),'unapproved candidate records to',opt.out)
    except (OSError,ValueError,KeyError,TypeError,SemanticError) as exc:
        a.exit(2,'Ledger export refused: '+str(exc)+'\n')
if __name__=='__main__': main()
