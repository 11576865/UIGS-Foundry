#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, urllib.parse, urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "domains" / "interface-grammar" / "realizations" / "manifests"
REPORT_JSON = ROOT / "reports" / "generated" / "ui-realization-state.json"
REPORT_MD = ROOT / "reports" / "generated" / "ui-realization-state.md"
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def api(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "UIGS-Realization-Verifier/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

def verify_one(data: dict[str, Any], online: bool) -> dict[str, Any]:
    repo = str(data["repository"])
    revision = str(data["revision"])
    branch = str(data.get("default_branch", "main"))
    result: dict[str, Any] = {
        "id": data["id"],
        "project": data["project"],
        "platform": data["platform"],
        "repository": repo,
        "revision": revision,
        "source_files": [],
        "validation_files": [],
        "source_verified": True,
        "current_head": None,
        "head_matches_revision": None,
    }
    if online:
        branch_doc = api(
            "https://api.github.com/repos/"
            + repo
            + "/branches/"
            + urllib.parse.quote(branch, safe="")
        )
        head = str(branch_doc["commit"]["sha"])
        result["current_head"] = head
        result["head_matches_revision"] = head == revision

    for section in ("source_files", "validation_files"):
        for item in data.get(section, []):
            row = {
                "path": item["path"],
                "expected_blob_sha": item["blob_sha"],
                "verified": None,
            }
            if online:
                quoted_path = urllib.parse.quote(str(item["path"]), safe="/")
                quoted_ref = urllib.parse.quote(revision, safe="")
                doc = api(
                    "https://api.github.com/repos/"
                    + repo
                    + "/contents/"
                    + quoted_path
                    + "?ref="
                    + quoted_ref
                )
                row["actual_blob_sha"] = str(doc.get("sha", ""))
                row["verified"] = row["actual_blob_sha"] == item["blob_sha"]
                if not row["verified"]:
                    result["source_verified"] = False
            result[section].append(row)
    return result

def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# UI Production Realization State",
        "",
        "| Realization | Platform | Revision vs current HEAD | Source blobs |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        if row["head_matches_revision"] is None:
            current = "offline"
        else:
            current = "HEAD" if row["head_matches_revision"] else "older revision"
        blobs = "verified" if row["source_verified"] else "MISMATCH"
        lines.append(
            f"| {row['id']} | {row['platform']} | {current} | {blobs} |"
        )
    lines.extend([
        "",
        "## Evidence boundary",
        "",
        "- source_verified means declared source/test paths resolve at the immutable revision with the declared Git blob identities.",
        "- HEAD means that immutable revision currently equals the source repository default-branch HEAD.",
        "- An older revision remains historical production evidence, but it is not silently described as the current implementation.",
        "- Source verification is not production visual evidence; screenshots and recordings remain a separate Showcase evidence class.",
        "",
    ])
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(MANIFESTS.glob("*.json")):
        data = load(path)
        try:
            row = verify_one(data, not args.offline)
        except Exception as exc:
            errors.append(f"{data.get('id', path.name)}: {type(exc).__name__}: {exc}")
            continue
        rows.append(row)
        if not args.offline and not row["source_verified"]:
            errors.append(f"{row['id']}: source blob mismatch")
    if args.write_report:
        REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        REPORT_JSON.write_text(
            json.dumps({"schema_version": 1, "realizations": rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        REPORT_MD.write_text(render_markdown(rows), encoding="utf-8")
    for row in rows:
        print(
            f"{row['id']}: blobs={'ok' if row['source_verified'] else 'BAD'}; "
            f"head={row['head_matches_revision']}"
        )
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
