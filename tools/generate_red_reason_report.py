#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TRIAGE=ROOT/"outbox"/"triage"
OUT=ROOT/"reports"/"red-reason-status.md"

rows=[]
if TRIAGE.exists():
    for path in sorted(TRIAGE.rglob("*.json")):
        try:
            item=json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        red=item.get("red_reason")
        if isinstance(red,dict):
            rows.append((item,red))

categories=Counter(red.get("category","unknown") for _,red in rows)
review=sum(1 for _,red in rows if red.get("needs_review"))
by_repo=defaultdict(Counter)
for item,red in rows:
    by_repo[item.get("source_repository","unknown")][red.get("category","unknown")]+=1

lines=[
    "# UIGS Red Reason Status","",
    f"Generated: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
    f"Triaged CI failures: {len(rows)}",
    f"Needs review: {review}","",
    "## Categories"
]
lines += [f"- {k}: {v}" for k,v in sorted(categories.items())] or ["- none"]
lines += ["","## By repository"]
if by_repo:
    for repo,counter in sorted(by_repo.items()):
        details=", ".join(f"{k}={v}" for k,v in sorted(counter.items()))
        lines.append(f"- {repo}: {details}")
else:
    lines.append("- none")
lines += ["","Automatic Red Reason classification is a triage aid, not a root-cause verdict.",""]
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text("\n".join(lines),encoding="utf-8")
print(OUT)
