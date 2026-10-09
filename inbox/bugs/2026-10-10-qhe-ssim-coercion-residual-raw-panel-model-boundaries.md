# Bug: Strict SSIM input validation is bypassed by intermediate numeric coercion

Status: Open — code-inspected, regression/runtime reproduction pending
Date: 2026-10-10
Source project: 11576865/Quick-Automatic-Hardsub-Encoder
Source main: `2eeaab388851008a72c653aaf9f0f14560262b76`
Domain: data provenance, measurement validation, rate-distortion prediction

## Code-level reproduction hypothesis

PR #72 made `src/transcode-curves.js` reject null/blank/boolean SSIM inputs in `measurement()` and `qualityMeasurement()`, and tests cover those public functions. However, in `src/transcode-calibration-panel.js` the result of `hooks.calibrationSample()` is checked only with `sample.ssim == null`, then stored as `ssim: Number(sample.ssim)` in the `sampleMeasurements` array.

Therefore an upstream value `sample.ssim = false` or `sample.ssim = ''` is non-null and is converted to real numeric `0`; `true` converts to `1`. A subsequent strict validator cannot distinguish the synthesized number from a genuine measurement. `Number(' ') === 0` is another instance. This is a visible input validation gap, not proof that current native FFmpeg actually emits such values in normal operation.

Separately, `src/rate-distortion-model.js` has its own `finite()` wrapper: it excludes null/undefined/empty string but accepts booleans and whitespace via `Number(value)`. Thus direct model callers remain susceptible to nonexistent quality being ingested as 0/1 if no upstream strict normalization is enforced. Existing `rate-distortion-model.test.mjs` covers null but not these boolean/whitespace cases at the model boundary.

## Risks

Fabricated endpoints and threshold-passing/failing statuses; artificial low/high R-D observations; model fit and UI selection derived from unmeasured values. Impact requires actual malformed upstream input or an untrusted caller and is **not** claimed reproduced against a real device.

## Proposed test and fix

1. Pass `false`, `true`, `''`, `' '`, `null`, valid numeric 0/1 and valid numeric strings through the *complete* calibration callback -> sampleMeasurements -> exploreQuality -> model path.
2. Validate raw measurements before any `Number()`; define a shared strict parse for evidence-bearing quality fields at each trust boundary, or keep typed validated measurement objects.
3. Directly test `fitRateDistortionModel()` against boolean/whitespace quality fields while retaining valid 0/1.
4. Verify no invalid input is plotted/persisted/applied as a measured result.

## Deduplication and evidence boundary

Related existing bug: `inbox/bugs/2026-10-09-qhe-numeric-coercion-invents-missing-measurement-evidence.md`, marked fixed-verified for three entry points (`exploreQuality`, `summarizeCalibrationEvidence`, `buildExplorationPlot`) in PR #72. This new record documents previously unverified **different boundaries** (upstream panel's coercion and direct model entry), without contradicting the earlier scoped fix or declaring a verified runtime failure.

Do not promote to Canonical. No source code was changed in this intake.
