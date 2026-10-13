# Test: QHE Manual and Guided may share risk-window planning without sharing quality evidence

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact source commit: `7e8c150b1dcbe116c9139a04419d1dd957707a49`
Status: source-logic unit tests passed in isolated V8; exact-head Node/Windows/Browser CI Pending
Relevant requirements: B04/B11/B12/B15, with B15 partial implementation only

## Reuse decision and boundary

Guided ASS already used `scene-risk-selection.js::selectPairedSceneWindows` with Windows Native `sceneRiskOnly` probes. Manual two-codec/preset/geometry calibration used purely time-spaced `calibrationSampleStarts`. The new Manual adapter uses the *same* Native scene-risk probe and scene-stratification logic, while each decision session retains its own measurement/protocol identity.

The critical negative requirement is that **shared source-scene positions do not make measured quality references interchangeable**:
- Manual uses SDR pure-source SSIM with no ASS.
- Guided ASS uses subtitle-rendered reference and must account for ASS content/font/rendering identity.
- A paired window's risk score is not an SSIM observation and cannot attest encoding throughput or final output size.
- A time-scoped Manual CQ native receipt still must pass its own source/runtime/reference/filter/window identity gate and subsequent VBR confirmation before explicit adoption.

## Implementation and test

- `src/manual-paired-risk-plan.js`: bounded at most three Native risk probes, total 9s planning budget, 2 nonoverlapping paired windows, absolute source-trim times, fail closed on stale settings or nonseekable source, fallback to time-stratified windows without declaring fabricated risk coverage.
- `src/main.js`: exposes existing Windows Native `sceneRiskOnly` endpoint to Manual and forwards seekability in shared probe metadata.
- `src/manual-transcode-compare-ui.js`: one sampled plan/fingerprint for all candidate codec × preset × resolution branches in the current comparison session. Does not alter the explicit native VBR adoption transaction.
- `src/manual-paired-risk-plan.test.mjs`: signal-dependent risk-window selection, absolute trim time, one Native risk failure fallback, late/stale rejection, malformed/unseekable/short source refusals, short four-second nonoverlap, and source-level Native/UI wiring.
- `.github/workflows/test-frontend.yml`: added to Draft fast and full frontend gates.

Six independent pure logic tests executed successfully on the retrieved source in an isolated V8 evaluator; UI module parsed. These checks are limited and are **not** full Node import/module execution, native FFmpeg, browser or long-form field acceptance. Exact-head CI still Pending at recording.

## Further verification requirements

1. On Windows Native, produce actual `sceneRiskOnly` measurements for multiple video scene types; compare sampled positions and receipt source IDs with all codec branches.
2. Change source/settings during a probe: late result must be rejected before any CQ point is accepted.
3. Verify trim ranges use absolute source timestamps, two windows never overlap, and unseekable material is explicitly rejected.
4. Verify Guided ASS still renders subtitle reference, and no Manual SSIM evidence can be transposed into a Guided ASS frontier.
5. Verify Draft-fast Node tests, full browser run at review gate, and actual ASS-heavy/high-risk material.

This extends prior `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md` but is a distinct Test of *sampling policy versus reference-identity separation*. No promotion to Canonical or claim of full B15 / theoretical initial version completion.
