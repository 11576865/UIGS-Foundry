#!/usr/bin/env python3
"""Adversarial, manually specified *bounded* precision check.

This checks known call relationships and known non-relationships. It does NOT
measure whole-repository recall or claim that Python AST proves runtime calls.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from code_atlas import index


FIXTURE = {
    "api.py": "def run():\n    return 1\n",
    "client.py": "from api import run as execute\ndef entry():\n    return execute()\n",
    "module_client.py": "import api as provider\ndef entry():\n    return provider.run()\n",
    "parameter_shadow.py": "from api import run\ndef entry(run):\n    return run()\n",
    "local_shadow.py": "from api import run\ndef entry():\n    run = lambda: 2\n    return run()\n",
    "module_shadow.py": "from api import run\nrun = lambda: 2\ndef entry():\n    return run()\n",
    "foreign_lookalike.py": "from foreign.api import run\ndef entry():\n    return run()\n",
    "foreign_import.py": "import foreign.api as provider\ndef entry():\n    return provider.run()\n",
    "nested.py": "from api import run\ndef outer():\n    def inner():\n        run()\n    return inner\n",
    "except_shadow.py": "from api import run\ndef entry():\n    try:\n        raise RuntimeError()\n    except Exception as run:\n        return run()\n",
    "inner_import.py": "from api import run\ndef entry():\n    from external import run\n    return run()\n",
    "pkg/__init__.py": "",
    "pkg/api.py": "def unique():\n    return 3\n",
    "correct_package.py": "from pkg.api import unique\ndef entry():\n    return unique()\n",
    "foreign_pkg.py": "from outside.api import unique\ndef entry():\n    return unique()\n",
}

# Each expected/forbidden pair was written without executing the indexer.
REQUIRED = [
    ("fn:client.py:entry", "fn:api.py:run"),
    ("fn:module_client.py:entry", "fn:api.py:run"),
    ("fn:correct_package.py:entry", "fn:pkg/api.py:unique"),
]
FORBIDDEN = [
    ("fn:parameter_shadow.py:entry", "fn:api.py:run"),
    ("fn:local_shadow.py:entry", "fn:api.py:run"),
    ("fn:module_shadow.py:entry", "fn:api.py:run"),
    ("fn:foreign_lookalike.py:entry", "fn:api.py:run"),
    ("fn:foreign_import.py:entry", "fn:api.py:run"),
    ("fn:nested.py:outer", "fn:api.py:run"),
    ("fn:except_shadow.py:entry", "fn:api.py:run"),
    ("fn:inner_import.py:entry", "fn:api.py:run"),
    ("fn:foreign_pkg.py:entry", "fn:pkg/api.py:unique"),
]

REAL_REQUIRED = [
    ("fn:tools/code_atlas.py:serve", "fn:tools/code_atlas.py:index"),
    ("fn:tools/generate_validation_missions.py:generate", "fn:tools/evaluate_epistemic_graph.py:evaluate"),
    ("fn:tools/test_epistemic_graph.py:test_same_lineage_counts_once", "fn:tools/evaluate_epistemic_graph.py:evaluate"),
]


def measure(root: Path) -> dict:
    with tempfile.TemporaryDirectory() as folder:
        tmp = Path(folder)
        for filename, source in FIXTURE.items():
            p = tmp / filename
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(source, encoding="utf-8")
        graph = index(tmp)
    calls = {(e["from"], e["to"]) for e in graph["edges"] if e["kind"] == "calls"}
    missing = [a for a in REQUIRED if a not in calls]
    wrong = [a for a in FORBIDDEN if a in calls]
    self_graph = index(root)
    real_calls = {(e["from"], e["to"]) for e in self_graph["edges"] if e["kind"] == "calls"}
    real_missing = []
    # Only compare the real-source anchors on a complete Foundry checkout.
    complete = (root / "tools" / "generate_validation_missions.py").is_file() and (root / "tools" / "test_epistemic_graph.py").is_file()
    if complete:
        real_missing = [a for a in REAL_REQUIRED if a not in real_calls]
    return {
        "schema_version": 1,
        "kind": "bounded_adversarial_reference_check",
        "interpretation": "Fixture pass rates are not general precision/recall and do not prove runtime behavior.",
        "fixture_required": len(REQUIRED), "fixture_required_found": len(REQUIRED)-len(missing),
        "fixture_forbidden": len(FORBIDDEN), "fixture_forbidden_avoided": len(FORBIDDEN)-len(wrong),
        "real_checkout_checked": complete, "real_required": len(REAL_REQUIRED) if complete else 0,
        "real_required_found": len(REAL_REQUIRED)-len(real_missing) if complete else 0,
        "missing_expected_edges": missing + real_missing,
        "incorrectly_asserted_edges": wrong,
        "pass": not missing and not wrong and not real_missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = measure(args.root)
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print(content, end="")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
