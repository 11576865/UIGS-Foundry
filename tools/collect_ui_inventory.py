#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, os, urllib.error, urllib.parse, urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/"outbox"/"sources.json"
INDEX=ROOT/"domains"/"interface-grammar"/"inventory"/"index.json"
COVERAGE=ROOT/"domains"/"interface-grammar"/"inventory"/"coverage.json"
REPORT=ROOT/"reports"/"generated"/"ui-surface-inventory.md"
TOKEN=os.environ.get("GITHUB_TOKEN","").strip()

def load(path:Path)->Any:
    return json.loads(path.read_text(encoding="utf-8"))

def api(url:str)->Any:
    attempts=[TOKEN,None] if TOKEN else [None]
    last=None
    for token in attempts:
        headers={"Accept":"application/vnd.github+json","User-Agent":"UIGS-UI-Inventory/1","X-GitHub-Api-Version":"2022-11-28"}
        if token:headers["Authorization"]=f"Bearer {token}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            last=exc
            if token and exc.code in {401,403,404}:continue
            raise
    raise RuntimeError(f"GitHub API failed: {last}")

def repo_json(repo:str,path:str,ref:str)->dict[str,Any]:
    encoded=urllib.parse.quote(path,safe="/")
    doc=api(f"https://api.github.com/repos/{repo}/contents/{encoded}?ref={urllib.parse.quote(ref,safe='')}")
    raw=base64.b64decode(str(doc["content"]).replace("\n",""))
    return json.loads(raw.decode("utf-8"))

def normalize_inventory(repo:str,branch:str,head:str,adapter:dict[str,Any],inventory:dict[str,Any])->tuple[dict[str,Any],list[dict[str,Any]]]:
    if str(inventory.get("repository",""))!=repo:
        raise ValueError(f"{repo}: inventory repository mismatch")
    surfaces=inventory.get("surfaces")
    if not isinstance(surfaces,list):
        raise ValueError(f"{repo}: surfaces must be an array")
    if int(inventory.get("surface_count",-1))!=len(surfaces):
        raise ValueError(f"{repo}: surface_count mismatch")
    ids=set();normalized=[];path=str(adapter["ui_inventory"]["path"])
    for surface in surfaces:
        sid=str(surface.get("id",""))
        if not sid:raise ValueError(f"{repo}: empty surface id")
        if sid in ids:raise ValueError(f"{repo}: duplicate surface id {sid}")
        ids.add(sid)
        refs=surface.get("source_refs",[])
        if not isinstance(refs,list) or not refs:raise ValueError(f"{repo}:{sid}: source_refs required")
        item=dict(surface)
        item.update({"project":inventory["project"],"repository":repo,"platform":inventory["platform"],"source_head":head,"inventory_path":path})
        normalized.append(item)
    source={"repository":repo,"project":inventory["project"],"platform":inventory["platform"],"default_branch":branch,"head_sha":head,"status":"available","inventory_path":path,"surface_count":len(normalized)}
    return source,normalized

def build_coverage(sources:list[dict[str,Any]],surfaces:list[dict[str,Any]])->dict[str,Any]:
    by_project=Counter(str(s["project"]) for s in surfaces);by_kind=Counter(str(s["kind"]) for s in surfaces)
    linked=[s for s in surfaces if s.get("patterns")];visual=[s for s in surfaces if s.get("visual_evidence")]
    return {"version":1,"sources_total":len(sources),"with_ui_inventory":sum(s.get("status")=="available" for s in sources),
      "missing_ui_inventory":[s["repository"] for s in sources if s.get("status")!="available"],"total_surfaces":len(surfaces),
      "by_project":dict(sorted(by_project.items())),"by_kind":dict(sorted(by_kind.items())),"with_pattern_links":len(linked),
      "pattern_link_count":sum(len(s.get("patterns",[])) for s in surfaces),"with_visual_evidence":len(visual),
      "missing_visual_evidence":[s["id"] for s in surfaces if not s.get("visual_evidence")]}

