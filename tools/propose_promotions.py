#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, unicodedata
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PENDING=ROOT/"outbox"/"pending"
TRIAGE=ROOT/"outbox"/"triage"
PROPOSALS=ROOT/"outbox"/"proposals"
KNOWN_DOMAINS={"interface-grammar","reliability","architecture","operations"}
TYPE_PREFIX={"observation":"OBS","candidate":"CAND","bug":"BUG","case":"CASE","test":"TEST","lesson":"LESSON"}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value: str) -> str:
    value=unicodedata.normalize("NFKC",value).lower()
    return re.sub(r"\s+"," ",value).strip()

def grams(value: str) -> set[str]:
    value=re.sub(r"\s+","",norm(value))
    if len(value)<2:
        return {value} if value else set()
    return {value[i:i+2] for i in range(len(value)-1)}

def similarity(a: str,b: str) -> float:
    ga,gb=grams(a),grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga&gb)/len(ga|gb)

def safe_slug(value: str, limit: int=42) -> str:
    ascii_words=re.findall(r"[A-Za-z0-9]+",unicodedata.normalize("NFKD",value))
    slug="_".join(ascii_words[:6]).upper()
    return (slug[:limit].strip("_") or "RECORD")

def repo_slug(repo: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+","_",repo.split("/")[-1]).strip("_").upper()

def find_packet(packet_id: str) -> tuple[Path,dict[str,Any]] | None:
    if not PENDING.exists():
        return None
    for path in PENDING.rglob("*.json"):
        try:
            packet=load(path)
        except Exception:
            continue
        if str(packet.get("packet_id",""))==packet_id:
            return path,packet
    return None

def catalog_records() -> list[dict[str,str]]:
    catalog=load(ROOT/"catalog"/"index.json")
    out=[]
    for section in ("patterns","records"):
        for entry in catalog.get(section,[]):
            path=ROOT/str(entry.get("path",""))
            if not path.is_file():
                continue
            try:
                data=load(path)
            except Exception:
                continue
            name=data.get("name")
            if isinstance(name,dict):
                title=" / ".join(str(name.get(k,"")) for k in ("zh","en") if name.get(k))
                summary=str(data.get("intent",""))
            else:
                title=str(data.get("title",entry.get("id","")))
                summary=str(data.get("summary",""))
            out.append({"id":str(entry.get("id","")),"title":title,"summary":summary})
    return out

def dedupe_candidates(title: str, summary: str, related: list[str], records: list[dict[str,str]]) -> list[dict[str,Any]]:
    found={}
    for rid in related:
        found[rid]={"id":rid,"score":1.0,"reason":"triage-related-record"}
    needle=f"{title} {summary}"
    for item in records:
        score=max(similarity(title,item["title"]), similarity(needle,f"{item['title']} {item['summary']}"))
        if score>=0.34 and item["id"] not in found:
            found[item["id"]]={"id":item["id"],"score":round(score,3),"reason":"lexical-similarity"}
    return sorted(found.values(),key=lambda x:(-float(x["score"]),x["id"]))[:8]

def suggested_record(packet: dict[str,Any]) -> dict[str,Any]:
    record_type=str(packet.get("record_type","observation"))
    if record_type not in TYPE_PREFIX:
        record_type="observation"
    status="candidate" if record_type=="candidate" else "observed"
    title=str(packet.get("title","")).strip()
    summary=str(packet.get("summary","")).strip()
    source_repo=str(packet.get("source_repository",""))
    packet_id=str(packet.get("packet_id",""))
    short=hashlib.sha256(packet_id.encode("utf-8")).hexdigest()[:8].upper()
    rid=f"{TYPE_PREFIX[record_type]}.{repo_slug(source_repo)}.{safe_slug(title)}.{short}"
    hints=[str(x) for x in packet.get("routing_hints",[]) if str(x)]
    domains=sorted(set(x for x in hints if x in KNOWN_DOMAINS))
    evidence=packet.get("evidence") if isinstance(packet.get("evidence"),dict) else {}
    metadata=packet.get("metadata") if isinstance(packet.get("metadata"),dict) else {}
    provenance=[{
        "source_type":"repository",
        "source":source_repo,
        "revision":str(packet.get("source_sha","")),
        "evidence_level":"durable intake packet",
        "note":packet_id
    }]
    links=[str(packet.get("source_url",""))] if str(packet.get("source_url","")).strip() else []
    return {
        "id":rid,"type":record_type,"status":status,"title":title,"summary":summary,
        "domains":domains,"tags":sorted(set(hints)),"provenance":provenance,"links":links,
        "source_packet":packet_id,
        "evidence_summary":{
            "root_cause_resolved": metadata.get("root_cause_status")=="resolved" or bool(evidence.get("root_cause")),
            "fix_present": bool(evidence.get("fix_commit") or evidence.get("fix_pr") or metadata.get("fix_merged")),
            "regression_evidence_present": bool(evidence.get("ci_run") or evidence.get("ci_result") or evidence.get("regression_test"))
        }
    }

def build_proposal(triage: dict[str,Any], packet: dict[str,Any], packet_path: Path, records: list[dict[str,str]]) -> dict[str,Any]:
    digest=hashlib.sha256(packet_path.read_bytes()).hexdigest()
    suggested=suggested_record(packet)
    related=[str(x) for x in triage.get("related_records",[]) if str(x)]
    return {
        "schema_version":1,
        "proposal_id":"proposal."+str(packet["packet_id"]),
        "proposal_status":"review_required",
        "packet_id":str(packet["packet_id"]),
        "source_repository":str(packet.get("source_repository","")),
        "packet_sha256":digest,
        "suggested_record":suggested,
        "evidence_assessment":suggested.get("evidence_summary",{}),
        "dedupe_candidates":dedupe_candidates(suggested["title"],suggested["summary"],related,records),
        "related_records":related,
        "triage_status":str(triage.get("triage_status","")),
        "proposed_at":str(triage.get("triaged_at") or packet.get("created_at") or "")
    }

def output_path(packet: dict[str,Any]) -> Path:
    repo=re.sub(r"[^A-Za-z0-9._-]+","__",str(packet.get("source_repository","unknown"))).strip("._-") or "unknown"
    return PROPOSALS/repo/(str(packet.get("packet_id","unknown"))+".json")

def run() -> tuple[int,int]:
    records=catalog_records()
    total=0; changed=0
    if not TRIAGE.exists():
        return 0,0
    for triage_path in sorted(TRIAGE.rglob("*.json")):
        triage=load(triage_path)
        if triage.get("triage_status")!="ready-for-record":
            continue
        if triage.get("record_type")=="ci_failure":
            continue
        located=find_packet(str(triage.get("packet_id","")))
        if not located:
            continue
        packet_path,packet=located
        total+=1
        proposal=build_proposal(triage,packet,packet_path,records)
        out=output_path(packet)
        text=json.dumps(proposal,ensure_ascii=False,indent=2)+"\n"
        if out.is_file() and out.read_text(encoding="utf-8")==text:
            continue
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(text,encoding="utf-8")
        changed+=1
    return total,changed

def main() -> int:
    total,changed=run()
    print(f"promotion proposals: eligible={total}, changed={changed}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
