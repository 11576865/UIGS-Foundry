# Test: QHE Manual paired-candidate session atomicity, cancellation and Native replay

Date: 2026-10-12
Status: **PASS in exact-head CI**, limited to deterministic JS lifecycle regressions plus Windows-hosted real codec sample replay; not a user-facing Manual UI acceptance
QHE draft PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
Exact QHE SHA: `694dc6bfb05596fb40accfa36140c305a2b9ba30`
Related:
- `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`
- `inbox/tests/2026-10-12-qhe-manual-paired-candidate-evidence-contract-synthetic.md` (earlier protocol validation)
- `inbox/tests/2026-10-12-qhe-native-bridge-paired-x264-x265-comparison.md` (earlier real paired codec acceptance)

## What changed from existing tests
Prior tests established a valid multi-branch comparison from synthetic protocol points and, subsequently, from 12 real Windows x264/x265 short-sample observations. Neither guaranteed that **incomplete live per-window sampling**, cancellation, identity drift and incremental per-candidate session lifecycle could not contaminate previously measured curves.

QHE added `src/manual-transcode-session.js` with `createManualTranscodeSession` and `runManualPairedSweep`; wired `src/manual-transcode-session.test.mjs` into frontend CI. All 12 real Windows Native paired x264/x265 samples in `scripts/verify-manual-native-paired.mjs` now additionally traverse `session.addSample` before `session.compare`, cross-checking the old direct-comparison route.

## Exact assertions
- Session-specific reference protocol, source/runtime tokens, windows and candidate identities are frozen/validated and cannot be silently mutated via exposed session snapshot.
- A candidate quality setting needs *every* paired Native source window to complete; incomplete windows are never rate/distortion observations and never make a branch eligible.
- Duplicate window, wrong codec/preset, changed source/native provenance, unsupported geometry, unpaired/missing samples and invalid/partial receipt are rejected.
- Native source/reference/receipt incompatibility **invalidates complete as well as pending session evidence**; it must not leave an earlier valid-looking curve visible under a changed source.
- If the user stops between samples, or after Native returns but before admission, the late response is refused. Complete earlier CQ settings can remain while partial current CQ is discarded, provided the source/reference identity still matches. No claim of hard termination of the running FFmpeg process.
- Native failure cannot create a partial CQ point; a quality/samples/request/encode-cost budget is bounded. An empty/duplicate candidate or CQ plan cannot succeed as a no-op.
- Two or more complete eligible codec branches feed `createManualTranscodeComparison` and generate a single common measured byte-domain upper envelope; below/above-evidence predictions are refused.

## Real-media scope and CI
In `Windows Manual paired codec acceptance` `38270515270`, QHE Native Bridge genuinely sampled a 5-second FFV1 synthetic source with software x264/x265 × 3 CQ settings × 2 shared 1.5-second windows (12 real encodes/FFmpeg SSIM readings); the session registry accepted all 12 and produced the same bounded model branch IDs as the former independent direct-path verifier. This is **not** a mocked Native codec test. It remains a hosted Windows runner with synthetic content, not physical GPU/real-film or long-duration evidence.

Exact QHE SHA `694dc6bfb05596fb40accfa36140c305a2b9ba30` had all five successful workflows:
- Test frontend `38270515303`;
- Windows Manual paired codec acceptance `38270515270`;
- Windows local smoke `38270515272`;
- Windows Stream Plan v4 runtime acceptance `38270515300`;
- UIGS Evidence Coverage `38270515280`.

Two intermediate frontend test runs initially failed because test expectations disagreed with deliberately conservative cancellation timing and the `snapshot.stats.invalidated` shape. The assertions were corrected and **rerun at exact head**, without relaxing the provenance failure guard. Do not misreport those preliminary red runs as codec failures.

## Limits and next gate
The session module is not connected to Manual UI or current `hooks.calibrationSample` to drive an actual on-demand user comparison. It also does not yet provide persistent evidence storage, cryptographic source-file hashing, physical NVENC/AV1 acceptance, full film validity, hard wall-clock in-flight cancellation, or cross-codec formal VBR output adoption. The time budget tracks Native-reported *encode seconds*, excluding preprocessing, SSIM decode and transport. Scope is **Candidate/Test**, no Canonical promotion or main merge.
