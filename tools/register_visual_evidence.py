#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, struct
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
SURFACE_INDEX=ROOT/"domains"/"interface-grammar"/"inventory"/"index.json"

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))

def png_size(path:Path)->tuple[int,int]:
    raw=path.read_bytes()
    if len(raw)<24 or raw[:8]!=b"\x89PNG\r\n\x1a\n" or raw[12:16]!=b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II",raw[16:24])

def surface_patterns(ids:list[str])->list[str]:
    if not SURFACE_INDEX.is_file():return []
    index=load(SURFACE_INDEX);wanted=set(ids);patterns=set()
    for surface in index.get("surfaces",[]):
        if surface.get("id") in wanted:patterns.update(str(x) for x in surface.get("patterns",[]))
    return sorted(patterns)

def register(contract_path:Path,capture_id:str,source_repository:str,source_revision:str,image_path:Path,output_path:Path,metadata_path:Path|None=None)->dict[str,Any]:
    contract=load(contract_path)
    capture=next((x for x in contract.get("captures",[]) if x.get("id")==capture_id),None)
    if capture is None:raise ValueError(f"capture not found: {capture_id}")
    raw=image_path.read_bytes();digest=hashlib.sha256(raw).hexdigest();width,height=png_size(image_path)
    previous=None
    if output_path.is_file():
        try:previous=load(output_path).get("sha256")
        except Exception:previous=None
    change="new" if previous is None else ("unchanged" if previous==digest else "changed")
    metadata=load(metadata_path) if metadata_path and metadata_path.is_file() else {}
    rel=image_path.resolve().relative_to(ROOT.resolve()).as_posix()
    surfaces=[str(x) for x in capture["surface_ids"]]
    manifest={
      "$schema":"../../../../schemas/ui-production-visual-evidence.schema.json",
      "id":"VISUAL.PRODUCTION."+capture_id,
      "record_type":"ui-production-visual-evidence",
      "status":"experimental",
      "evidence_level":capture["evidence_level"],
      "platform":contract["platform"],
      "capture_id":capture_id,
      "surface_ids":surfaces,
      "patterns":surface_patterns(surfaces),
      "entrypoint":rel,
      "source_repository":source_repository,
      "source_revision":source_revision,
      "sha256":digest,
      "image":{"width":width,"height":height},
      "environment":metadata,
      "capture_contract":{
        "adapter":capture["adapter"],
        "route":capture.get("route"),
        "selector":capture.get("selector"),
        "capture_region":capture.get("capture_region"),
        "viewport":capture.get("viewport"),
        "device":capture.get("device"),
        "ready":capture.get("ready")
      },
      "change_status":change,
      "previous_sha256":previous,
      "limitations":capture.get("limitations",[]),
      "provenance":[
        {"source_type":"repository","source":source_repository,"revision":source_revision,"evidence_level":capture["evidence_level"]},
        {"source_type":"capture-contract","source":f"{source_repository}:{contract_path.name}","revision":source_revision,"evidence_level":"source-owned capture declaration"}
      ]
    }
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--contract",required=True);p.add_argument("--capture-id",required=True)
    p.add_argument("--source-repository",required=True);p.add_argument("--source-revision",required=True)
    p.add_argument("--image",required=True);p.add_argument("--output-manifest",required=True);p.add_argument("--metadata")
    a=p.parse_args()
    m=register(Path(a.contract),a.capture_id,a.source_repository,a.source_revision,Path(a.image),Path(a.output_manifest),Path(a.metadata) if a.metadata else None)
    print(f"{m['id']}: {m['change_status']} {m['image']['width']}x{m['image']['height']} {m['sha256']}")
    return 0
if __name__=="__main__":raise SystemExit(main())
