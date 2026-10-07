#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
LEVEL_ORDER={"project":0,"milestone":1,"work_package":2,"turn":3}

def load(path:Path)->dict[str,Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate(root:Path=ROOT)->list[str]:
    base=root/".uigs"/"tasks"
    if not base.exists():
        return []
    tasks={}
    errors=[]
    for path in sorted(base.glob("*.json")):
        data=load(path)
        tid=str(data.get("task_id",""))
        if not tid:
            errors.append(f"{path.relative_to(root)}: missing task_id")
            continue
        if tid in tasks:
            errors.append(f"duplicate task_id {tid}")
        tasks[tid]=(path,data)

    for tid,(path,data) in tasks.items():
        rel=path.relative_to(root).as_posix()
        version=int(data.get("schema_version",1))
        if version<2:
            continue
        level=str(data.get("level",""))
        project_id=str(data.get("project_id",""))
        if level not in LEVEL_ORDER:
            errors.append(f"{rel}: schema v2 requires valid level")
            continue
        if not project_id:
            errors.append(f"{rel}: schema v2 requires project_id")
        parent=data.get("parent_task_id")
        if level=="project":
            if parent not in (None,""):
                errors.append(f"{rel}: project task must not have parent_task_id")
            gates=data.get("completion_gates",[])
            if not isinstance(gates,list) or not gates:
                errors.append(f"{rel}: project task requires completion_gates")
                gates=[]
            if data.get("status")=="completed":
                bad=[g.get("id") for g in gates if g.get("required",True) and g.get("status") not in {"passed","not_required"}]
                if bad:
                    errors.append(f"{rel}: project cannot be completed with unfinished required gates: {', '.join(map(str,bad))}")
        else:
            if not parent:
                errors.append(f"{rel}: non-project task requires parent_task_id")
            elif str(parent) not in tasks:
                errors.append(f"{rel}: missing parent task {parent}")
            else:
                parent_level=str(tasks[str(parent)][1].get("level",""))
                if parent_level in LEVEL_ORDER and LEVEL_ORDER[parent_level]>=LEVEL_ORDER[level]:
                    errors.append(f"{rel}: parent level {parent_level} must be above child level {level}")
        if level!="project" and data.get("status")=="completed" and project_id in tasks:
            project=tasks[project_id][1]
            if project.get("status")=="completed":
                pass
            # Child completion is intentionally independent from project completion.
    return errors

def main()->int:
    errors=validate(ROOT)
    if errors:
        print("task-state hierarchy validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("task-state hierarchy validation passed")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
