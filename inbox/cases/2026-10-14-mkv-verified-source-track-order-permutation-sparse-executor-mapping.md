# Case: Portable source-track order is a complete permutation, not a scalar FFmpeg order assignment

Date: 2026-10-14  
Status: **Case / feature PR submitted, exact-head Node/build/Chromium Pending**  
Product: `11576865/MKV-Fast-Muxer`  
Implementation PR: [#132](https://github.com/11576865/MKV-Fast-Muxer/pull/132), head `b2a9e32faed85e1174f60aeea592d815d21bd301`, based on merged main `d1499ed3bb6eb59d05ded614587b3e0df3f0cdf0`.

## Why this is separate from prior Cases

The earlier `inbox/cases/2026-10-14-mkv-source-order-domain-advanced-flags-portability-boundary.md` established that *live* source-track up/down editing had one domain owner, but detached project ordering was intentionally not recoverable. The attachment recovery Case `inbox/cases/2026-10-14-mkv-verified-source-attachment-intent-atomic-cross-object-replay.md` established portable SHA/old-state checking for source attachment field edits. Neither demonstrated that a reorder operation could be portably restored without corrupting stream positions.

A Matroska `ffprobe` scan might report audio stream indices 1 and 6 while the detached `ContainerProject` serializes contiguous flattened presentation slots 1 and 2. Treating detached `reorder=2` as a writer-native numeric stream order is incorrect. A valid reorder is a bijection of one exact scanned kind's slot set.

## Concrete feature experiment

PR #132 changes actual export to reconstruct original source audio/subtitle order from ffprobe source stream indices, map that original order to the current same-kind project positions and emit scan-to-current `reorder` intents for all displaced objects. Like track/attachment edits, those are **derived effective deltas**, not signatures or proof of historical author actions.

Verified replay requires the existing strict JSON and chain audit, full source SHA-256 matching, same source/document/stream identities, inspected scan, old-slot three-way preview, explicit user confirmation, and selective editor mode. A whole audio or subtitle kind must contain every originally scanned, **included** track with distinct live numeric FFmpeg order values and exact stream references. The proposed target slots must form precisely the same set, with no duplicates/cross-kind/missing members. Excluded peers and partially recoverable groups are blocked (and UI discloses this), not silently reinterpreted.

The prepared plan converts a verified project-order permutation into a permutation of the **existing sparse FFmpeg numeric order set**. The order is composed into the same atomic track+source-attachment edit transaction as title/language/advanced flags and attachment name/MIME/inclusion. Final apply checks all targets again; the guarded inverse refuses stale stream, field or order and only then rolls back everything. Import alone never mutates the editor or source file and does not start a mux. Domain/order success does **not** imply general Matroska writer/AttachmentUID/Tag/Chapter preservation (#77).

## Evidence and current trust status

- An isolated execution of real source-project, JSON parser/intent-audit, conflict preview and replay functions passed a two-source-audio sparse-order swap mixed with one track title and one attachment rename. It restored original numeric order after inverse, and an externally changed attachment rejected the entire source transaction.
- Node regressions submitted for sparse audio indices **1 and 6** with independent attachment index **4**, typed reordered project deltas, exact slot preservation, mixed atomic commit/undo, illegal duplicate/cross-kind slot targets, excluded peer, wrong source stream reference and executor order drift.
- Existing Chromium source inspector scenario now asserts real complete reorder intents; a new real Chromium scenario exports/reimports the source, verifies SHA, explicitly restores and undoes the order, then muxes a real MKV and checks **delivered order** with independent native `ffprobe`, checking source bytes unchanged.
- Changed JavaScript syntax checks passed. **Exact-head Node/Vite/real Chromium PR CI is Pending**; no integrated green, device acceptance or lossless arbitrary EBML claim.

## Deduplication and reuse hypothesis

This is a narrower transferable **Case**, not a new Canonical rule. It extends the above live-order and attachment-recovery records without duplicating them. A source-neutral object model and a writer's numeric positions have different identity semantics; only a proven complete permutation permits their safe translation. Further confirmation requires full exact-head tests and other independent products before promotion.
