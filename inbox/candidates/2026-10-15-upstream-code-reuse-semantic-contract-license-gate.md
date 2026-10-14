# Candidate: Upstream code reuse requires semantic-contract and license gates

Date: 2026-10-15
Status: Candidate / read-only source-comparison observation
Source project: 11576865/Quick-Automatic-Hardsub-Encoder (QHE)
Scope: engineering-research, reuse, media execution, regression evidence

## Trigger
QHE full initial-version engineering was being estimated as if many existing workflows needed fresh implementations. A source-level review of comparable projects showed multiple reusable *implementation strategies* already available, alongside mature QHE facilities. The investigation did not modify QHE source code or verify an upstream integration.

## Concrete source comparisons
- alexheretic/ab-av1 (MIT): `src/command/crf_search.rs`, `sample_encode.rs`, `src/sample.rs`; bounded sample CRF search, quality measurement, cache, full-job predictions. QHE already has rate-distortion and sample evidence: compare convergence/stopping/cache identity before adding an alternative optimizer.
- mifi/lossless-cut (GPLv2): `src/renderer/src/smartcut.ts` plus `hooks/useFfmpegOperations.ts`; detect exact cut keyframe, encode short head, copy remainder, concatenate. Upstream documents experimental seek limits. Reference as algorithm and negative tests, not source-copy into MIT QHE without license assessment.
- skeskinen/smartcut (MIT): `smartcut/video_cutter.py`, timestamp/GOP handling via PyAV; code is available but the repository states maintenance moved elsewhere. Use as a test/problem guide, not a supported dependency.
- HandBrake/HandBrake (primarily GPLv2): `libhb/preset.c` audio copy mask and audio selection; source-level inspiration for explicit passthrough policy, not a code import into MIT QHE.
- staxrip/staxrip (MIT): `Source/Encoding/x264Enc.vb`, `Source/General/JobManager.vb`; multi-pass argument construction and saved job queue; QHE should extend `src/media-task.js` and existing execution lifecycle rather than copy a second scheduler.
- ffmpegwasm/ffmpeg.wasm (MIT wrapper; codec/core terms vary): `packages/ffmpeg/src/classes.ts`; its `FFmpeg.load/exec/writeFile` API is not the `FFmpegKitConfig/FFmpegKit/FFprobeKit` API expected by QHE `src/engine.js`. A vendor directory populated with a different package does not close the actual Web runtime gate.

## Proposed reusable engineering gate
For each candidate upstream implementation, require a five-column mapping: (1) exact upstream source and revision; (2) current authoritative project module; (3) the smallest missing behavior; (4) API, data semantics and licensing compatibility; (5) a failing regression plus real execution and independent result validation where meaningful.

Distinguish *algorithm reference* from *source import* from *runtime dependency*. Do not displace an existing canonical compiler, media plan or renderer when only a small adapter, missing dependency, or test is required. Observe upstream caveats and keep physical-device acceptance separate from hosted fixture success.

## Related Foundry records / deduplication
Reviewed adjacent Candidate `2026-10-03-reuse-existing-operational-history-before-adding-new-calibration-telemetry`, Candidate `2026-10-14-product-block-delivery-over-pr-fragmentation`, and the QHE report-scope Case `2026-10-13-qhe-report-baseline-cannot-be-replaced-by-scoped-ci-delivery`. They cover evidence reuse, delivery granularity, and approved requirement scope, not this exact upstream source-to-internal-authority compatibility gate. The user’s project principles already require studying others' successes/failures; this Candidate refines its code-reuse acceptance mechanism, not a new Canonical principle.

## Evidence and boundaries
Source inspection was read-only, 2026-10-15, on public upstream default branches and QHE PR #105. No comparative benchmark, fork, implementation, actual Smart Cut execution or ffmpeg.wasm adapter test was conducted. Upstream files may change; pin commit when implementing. No Canonical promotion from this single observation.

## Follow-up
On any concrete QHE task, select one actual missing behavior (e.g. Web runtime compatibility, keyframe cut handoff, sample cache invalidation), verify exact pinned upstream and QHE code, then write the smallest adapter plus independent media regression; do not convert this research note into a feature-completion claim.
