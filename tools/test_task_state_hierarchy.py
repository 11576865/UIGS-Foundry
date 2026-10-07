#!/usr/bin/env python3
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from validate_task_states import validate

def write(root:Path,name:str,obj:dict):
    p=root/".uigs"/"tasks"/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj),encoding="utf-8")

def base(tid,level,status="completed"):
    return {
        "schema_version":2,"task_id":tid,"goal":"x","status":status,"level":level,
        "project_id":"project","parent_task_id":None if level=="project" else "project",
        "current_work_unit":None,"completed_units":[],"next_units":[],"repository":"o/r",
        "last_durable_commit":None,"external_validation":{},"blockers":[],"updated_at":"2026-10-07T00:00:00+00:00"
    }

def run():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        project=base("project","project","completed")
        project["completion_gates"]=[{"id":"g","required":True,"status":"pending","description":"gate","evidence":[]}]
        write(root,"project.json",project)
        child=base("child","work_package","completed")
        write(root,"child.json",child)
        errs=validate(root)
        assert any("project cannot be completed" in x for x in errs)
        project["status"]="in_progress"
        write(root,"project.json",project)
        assert validate(root)==[]
    print("task-state hierarchy tests passed")

if __name__=="__main__":
    run()
