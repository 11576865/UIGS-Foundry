# Observation: HSR gradient backgrounds must follow the first theorem's prior-art gate

Date: 2026-10-13
Status: Observation / early source review; no feature implementation or runtime test
Project: `11576865/HSR-Voice-Archive-Builder`
Domains: background generation, UI reuse, FFmpeg integration, quality acceptance, engineering method

## Trigger: violated product process

The user pointed out that gradient and soft backgrounds are established capabilities, and challenged a proposal to design HSR-specific presets, controls and parameter taxonomy from scratch without first surveying successful and failed existing implementations. The authoritative `项目原则报告_2026-09-30.txt` explicitly calls its first principle `第一定理：既有经验与失败研究定理`: first survey comparable Internet projects, why implementations succeeded, public failures/maintenance costs, reusable/avoided choices, and the differentiator. A speculative UI design without that survey violates the first theorem.

## Preliminary authoritative examples (not a comprehensive competitive audit)

- Shotcut's preexisting Gradient Video Filter documents `linear/radial`, offset, colors, position and blend mode; a reply from a user briefly thought options missing, then retracted that report. Distinguish this from Shotcut's *Gradient Map* (maps image intensities to a color ramp; not the same function): https://forum.shotcut.org/t/gradient-video-filter/14508
- Kdenlive's maintained `Cairogradient` lists pattern, start/end colors and opacity, normalized start/end coordinates and blend mode as a video effect: https://docs.kdenlive.org/en/effects_and_filters/video_effects/generate/cairogradient.html
- Kdenlive's title shape editor provides solid color or gradient, selectable presets and gradient editor without making users use a standalone paint product: https://docs.kdenlive.org/en/titles_and_graphics/titles/title_shapes.html
- GIMP's gradient tool exposes linear/radial and many additional shapes, and separates perceptual RGB, linear RGB and CIE Lab interpolation. Their existence is *prior art*, not evidence HSR requires an eleven-mode paint UI: https://docs.gimp.org/3.2/en/gimp-tool-gradient.html
- **FFmpeg itself already implements the `gradients` video source** with linear/radial/circular/spiral/square modes and multiple colors in newer source; available options vary across version; feature must be checked at runtime. This makes coding an entirely separate gradient renderer premature. https://www.ffmpeg.org/doxygen/8.1/vsrc__gradients_8c_source.html and https://ffmpeg.org/doxygen/5.1/vsrc__gradients_8c_source.html

## Initial failure/risk research

- FFmpeg's `gradfun` documentation explicitly states that 8-bit truncation causes **banding** in near-flat gradients, and it says the `gradfun` filter is designed for playback, not as pre-lossy-compression mitigation; encoding may erase the dithering. A linear/radial gradient is easy to render yet can still look poor in the final H.264 output. Source: https://ffmpeg.org/ffmpeg-filters.html (gradfun section).
- Cross-platform FFmpeg versions and static builds may differ in `gradients` availability or parameters, so a planned integration must discover the installed capability, test generated pixels with real FFmpeg and verify the final MKV on representative targets. This is a validation hypothesis, not a reported HSR field failure.
- Gradient Map versus Gradient generator are different operations; the names must not be conflated in the design or testing.

## Bounded consequence for HSR

Stop inventing novel soft-background option lists before evidence. First compare existing workflow controls and real source filter support. HSR likely needs only a *small reuse/adaptation* of proven linear/radial gradient input and preview behavior, integrated into the current Export/background scope, while keeping source FLAC, ASS and atomic MKV publication unchanged. Advanced gradient editing or broad creative presets are not established user requirements.

Acceptance must include actual FFmpeg output and final H.264/MKV frames (especially banding, clipping, black borders, text contrast and cross-build filter support), plus project-setting persistence; raw preview CSS is not a substitute. At this intake point there is **no code implementation, no validated gradient feature or production failure reproduction**.

Related: `inbox/observations/2026-10-13-hsr-mkv-track-refresh-vs-full-rebuild.md` tracks *export lifecycle* rather than prior-art background controls. Dedup search for gradient/background prior-art returned no matching Foundry records. No Canonical change.


## Implemented and exact-head verified — HSR PR #157 (2026-10-13)

