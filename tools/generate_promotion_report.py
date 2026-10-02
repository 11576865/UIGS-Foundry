#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import Counter,defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import intake_state

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reports"/"promotion-status.md"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

proposals=[]
base=ROOT/"outbox"/"proposals"
if base.exists():
    for path in sorted(base.rglob("*.json")):
        try: proposals.append((path,load(path)))
        except Exception: pass
reviews=intake_state.review_items(ROOT)
review_by_packet={str(item.get("packet_id","")):item for _,item in reviews}
open_props=[(p,x) for p,x in proposals if str(x.get("packet_id","")) not in review_by_packet]
decisions=Counter(str(x.get("decision","unknown")) for _,x in reviews)
by_repo=defaultdict(int)
for _,x in open_props:
    by_repo[str(x.get("source_repository","unknown"))]+=1
typed=list((ROOT/"intake"/"records").rglob("*.json")) if (ROOT/"intake"/"records").exists() else []

lines=[
    "# UIGS Promotion Status","",
    f"Proposals total/open: {len(proposals)}/{len(open_props)}",
    f"Reviews: {len(reviews)}",
    f"Typed intake records: {len(typed)}",
    "",
    "## Review decisions"
]
lines += [f"- {k}: {v}" for k,v in sorted(decisions.items())] or ["- none"]
lines += ["","## Open proposals by source"]
lines += [f"- {repo}: {count}" for repo,count in sorted(by_repo.items())] or ["- none"]
lines += ["","Accepted records remain low-maturity intake knowledge unless separately promoted under governance/PROMOTION.md.",""]
OUT.write_text("\n".join(lines),encoding="utf-8")
print(OUT)
