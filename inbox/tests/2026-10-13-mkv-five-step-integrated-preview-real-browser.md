# Test: five-step Matroska preview — project authority prototype, honest runtime capability, portable recipe, product UI and real-browser exports

Date: 2026-10-13
Status: **PASS — PR #120 head and independently re-tested main, named browser JSON/PNG artifacts verified**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/120
Baseline main: `383274ad586719b202d7412a8e812b8d9398781c`
Accepted PR head: `ae7d297f1e4c35b9814756dc46be3afe76452f60`

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

## Verified result and scope correction

- Actual accepted PR head `ae7d297f1e4c35b9814756dc46be3afe76452f60`: [Node/build run 38413814638](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38413814638) **PASS 445/445** and production build; [complete Chromium run 38413814542](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38413814542) **PASS** with P0/P1 refusal and P3 dynamic test still enforced.
- Downloaded and independently inspected named artifact `five-step-container-recipe-workbench-evidence` **ID 11822619407**: 5 files (portable batch recipe, exported versioned project, 1440, 1024, 390 viewport PNGs).
- Recipe policy `preserveAttachments=false`, `subsetEnabled=true`, `subsetScope=group`; source relink required, no destination access, no completed artifacts. Project snapshot source `base.mp4` was **a header-only, pre-scan placeholder** `kind=other`; this is a *draft* and not a verified typed video track tree or eligible writer. No universal source-relink or import yet.
- Initial browser red runs exposed an actual UI accessibility defect: the project-export button was inserted in the mobile-only `.composition-actions` region and could not be clicked on desktop. Native instrumentation saw zero click/pointer events. Fix moved the export button to the visible composition header. Final real source-unified intake, downloadable JSON and three viewport images passed.
- Squash merge PR #120 to `main@31af804e5f60ec0da0f8dccf70e11e2551b7e591`. Independently verified post-merge [main build+Pages 38414919425](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38414919425) PASS and [main full Chromium E2E 38414919676](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38414919676) PASS.
- No Canonical promotion; still only the bounded five-step incremental prototype described above, not P0–P6 final stable release.
