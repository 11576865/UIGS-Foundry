#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

LEVELS={"source","test","workflow","runtime","visual","device"}
KINDS={"pattern","capture_equal","capture_in_integer_set"}

def _safe_path(root: Path, raw: str) -> Path:
    path=(root/raw).resolve()
    try: path.relative_to(root)
    except ValueError: raise ValueError(f"path escapes root: {raw}")
    return path

def _read(root: Path, raw: str) -> str:
    path=_safe_path(root,raw)
    if not path.is_file(): raise ValueError(f"missing evidence file: {raw}")
    return path.read_text(encoding="utf-8")

def _capture(root: Path, locator: dict) -> str:
    raw_path=str(locator.get("path",""))
    pattern=str(locator.get("pattern",""))
    if not raw_path or not pattern: raise ValueError("capture locator requires path and pattern")
    try: match=re.search(pattern,_read(root,raw_path),re.MULTILINE)
    except re.error as exc: raise ValueError(f"{raw_path}: invalid regex: {exc}")
    if not match: raise ValueError(f"{raw_path}: pattern did not match: {pattern}")
    if match.lastindex is None: raise ValueError(f"{raw_path}: capture pattern requires a group")
    return match.group(1)

def validate_manifest(root: Path, manifest_path: Path) -> list[str]:
    errors=[]
    try: data=json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc: return [f"{manifest_path}: invalid JSON: {exc}"]
    if data.get("schema_version") != 1: errors.append("schema_version must be 1")
    if not str(data.get("project","")).strip(): errors.append("project is required")
    if "/" not in str(data.get("repository","")): errors.append("repository must be owner/name")
    invariants=data.get("invariants")
    if not isinstance(invariants,list) or not invariants: return errors+["invariants must be a non-empty array"]
    seen=set()
    for inv in invariants:
        iid=str(inv.get("id","")).strip()
        prefix=f"{iid or '<missing-id>'}: "
        if not iid: errors.append(prefix+"id is required"); continue
        if iid in seen: errors.append(prefix+"duplicate invariant id")
        seen.add(iid)
        if inv.get("status") not in {"active","retired"}: errors.append(prefix+"status must be active/retired")
        if inv.get("criticality") not in {"required","recommended"}: errors.append(prefix+"criticality must be required/recommended")
        if not str(inv.get("claim","")).strip(): errors.append(prefix+"claim is required")
        if inv.get("status")=="retired": continue
        required=set(inv.get("required_levels") or [])
        unknown=required-LEVELS
        if unknown: errors.append(prefix+f"unknown required_levels: {sorted(unknown)}")
        evidence=inv.get("evidence")
        if not isinstance(evidence,list) or not evidence:
            errors.append(prefix+"active invariant requires evidence")
            continue
        levels=set()
        eids=set()
        for item in evidence:
            eid=str(item.get("id","")).strip()
            eprefix=prefix+(eid or "<missing-evidence-id>")+": "
            if not eid: errors.append(eprefix+"id is required")
            elif eid in eids: errors.append(eprefix+"duplicate evidence id")
            eids.add(eid)
            level=item.get("level")
            kind=item.get("kind")
            if level not in LEVELS: errors.append(eprefix+"invalid level")
            else: levels.add(level)
            if kind not in KINDS: errors.append(eprefix+"invalid kind"); continue
            try:
                if kind=="pattern":
                    raw_path=str(item.get("path","")); pattern=str(item.get("pattern",""))
                    if not raw_path or not pattern: raise ValueError("pattern evidence requires path and pattern")
                    try: matched=re.search(pattern,_read(root,raw_path),re.MULTILINE)
                    except re.error as exc: raise ValueError(f"{raw_path}: invalid regex: {exc}")
                    if not matched: raise ValueError(f"{raw_path}: pattern did not match: {pattern}")
                elif kind=="capture_equal":
                    sources=item.get("sources")
                    if not isinstance(sources,list) or len(sources)<2: raise ValueError("capture_equal requires at least two sources")
                    values=[_capture(root,src) for src in sources]
                    if len(set(values))!=1: raise ValueError("captured values differ: "+", ".join(values))
                elif kind=="capture_in_integer_set":
                    needle=int(_capture(root,item.get("needle") or {}))
                    raw=_capture(root,item.get("haystack") or {})
                    values={int(v) for v in re.findall(r"\d+",raw)}
                    if needle not in values: raise ValueError(f"current version {needle} not accepted by {sorted(values)}")
            except Exception as exc:
                errors.append(eprefix+str(exc))
        missing=required-levels
        if missing: errors.append(prefix+f"missing required evidence levels: {sorted(missing)}")
    return errors

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description="Validate a source-owned UIGS invariant/evidence manifest")
    parser.add_argument("--root",default=".")
    parser.add_argument("--manifest",default=".uigs/invariants.json")
    args=parser.parse_args(argv)
    root=Path(args.root).resolve()
    manifest=(root/args.manifest).resolve() if not Path(args.manifest).is_absolute() else Path(args.manifest).resolve()
    errors=validate_manifest(root,manifest)
    if errors:
        print("UIGS invariant evidence validation failed:",file=sys.stderr)
        for err in errors: print(f"- {err}",file=sys.stderr)
        return 1
    data=json.loads(manifest.read_text(encoding="utf-8"))
    active=sum(1 for x in data["invariants"] if x.get("status")=="active")
    print(f"UIGS invariant evidence validation passed ({active} active invariants)")
    return 0

if __name__=="__main__": raise SystemExit(main())