def render_report(sources:list[dict[str,Any]],coverage:dict[str,Any])->str:
    lines=["# Cross-project UI Surface Inventory","",
      f"Sources with inventory: {coverage['with_ui_inventory']}/{coverage['sources_total']}",
      f"Concrete surfaces: {coverage['total_surfaces']}",f"Pattern-linked surfaces: {coverage['with_pattern_links']}",
      f"Surfaces with production visual evidence: {coverage['with_visual_evidence']}","",
      "| Project | Repository | Source HEAD | Status | Surfaces |","| --- | --- | --- | --- | ---: |"]
    for source in sources:
        lines.append(f"| {source.get('project','—')} | {source['repository']} | {source['head_sha'][:10]} | {source['status']} | {source['surface_count']} |")
    lines += ["","## Boundary","",
      "- Concrete UI inventory is authoritative in each source repository; Foundry stores a derived cross-project index.",
      "- A surface may link zero or more reusable UIGS Patterns. Absence of a Pattern link does not make the concrete UI nonexistent.",
      "- Source references describe implementation location; production screenshots/recordings are a separate visual-evidence field.",
      "- Missing visual evidence remains explicit and is never substituted with Foundry reference-demo screenshots.",""]
    return "\n".join(lines)

def collect()->tuple[dict[str,Any],dict[str,Any],str]:
    cfg=load(SOURCES);sources=[];surfaces=[];global_ids=set()
    for source_cfg in cfg.get("sources",[]):
        repo=str(source_cfg["repository"]);meta=api(f"https://api.github.com/repos/{repo}");branch=str(meta.get("default_branch") or "main")
        branch_doc=api(f"https://api.github.com/repos/{repo}/branches/{urllib.parse.quote(branch,safe='')}");head=str(branch_doc["commit"]["sha"])
        try:adapter=repo_json(repo,".uigs/project.json",head)
        except urllib.error.HTTPError as exc:
            if exc.code==404:
                sources.append({"repository":repo,"default_branch":branch,"head_sha":head,"status":"adapter-missing","surface_count":0});continue
            raise
        ui=adapter.get("ui_inventory")
        if not isinstance(ui,dict):
            sources.append({"repository":repo,"project":adapter.get("project",repo.split("/")[-1]),"default_branch":branch,"head_sha":head,"status":"ui-inventory-missing","surface_count":0});continue
        inventory=repo_json(repo,str(ui["path"]),head);source,items=normalize_inventory(repo,branch,head,adapter,inventory)
        for item in items:
            if item["id"] in global_ids:raise ValueError(f"cross-project duplicate surface id {item['id']}")
            global_ids.add(item["id"]);surfaces.append(item)
        sources.append(source)
    sources.sort(key=lambda x:x["repository"]);surfaces.sort(key=lambda x:x["id"]);coverage=build_coverage(sources,surfaces)
    return {"version":1,"sources":sources,"surface_count":len(surfaces),"surfaces":surfaces},coverage,render_report(sources,coverage)

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args()
    index,coverage,report=collect()
    if args.check:
        if (load(INDEX) if INDEX.exists() else None)!=index or (load(COVERAGE) if COVERAGE.exists() else None)!=coverage:
            print("UI inventory derived files are stale");return 1
        print(f"UI inventory current: {coverage['total_surfaces']} surfaces");return 0
    INDEX.parent.mkdir(parents=True,exist_ok=True);REPORT.parent.mkdir(parents=True,exist_ok=True)
    INDEX.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    COVERAGE.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");REPORT.write_text(report,encoding="utf-8")
    print(f"UI inventory collected: {coverage['with_ui_inventory']}/{coverage['sources_total']} sources; {coverage['total_surfaces']} surfaces");return 0
if __name__=="__main__":raise SystemExit(main())
