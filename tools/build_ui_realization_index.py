#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "domains" / "interface-grammar" / "registry" / "patterns"
MANIFESTS = ROOT / "domains" / "interface-grammar" / "realizations" / "manifests"
INDEX = ROOT / "domains" / "interface-grammar" / "realizations" / "index.json"
COVERAGE = ROOT / "domains" / "interface-grammar" / "realizations" / "coverage.json"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def build(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    pattern_dir = root / "domains" / "interface-grammar" / "registry" / "patterns"
    manifest_dir = root / "domains" / "interface-grammar" / "realizations" / "manifests"
    pattern_ids = sorted(load(path)["id"] for path in pattern_dir.glob("*.json"))
    manifests: list[dict[str, Any]] = []
    by_pattern: dict[str, list[dict[str, Any]]] = defaultdict(list)
    platform_links: Counter[str] = Counter()
    project_links: Counter[str] = Counter()

    for path in sorted(manifest_dir.glob("*.json")):
        data = load(path)
        row = {
            "id": data["id"],
            "implementation_kind": data["implementation_kind"],
            "verification_status": data["verification_status"],
            "platform": data["platform"],
            "project": data["project"],
            "repository": data["repository"],
            "revision": data["revision"],
            "patterns": data["patterns"],
            "source_files": data["source_files"],
            "validation_files": data.get("validation_files", []),
            "implementation_effects": data.get("implementation_effects", []),
            "limitations": data.get("limitations", []),
            "path": path.relative_to(root).as_posix(),
        }
        manifests.append(row)
        for link in data["patterns"]:
            pid = str(link["id"])
            by_pattern[pid].append({
                "realization_id": data["id"],
                "platform": data["platform"],
                "project": data["project"],
                "repository": data["repository"],
                "revision": data["revision"],
                "role": link["role"],
                "verification_status": data["verification_status"],
                "path": row["path"],
            })
            platform_links[data["platform"]] += 1
            project_links[data["project"]] += 1

    index = {
        "version": 1,
        "realization_count": len(manifests),
        "realizations": manifests,
        "by_pattern": {pid: by_pattern.get(pid, []) for pid in pattern_ids},
    }
    covered = [pid for pid in pattern_ids if by_pattern.get(pid)]
    coverage = {
        "version": 1,
        "total_patterns": len(pattern_ids),
        "with_production_implementation": len(covered),
        "missing_production_implementation": [pid for pid in pattern_ids if pid not in covered],
        "realization_records": len(manifests),
        "platform_pattern_links": dict(sorted(platform_links.items())),
        "project_pattern_links": dict(sorted(project_links.items())),
    }
    return index, coverage

def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    index, coverage = build()
    if args.check:
        current_index = load(INDEX) if INDEX.is_file() else None
        current_coverage = load(COVERAGE) if COVERAGE.is_file() else None
        if current_index != index or current_coverage != coverage:
            print("UI realization index is stale")
            return 1
        print(f"UI realization index current: {index['realization_count']} records")
        return 0
    write(INDEX, index)
    write(COVERAGE, coverage)
    print(
        "UI realization index built: "
        f"{index['realization_count']} records; "
        f"pattern coverage={coverage['with_production_implementation']}/{coverage['total_patterns']}"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
