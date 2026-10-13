# Observation: HSR subtitle-request closure differs from branch implementation and delivered main

Status: Observation / requirement-to-delivery audit, not Canonical
Date: 2026-10-13
Domains: UI, subtitle effects, media preview, engineering process, stacked PR integration
Source: `11576865/HSR-Voice-Archive-Builder`

## User-stated task boundary (current conversation)

The user describes three desired changes: remove the duplicated subtitle layout boundary, split out a subtitle effects workbench, and add video preview for judging animated effects. This is a current user report, not a reconstructed verbatim earlier specification; do not infer that no other directions were authorized in unseen conversations.

## Repository observations

1. PR #132 was merged directly to main at `88cbadd80229720c88f85903fa3924e6a4fac2a3`. Its work is a much wider subtitle studio: cue editing, non-destructive display timing, interactive event timeline, WAV audition/waveform, export evidence, concurrency protection and Chromium/libass tests.
2. PR #133 was merged into feature branch `feat/subtitle-style-workbench-evidence-v15`, not main. PR #134 was merged into feature branch `feat/hsr-archive-audit-karaoke-v1`, not main. GitHub reports all three as `merged=true`, but that metadata alone does not prove #133/#134 content is in main.
3. At inspected main HEAD `88cbadd80229720c88f85903fa3924e6a4fac2a3`, `docs/subtitle-layout-safety-ratio.md` is absent. It exists at #134's feature head. `compare_commits(main, #134 feature head)` reports `status=diverged`, `ahead_by=180`, `behind_by=3`; therefore the #134 implementation has not been integrated as current-main authority.
4. PR #134 narrows “duplicated boundaries” to one layout `SafeArea`, suppressed diagnostic boxes, and zero additional ASS Style margins for explicitly positioned bilingual text. This still retains the safe area and central gap; it is not a wholesale abolition of all geometry constraints.
5. Current-main UI inventory exposes `HSR.WORKSPACE.LAYOUT` and inspector sections rather than a separate subtitle-effects workbench. The current v15 workbench document expressly characterizes itself as one editing surface, not a separate tab/product.
6. Current-main preview consists of browser geometry and on-demand FFmpeg/libass rendered still frames. PR #132's scope explicitly excludes render-backed video playback. #134's timestamp and sampled-interval rendered-ink checks explicitly do not constitute continuous video playback.

## Requirement-to-acceptance gap

The reusable issue is not that these additional features are intrinsically wrong. It is that capability completion must be checked against the user's original *interaction-level request*, the actual current-main code and the requested runtime/media evidence, not against number of commits, green CI, merged labels or visually adjacent substitutes.

A single FFmpeg/libass PNG is renderer evidence, not video playback. Effects controls inside a style Inspector are not automatically an independent effects workbench. Removing redundant ASS margins while preserving one layout SafeArea is a narrower interpretation of “remove duplicate boundary” and needs acceptance against the user's intended meaning.

## Actionable follow-up (not performed by this observation)

- Make a three-row acceptance ledger with explicit semantics and user approval.
- Inspect branch ancestry and integrate only the wanted verified delta onto current main; do not force-reset a divergent branch.
- For video: require actual user-supplied moving media, playback/scrub with audio-time identity, ASS composited at the selected instant, and field verification; do not substitute browser bounding boxes or synthetic black-frame renders.
- Do not promote this single case into Canonical.

## Deduplication

