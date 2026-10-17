# Owner Atlas: real-repository integration pilot (review-only)

**Status:** local integration proposal. This directory is not installed in UIGS-Foundry or HSR until separately approved. Neither code quotes nor CI success constitute semantic correctness or product acceptance.

## Why

The previous standalone HTML v0.9 could export unapproved AI claims but had no durable integration layout or repeatable real-repository replay. This kit carries the reviewed v0.8/v0.9 Python engines into a repository-ready structure, pins one historical HSR comparison, adds a manual CI template and replays source validation to an exportable ledger.

## Contents

- `tools/owner_atlas/intake_git_v08.py`: local Git diff -> source-anchored candidate impact queue.
- `tools/owner_atlas/reconcile_semantics_v09.py`: fixed Git-blob quote check -> unapproved semantic claim receipt.
- `tools/owner_atlas/export_semantic_ledger_v09.py`: content-addressed bundle export with tamper/authority checks.
- `tools/owner_atlas/pilot_cli.py`: a single read-only historical HSR replay entrypoint.
- `fixtures/hsr-pr194/`: minimized source-reviewed comparison `01ad440... -> dea541...` (one internal ASS preflight candidate; not complete HSR model).
- `.github/workflows/owner-atlas-replay.yml`: **optional workflow template**, manual dispatch only, GitHub read-only, no model API, no writes, no merges, 14-day unsigned artifact.

## Run after an authorized installation

```bash
python -m unittest discover -s tools/owner_atlas -p 'test_*.py' -q
python tools/owner_atlas/pilot_cli.py \
  --repo-root /full/local/HSR-Voice-Archive-Builder \
  --fixture fixtures/hsr-pr194 \
  --out /tmp/owner-atlas-pr194
```

**Prerequisite:** full HSR Git history containing both commit SHAs. `pilot_cli.py` does not clone repositories or make network calls itself. If the Git objects are unavailable, the check fails closed. `handoff.json` is **unsigned** and cannot authorize changes. The embedded candidate states a source-observed *hypothesis* about internal ASS behavior only; product runtime and acceptance are **not tested** here.

## Roles and authority

HSR is authoritative for shipped behavior; Foundry is the control/knowledge plane. A Candidate ledger cannot upgrade repository documentation to owner-approved theory. Any new AI must independently recheck Git object identity. Product changes, Foundry branch/PR, CI workflow installation or promotion require explicit owner authorization. Conflicting semantic candidates coexist; neither silently replaces As-Is.

## Known limitations and next proof

- The currently available container cannot resolve `github.com` for Git clone, so exact historical Git object replay is **Pending external authorized runner**. Old/new source quotes and their line numbers were independently inspected via connected GitHub read actions.
- No dynamic behavior tracer, AST semantic inference, model invocation, runtime audio/visual tests or device inspection runs in this kit.
- The pilot fixture addresses one HSR PR194 behavior, not all product entrypoints or all theoretical goals.
- Integration should occur in a separately authorized review branch, never directly on main, and no workflow should auto-promote Candidate or Canonical.
