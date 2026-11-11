#!/usr/bin/env python3
"""UIGS Owner Atlas v0.8: read-only, commit-pinned, evidence-aware Git change intake.

Only maps changed *source line ranges* to pre-existing evidence anchors; it cannot
claim semantic effects, tested behavior, theory approval, or agent authority.
Python 3.11+, git CLI, no external Python dependencies.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = 'uigs-owner-atlas-git-intake/1'
SHA = re.compile(r'^[0-9a-f]{40}$')
HUNK = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')
MAX_FILES = 500
MAX_HUNKS = 10000

class IntakeError(Exception):
    pass


def git(root: Path, *args: str, check: bool=True) -> str:
    cp = subprocess.run(['git', '-C', str(root), *args], stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, check=False, timeout=40)
    if check and cp.returncode:
        raise IntakeError('Git command failed (' + ' '.join(args[:3]) + '): '
                          + cp.stderr.decode('utf-8', 'replace')[:280].strip())
    return cp.stdout.decode('utf-8', 'replace').strip() if cp.returncode == 0 else ''


def verify_repo(root: Path, repository: str) -> dict[str, Any]:
    actual = Path(git(root, 'rev-parse', '--show-toplevel')).resolve()
    if root.resolve() != actual:
        raise IntakeError('Repository root must be the git toplevel (not an arbitrary subdirectory)')
    remote = git(root, 'remote', 'get-url', 'origin', check=False)
    # If a remote exists, it must not contradict the data's expected repository.
    if remote:
        cleaned = remote.rstrip('/').removesuffix('.git')
        match = (re.search(r'github\.com[:/]([^/]+/[^/]+)$', cleaned, flags=re.I))
        if not match or match.group(1).lower() != repository.lower():
            raise IntakeError('origin remote does not match the snapshot repository')
    return {'origin_remote_matches_snapshot': bool(remote),
            'origin_remote_not_configured': not bool(remote)}


def changed_files(root: Path, old: str, new: str) -> list[dict[str, Any]]:
    # name-status -z avoids shell splitting and handles CJK and spaces correctly.
    raw = subprocess.run(['git','-C',str(root),'diff','--no-ext-diff','--no-renames',
                          '--name-status','-z',old,new,'--'],capture_output=True,check=True,timeout=40).stdout
    parts = raw.decode('utf-8','replace').split('\0')
    if parts[-1] == '': parts.pop()
    if len(parts)%2: raise IntakeError('Unexpected git name-status format')
    if len(parts)//2 > MAX_FILES: raise IntakeError('Too many changed files to prove completeness')
    files = []
    for i in range(0,len(parts),2):
        status, path = parts[i:i+2]
        if status not in {'A','M','D','T','U'} or not path or '\0' in path:
            raise IntakeError('Unsupported Git path status (rename/copy/conflict must be reviewed manually)')
        hunks=[]
        diff = git(root,'diff','--no-ext-diff','--no-renames','--unified=0',old,new,'--',path)
        for line in diff.splitlines():
            m=HUNK.match(line)
            if m:
                hunks.append({'old_start':int(m[1]),'old_count':int(m[2] or 1),
                              'new_start':int(m[3]),'new_count':int(m[4] or 1)})
        files.append({'path':path,'status':status,'hunks':hunks})
    if sum(len(f['hunks']) for f in files)>MAX_HUNKS:
        raise IntakeError('Too many changed hunks to prove complete analysis')
    return files


def anchors_for(snapshot: dict[str, Any]):
    # Capability evidence belongs to pinned BEFORE commit. Other source lists
    # contribute anchors only to their own documented-goal objects.
    for c in snapshot['capabilities']:
        yield 'capability', c['id'], c['name'], c.get('evidence', [])
    for g in snapshot.get('goal_ledger',{}).get('goals',[]):
        yield 'documented_goal', g['id'], g['title'], (g.get('source', []) + g.get('implementation_evidence', []))


def classify(evidence: dict[str, Any], file: dict[str, Any]) -> str:
    """Direct old-line overlap; insertion adjacency; earlier line shift; path only."""
    try:
        start=int(evidence.get('start',0)); end=int(evidence.get('end',0))
    except (TypeError,ValueError): return 'file-only'
    if start<=0 or end<start: return 'file-only'
    for h in file['hunks']:
        a,b=h['old_start'],h['old_count']
        if b>0 and a<=end and a+b-1>=start:
            return 'anchor-overlap'
    for h in file['hunks']:
        if h['old_count']==0 and start-2<=h['old_start']<=end+2:
            return 'adjacent-insertion'
    for h in file['hunks']:
        if h['old_start']<start and h['new_count']!=h['old_count']:
            return 'anchor-line-shift-risk'
    return 'file-only'


RANK={'anchor-overlap':0,'adjacent-insertion':1,'anchor-line-shift-risk':2,'file-only':3}

def build_intake(root: Path, snapshot: dict[str, Any], after_rev: str='HEAD') -> dict[str, Any]:
    project=snapshot.get('project',{})
    repository=project.get('repository')
    base=project.get('pinned_sha')
    if not isinstance(repository,str) or not re.fullmatch(r'[\w.-]+/[\w.-]+',repository):
        raise IntakeError('Snapshot repository is missing/invalid')
    if not isinstance(base,str) or not SHA.fullmatch(base):
        raise IntakeError('Snapshot pinned SHA is invalid')
    if snapshot.get('schema_version')!=2:
        raise IntakeError('Expected Owner Atlas snapshot schema_version 2')
    meta=verify_repo(root,repository)
    if not git(root,'cat-file','-e',base+'^{commit}',check=False) and git(root,'cat-file','-t',base)!='commit':
        raise IntakeError('Pinned commit is absent: fetch full history or use the correct repository')
    head=git(root,'rev-parse','--verify',after_rev+'^{commit}')
    if not SHA.fullmatch(head): raise IntakeError('Git did not resolve a commit SHA')
    if subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',base,head],check=False,timeout=40).returncode:
        raise IntakeError('Selected head is NOT descended from the Atlas pinned commit')
    files=changed_files(root,base,head)
    by_path={f['path']:f for f in files}
    mapping=[]
    for kind,id_,name,anchors in anchors_for(snapshot):
        refs=[]
        for a in anchors:
            p=a.get('path','')
            if p in by_path:
                f=by_path[p]
                refs.append({'path':p,'label':a.get('label',a.get('note','')),
                             'old_start':a.get('start'), 'old_end':a.get('end'),
                             'kind':classify(a,f)})
        if refs:
            refs.sort(key=lambda x:(RANK[x['kind']], x['path']))
            mapping.append({'object_type':kind,'id':id_,'name':name,
                            'scope':'candidate-recheck-not-semantic-effect',
                            'strongest_overlap':refs[0]['kind'], 'anchors':refs})
    covered={x['path'] for x in mapping for x in x['anchors']}
    uncovered=[f['path'] for f in files if f['path'] not in covered]
    dirty=bool(git(root,'status','--porcelain',check=False))
    return {'schema':SCHEMA,'authority':'local-git-structural-evidence-not-semantic-approval',
            'repository':repository,'base_sha':base,'head_sha':head,
            'source':{'transport':'local-git-cli','revision_checked':True,
                      'worktree_dirty_ignored_for_commit_comparison':dirty, **meta},
            'summary':{'changed_files':len(files),'mapped_objects':len(mapping),
                       'direct_anchor_objects':sum(x['strongest_overlap']=='anchor-overlap' for x in mapping),
                       'unmapped_paths':len(uncovered)},
            'changed':files,'mapping':mapping,'unmapped_paths':uncovered,
            'test_execution_proven':False,'semantic_change_proven':False,
            'theory_approved':False,'owner_accepted':False,
            'next_agent_checks':[
                '读取现有目标台账和批准状态；不得从本报告推断授权实施',
                '在固定 head_sha 上重新核查每个被命中的真实调用、状态、副作用及 UI 路由',
                'anchor-overlap 只是旧源码区间交叉，不证明业务语义已经变化',
                'file-only/line-shift 是排查线索，不能作为所有功能都改变的结论',
                '未建立源代码锚点的新文件必须单独发现和分类能力',
                '将实际模型/理论差异与精确 SHA 测试、运行证据分开记录',
                '任何变更须先获得独立的产品实施授权'
            ]}


def agent_packet(report: dict[str,Any]) -> dict[str,Any]:
    return {'schema':'uigs-owner-atlas-change-review-task/1',
            'authority':'analysis-only-no-product-change-authorization',
            'repository':report['repository'], 'baseline_revision':report['base_sha'],
            'candidate_revision':report['head_sha'],
            'mapped':report['mapping'], 'unmapped_paths':report['unmapped_paths'],
            'required_verification':report['next_agent_checks'],
            'explicit_nonclaims':['not a semantic code analysis','no tests executed',
                                  'no owner-approved To-Be','not a product acceptance'],
            'required_output':['source-anchored As-Is before/after',
                               'affected capabilities and unaffected neighboring work',
                               'suspected duplicate state writers and alternate UI routes',
                               'tests actually run and remaining uncertainties',
                               'owner-readable proposed Delta, without modifying code']}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root',required=True,type=Path,help='full local git clone / CI checkout')
    p.add_argument('--snapshot',required=True,type=Path,help='v0.7 source-anchored JSON snapshot')
    p.add_argument('--after',default='HEAD',help='target commit or HEAD')
    p.add_argument('--out',required=True,type=Path,help='Git intake JSON')
    p.add_argument('--task-out',type=Path,help='optional next-agent analysis task JSON')
    a=p.parse_args()
    try:
        snapshot=json.loads(a.snapshot.read_text('utf-8'))
        report=build_intake(a.repo_root,snapshot,a.after)
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
        if a.task_out:
            a.task_out.parent.mkdir(parents=True,exist_ok=True)
            a.task_out.write_text(json.dumps(agent_packet(report),ensure_ascii=False,indent=2)+'\n','utf-8')
    except (IntakeError,OSError,ValueError,KeyError,subprocess.TimeoutExpired) as exc:
        p.exit(2,'Intake rejected: '+str(exc)+'\n')
    print(json.dumps({'out':str(a.out),'base':report['base_sha'][:12],
                      'head':report['head_sha'][:12],**report['summary']},ensure_ascii=False))

if __name__=='__main__':main()
