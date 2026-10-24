# Bug — ASS safe save can falsely clear newer edits after an older snapshot was written

Date: 2026-10-24
Lifecycle: **source-confirmed logic risk; repair committed; external validation pending**
Source: [ASS-Workbench-Android / PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149)
Severity: **Editor data-integrity / false saved status / recovery loss**

## Exact source issue

Before the repair, `EditorViewModel.saveTo(uri)` captured `snapshot = _state.value` and passed `snapshot.document` to production `SafeSubtitleSave.write`. That save code stages bytes, writes to the document provider, and independently reads them back. However, its successful callback then called `clearPendingRecovery()` and unconditionally published `dirty = false`, regardless of whether the editor's current `workspaceSessionId`, `documentRevision`, `document`, or text encoding still matched the saved snapshot.

If another edit occurred while the provider was performing write/read-back, the on-disk **older** snapshot could be perfectly verified while the **newer** editor state was incorrectly marked saved and its pending recovery record discarded. A workspace switch during save could additionally cause an old operation to overwrite the new project's destination/status. These are source-grounded race risks; no user-file loss is claimed.

## Product and test repair

- [f914c466](https://github.com/11576865/ASS-Workbench-Android/commit/f914c466c86381a95d2d2332a2cd839afa11b975): success callback now checks session, document revision, document contents, and encoding. A same-session stale result retains `dirty = true`, reports the saved file is an earlier version, and does not clear pending recovery. A newer workspace is left unchanged. A narrowly possible edit between the initial recovery clear and final state publication triggers re-journaling.
- [364b63c3](https://github.com/11576865/ASS-Workbench-Android/commit/364b63c346e2edb19b8a04d240c21e342fc8d6ba): debug-only `SafeSaveTestProvider` exposes a one-shot callback just before the second input open, after the initial target read and output write.
- [d3eaf141](https://github.com/11576865/ASS-Workbench-Android/commit/d3eaf1416dc09f06a0a0dd2754bfa02fd31c39dc): Android test simulates a newer document edit during save read-back; asserts saved bytes contain only the captured old revision, editor retains newer text, stays dirty and explicitly reports unsaved changes.
- [a66c8bcf](https://github.com/11576865/ASS-Workbench-Android/commit/a66c8bcf4e699c02259e847ade5d18f68a756193): parallel regression for switching to an entirely new project during save; assert old save cannot replace new project destination or state. Existing verified-save and rollback tests are retained.

## Evidence and next gate

The *preceding* exact-head `23ab5a1d` source/JVM CI [40081217144](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40081217144) succeeded. Emulator [40081217091](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40081217091) executed 188 tests / 4 failures / 0 errors / 0 skipped, with both strict tablet screenshot jobs successful. Its failures were unrelated rotation Event navigation, SPATIAL resident pin, BATCH IME root focus and Transform field lifecycle; this **does not validate** the subsequent stale-save repair.

New exact-head Gradle, device regression and real files are **Pending External Validation**. A pass would establish the two deterministic provider interleavings, not universal concurrency safety for every ContentProvider.

## UIGS intake and dedup

Queried Foundry for `SafeSubtitleSave`, stale save success, dirty flag, concurrent save, revision recovery and output race. This is distinct from the existing ASS Text/opaque-column trim Bug and HSR's MKV stale-subtitle writer Bug. The reusable *principle* already appears in experimental pattern `REL.GENERATION_SAFE_ASYNC_PUBLICATION`; this source-specific failure is recorded as a Bug, not a duplicate universal Candidate, and **no Canonical promotion** is made.
