#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"domains"/"interface-grammar"/"showcases"/"baseline-targets.json"
MANIFESTS=ROOT/"domains"/"interface-grammar"/"showcases"/"manifests"
BASELINES=ROOT/"domains"/"interface-grammar"/"showcases"/"baselines"

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def browser()->str:
    for name in ("google-chrome","google-chrome-stable","chromium","chromium-browser"):
        found=shutil.which(name)
        if found:return found
    raise RuntimeError("No supported Chromium/Chrome executable found on runner")
def version(exe:str)->str:
    return subprocess.check_output([exe,"--version"],text=True,stderr=subprocess.STDOUT).strip()

def main()->int:
    cfg=load(CONFIG);exe=browser();browser_version=version(exe);BASELINES.mkdir(parents=True,exist_ok=True)
    source_by_id={}
    for p in MANIFESTS.glob("*.json"):
        d=load(p)
        if d.get("type")=="reference-demo":source_by_id[str(d["id"])]=(p,d)
    generated=0
    for target in cfg.get("targets",[]):
        source_id=str(target["source_showcase"])
        if source_id not in source_by_id:raise RuntimeError(f"Unknown source showcase: {source_id}")
        source_path,source=source_by_id[source_id]
        viewport=target.get("viewport",{});width=int(viewport.get("width",1440));height=int(viewport.get("height",900))
        suffix=f"{width}X{height}"
        baseline_id="SHOWCASE.BASELINE."+source_id.removeprefix("SHOWCASE.").replace(".WEB_REFERENCE","")+"."+suffix
        filename=baseline_id+".png";png=BASELINES/filename
        entry=ROOT/source["entrypoint"]
        cmd=[exe,"--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars",f"--window-size={width},{height}",f"--screenshot={png}",entry.resolve().as_uri()]
        subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
        digest=hashlib.sha256(png.read_bytes()).hexdigest()
        manifest={
            "$schema":"../../../../../schemas/ui-showcase.schema.json",
            "id":baseline_id,"type":"visual-baseline","status":"experimental","platform":"web",
            "patterns":source["patterns"],"entrypoint":png.relative_to(ROOT).as_posix(),
            "states":["reference demo default state"],"expected_effects":["Pixel baseline for deterministic reference-demo regression at the declared viewport."],
            "limitations":["Baseline covers only the default state; interactive states require separate declared captures.","Reference-demo baseline is not production-product visual evidence."],
            "source_showcase":source_path.relative_to(ROOT).as_posix(),
            "viewport":{"width":width,"height":height},"theme":str(target.get("theme","browser-default")),
            "browser":{"executable":Path(exe).name,"version":browser_version},"sha256":digest,
            "provenance":[{"source_type":"repository","source":"11576865/UIGS-Foundry","revision":os.environ.get("GITHUB_SHA","local"),"evidence_level":"generated visual baseline"}]
        }
        out=MANIFESTS/(baseline_id+".json")
        out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        generated+=1
        print(f"{baseline_id}: {digest}")
    print(f"generated baselines: {generated}; browser={browser_version}")
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except Exception as exc:
        print(f"baseline capture failed: {type(exc).__name__}: {exc}",file=sys.stderr);raise
