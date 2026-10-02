#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, os, re, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = ROOT / "outbox" / "sources.json"
DEFAULT_RECEIPTS = ROOT / "outbox" / "receipts.json"
PACKET_ID_RE = re.compile(r"^[A-Za-z0-9._-]{3,180}$")
ALLOWED_RECORD_TYPES = {"observation","candidate","bug","case","test","lesson","ci_failure"}

class PacketError(ValueError):
    pass

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def sanitize_component(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9._-]+", "__", value.strip())
    return result.strip("._-") or "unknown"

def receipt_key(repository: str, packet_id: str) -> str:
    return f"{repository}#{packet_id}"

def validate_packet(packet: Any, expected_repository: str | None = None) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise PacketError("packet is not a JSON object")
    required = ("packet_version","packet_id","status","record_type","title","summary","source_repository","source_event","created_at","dedupe_key")
    missing = [key for key in required if key not in packet]
    if missing:
        raise PacketError("missing required fields: " + ", ".join(missing))
    if packet.get("packet_version") != 1:
        raise PacketError("unsupported packet_version")
    packet_id = str(packet.get("packet_id", ""))
    if not PACKET_ID_RE.fullmatch(packet_id):
        raise PacketError(f"invalid packet_id: {packet_id!r}")
    if packet.get("status") != "pending":
        raise PacketError("source packet status must be pending")
    if packet.get("record_type") not in ALLOWED_RECORD_TYPES:
        raise PacketError(f"unsupported record_type: {packet.get('record_type')!r}")
    repository = str(packet.get("source_repository", ""))
    if "/" not in repository:
        raise PacketError("source_repository must be owner/repo")
    if expected_repository and repository != expected_repository:
        raise PacketError(f"source_repository mismatch: packet={repository!r}, source={expected_repository!r}")
    if not str(packet.get("title", "")).strip() or not str(packet.get("summary", "")).strip():
        raise PacketError("title/summary must be non-empty")
    if not str(packet.get("dedupe_key", "")).strip():
        raise PacketError("dedupe_key is empty")
    return packet

def load_receipts(path: Path = DEFAULT_RECEIPTS) -> dict[str, Any]:
    if not path.is_file():
        return {"version":1,"items":{}}
    value = load_json(path)
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("items"), dict):
        raise PacketError(f"invalid receipts file: {path}")
    return value

def dedupe_owner(receipts: dict[str, Any], dedupe_key: str) -> str | None:
    for key, item in receipts["items"].items():
        if isinstance(item, dict) and item.get("dedupe_key") == dedupe_key and item.get("disposition") == "pending":
            return key
    return None

def apply_packet(packet: dict[str, Any], expected_repository: str, origin_path: str, receipts: dict[str, Any], root: Path = ROOT) -> tuple[str,str]:
    packet = validate_packet(packet, expected_repository)
    packet_id = packet["packet_id"]
    key = receipt_key(expected_repository, packet_id)
    if key in receipts["items"]:
        return "already-received", key
    dedupe_key = str(packet["dedupe_key"])
    existing = dedupe_owner(receipts, dedupe_key)
    now = utc_now()
    if existing:
        receipts["items"][key] = {
            "repository":expected_repository,"packet_id":packet_id,"dedupe_key":dedupe_key,
            "origin_path":origin_path,"ingested_at":now,"disposition":"duplicate",
            "canonical_receipt":existing
        }
        return "duplicate", key
    pending_path = root / "outbox" / "pending" / sanitize_component(expected_repository) / f"{packet_id}.json"
    write_json(pending_path, packet)
    receipts["items"][key] = {
        "repository":expected_repository,"packet_id":packet_id,"dedupe_key":dedupe_key,
        "origin_path":origin_path,"ingested_at":now,"disposition":"pending",
        "pending_path":pending_path.relative_to(root).as_posix()
    }
    return "pending", key

