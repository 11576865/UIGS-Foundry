# Test: five-step Matroska preview — project authority prototype, honest runtime capability, portable recipe, product UI and real-browser exports

Date: 2026-10-13
Status: **PENDING exact-head full Chromium CI and named artifact**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/120
Baseline main: `383274ad586719b202d7412a8e812b8d9398781c`
Current head under review: `fd50fc09c50a816ffcbe97f826f210823639e409`

## Independent Test scope

Five vertical cuts after PR #119, explicitly **not** the complete product architecture nor stable release:

1. `ContainerProject v1`: domain may represent zero-video/attachment-only and track/chapter/tag object intents; project revisions, undo and explicit source relink; from a live `container-document-projection-v0` export a versioned JSON draft. Snapshot exports have no media bytes, File handles, directory permission or automatic execution authority. Not a second writable store integrated across the production editor.
2. `ContainerCapability v1`: separate planning validity, current FFmpeg video-rooted execution, narrow Void-based original-MKV attachment writer, attachment-only as experimental, general EBML preservation as unsupported and other-player playback as unverified. UI summary+details are projections, never replace existing executor-level preservation audit.
3. `BatchRecipe v1`: source-neutral policy-only JSON import/export, 32 KiB schema bound, no stale manual assignments or automatic mux; imported rules trigger a fresh current batch plan and cannot resurrect source/target directory grants.
4. Source composition and batch workbench support actual user actions plus accessible reason details and source-aware labels, viewport screenshots at 1440×900 and 1024×768.
5. Automated guards include immutable revisions, refusal of unknown/deceptive JSON, 20-episode **plan-only** fixture (not 20 real MKVs), actual Chromium import/export and rebind, as well as the entire preexisting P0/P2/P3/BatchRunner browser suite. Downloaded JSON and screenshots are requested as named CI evidence `five-step-container-recipe-workbench-evidence`.

## Dedup

- `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md`: original cross-capability migration proposal. This is a *specific implementation Test*, not a duplicate prescriptive Candidate.
- `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md`: already distinguishes domain plans from browser runtime limits. The implementation is narrower, empirical and does not change that Observation's normative status.
- `inbox/candidates/2026-10-03-batch-intent-vs-local-draft-ui-contract.md`: ASS Android batch scope controls; current specific MKV Recipe needs independent media/permission relinking.
- `inbox/tests/2026-10-13-mkv-dynamic-ass-four-pts-delivery-proof.md`: previous PR #119 output renderer proof, unrelated to portable project drafts or policy import.

## Known unimplemented exit gates

The project still lacks whole-product single-writable-authority, generic EBML-safe container writer, durable batch resume/relink, real 20-large-media performance acceptance, cross-device platform & user task efficiency measurements. No Canonical promotion and no claim full P0—P6 completion.

*This Test remains Pending until exact PR head green and actual named output artifact is inspected; merge and post-merge main CI are separate events.*
