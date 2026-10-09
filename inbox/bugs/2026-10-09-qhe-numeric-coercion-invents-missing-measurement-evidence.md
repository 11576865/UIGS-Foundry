# Bug: Numeric coercion can invent measurement evidence

Status: fixed-verified
Lifecycle: regression-verified
Date: 2026-10-09
Source project: 11576865/Quick-Automatic-Hardsub-Encoder
Domains: evidence-validation, media-processing, data-visualization

## Reproduction

`Number(null)`, `Number('')`, `Number(' ')`, and `Number(false)` yield zero. `Number(true)` yields one. Checking finite/range constraints after this coercion alone accepts missing/nonmeasurement values as valid SSIM observations.

Reproduced in three QHE entry points:
- `exploreQuality`: null SSIM was published as a real zero-quality result; infinite bitrate also passed the positive-rate check.
- `summarizeCalibrationEvidence`: null SSIM became a reported measured minimum of zero.
- `buildExplorationPlot`: absent SSIM became a plotted point; missing sample values expanded scene ranges toward zero.

## Correction and test evidence

Parse measurement values only when the input is a number or a nonblank numeric string, then enforce finiteness and the application's SSIM contract. Reject booleans and absent/blank values. Preserve legitimate measured zero/one endpoints and numeric strings. Search rejects invalid evidence before calling onPoint; summaries require all sample fields; plots omit invalid rows without silently renumbering source-order trials. Pass status derives from the plotted threshold.

Five new regression tests were run red before implementation. Follow-up local verification: `FFMPEG_INTEGRATION=1 node --test src/*.test.mjs` passes 114 tests, zero skipped. Build and diff checks pass.

PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/72
Commit: 2373ec71a490146263fc9320081f27122902e5d7

The same PR moves target-label text outside the data area and adds browser geometry checks; standard CI subsequently passed both desktop and narrow-screen geometry checks. PR #72 merged as `2eeaab388851008a72c653aaf9f0f14560262b76`; release verification is separate.

## Deduplication and limits

Foundry searches for `null zero measurement`, `missing measurement`, and `finite coercion` returned no matching records. This concretizes existing raw-evidence principles rather than modifying Canonical rules. No real GPU, long-material or device acceptance is claimed.
