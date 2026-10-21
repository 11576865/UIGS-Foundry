#!/usr/bin/env python3
"""Source-anchored AI semantic proposal review for UIGS Owner Atlas.

Verify Git *source quotes* at exact before/after revisions and persist only an
UNAPPROVED interpretation. Never infer behavior, acceptance or model authority.
Python >=3.11, stdlib + local git, no credentials or model API.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from intake_git_v08 import build_intake, IntakeError

PROP_SCHEMA='uigs-owner-atlas-semantic-proposal/1'
REVIEW_SCHEMA='uigs-owner-atlas-semantic-review/1'
LEDGER_SCHEMA='uigs-owner-atlas-semantic-ledger/1'
SHA=re.compile(r'^[0-9a-f]{40}$')
SAFE_ID=re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$')
MAX_BYTES=128*1024

class SemanticError(ValueError):pass

def canonical(obj:Any)->str:
    return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def digest(obj:Any)->str:
    return hashlib.sha256(canonical(obj).encode('utf-8')).hexdigest()

def check(condition:bool,message:str)->None:
    if not condition: raise SemanticError(message)

def read_limited(p:Path)->dict:
    check(p.stat().st_size<=MAX_BYTES, 'Input file exceeds 128 KiB')
    data=json.loads(p.read_text('utf-8'))
    check(type(data) is dict,'Input must be an object')
    return data

def git(root:Path,*args:str)->bytes:
    try:
        proc=subprocess.run(['git','-C',str(root),*args],stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,check=False,timeout=35)
    except subprocess.TimeoutExpired as exc:raise SemanticError('Git timed out') from exc
    check(proc.returncode==0,'Git object lookup failed: '+proc.stderr.decode('utf-8','replace')[:160])
    return proc.stdout

def checked_path(path:str)->None:
    check(isinstance(path,str) and 0<len(path)<=260 and not path.startswith('/') and
          '\\' not in path and '\x00' not in path and not any(x in ('','.','..') for x in path.split('/')),
          'Unsafe source path')

def source_anchor(root:Path,repository:str,sha:str,anchor:dict)->dict:
    check(type(anchor) is dict and set(anchor)=={'path','start','end','quote'},'Source anchor keys invalid')
    path=anchor['path'];checked_path(path)
    start,end=anchor['start'],anchor['end']
    check(type(start) is int and type(end) is int and 1<=start<=end<=100000 and end-start<45,'Source range invalid')
    quote=anchor['quote']
    check(isinstance(quote,str) and 12<=len(quote)<=360 and '\x00' not in quote and '\n' not in quote,
          'Anchor quote must be a single source line excerpt of at least 12 chars')
    blob=git(root,'show',f'{sha}:{path}')
    check(len(blob)<=3*1024*1024, 'Source file too large for bounded verifier')
    try: decoded=blob.decode('utf-8')
    except UnicodeDecodeError as exc:raise SemanticError('Source file is not UTF-8') from exc
    lines=decoded.splitlines()
    check(end<=len(lines),'Anchor line range is absent from Git revision')
    # Require the quote on a single physical line in the submitted range.
    check(any(quote in line for line in lines[start-1:end]), 'Claimed quote does not exist at pinned source lines')
    return {'path':path,'start':start,'end':end,'quote':quote,
            'git_revision':sha,'source_sha256':hashlib.sha256(blob).hexdigest(),
            'source_url':f'https://github.com/{repository}/blob/{sha}/{path}#L{start}-L{end}'}

def review(root:Path,snapshot:dict,proposal:dict)->dict:
    check(proposal.get('schema')==PROP_SCHEMA,'Incorrect semantic proposal schema')
    project=snapshot['project'];repo=project['repository'];base=project['pinned_sha'];head=proposal.get('head_sha')
    check(proposal.get('repository')==repo and proposal.get('base_sha')==base,'Proposal repo/base mismatch')
    check(isinstance(head,str) and SHA.fullmatch(head) is not None,'Invalid head SHA')
    check(head!=base,'Semantic delta requires a different target commit')
    check(proposal.get('authority')=='ai-proposed-not-approved','AI proposal must not imply approval')
    for fld in ('theory_approved','owner_accepted','tests_verified','runtime_verified','semantic_verified','authorized_to_edit'):
        check(proposal.get(fld) is False,f'Proposal may not elevate {fld}')
    check(isinstance(proposal.get('claims'),list) and 1<=len(proposal['claims'])<=16,'1–16 claims required')
    intake=build_intake(root,snapshot,head)
    check(intake['base_sha']==base and intake['head_sha']==head,'Cannot verify exact commit ancestry')
    capids={c['id'] for c in snapshot['capabilities']}
    goalids={g['id'] for g in snapshot['goal_ledger']['goals']}
    accepted=[];seen=set()
    for item in proposal['claims']:
        check(type(item) is dict,'Invalid claim')
        cid=item.get('id');check(isinstance(cid,str) and SAFE_ID.fullmatch(cid) is not None and cid not in seen,'Claim ID invalid or duplicated');seen.add(cid)
        c=item.get('capability_id');check(c in capids,'Unknown capability ID')
        goals=item.get('goal_ids');check(type(goals) is list and len(goals)<=8 and all(g in goalids for g in goals),'Unknown documented goals')
        for field in ('before','after','user_effect','rationale'):
            check(isinstance(item.get(field),str) and 16<=len(item[field])<=1100,field+' must be a clear bounded explanation')
        checks=item.get('open_questions')
        check(type(checks) is list and 1<=len(checks)<=8 and all(isinstance(x,str) and 10<=len(x)<=300 for x in checks),'Open questions required')
        if item.get('relationship') not in ('replace','add','remove','move','split','preserve','unknown'):
            raise SemanticError('Relationship transition type invalid')
        old=item.get('before_evidence');new=item.get('after_evidence')
        check(type(old) is list and type(new) is list and 1<=len(old)<=5 and 1<=len(new)<=5,'Before & after evidence required')
        old_ok=[source_anchor(root,repo,base,a) for a in old]
        new_ok=[source_anchor(root,repo,head,a) for a in new]
        # No full inference from matching file names: evidence checked != behavior verified.
        accepted.append({'id':cid,'capability_id':c,'goal_ids':goals,'relationship':item['relationship'],
           'before':item['before'],'after':item['after'],'user_effect':item['user_effect'],
           'rationale':item['rationale'],'open_questions':checks,
           'before_source_checked':old_ok,'after_source_checked':new_ok,
           'interpretation_state':'source-anchored-candidate-semantic-review-pending',
           'business_meaning_verified':False,'tests_executed_here':False,
           'owner_theory_approved':False})
    report={'schema':REVIEW_SCHEMA,'authority':'git-objects-source-checked-not-semantic-approved',
      'repository':repo,'base_sha':base,'head_sha':head,
      'proposal_digest':digest(proposal),'git_intake_digest':digest(intake['changed']),
      'claimed_count':len(accepted),'claims':accepted,
      'git_diff_summary':intake['summary'], 'git_changed_paths':[f['path'] for f in intake['changed']],
      'source_revision_checked':True,'source_quote_checked':True,
      'semantic_correctness_proven':False,'tests_verified':False,'runtime_verified':False,
      'owner_approved_theory':False,'owner_accepted':False,'implementation_authorized':False,
      'required_next_actions':['AI 对照真实调用路径和持久理论要求复核每项候选语义解释',
       '用户审查 before/after 的业务理解；此收据不包含授权修改代码',
       '按固定 head SHA 分别验证测试、真实产物和历史行为保护',
       '交给下一线程后从 Git 重新核查源码证据，勿直接信任未签名 JSON']}
    return report

def atomic_json(path:Path,value:dict)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    candidate=path.with_name(path.name+'.tmp-'+str(os.getpid()))
    candidate.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n','utf-8')
    os.replace(candidate,path)

def store_in_ledger(directory:Path,report:dict)->dict:
    """Content-addressed candidate archive. Parallel interpretations stay visible.

    A create-exclusive lock fails closed on concurrent writers (and after an
    interrupted process); never overwrite a co-worker's ledger silently.
    """
    directory.mkdir(parents=True,exist_ok=True)
    lock=directory/'.writer-lock'
    try:
        fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError as exc:
        raise SemanticError('Ledger write locked; stop and investigate a concurrent/crashed writer') from exc
    try:
        os.close(fd)
        index=directory/'index.json'; content_id=digest(report)
        record=directory/'candidates'/f'{content_id}.json'
        if record.exists():
            check(read_limited(record)==report,'Existing content-addressed review was corrupted')
        else: atomic_json(record,report)
        if index.exists():
            manifest=read_limited(index)
            check(manifest.get('schema')==LEDGER_SCHEMA and isinstance(manifest.get('entries'),list),'Invalid existing ledger index')
        else: manifest={'schema':LEDGER_SCHEMA,'authority':'candidate-only-not-approved','entries':[]}
        if not any(x['digest']==content_id for x in manifest['entries']):
            caps=sorted({c['capability_id'] for c in report['claims']})
            clashes=[]
            for e in manifest['entries']:
                if e.get('repository')==report['repository'] and e.get('head_sha')==report['head_sha'] and set(caps).intersection(e.get('capability_ids',[])):
                    clashes.append(e['digest'])
                    e['review_status']='parallel-interpretations-review-required'
                    e['conflicts_with']=sorted(set(e.get('conflicts_with',[])+[content_id]))
            manifest['entries'].append({'digest':content_id,'repository':report['repository'],
                'base_sha':report['base_sha'],'head_sha':report['head_sha'],
                'capability_ids':caps,'claims':report['claimed_count'],
                'review_status':'parallel-interpretations-review-required' if clashes else 'semantic-owner-review-pending',
                'conflicts_with':clashes,'receipt_path':f'candidates/{content_id}.json'})
            atomic_json(index,manifest)
        return {'ledger_index':str(index),'receipt_path':str(record),'digest':content_id}
    finally:
        lock.unlink(missing_ok=True)

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root',required=True,type=Path)
    p.add_argument('--snapshot',required=True,type=Path)
    p.add_argument('--proposal',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--ledger-dir',type=Path,help='append candidate record and update index (no promotion)')
    args=p.parse_args()
    try:
        snap=read_limited(args.snapshot);prop=read_limited(args.proposal)
        result=review(args.repo_root,snap,prop)
        atomic_json(args.out,result)
        status=store_in_ledger(args.ledger_dir,result) if args.ledger_dir else None
        print(json.dumps({'review_out':str(args.out),'head':result['head_sha'],
           'source_checked_claims':result['claimed_count'], 'semantic_accepted':False,
           'ledger':status},ensure_ascii=False))
    except (OSError,ValueError,KeyError,TypeError,IntakeError,subprocess.SubprocessError) as exc:
        p.exit(2,'Semantic proposal refused: '+str(exc)+'\n')

if __name__=='__main__':main()
