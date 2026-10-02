#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def review_items(root: Path) -> list[tuple[Path,dict[str,Any]]]:
    base=root/"outbox"/"reviews"
    out=[]
    if not base.exists(): return out
    for path in sorted(base.rglob("*.json")):
        try: item=load(path)
        except Exception: continue
        if isinstance(item,dict): out.append((path,item))
    return out

def reviewed_packet_ids(root: Path) -> set[str]:
    return {str(item.get("packet_id","")) for _,item in review_items(root) if str(item.get("decision","")) in {"accept","reject"}}

def pending_packets(root: Path, open_only: bool=True) -> list[tuple[Path,dict[str,Any]]]:
    base=root/"outbox"/"pending"
    reviewed=reviewed_packet_ids(root) if open_only else set()
    out=[]
    if not base.exists(): return out
    for path in sorted(base.rglob("*.json")):
        try: item=load(path)
        except Exception: continue
        if not isinstance(item,dict): continue
        packet_id=str(item.get("packet_id",""))
        if open_only and packet_id in reviewed: continue
        out.append((path,item))
    return out