The first-theorem research is now consumed by a shipped implementation, not just a proposed design. [HSR PR #157](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/157) merged into `main@2c2bf0845d1088b194de80c78f17b2f6ba368819`; its exact tested head is `19aab7466be868dc6aaa6dc21092bfb305a563bf`, with postmerge comparison `identical`.

- `app/archive_bundle_backgrounds.py` centralizes strict background mode/color/direction/resolution/quality validation, uses existing FFmpeg `gradients` source for linear/radial/soft, and `gblur` for soft. Static frame is encoded once and looped as a 1 fps source; 720p and 1080p, H.264 CRF 28 and 19 selectable. Pure color and uploaded image modes remain.
- The existing Export/complete MKV panel includes mode and color controls, FFmpeg-rendered 640x360 PNG preview, output quality choices, and persistence in `archive_bundle_receipt.json` across projects. Both full FastAPI and Termux Lite APIs share the input validation and preview. No arbitrary FFmpeg filter strings are accepted; existing stale-ASS checks, stream validation, and last-known-good MKV publication remain intact.
- New `tests/test_archive_bundle_backgrounds.py` and companion UI contracts verify input bounds/injection, FFmpeg-rendered PNG, actual MKV H.264+FLAC+ASS streams, decoded colors and 1080p output. `tests/browser_visual_evidence.py` verifies production HTML in 1600x900 and 390x844 Chromium with a *real FFmpeg generated PNG* in the browser fixture (the preview endpoint is test-intercepted with a real encoded FFmpeg result; it is not a live webserver integration proof).
- [Python 3.11–3.13 + Termux green](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38400360280), [real FFmpeg/libass and Chromium green](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38400360262). All are verified against exactly `19aab746...` before the PR was merged.
- Two important regressions surfaced and were fixed by evidence: `gradients:speed=0` is invalid in the installed FFmpeg (minimum is `0.00001`), so a legal minimum is used while rendering a single still; CSS author display rules overrode the HTML `hidden` attribute on irrelevant background controls. A separate existing workspace auto-collapse initially hid the Archive panel; `archiveCard` is now a primary Export panel.

**Evidence limits:** No physical Android playback, multi-hour throughput benchmarking, or cross-player guaranteed gradient banding elimination. FFmpeg gradient availability remains a runtime compatibility requirement. The previously stated `not implemented` status above is historical and superseded by this section. No Canonical promotion.


## Follow-up acceptance tracking #158 / closing audit (2026-10-13)

A postmerge recheck confirmed `main` is exactly `2c2bf0845d1088b194de80c78f17b2f6ba368819` (comparison `identical`), PR #157 remains merged and closed with no unresolved review threads, and all exact-head runs including Python/Termux, Chromium/real FFmpeg, and branch hygiene concluded `success`.

The production-only evidence gap is now explicitly tracked in [HSR issue #158](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/158): real Android FFmpeg/filter support and player behavior, decoded H.264 gradient banding on physical displays, long-duration performance/memory, and separately whether the older 4 MiB *uploaded image* input limit merits future safe-streaming treatment. This issue is non-blocking for merged PR #157; it must not be represented as tests already passed.

**Administrative caveat:** the squash-merged feature ref `feat/hsr-gradient-soft-background-complete-20261013` remained discoverable after the successful branch hygiene sweep because squash merge does not imply the original feature commit is ancestrally contained in `main`. This is consistent with existing Foundry `inbox/tests/2026-10-04-branch-hygiene-deletes-only-ancestry-proven-merged-branches.md` and `inbox/candidates/2026-10-11-squash-merged-branch-tags-before-ref-pruning.md`; do not force-rewrite the feature ref as a workaround. No new Candidate or Canonical modification.


## HSR Issue 158: direct-main technical acceptance checkpoint

A read-only MKV technical acceptance script (`scripts/hsr_mkv_acceptance_probe.py`), tests (`tests/test_hsr_mkv_acceptance_probe.py`), and instructions (`docs/mkv-gradient-backgrounds.md`) have been committed to HSR `main`. Latest product checkpoint: `d9ac8e4b8cf9d64a8d518238072b6c81fc021e2f`. The script examines final MKV H.264/FLAC/ASS tracks and decoded H.264 PNG samples, not source/preview images. The output explicitly keeps real Android playback, visual banding, and multi-hour performance `unverified`; those remain open in Issue #158. CI for these direct-main commits has not been confirmed. This updates the existing Observation only; no Canonical changes.


## Direct-main HSR derived-bundle and image-cap repair (2026-10-13)

User feedback identified two gaps after PR #157: HSR displayed a stale complete MKV as merely "available" alongside independent FLAC/SRT/ASS and old black MKV; the advertised uploaded-image cap was still 4 MiB despite a prior recommendation to raise it.

Mainline repair checkpoints culminating in `2015dda5c60834f6aeed84ec8b31910da5a77b7b` address both as one source-aware delivery contract. The bundle status now reports explicit `depends_on`, `prerequisites`, `can_generate`, and `blockers`; old MKV bytes remain recoverable but "stale/unverified" no longer counts as current. The UI puts the derived complete MKV first, keeps FLAC and subtitle sidecars independent, labels the historical black MKV as a legacy compatibility output, and provides source-specific next steps rather than presenting both MKVs as equivalent. The project summary additionally classifies `playback_bundle`, `independent_products` and `legacy_outputs` without breaking `final_products`.

The background image cap is now centrally 16 MiB, and full/Lite JSON requests allow at most 24 MiB for base64 transport. The FastAPI handler checks *actual streamed bytes*, not only Content-Length. Backend receipt persistence/reuse, source export decoder, genuine FFmpeg preview and the optional subtitle-effects still-image preview share the 16 MiB limit while retaining image-format, 8192-per-side/24-million-pixel bundle checks and the separate preview dimension constraints. Regression tests cover >4 MiB replay, 16 MiB acceptance/oversize rejection, streamed FastAPI limits, Termux Lite endpoint-specific body limits and dependency-state transitions.

Evidence status: source commits are pushed directly to HSR `main` for user feedback; **do not claim CI or physical-device acceptance until an actual matching run is observed**. The image-cap portion of Issue #158 has an implementation checkpoint, but Android player behavior, color banding and multi-hour benchmarks remain open. This observation updates an existing finding; no automatic Canonical changes.


## Follow-up: real >4 MiB image and stale-product browser assertions (2026-10-13)

The previous repair had simulated a 5 MiB PNG header for storage/identity testing. That validates byte limits but not actual picture decode. A new real-image regression generates an approximately 5.58 MiB, 1500×1300 RGB PNG and attempts genuine FFmpeg preview, full H.264/FLAC/ASS Matroska publication, SHA-256 persisted-image reuse, and identical preview after reload (product `tests/test_archive_bundle_large_image_integration.py`). An isolated local FFmpeg image decode was exercised successfully; **the newly committed end-to-end test is not yet confirmed by a matching CI result**.

The production Chromium evidence script now checks independent FLAC/SRT/ASS, stale/current complete-MKV badges, an actionable stale-subtitle prerequisite, and legacy black MKV identification. New source-level bug: the project overview's product-visibility test accidentally read `finalProducts` before its `const` initializer; fixed by early `availableProducts` binding and recorded separately in `inbox/bugs/2026-10-13-hsr-output-browser-premature-final-products-reference.md`. A malformed background receipt is also now treated as unverified rather than crashing project summary.

Main latest at time of intake: `dabb1fd65a1523b4788d06f4eb0756779b8f42ac`. These are direct-main source/test checkpoints, not yet passing-CI or physical-Android verdicts. No Canonical modification.


## Additional mainline prerequisite and 16 MiB memory regression (2026-10-13)

Further direct-main verification identified two bounded gaps after initial HSR derived-bundle and upload-budget delivery. Existing checks treated *existing but zero-byte* FLAC/ASS/SRT files as ready to package, and project status recomputed saved-image SHA-256 with `Path.read_bytes()` despite the newly raised 16 MiB budget. Source commit [`378e276`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/378e276df660a99a3f815d2a4b2d81c615212b9c) now treats empty source files as blockers while preserving the last-known-good MKV, and hashes saved images in 1 MiB chunks rather than loading them eagerly on dashboard refresh. Regression commit [`6d9fc7c`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/6d9fc7c18e6bd197ede3757dd31f9ef6bf4e1ac1) tests empty FLAC/ASS/SRT gating, old MKV retention, and bounded-memory content-addressed image validation.

**Evidence boundary:** the per-source check is a fast size/mtime presence preflight, not a full FFprobe or immutable cryptographic audio seal; project subtitle receipt separately checks text artifacts. Only source commits and test declarations verified so far. The connector's commit status endpoint returned no status records and its workflow-run listing only surfaces PR runs; therefore newer *push-only mainline CI remains unverified*, not assumed green. Android player compatibility and visual banding remain open in issue #158. This extends the existing Observation; no Canonical changes.


## Follow-up: independent SRT validity vs derived MKV readiness (2026-10-14)

After increasing the HSR source-image cap to 16 MiB, the derived-MKV product relationship was further tightened on product `main`. This iteration revealed a narrower source-state error: a valid standalone SRT export can have `ass_required=false`, so it must not be marked stale merely because ASS is missing. Full MKV export *does* require validated ASS plus FLAC and SRT. Conflating independent SRT validity with combined ASS/MKV readiness made the product browser misrepresent the standalone deliverable.

- `bundle_export_status.prerequisites` now exposes `srt_current` separately from `ass_current` and combined `subtitles_current`. Complete MKV `can_generate` is false until all required sources pass; a published MKV cannot remain `state=current` if blockers exist.
- Production artifact browser now uses independent source readiness to badge SRT and ASS separately, rather than propagating the MKV blocker onto both.
- `project_summary.output_groups.playback_bundle` is enriched using exactly one receipt-backed `bundle_health` status calculation: `freshness`, `current`, `needs_rebuild`, `can_generate`, `depends_on`, `blockers`. Historical `final_products` remains available; legacy black MKV is explicitly a separate `legacy_independent_video`.
- New regressions: SRT-only current receipt with absent ASS leaves SRT independently valid and blocks MKV, project-summary source-status coherence, and Chromium cards showing current SRT alongside stale ASS and stale MKV.
- Product `main` rechecked at `b77fccaa0a5b5a496a0f0d4142a8a79d2c89ef75` after direct-main checkpoints. Static source and test presence verified; **matching push-event CI and physical Android evidence not verified**.

Reusable distinction: **artifact state is scoped to its own provenance and intended use, not automatically inherited from a downstream composite artifact**. The downstream MKV may be blocked while an independent upstream SRT remains usable. Keep this as evidence-backed Observation rather than auto-promoting to Canonical.
