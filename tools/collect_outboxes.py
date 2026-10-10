#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, os, re, sys, tempfile, urllib.error, urllib.request
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
    """Write a complete JSON snapshot atomically, including Receipt files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

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

def check_receipt_storage(receipts: dict[str, Any], key: str, root: Path = ROOT) -> None:
    """Never treat a missing or unrelated Pending payload as successfully received."""
    entry = receipts["items"][key]
    if not isinstance(entry, dict):
        raise PacketError(f"invalid receipt entry: {key}")
    if entry.get("_dry_run_only"):
        # A simulated receipt exists only in this invocation's memory.
        return
    disposition = entry.get("disposition")
    if disposition == "duplicate":
        owner = str(entry.get("canonical_receipt", ""))
        if owner not in receipts["items"] or receipts["items"][owner].get("disposition") != "pending":
            raise PacketError(f"duplicate receipt has no pending owner: {key}")
        check_receipt_storage(receipts, owner, root)
        return
    if disposition != "pending":
        raise PacketError(f"unsupported receipt disposition: {key}: {disposition}")
    relative = entry.get("pending_path")
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise PacketError(f"invalid pending path in receipt: {key}")
    stored_path = root / relative
    if not stored_path.is_file():
        raise PacketError(f"receipt has no persisted Pending packet: {key}")
    persisted = load_json(stored_path)
    repository, packet_id = key.rsplit("#", 1)
    if not isinstance(persisted, dict) or persisted.get("source_repository") != repository or persisted.get("packet_id") != packet_id:
        raise PacketError(f"receipt/Pending identity mismatch: {key}")


def apply_packet(packet: dict[str, Any], expected_repository: str, origin_path: str,
                 receipts: dict[str, Any], root: Path = ROOT, dry_run: bool = False) -> tuple[str, str]:
    packet = validate_packet(packet, expected_repository)
    packet_id = packet["packet_id"]
    key = receipt_key(expected_repository, packet_id)
    if key in receipts["items"]:
        check_receipt_storage(receipts, key, root)
        return "already-received", key
    dedupe_key = str(packet["dedupe_key"])
    existing = dedupe_owner(receipts, dedupe_key)
    now = utc_now()
    if existing:
        check_receipt_storage(receipts, existing, root)
        receipts["items"][key] = {
            "repository": expected_repository, "packet_id": packet_id, "dedupe_key": dedupe_key,
            "origin_path": origin_path, "ingested_at": now, "disposition": "duplicate",
            "canonical_receipt": existing
        }
        if dry_run:
            receipts["items"][key]["_dry_run_only"] = True
        return "duplicate", key
    pending_path = root / "outbox" / "pending" / sanitize_component(expected_repository) / f"{packet_id}.json"
    if pending_path.exists():
        # Retry after crash between Pending publish and Receipt commit.
        if load_json(pending_path) != packet:
            raise PacketError(f"existing Pending packet differs from source: {pending_path}")
    elif not dry_run:
        write_json(pending_path, packet)
    receipts["items"][key] = {
        "repository": expected_repository, "packet_id": packet_id, "dedupe_key": dedupe_key,
        "origin_path": origin_path, "ingested_at": now, "disposition": "pending",
        "pending_path": pending_path.relative_to(root).as_posix()
    }
    if dry_run:
        receipts["items"][key]["_dry_run_only"] = True
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
    lines += [
        "",
        "Packets in outbox/pending are durable intake evidence, not Canonical knowledge.",
        "Triage/proposal/review state is stored separately, so this raw Pending count is not an unprocessed-backlog count.",
        "",
    ]
    path = root / "reports" / "outbox-status.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")

def collect(sources_path: Path, receipts_path: Path, dry_run: bool = False,
            root: Path = ROOT) -> tuple[int, list[str]]:
    sources_doc = load_json(sources_path)
    sources = sources_doc.get("sources", []) if isinstance(sources_doc, dict) else []
    receipts = load_receipts(receipts_path)
    token = os.environ.get("GITHUB_TOKEN", "").strip() or None
    changes = 0
    errors: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            errors.append("invalid source entry")
            continue
        repository = str(source.get("repository", "")).strip()
        branch = str(source.get("branch", "uigs-outbox")).strip()
        prefix = str(source.get("path_prefix", "packets/"))
        try:
            tree = fetch_source_tree(repository, branch, token)
        except Exception as exc:
            errors.append(f"{repository}: {type(exc).__name__}: {exc}")
            continue
        if tree is None:
            print(f"{repository}: no {branch} branch yet")
            continue
        for item in tree:
            path = str(item.get("path", ""))
            if item.get("type") != "blob" or not path.startswith(prefix) or not path.endswith(".json"):
                continue
            try:
                key = receipt_key(repository, Path(path).stem)
                if key in receipts["items"]:
                    check_receipt_storage(receipts, key, root)
                    continue
                packet = fetch_blob_json(repository, str(item["sha"]), token)
                disposition, _ = apply_packet(packet, repository, f"{branch}:{path}", receipts, root, dry_run)
                if disposition != "already-received":
                    changes += 1
                    print(f"{repository}: {path} -> {disposition}" + (" (dry-run)" if dry_run else ""))
            except Exception as exc:
                errors.append(f"{repository}: {path}: {type(exc).__name__}: {exc}")
    if changes and not dry_run:
        write_json(receipts_path, receipts)
        write_report(receipts, root)
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
