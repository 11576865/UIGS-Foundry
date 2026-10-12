# Test: QHE actual Windows localhost Native paired x264/x265 CQ comparison

Date: 2026-10-12
Status: **PASS in hosted Windows CI**; full-length, user device, GPU, UI handoff, and final VBR acceptance **not proven**
Project PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104 (draft/unmerged)
Exact QHE SHA: `3f1b4fbc1d6a2c02c269f920a9db92adf04a9c52`
Workflow: Windows Manual paired codec acceptance `38268364465` (SUCCESS; exact SHA)

## Why this is new evidence
Previous `2026-10-12-qhe-manual-paired-candidate-evidence-contract-synthetic.md` tested paired model behavior with artificially authored response values and a single-encoder real-media stamp helper, **not** actual codec-paired FFmpeg samples through the production localhost API. This experiment is the next distinct proof layer.

## Executed path
- `scripts/check-manual-native-paired.ps1` uses installed FFmpeg to create a real, synthetic (non-user) 5-second FFV1 / yuv420p / 320x180 / 12-fps source file.
- Starts actual `windows/native-bridge.ps1` with `-InitialVideo` and fixed localhost session token. Confirms health, software `libx264` + `libx265` availability, and original media probe dimensions.
- Sends **12 actual POST /api/sample requests**: 2 codec implementations × 3 CQ/CRF settings (18, 28, 40) × 2 identical requested source windows (0.25s+1.5s, 3.0s+1.5s); `sampleExact:true`, `withSubtitles:false`, source-backed FFmpeg SSIM, fixed `medium` preset, no audio, no resolution change.
- Windows bridge returns actual selected encoder, measured sample duration, video packet byte totals and SSIM plus pre-/post-run source/runtime stat snapshot receipt.
- `scripts/verify-manual-native-paired.mjs` checks each candidate+quality+window pairing is unique and complete, runs `admitManualNativeCqSample` on every receipt, creates per-quality trial points (mean measured packet bitrate, minimum/mean window SSIM), and invokes existing `createManualTranscodeComparison` / `createMultiBranchFrontier`, then plots **one** bounded envelope via `buildSizeFrontierPlot` with explicit no-extrapolation assertions.

## Actual results for this CI run (do not generalize)
- Sample count = 12; per-sample FFmpeg SSIM approximately **0.93529–0.99828** on this 5-second synthetic source.
- Combined common modeled output-byte evidence domain approximately **39,986–149,237 bytes** (model's reserved-byte conventions; not actual output container size guarantee).
- Both candidate identities present with valid fitted alternatives at the same target budget; one upper-envelope curve is available. Midrange `incumbentOrPreferred` reported `h264-x264` for this run **only**, not a general codec ranking.
- Exact GitHub workflow `38268364465` succeeded. An earlier run `38268001729` also passed the same real path before package-install-hardening changes.

## Limits / non-claims
- It is a *real FFmpeg* experiment on *synthetically generated source media*, not a real film, user GPU, long-form scene range, physical Android, or actual app-facing manual multibranch scheduler.
- These are CQ/CRF source-backed short-sample SSIM measurements, **not** independent full-length VBR target-size/quality acceptance.
- `stat-sha256:` receipts hash filesystem path, size and mtime (FFmpeg token also version text), **not the file contents**, and do not prove time-frame identity cryptographically.
- Only two Windows software encoders were tested. No AV1, NVENC, multi-resolution Cartesian search, HDR/VFR, crop/filter/reference alterations, auto-switch or user-facing UI verification.
- CI evidence does not promote the PR to Canonical or authorize a merge. Owner review and broader fixtures remain pending.

## Follow-up gates
- Make measured real same-reference per-candidate trials an explicit, bounded Manual session registry without abandoning the one-branch quick path.
- Test per-branch cancellation, partial/missing sample invalidation, time-cost accounting, stable source/runtime identity, additional content types and bitrate-mode post-acceptance.
- Verify the actual browser visual interpretation and all relevant output artifacts before describing the experience as delivered.
