# Bug / MKV P0 finite Segment tail bypasses structural preflight

Status: **Submitted fix on PR, exact-head CI Pending** (not Accepted / not Canonical)
Date: 2026-10-15
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Product PR: [#142](https://github.com/11576865/MKV-Fast-Muxer/pull/142)
Exact submitted head: `85cc5c143e1e56ac77c7b848ba9ee02158199739`
Baseline main: `fefd97e0c1386d8b4f30328c167561f6690bf628`

## Observation (source-reviewed, not yet CI accepted)

`src/preservation-preflight.js::inspectMatroskaPreservation` previously found the **first** Matroska Segment and iterated from its data start to `segment.end`. When this finite Segment ended before `file.size`, the scanner did **not** inspect the following bytes or a second Segment. If the inspected first Segment contained none of the limited known risks, its return state could be `NO_KNOWN_HAZARD` even though the source had uninspected trailing data. This is a preflight coverage gap; no real output corruption caused by this specific input family has yet been demonstrated.

## Bounded repair / regression

PR #142 adds a fail-closed check `segment.end !== null && segment.end < file.size`: return `BLOCKED_UNKNOWN` via existing diagnostic path, explaining the uninspected tail. A new `tests/preservation-preflight.test.mjs` case synthesizes a valid first finite Segment followed by a second finite Segment with nested chapters; also checks arbitrary trailing bytes. Existing clean simple Matroska remains under previous tests.

This is a **source preflight** guard for old FFmpeg remux, not proof that all EBML layouts are recognized. Unknown-length Segment behavior remains unchanged, so the change is not a general multi-Segment parsing solution. It cannot be used to claim Issue #77's old ChapterUID/Tag data loss has been repaired.

## Reusable lesson / dedup

A bounded semantic validator must not classify a file as within examined scope merely because the **first recognized root** was safe. For a finite root, trailing bytes or additional roots must be explicitly inspected or treated as unknown before authorizing transformations.

Searched Foundry for `finite Segment`, `trailing Segment`, `extra Segment`, and `P0 preflight`. Related existing knowledge: `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md`, `inbox/bugs/2026-10-12-mkv-browser-remux-nested-chapter-and-target-tag-loss.md`. Neither already records the **finite-first-Segment tail omission**. This Bug is specific, not an attempted Canonical update.

## Acceptance to complete later

Require exact PR-head Node suite, build, full Chromium old-workflow regressions and confirmation that the new P0 test executes and passes. If CI is red, update this Bug with actual failure evidence; do not retroactively mark fixed merely because a PR was submitted.
