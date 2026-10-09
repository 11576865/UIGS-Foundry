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

## Follow-up: pre-existing destination protection and artifact retention (same Candidate)

Date: 2026-10-09  
Project branch: `11576865/MKV-Fast-Muxer:fix/batch-ambiguous-pairing-output-collisions`

Further source review identified a distinct destination-side hazard: the existing browser File System Access write routine used `getFileHandle(filename, {create:true})` followed by `createWritable()`, without checking whether a previous output file or matching report was already in the selected directory. The earlier batch-internal collision guard did not protect **pre-existing** user artifacts.

Correction on the same feature branch:
- `src/batch-output.js` provides directory-content preflight for the planned MKV + JSON report names, including Unicode NFKC / casefold equivalence, read/permission error fail-closed behavior, and repeat checks just before writing.
- `src/main.js` blocks execution for pre-existing output or unknown directory state, revalidates at the click boundary, and retains download links if optional directory persistence fails after successful mux.
- Added isolated directory-handle regression fixtures for existing files, case/Unicode collisions, unreadable directories, directory-vs-file conflicts and failed writable abort.
- Browser E2E scenarios cover pre-existing reports preventing Start, and completed mux results remaining downloadable after simulated directory write failure.
- Source-derived V8 execution of **7 directory-helper regression fixtures passed**. Six touched JS files passed V8 parsing. Node and real browser test execution remain **Pending CI**.

Important limit: browser File System Access offers no atomic cross-process `create-if-absent` reservation. A competing writer could create the same filename after the final check. Therefore the improvement is a **conservative best-effort guard**, not a proof of atomic no-clobber publication. Tests on mock DirectoryHandle are not evidence for every filesystem/OEM behavior.

Deduplication: this continues the destination-identity scope in the existing Candidate and does not create a second general record. It also aligns with the previously recorded principle of separating completed artifact identity from current configuration or downstream save state. The Candidate remains non-Canonical.

## PR #64 review-derived hardening: stale assertion and aborted destination entry

Date: 2026-10-09  
Review evidence: [MKV-Fast-Muxer PR #64](https://github.com/11576865/MKV-Fast-Muxer/pull/64), Codex P1 and P2 findings, head `d7ab8e4f272f446712c3cbb80467acbcbb1ac70e`.

After opening the PR, GitHub Actions exposed a single deterministic `npm test` failure: `tests/features-1.2.test.mjs` asserted the removed helper name `writeBlobToBatchDirectory`. The automated review independently identified the stale source-shape assertion. On the reviewed head, the two independent CI pipelines each recorded 146/147 passing unit tests, with later build / browser tests skipped; this was **not** an engine failure. The replacement checks assert the current safe-writer API, and the subsequent Pages workflow for the correction head completed successfully. Full Browser E2E remains pending at this intake point.

The P2 review highlighted that aborting a File System Access `FileSystemWritableFileStream` does not necessarily remove the new destination directory entry previously created by `getFileHandle(name,{create:true})`. A leftover empty file is subsequently caught by the no-overwrite preflight and prevents retry.

Correction: on a failed write, abort the writer, then **conditionally** remove a created empty destination only when `removeEntry` exists, `createdHandle.isSameEntry(currentHandle)` confirms file identity, and `currentHandle.getFile().size === 0`. Never delete a nonempty entry or mismatched identity; when safe cleanup cannot be shown, surface an explicit manual-inspection warning. These guards reduce accidental cleanup of unrelated artifacts but cannot eliminate a concurrent filesystem time-of-check-to-time-of-use race. Tests cover successful cleanup, writable creation failure, changed identity, nonempty entry, and unavailable remove capability; eleven source-derived executable helper regressions passed.

Reusable Candidate-level observations (not promoted):
1. When a side-effecting API **creates a filesystem entry before committing contents**, rolling back the writable stream may not roll back the namespace entry; distinguish content rollback from destination-entry rollback.
2. Cleanup after failure must be narrower than normal write authorization. A conservative identity-and-emptiness guard is preferable to deleting based solely on a filename.
3. Source-shape / legacy helper-name feature assertions are implementation-coupled: API refactors require synchronized test updates. A CI regression caused by an obsolete test must not be described as a functional mux failure.

Deduplication: keep these as added evidence on the same destination-identity Candidate, since the P2 retry trap is part of its output-safety boundary. No Canonical edits.
