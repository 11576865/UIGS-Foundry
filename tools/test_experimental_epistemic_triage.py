#!/usr/bin/env python3
from __future__ import annotations
import json
import tempfile
from pathlib import Path

from generate_experimental_epistemic_triage import generate

def write(root:Path,path:str,obj:dict):
    p=root/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")

def run():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        entries=[
            {"id":"REC.AGG","status":"experimental","path":"records/a.json"},
            {"id":"REC.PROMOTE","status":"experimental","path":"records/b.json"},
            {"id":"REC.MISSION","status":"experimental","path":"records/c.json"},
            {"id":"REC.CHALLENGE","status":"experimental","path":"records/d.json"},
        ]
        write(root,"catalog/index.json",{"patterns":[],"records":entries})
        write(root,"prevention/registry.json",{"schema_version":1,"entries":[{"id":"PREVENT.X","knowledge_refs":["records/d.json"],"enforcement":[],"recurrence_count":1}]})
        write(root,"records/a.json",{"claim_refs":["CLAIM.X"],"provenance":[]})
        write(root,"records/b.json",{"provenance":[
            {"source_type":"file","source":"o/r:impl","evidence_level":"production implementation"},
            {"source_type":"file","source":"o/r:test","evidence_level":"automated tests"}
        ]})
        write(root,"records/c.json",{"provenance":[{"source_type":"file","source":"o/r:policy","evidence_level":"documented policy"}]})
        write(root,"records/d.json",{"provenance":[{"source_type":"file","source":"o/r:impl","evidence_level":"production implementation"}]})
        report=generate(root,"2026-10-07T00:00:00+00:00")
        got={x["record_id"]:x["classification"] for x in report["items"]}
        assert got["REC.AGG"]=="aggregate_view"
        assert got["REC.PROMOTE"]=="promotion_candidate"
        assert got["REC.MISSION"]=="validation_mission"
        assert got["REC.CHALLENGE"]=="challenge_or_narrow"
        assert report["summary"]["experimental_records"]==4
    print("experimental epistemic triage tests passed")

if __name__=="__main__":
    run()
