# Observation: QHE competitive scope is evidence-led encoding delivery, not generic editor feature parity

Date: 2026-10-12
Status: Observation / public-code and official-competitor-document review, not benchmark or field acceptance
Product: `11576865/Quick-Automatic-Hardsub-Encoder`
Main reviewed: `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38` (2026-10-11T17:30:39Z)
External PR: #102 open, not in reviewed main
Relationship: corroborates rather than supersedes `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md` and `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`.

## Verified product scope
QHE main now combines ASS hardsub with actual libass/font diagnostics, pure-video transcode, and stream-copy/trim. Source task schema v4 treats video stream selection, audio action, and independent trim/full policies separately; PRs #99-#101 added multi-clip queue, save-only recovery and in-place unsaved interval editing. #93-#97 rebuilt shared UI and Windows desktop source/viewer/inspector shell. Exact-device visual acceptance remains separate.

The guided compression decision path offers tested single-/multi-branch CQ/CRF quality-size evidence, sampled scene risk, resolution comparisons, bounded additional paired measurement, and optional Windows Native software-H.264 two-pass/strict byte-ceiling policies. Strict mode can refuse export of an over-ceiling artifact; it **does not** guarantee producing an artifact under arbitrary limits at acceptable quality. PRs #88-#90 added cancellation/staging cleanup, numeric budget feasibility, stream and packet verification, and digest verification, on synthetic Windows FFmpeg/Bridge regression evidence. Windows real GPU, complex ASS, HDR/VFR, and long film acceptance remain `FIELD-PENDING` (QHE #77; risk-sampling #76).

Cross-platform presentation must not be equated with equal capabilities: Android currently defaults to software encoding, browsers are memory/1 GiB-input-limited fallback, and the special strict/two-pass guided contracts are Windows Native H.264 libx264 only. HDR/high-bit-depth re-encoding remains blocked by conservative protection in current documentation; Stream Copy is an available separate path.

Sources:
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/README.md
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/docs/manual-media-workspace.md
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/88
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/89
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/90
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/97
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/99
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/101
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/102
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/76
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/77

## Official competitor reference boundary
- HandBrake: mature codec/preset/average-bitrate/multipass and ASS/SSA burn-in capability, not absent-market innovations. https://handbrake.fr/docs/en/latest/advanced/subtitles.html and https://handbrake.fr/docs/en/latest/technical/video-cq-vs-abr.html
- StaxRip: extensive Windows encoder GUI, script/filters, subtitle hardcoding, NVEnc. https://github.com/staxrip/staxrip/wiki/How-to-hardcode-subtitles
- Shutter Encoder: FFmpeg general transcoding and embedded/burned external ASS workflows. https://www.shutterencoder.com/documentation/
- ab-av1: sample-driven automatic CRF search with VMAF/XPSNR targets. https://github.com/alexheretic/ab-av1
- Av1an: per-scene target quality, multiple perceptual metrics, parallel and resumable encoding. https://github.com/rust-av/Av1an
- LosslessCut: established multi-segment stream-copy cutting, timeline and keyframe navigation. https://github.com/mifi/lossless-cut
- Tdarr: library-scale, scheduled/distributed video automation. https://github.com/HaveAGitGat/Tdarr

These are documented capability observations, **not** controlled superiority scores or recent hands-on tests.

## Product-evidence interpretation
A generic conversion/cutting feature alone is not a defensible unique selling proposition. QHE's potential coherent differentiator is the full source + ASS/font-render reference -> matched quality/cost/size decision -> native job -> verified final output chain, with explicit evidence modality and honest refusal paths.

Do not mistake:
- a merged implementation for actual GPU/long-form acceptance;
- measured CQ/CRF samples for guaranteed formal VBR quality/size;
- strict refusal to export over limit for guaranteed successful size attainment;
- common UI task semantics for native runtime feature parity;
- a curve over the tested branch/sample domain for an all-codec global optimum;
- a recently merged clip queue for established feature parity with LosslessCut;
- public feature inventories for measured competitor UX or user adoption.

Next proposed comparison should run a fixed corpus (ASS/font/render variation, motion/grain/dark scenes, 720p/1080p/4K, multi-track, HDR rejected cases) and report output byte accuracy, PSNR/SSIM/VMAF where comparable, runtime/calibration cost, user actions, failures, stream integrity and recovery alongside directly comparable competitor workflows.

This observation supplies a second product-specific ecosystem scope case and a QHE-specific benchmark matrix. It does not assert new Canonical product direction, that QHE wins any benchmark, or that this review implemented new functions.
