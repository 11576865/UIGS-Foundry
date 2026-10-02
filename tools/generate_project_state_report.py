#!/usr/bin/env python3
from __future__ import annotations
import json, os, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT_DIR=ROOT/"reports"/"generated"
TOKEN=os.environ.get("GITHUB_TOKEN","").strip() or None

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def api_json(url: str) -> Any:
    attempts=[TOKEN,None] if TOKEN else [None]
    last=None
    for token in attempts:
        headers={"Accept":"application/vnd.github+json","User-Agent":"UIGS-Project-State/1","X-GitHub-Api-Version":"2022-11-28"}
        if token:
            headers["Authorization"]=f"Bearer {token}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as exc:
            last=exc
            if token and exc.code in {401,403,404}:
                continue
            raise
        except Exception as exc:
            last=exc
            raise
    raise RuntimeError(f"GitHub API failed: {last}")

def latest_by_name(runs: list[dict[str,Any]], names: list[str]) -> list[dict[str,Any]]:
    result=[]
    for name in names:
        matches=[r for r in runs if str(r.get("name",""))==name]
        matches.sort(key=lambda r:(str(r.get("created_at","")),int(r.get("run_number") or 0)),reverse=True)
        if not matches:
            result.append({"name":name,"found":False,"status":"unknown","conclusion":"unknown","head_sha":"","head_matches_main":False})
            continue
        r=matches[0]
        result.append({
            "name":name,
            "found":True,
            "status":str(r.get("status") or "unknown"),
            "conclusion":str(r.get("conclusion") or ""),
            "head_sha":str(r.get("head_sha") or ""),
            "head_matches_main":False,
            "run_id":r.get("id"),
            "run_number":r.get("run_number"),
            "event":str(r.get("event") or ""),
            "created_at":str(r.get("created_at") or ""),
            "updated_at":str(r.get("updated_at") or ""),
            "html_url":str(r.get("html_url") or ""),
        })
    return result

def count_local(repo: str) -> tuple[int,int]:
    pending=0; triage=0
    for base,kind in ((ROOT/"outbox"/"pending","pending"),(ROOT/"outbox"/"triage","triage")):
        if not base.exists():
            continue
        for path in base.rglob("*.json"):
            try:
                item=load(path)
            except Exception:
                continue
            if str(item.get("source_repository",""))==repo:
                if kind=="pending": pending+=1
                else: triage+=1
    return pending,triage

def knowledge_count(repo: str) -> int:
    catalog=load(ROOT/"catalog"/"index.json")
    count=0
    for section in ("patterns","records"):
        for entry in catalog.get(section,[]):
            path=ROOT/str(entry.get("path",""))
            if not path.is_file():
                continue
            try:
                record=load(path)
            except Exception:
                continue
            prov=record.get("provenance",[]) if isinstance(record,dict) else []
            if any(repo in str(p.get("source","")) for p in prov if isinstance(p,dict)):
                count+=1
    return count

def project_state(manifest: dict[str,Any]) -> dict[str,Any]:
    project=str(manifest["project"]); repo=str(manifest["repository"])
    branch=str(manifest.get("default_branch") or "main")
    branch_doc=api_json(f"https://api.github.com/repos/{repo}/branches/{urllib.parse.quote(branch,safe='')}")
    head_sha=str(branch_doc["commit"]["sha"])
    head_date=str(branch_doc["commit"]["commit"]["committer"]["date"])
    runs_doc=api_json(f"https://api.github.com/repos/{repo}/actions/runs?branch={urllib.parse.quote(branch,safe='')}&per_page=100")
    runs=list(runs_doc.get("workflow_runs",[]))
    tracked=latest_by_name(runs,[str(x) for x in manifest.get("tracked_workflows",[])])
    for item in tracked:
        if item.get("found"):
            item["head_matches_main"]=item.get("head_sha")==head_sha
    pending,triage=count_local(repo)
    times=[head_date]+[str(x.get("updated_at","")) for x in tracked if x.get("updated_at")]
    return {
        "project":project,"repository":repo,"default_branch":branch,
        "head_sha":head_sha,"head_commit_date":head_date,
        "tracked_workflows":tracked,
        "pending_intake":pending,"triage_records":triage,
        "knowledge_records":knowledge_count(repo),
        "source_updated_at":max((t for t in times if t),default=head_date)
    }

def render_markdown(snapshot: dict[str,Any]) -> str:
    lines=[
        "# Cross-project State","",
        f"Source max updated at: {snapshot.get('source_max_updated_at','')}",
        "",
        "| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |",
        "| --- | --- | --- | ---: | ---: | ---: |"
    ]
    for p in snapshot["projects"]:
        wf=[]
        for x in p["tracked_workflows"]:
            if not x.get("found"):
                wf.append(f"{x['name']}: unknown")
                continue
            state=x.get("conclusion") or x.get("status") or "unknown"
            coverage="HEAD" if x.get("head_matches_main") else "older SHA"
            wf.append(f"{x['name']}: {state} ({coverage})")
        wf_text="<br>".join(wf) if wf else "none configured"
        lines.append(f"| {p['project']} | `{p['head_sha'][:10]}` | {wf_text} | {p['pending_intake']} | {p['triage_records']} | {p['knowledge_records']} |")
    lines += [
        "",
        "## Interpretation boundary","",
        "- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.",
        "- Path-filtered workflows may intentionally not run for every commit.",
        "- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.",
        "- API/report generation failure leaves the previous report untouched and makes the report workflow red.",
        ""
    ]
    return "\n".join(lines)

def main() -> int:
    manifests=[load(p) for p in sorted((ROOT/"projects").glob("*.project.json"))]
    projects=[]
    errors=[]
    for manifest in manifests:
        try:
            projects.append(project_state(manifest))
        except Exception as exc:
            errors.append(f"{manifest.get('repository','unknown')}: {type(exc).__name__}: {exc}")
    if errors:
        for e in errors: print("ERROR:",e)
        return 2
    snapshot={"schema_version":1,"projects":projects}
    snapshot["source_max_updated_at"]=max((p.get("source_updated_at","") for p in projects),default="")
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    (OUT_DIR/"project-state.json").write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT_DIR/"project-state.md").write_text(render_markdown(snapshot),encoding="utf-8")
    print(f"project-state: {len(projects)} projects")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
