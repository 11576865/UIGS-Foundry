# Candidate: Batch plans require explicit ambiguity and destination-identity gates

Status: **Candidate** (not Canonical)  
Date: 2026-10-09  
Domains: batch processing, filename heuristics, artifact identity, non-destructive output, asynchronous UI plans

## Observation / concrete source

Project: `11576865/MKV-Fast-Muxer`  
Baseline: `main@9eb28679fd1fe3d69a699eeb094b114e06b049d0`  
Implementation branch: `fix/batch-ambiguous-pairing-output-collisions`  
Implementation commits: `2a9545134d7ad5b941233e29e21eaaa569ccc808`, `9ef4fdda7b9ce926be97000ac2d0818119ac9bf9`

The baseline batch planner uses filename/stem and episode-token scores. With two videos sharing the top episode-token score, it selected the first video in enumeration order. That produces an apparently valid batch assignment despite absent evidence identifying which video owns the subtitle.

The planner also generates a destination filename from the input video basename. Distinct sources can share a destination filename (including case/Unicode compatibility variants); batch directory writes use that destination name. Without a separate output-name identity check, a task can overwrite another output at the same destination.

These are **code-path risks** found by source review, not a reported end-user data loss incident.

## Candidate rule

1. A heuristic match is not an identity proof. Collect all candidates sharing the best score; a tie remains ambiguous and must not silently resolve using file enumeration order.
2. Report ambiguous inputs and candidate names in the derived plan; do not start a side-effecting batch while unresolved.
3. Derive and compare **destination** identities independently of source identity; reject colliding output names before execution. Case/Unicode normalization is conservative preflight, not proof of file-system atomicity.
4. Batch command handlers must repeat plan-conflict checks at execution time, not only disable a UI button.
5. An asynchronously superseded plan must not be returned as though it were the latest approved plan.
6. Preserve clear distinctions between `unmatched`, `ambiguous`, `invalid`, and `executable`. An unrelated executable item must not mask global blocking conflicts.

## Evidence and verification status

Implementation changes:
- `src/batch.js`: collect tied candidates; compute output-name collisions.
- `src/main.js`: detailed preflight diagnostics; blocked Start; execution-time validation; stale-plan return disabled.
- Unit fixtures cover tied episodes, decisive full-name matches, mixed valid/ambiguous plans, and normalized output-name collisions.
- Browser E2E fixture checks disabled batch Start for ambiguity and readiness after correcting the subtitle name.

A source-derived V8 logic smoke for the exact branch version passed, and modified JavaScript files passed V8 parsing. **The repository's Node suite and Browser E2E/CI are still pending at intake time**; no production or device validation is asserted.

## Deduplication

Related prior evidence: `BUG.HSR.SAME_BASENAME_COLLISION` and `CLAIM.HSR.SAME_BASENAME_COLLISION` already establish that display basenames are not stable cross-directory identities and that ambiguous fallback should not guess. This candidate does **not** reassert that as a new general law. It adds concrete batch-plan tie semantics, a distinct destination-identity guard and the UI/execute-time enforcement boundary. Related orchestration: `inbox/candidates/2026-10-02-batch-execution-async-preflight-readiness-race.md`.

No Canonical promotion is requested from this single implementation.