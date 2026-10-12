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
