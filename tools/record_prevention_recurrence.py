#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
def load(path:Path)->dict[str,Any]: return json.loads(path.read_text(encoding="utf-8"))
def dump(path:Path,data:dict[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def slug(value:str)->str: return re.sub(r"[^A-Za-z0-9._-]+","_",value).strip("_")
def record_recurrence(root:Path,prevention_id:str,event_id:str,observed_at:str,source_ref:str,project:str|None=None,pull_request:int|None=None,directness:str="real_sample",notes:str|None=None):
    registry_path=root/"prevention"/"registry.json"; registry=load(registry_path)
    if registry.get("schema_version")!=2: raise ValueError("prevention registry must be schema_version 2")
    entry=next((x for x in registry.get("entries",[]) if x.get("id")==prevention_id),None)
    if entry is None: raise ValueError(f"unknown prevention id {prevention_id}")
    if any(x.get("id")==event_id for e in registry.get("entries",[]) for x in e.get("recurrence_events",[])): raise ValueError(f"duplicate recurrence event {event_id}")
    generation=int(entry["enforcement_generation"]); claim_id=str(entry["effectiveness_claim_ref"])
    claim_path=root/"knowledge"/"claims"/f"{claim_id}.json"; claim=load(claim_path)
    if not claim_id.endswith(f".G{generation}"): raise ValueError("effectiveness claim is not generation-aligned")
    if not (root/source_ref).is_file(): raise ValueError(f"source_ref does not exist: {source_ref}")
    evidence_id=f"EVID.PREVENT.{slug(event_id.removeprefix('RECURRENCE.'))}"; evidence_path=root/"knowledge"/"evidence"/f"{evidence_id}.json"
    if evidence_path.exists(): raise ValueError(f"evidence already exists: {evidence_id}")
    evidence={"schema_version":1,"id":evidence_id,"status":"active","source":{"type":"file","locator":source_ref,"revision":None,"environment_fingerprint":f"{prevention_id}:generation-{generation}"},"observed_at":observed_at,"valid_until":None,"independence_key":f"RECURRENCE.{slug(prevention_id)}.{slug(event_id)}","provenance":{"entity_id":event_id,"activity_id":"prevention-recurrence-recording","agent_id":"UIGS-Foundry","was_derived_from":[],"was_attributed_to":project},"relations":[{"claim_id":claim_id,"result":"contradicts","defeater_type":"rebutting","directness":directness,"scope_relation":"within_scope","assumption_context":[],"notes":notes or f"Recurrence occurred while prevention generation {generation} was current."}]}
    refs=list(claim.get("evidence_refs",[]))
    if evidence_id not in refs: refs.append(evidence_id)
    claim["evidence_refs"]=refs; claim["updated_at"]=observed_at
    event={"id":event_id,"generation":generation,"observed_at":observed_at,"source_ref":source_ref,"evidence_ref":evidence_id,"status":"active","project":project,"pull_request":pull_request,"resolved_by_generation":None,"notes":notes}
    entry.setdefault("recurrence_events",[]).append(event); entry["recurrence_count"]=int(entry.get("legacy_unattributed_recurrence_count",0))+len(entry["recurrence_events"])
    dump(evidence_path,evidence); dump(claim_path,claim); dump(registry_path,registry)
    return event,evidence,claim
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--prevention-id",required=True); ap.add_argument("--event-id",required=True); ap.add_argument("--observed-at",required=True); ap.add_argument("--source-ref",required=True); ap.add_argument("--project",default=None); ap.add_argument("--pull-request",type=int,default=None); ap.add_argument("--directness",choices=["static","inferred","runtime","real_sample","device_or_final_output"],default="real_sample"); ap.add_argument("--notes",default=None); a=ap.parse_args()
    event,evidence,claim=record_recurrence(ROOT,a.prevention_id,a.event_id,a.observed_at,a.source_ref,a.project,a.pull_request,a.directness,a.notes)
    print(json.dumps({"event":event["id"],"evidence":evidence["id"],"claim":claim["id"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
