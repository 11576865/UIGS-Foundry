#!/usr/bin/env python3
from __future__ import annotations
import json, tempfile
from pathlib import Path
from validate_invariant_evidence import validate_manifest

def write(path: Path, text: str):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8")

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    write(root/"producer.js","export const TASK_VERSION = 3;")
    write(root/"bridge.ps1","taskSchemaVersion=3")
    write(root/"parser.ps1","version -notin @(1,2,3)")
    write(root/"smoke.yml","version=3;operation='copy'")
    manifest={
      "schema_version":1,
      "project":"fixture",
      "repository":"owner/repo",
      "invariants":[{
        "id":"MEDIA.TASK_SCHEMA.VERSION_ALIGNMENT",
        "title":"Task schema aligns",
        "status":"active",
        "criticality":"required",
        "claim":"Current producer version is advertised, accepted and exercised.",
        "boundaries":["producer","capability","parser","ci"],
        "required_levels":["source","test"],
        "evidence":[
          {"id":"versions-equal","level":"source","kind":"capture_equal","sources":[
            {"path":"producer.js","pattern":"TASK_VERSION\\s*=\\s*(\\d+)"},
            {"path":"bridge.ps1","pattern":"taskSchemaVersion=(\\d+)"}
          ]},
          {"id":"parser-accepts-current","level":"source","kind":"capture_in_integer_set",
           "needle":{"path":"producer.js","pattern":"TASK_VERSION\\s*=\\s*(\\d+)"},
           "haystack":{"path":"parser.ps1","pattern":"@\\(([^)]*)\\)"}},
          {"id":"current-version-smoke","level":"test","kind":"pattern","path":"smoke.yml","pattern":"version=3;operation='copy'"}
        ]
      }]
    }
    m=root/".uigs/invariants.json"; write(m,json.dumps(manifest))
    errors=validate_manifest(root,m)
    assert not errors, errors
    write(root/"parser.ps1","version -notin @(1,2)")
    errors=validate_manifest(root,m)
    assert any("current version 3 not accepted" in e for e in errors), errors
print("Invariant evidence validator tests passed")
