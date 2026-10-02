#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROPOSALS=(ROOT/"outbox"/"proposals").resolve()
REVIEWS=ROOT/"outbox"/"reviews"
RECORDS=ROOT/"intake"/"records"
ALLOWED_TYPES={"observation","candidate","bug","case","test","lesson"}
ALLOWED_STATUS={"observed","candidate"}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def inside(base: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(base)
        return True
    except ValueError:
        return False

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--proposal",required=True)
    p.add_argument("--decision",choices=["accept","reject"],required=True)
    p.add_argument("--record-id",default="")
    p.add_argument("--status",choices=sorted(ALLOWED_STATUS),default="")
    p.add_argument("--reason",default="")
    args=p.parse_args()

    proposal_path=(ROOT/args.proposal).resolve()
    if not inside(PROPOSALS,proposal_path) or not proposal_path.is_file():
        raise SystemExit("proposal path must be an existing file under outbox/proposals")
    proposal=load(proposal_path)
    suggested=proposal["suggested_record"]
    packet_id=str(proposal["packet_id"])
    review={
        "schema_version":1,"packet_id":packet_id,"proposal_path":proposal_path.relative_to(ROOT).as_posix(),
        "decision":args.decision,"reason":args.reason
    }

    if args.decision=="accept":
        record_type=str(suggested.get("type",""))
        if record_type not in ALLOWED_TYPES:
            raise SystemExit("unsupported record type")
        status=args.status or str(suggested.get("status","observed"))
        if status not in ALLOWED_STATUS:
            raise SystemExit("acceptance may create only observed/candidate records")
        record_id=args.record_id.strip() or str(suggested.get("id",""))
        if not re.fullmatch(r"[A-Za-z0-9._-]{3,180}",record_id):
            raise SystemExit("invalid record id")
        record=dict(suggested)
        record["id"]=record_id
        record["status"]=status
        record["review_source"]=proposal_path.relative_to(ROOT).as_posix()
        out=RECORDS/record_type/(record_id+".json")
        text=json.dumps(record,ensure_ascii=False,indent=2)+"\n"
        if out.exists() and out.read_text(encoding="utf-8")!=text:
            raise SystemExit(f"record collision: {out.relative_to(ROOT)}")
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(text,encoding="utf-8")
        review["record_path"]=out.relative_to(ROOT).as_posix()
        review["record_id"]=record_id
        review["status"]=status

    REVIEWS.mkdir(parents=True,exist_ok=True)
    review_path=REVIEWS/(re.sub(r"[^A-Za-z0-9._-]+","_",packet_id)+".json")
    review_path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(review_path.relative_to(ROOT))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