def api_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept":"application/vnd.github+json",
        "User-Agent":"UIGS-Foundry-Outbox-Collector/1",
        "X-GitHub-Api-Version":"2022-11-28"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def fetch_source_tree(repository: str, branch: str, token: str | None) -> list[dict[str,Any]] | None:
    try:
        branch_payload = api_json(f"https://api.github.com/repos/{repository}/branches/{branch}", token)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    tree_sha = branch_payload["commit"]["commit"]["tree"]["sha"]
    tree_payload = api_json(f"https://api.github.com/repos/{repository}/git/trees/{tree_sha}?recursive=1", token)
    if tree_payload.get("truncated"):
        raise RuntimeError(f"{repository}: outbox tree is truncated")
    return list(tree_payload.get("tree", []))

def fetch_blob_json(repository: str, sha: str, token: str | None) -> Any:
    payload = api_json(f"https://api.github.com/repos/{repository}/git/blobs/{sha}", token)
    if payload.get("encoding") != "base64":
        raise RuntimeError(f"{repository}: unsupported blob encoding")
    return json.loads(base64.b64decode(payload.get("content", "")).decode("utf-8"))

def write_report(receipts: dict[str,Any], root: Path = ROOT) -> None:
    items = list(receipts["items"].values())
    pending = [x for x in items if isinstance(x,dict) and x.get("disposition") == "pending"]
    duplicates = [x for x in items if isinstance(x,dict) and x.get("disposition") == "duplicate"]
    by_repo: dict[str,int] = {}
    for item in pending:
        repo = str(item.get("repository","unknown"))
        by_repo[repo] = by_repo.get(repo,0) + 1
    lines = [
        "# UIGS Durable Outbox Status","",f"Updated: {utc_now()}",
        f"Pending packets: {len(pending)}",f"Duplicate receipts: {len(duplicates)}","",
        "## Pending by source repository"
    ]
    lines.extend([f"- {repo}: {count}" for repo,count in sorted(by_repo.items())] or ["- none"])
    lines += ["","Packets in outbox/pending are durable intake evidence, not Canonical knowledge.",""]
    path = root / "reports" / "outbox-status.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")

def collect(sources_path: Path, receipts_path: Path, dry_run: bool = False) -> tuple[int,list[str]]:
    sources_doc = load_json(sources_path)
    sources = sources_doc.get("sources", []) if isinstance(sources_doc,dict) else []
    receipts = load_receipts(receipts_path)
    token = os.environ.get("GITHUB_TOKEN","").strip() or None
    changes = 0
    errors: list[str] = []
    for source in sources:
        if not isinstance(source,dict):
            errors.append("invalid source entry")
            continue
        repository = str(source.get("repository","")).strip()
        branch = str(source.get("branch","uigs-outbox")).strip()
        prefix = str(source.get("path_prefix","packets/"))
        try:
            tree = fetch_source_tree(repository, branch, token)
            if tree is None:
                print(f"{repository}: no {branch} branch yet")
                continue
            for item in tree:
                path = str(item.get("path",""))
                if item.get("type") != "blob" or not path.startswith(prefix) or not path.endswith(".json"):
                    continue
                key = receipt_key(repository, Path(path).stem)
                if key in receipts["items"]:
                    continue
                packet = fetch_blob_json(repository, str(item["sha"]), token)
                disposition, _ = apply_packet(packet, repository, f"{branch}:{path}", receipts, ROOT)
                if disposition != "already-received":
                    changes += 1
                    print(f"{repository}: {path} -> {disposition}")
        except Exception as exc:
            errors.append(f"{repository}: {type(exc).__name__}: {exc}")
    if changes and not dry_run:
        write_json(receipts_path, receipts)
        write_report(receipts, ROOT)
    return changes, errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--receipts", type=Path, default=DEFAULT_RECEIPTS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changes, errors = collect(args.sources, args.receipts, args.dry_run)
    print(f"outbox collector: changes={changes}, errors={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 2 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
