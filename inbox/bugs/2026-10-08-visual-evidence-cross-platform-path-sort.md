# Bug: Visual evidence index ordering differed between Windows and POSIX runners

Date: 2026-10-08
Status: Bug
Lifecycle: repair-evidenced
Scope: generated indexes / cross-platform determinism / GitHub Actions / pathlib

## Symptom

Validate Foundry runs #406 and #407 failed with:

`production visual evidence index is stale`

The stored index and manifest contents were otherwise semantically identical.

## Root cause

`tools/build_visual_evidence_index.py` iterated manifests with:

`sorted(MANIFESTS.glob("*.json"))`

Sorting `Path` objects is platform-sensitive because `WindowsPath` and `PosixPath` have different comparison semantics.

For the concrete pair:

- `VISUAL.PRODUCTION.ASS.FONTS_TOOL.FIXTURE_LANDSCAPE.json`
- `VISUAL.PRODUCTION.ASS.FONT_REQUIREMENTS_TOOL.FIXTURE_LANDSCAPE.json`

POSIX ordered `FONTS` before `FONT_REQUIREMENTS`, while Windows ordered `FONT_REQUIREMENTS` before `FONTS`.

A Windows production-capture workflow therefore wrote an index that Ubuntu validation deterministically rejected.

## Repair

The generator now sorts by the platform-neutral string key `p.as_posix()`.

A regression test compares `PureWindowsPath` and `PurePosixPath` ordering for the failing filename pair and requires identical output.

The visual-evidence index is regenerated using the fixed ordering.

## Reusable lesson

A deterministic generated artifact must not rely on native `Path` ordering when it can be produced and validated on different operating systems.

Normalize path representation before ordering, hashing, or canonical serialization.

## Evidence

- Validate Foundry #406: failure at production visual evidence index check.
- Validate Foundry #407: same deterministic failure.
- Static comparison confirmed manifest contents, inventory coverage, and all evidence rows were otherwise consistent.

This Bug entry is evidence, not a Canonical rule.