Extends rather than replaces existing Foundry knowledge:
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md`
- `inbox/observations/2026-10-04-collapse-stacked-pr-chain-by-retargeting-top.md`
- `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`

Specific new observation: this HSR three-requirement audit reveals both mainline ancestry and semantic substitution (still-frame evidence versus requested moving video, inspector section versus separate workbench).

References:
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/132
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/.uigs/ui-surfaces.json

## Follow-up: concrete duplicate-control ownership and CSS accumulation (2026-10-13)

Source inspected: HSR `main`, commit `88cbadd80229720c88f85903fa3924e6a4fac2a3`, `app/static/index.html`.

- Proofreading workspace has `subFinalEditor` for final Chinese and states that it auto-saves after approximately one second of idle input. Layout workspace has a separate `layoutCueFinalText` editor and explicitly requires `layoutCueSaveBtn`. This is not merely two read-only projections: the same kind of final subtitle text is independently editable through UI with divergent save semantics. A single authoritative final-text write path is preferable, retaining the distinct high-value proofreading context and shared per-cue identity.
- Proofreading has `subListView` / `subSearchQuery`, while layout has `layoutCorpusList` / `layoutCorpusSearch`; both provide project subtitle navigation. The original WAV is available via `subOriginalAudio` and via layout's `layoutCueAudio` with waveform. A shared item-selection/audio resource component or explicit read-only projections can eliminate duplicate business ownership without eliminating purpose-specific affordances.
- Layout's `layoutCueScrubber` and karaoke `prevKaraokePreviewTime` are separate time-position controls that need an explicit shared preview-clock contract; they need not be identical controls, but inconsistent clocks or effects are a risk worth testing.
- The production `index.html` is 8,516 lines / 421,591 characters at inspected main; its CSS contains 945 `!important` uses and repeated layout/workbench selector overrides. This count is a maintainability signal, *not* proof that every override is a defect. A previous HSR #129 explicitly fixed a real old/new CSS layout-authority collision.
- Proposed acceptance structure: one authoritative cue editor and commit path; per-workspace presentation projections; a distinct typography/layout workspace and motion/Karaoke effects workspace sharing one preview/clock/state; preview-render verification separated from actual moving-video playback; output execution remains in Export. Never silently remove existing actions before an ID→owner→destination parity ledger and regression.
- This overlaps the existing Foundry MKV two-editor Candidate `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md` and CSS authority Candidate `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md`. Treat the HSR facts as project-specific corroboration in this existing Observation, not as a new universal rule. Do not auto-promote Canonical.

Suggested validation: user-visible save behavior across Review/Layout, delayed input vs stale backend response, identical export text/sidecar, cross-workspace focus/preview identity, FFmpeg/libass v. browser still-frame mode, actual video playback, and 390px/768px/1600px responsive captures.


## Delivery follow-up: three-pass implementation landed to main (2026-10-13 discussion / UTC merge 2026-10-12)

Product: `11576865/HSR-Voice-Archive-Builder`. User explicitly constrained scope to **three processes only** (deduplication, UI workbench division, actual playable preview and acceptance), to prevent feature creep.

- Implemented PR [#135](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/135), source head `4072b8c43098d26512071b4c6e4054ee7e40ed63`, merged **directly to main** at `5e7fa67a2d3285c611390c1e0651ffcf24f5979e`. Verified subsequent main search and main file fetch.
- Pass 1: Review is the user-facing final Chinese text and original WAV editing/listening owner; Layout projects the selected text as read-only, routes to Review by cue identity; Review draft flush and Layout refresh on navigation. Existing timeline display timing editing remains.
- Pass 2: separate scoped Style and Effects views share a single project/render config/preview. Bilingual explicitly positioned CHS/Primary ASS styles no longer apply redundant Style margins on top of solver SafeArea. Debug boundary overlays default off.
- Pass 3: FFmpeg/libass renders **actual video over a generated black background**, 24fps, max 8s; WebM/VP8 chosen for Chromium where H.264 decoder unavailable, MP4/H.264 otherwise. Browser must decode and allows seeking; stale requests discarded. Backend FastAPI and Termux Lite provide protected API. This does **not** contain a user-provided moving video, source WAV synchronized audio, or physical device acceptance, and must not be described as such.
- Exact-head tests CI [38293666205](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38293666205) `success`; Chromium + libass [38293666354](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38293666354) `success`. The Chromium playback test used independently generated **real VP8 video bytes served by API fixture**; backend FFmpeg/libass actual video encoding/decode-frame difference was tested in a separate job. This scope distinction prevents E2E overclaiming.
- Maintains important explicit non-claims: complete removal of all duplicate code (legacy handlers remain for compatibility), comprehensive CSS refactoring, production multimedia user-supplied video overlay, and field/device sign-off have **not** been proven. Source-level UI deduplication and two-role projection were delivered; this is a bounded implementation, not full architectural rewrite.

Reusable observation: define and prove **user-facing ownership / product acceptance** separately from source-code deduplication and automated rendering evidence. A three-pass stop rule forced main integration and eliminated unbounded feature expansion, while distinguishing actual playable black-background preview from actual source-footage composite.

Deduplication: retain existing `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md`; related records: `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` and `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`. Observation only; **Canonical unchanged**.


## Delivery follow-up: opt-in local moving footage composite (2026-10-13)

Converged directly on main via HSR PR [#136](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/136), exact source head `e3e2ff874260e56ea0295ab631be4cd2cca1a985`, squash merge `b51cf24e11f095329527ca6594af7199054a6002`; post-merge main tip and test file were verified.

User-facing improvement: the previously black-only animated libass proof now has an **optional** user-selected local moving-video input (with source offset and clear-to-black). The same renderer burns animated ASS over a real moving background. UI represents `video-footage` separately from `video` (generated-black) and displays source provenance. This is not a new production export or second subtitle authoring system.

Implementation and limitations: no user-provided path or URL is accepted by the FFmpeg execution plan; the API accepts only up to **4 MiB** of base64-decoded local bytes, checks actual JSON request length at **8 MiB**, and probes the file for a video stream, source-window duration, and maximum **3840×2160** dimensions. Selected start offset is **0–600 s** and preview output **0.5–8 s**, 960×540, 24fps, without audio. Input is held in a temporary directory and deleted after each render. Termux Lite and FastAPI keep their distinct host implementation but share the renderer.

Exact-head CI:
- [38326261385](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38326261385): `success` (Python matrix and Termux Lite).
- [38326261297](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38326261297): `success` (Chromium interactions and actual FFmpeg/libass backend proof).
- Chromium test picks real WebM bytes via a file control and proves browser decode, state provenance, and seeking. API is fixture-backed for this browser test. A **separate backend test** synthesizes a real moving-video source, compares a rendered ASS overlay against a source-only encode, and decodes actual pixel differences. Do not misreport the Chromium test as an integrated actual backend E2E with real user clips.

Observed edge case: A pixel-comparison control test initially supplied both dialogue fields empty to the ASS writer, which correctly rejects dialogue-less output; test repaired by independently generating a no-subtitle FFmpeg control clip using equivalent frame normalization. This is a **test fixture defect**, not an application regression.

Still out of scope: unbounded/full-length footage, audio synchronization, source-time-aware word highlighting beyond the preview-local interval, large uploads, arbitrary codec/device coverage, end-to-end actual backend Chromium playback, real Android-device validation, or final project export.

Reusable project-specific lesson: a video-effect preview has multiple distinct evidence layers—UI provenance, actual source-byte forwarding, decoder usability, and source-vs-overlay rendered pixel proof. Green at any one layer cannot stand in for the rest. Deduplication: attach to this existing HSR Observation and the related subtitle preview Case rather than creating another overlapping Candidate. **Do not promote to UIGS Canonical from this single project.**


## Mainline update: opt-in source audio and live Chromium/libass E2E (2026-10-13)

HSR [PR #137](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/137) merged **directly into main**, exact source head `a24b25889b8b19dfafab6c05492e1edf44a1bd9f`, squash commit `aba42855b32828e12c86b209ff000440e364adc8`. Verified post-merge main tip and the live E2E test file.

Product boundary: extends *existing* Effects workbench, no second editor, no new workbench. Opt-in local source input increases from 4 MiB to **24 MiB** with 36 MiB request-body bound on the preview endpoint only (Lite's other operations retain the 8 MiB request cap). Video output stays **0.5–8s**, source offset **0–600s**, 960×540, 24fps, ephemeral source within the FFmpeg temp dir. This remains Base64 JSON (not an unbounded/streaming full-movie design).

Audio semantics: `include_source_audio` selects the **first audio track of the user-selected video**, if present. It is seeked and clipped in the *same* FFmpeg operation as source picture + libass ASS. MP4 transcodes that audio to AAC; WebM to Opus; opting out or using black input yields silence. This is **not** synchronization with the HSR archive's separate WAV file, nor proof of all audio tracks/encoders/devices.

Exact-head green CI:
- [38328657466](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38328657466) — Python matrix 3.11/3.12/3.13 + Termux Lite, all success.
- [38328657467](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38328657467) — real FFmpeg/libass unit proof, responsive Chromium layout tests and **live browser-to-server media request**.

The newly added `tests/browser_live_preview_e2e.py` runs the real FastAPI application through uvicorn, loads the shipped HTML under **production CSP**, selects real synthetically generated WebM video with an Opus tone, and forwards its video-preview API through Playwright's `route.fetch()` to the **actual backend**. It captures that actual response body (not a mock media fixture), delivers those same bytes to Chromium, confirms FFprobe codec and AV start alignment, actually decodes output audio samples, and checks browser decoded video + seeking. Unrelated project/corpus endpoints retain fixtures; real Android/production user-media coverage remains unproven.

Two newly observed testing pitfalls (not automatically Canonical):
1. The old fixture-only browser suite lacked production Content Security Policy, so `page.wait_for_function` string-expression tests did not catch `unsafe-eval` restrictions. Live test retains CSP and uses `page.evaluate` callable polling, never weakens production policy.
2. Under Playwright `route.continue_()`, the subsequent page response's `Response.body()` was empty in this CI environment even though it had HTTP 200 and real media headers. The test captures original binary using `route.fetch()` and `APIResponse.body()`, then `route.fulfill(response=upstream, body=payload)`. It does not fabricate rendered media; E2E assertions read verified upstream bytes and confirm the same bytes are playable in Chromium.

Deduplication: recorded as a follow-up to this existing HSR Observation, and complementary to `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`; do not generate redundant generalized rules from one app. Canonical unchanged.
