# Test: QHE B14 Native matched-source CQ encode time is observational, not a whole-movie forecast

Date: 2026-10-14
Status: Implemented in QHE PR #105, exact-head CI Pending
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Product commit: `2df06aa11f9cdc8e26aa7a9e45042641ec8cecd1`
Scope: Windows Native Manual pure transcode; same source/reference windows; per-CRF FFmpeg short encode stopwatch

## Distinct verification boundary

The Manual comparison already collected CQ rate-distortion points with a Native receipt and `sample.elapsedSeconds`. This implementation adds a separate, explicit time-cost interpretation. A curve's interpolated, selected budget bitrate does **not** inherit the encode time of the closest observed CQ point, nor a forecast of whole-movie throughput.

Input constraints for a recognized time observation:
- normalized protocol and source/runtime/reference/window identity equal across candidates;
- complete, paired windows at a directly measured CQ quality setting;
- finite, positive FFmpeg stopwatch seconds per window, finite SSIM and packet-derived video bitrate;
- aggregate min/average SSIM and bitrate recomputed from the actual window measurements;
- no changed-source/stale-session/partial CQ measurements;
- quality-near pair only when minimum and mean SSIM differences are each ≤ 0.003; this threshold defines observational proximity, not equality.

Expected output: per candidate measured media seconds, FFmpeg encode seconds, realtime speed factor, closest **measured** quality setting and delta from selected budget. An optional near-quality sample pair describes both time and video-rate ratios. User-initiated JSON evidence export carries protocol identity and explicit `fullMovieEncodeTimeVerified:false`, `vbrResultNotImplied:true` and `canAutoAdopt:false`.

## Evidence
- `src/manual-time-tradeoff.js` plus `src/manual-transcode-compare-ui.js`.
- `src/manual-time-tradeoff.test.mjs`: actual matched-window aggregation; two-codec ratios; quality-gap noncomparable; zero, missing, malformed, negative, nonfinite cost refusal; different source/protocol refusal; incomplete windows, rate-summary mismatch, no full-film prediction and no implicit codec adoption.
- `src/manual-transcode-session.test.mjs`: exercises the timing view through the existing source-validated in-memory Manual session path.
- `.github/workflows/test-frontend.yml` includes the new test in draft-fast and full frontend checks.
- Before push, six extracted pure tests executed PASS in an isolated JS V8 environment against actual retrieved QHE module code. This is **not** Node, browser or Windows runtime acceptance; parsed authored module/UI function source without a build failure.
- PR #105 exact-head status at the immediate one-time read: Test frontend and UIGS Evidence Coverage queued, some heavy Draft jobs skipped, Android/Windows Stream Plan workflow containers listed in progress (job-level conclusion not yet established).

## Open acceptance
Observe exact-head Node CI and real Manual browser presentation/export, then measured Windows Native test sources. Full-film time, GPU/ASS workloads, resource usage and user time-intent optimization remain incomplete B14 obligations. No Canonical promotion, no B14 completion claim.

## Dedup
Foundry searches `measured codec time quality tradeoff`, `sample encode time matched windows`, `time estimates native codec frontier`, `QHE B14`. Related `inbox/candidates/2026-10-03-calibration-must-optimize-information-gain-per-unit-time.md` covers *sampling policy*; `inbox/tests/2026-10-12-qhe-manual-paired-candidate-evidence-contract-synthetic.md` covers CQ *source comparability*. This Test covers measured encoding compute costs and excludes silent extrapolation to unmeasured target/whole movie.
