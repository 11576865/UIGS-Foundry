#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,urllib.error,urllib.parse,urllib.request
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1];MANIFESTS=ROOT/"domains"/"interface-grammar"/"realizations"/"manifests";REPORT_JSON=ROOT/"reports"/"generated"/"ui-realization-state.json";REPORT_MD=ROOT/"reports"/"generated"/"ui-realization-state.md";TOKEN=os.environ.get("GITHUB_TOKEN","").strip()
def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def api(url:str)->Any:
    headers={"Accept":"application/vnd.github+json","User-Agent":"UIGS-Realization-Verifier/2","X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN:headers["Authorization"]=f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:return json.load(r)
def content_sha(repo:str,path:str,ref:str,api_func=api)->str|None:
    url=f"https://api.github.com/repos/{repo}/contents/{urllib.parse.quote(path,safe='/')}?ref={urllib.parse.quote(ref,safe='')}"
    try:doc=api_func(url)
    except urllib.error.HTTPError as exc:
        if exc.code==404:return None
        raise
    return str(doc.get("sha","")) or None
def verify_one(data:dict[str,Any],online:bool,api_func=api)->dict[str,Any]:
    repo=str(data["repository"]);revision=str(data["revision"]);branch=str(data.get("default_branch","main"))
    result={"id":data["id"],"project":data["project"],"platform":data["platform"],"repository":repo,"revision":revision,"source_files":[],"validation_files":[],"source_verified":True,"current_head":None,"head_matches_revision":None,"source_content_current":None,"validation_content_current":None}
    current_head=None
    if online:
        branch_doc=api_func(f"https://api.github.com/repos/{repo}/branches/{urllib.parse.quote(branch,safe='')}");current_head=str(branch_doc["commit"]["sha"]);result["current_head"]=current_head;result["head_matches_revision"]=current_head==revision
    for section in ("source_files","validation_files"):
        for item in data.get(section,[]):
            expected=str(item["blob_sha"]);path=str(item["path"]);row={"path":path,"expected_blob_sha":expected,"verified":None,"current_blob_sha":None,"current":None}
            if online:
                immutable=content_sha(repo,path,revision,api_func);row["actual_blob_sha"]=immutable;row["verified"]=immutable==expected
                if not row["verified"]:result["source_verified"]=False
                current=content_sha(repo,path,current_head,api_func) if current_head else None;row["current_blob_sha"]=current;row["current"]=current==expected
            result[section].append(row)
    if online:
        result["source_content_current"]=all(x["current"] is True for x in result["source_files"])
        vals=result["validation_files"];result["validation_content_current"]=all(x["current"] is True for x in vals) if vals else True
    return result
def render_markdown(rows:list[dict[str,Any]])->str:
    lines=["# UI Production Realization State","","| Realization | Platform | Revision vs HEAD | Immutable blobs | Current source content | Current validation content |","| --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        head="offline" if row["head_matches_revision"] is None else ("HEAD" if row["head_matches_revision"] else "older revision");immutable="verified" if row["source_verified"] else "MISMATCH"
        source="offline" if row["source_content_current"] is None else ("current" if row["source_content_current"] else "changed/missing");validation="offline" if row["validation_content_current"] is None else ("current" if row["validation_content_current"] else "changed/missing")
        lines.append(f"| {row['id']} | {row['platform']} | {head} | {immutable} | {source} | {validation} |")
    lines += ["","## Evidence boundary","","- Immutable verification proves the recorded historical evidence.","- Revision-vs-HEAD is repository-level currentness only; unrelated commits can move HEAD.","- Current source content compares declared implementation paths at current HEAD to recorded blob identities.","- Validation content is reported separately because tests can change without implementation source changing.","- Source currentness is not production visual evidence.",""];return "\n".join(lines)
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--offline",action="store_true");p.add_argument("--write-report",action="store_true");a=p.parse_args();rows=[];errors=[]
    for path in sorted(MANIFESTS.glob("*.json")):
        data=load(path)
        try:row=verify_one(data,not a.offline)
        except Exception as exc:errors.append(f"{data.get('id',path.name)}: {type(exc).__name__}: {exc}");continue
        rows.append(row)
        if not a.offline and not row["source_verified"]:errors.append(f"{row['id']}: immutable source blob mismatch")
    if a.write_report:
        REPORT_JSON.parent.mkdir(parents=True,exist_ok=True);REPORT_JSON.write_text(json.dumps({"schema_version":2,"realizations":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8");REPORT_MD.write_text(render_markdown(rows),encoding="utf-8")
    for row in rows:print(f"{row['id']}: immutable={'ok' if row['source_verified'] else 'BAD'}; head={row['head_matches_revision']}; source-current={row['source_content_current']}")
    if errors:
        for e in errors:print("ERROR:",e)
        return 2
    return 0
if __name__=="__main__":raise SystemExit(main())
