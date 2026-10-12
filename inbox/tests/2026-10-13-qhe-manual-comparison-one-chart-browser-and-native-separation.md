# Test: QHE Manual x264/x265 optional one-chart comparison — browser UI and Native evidence boundaries

Date: 2026-10-13 (Asia/Shanghai; QHE GitHub CI recorded on 2026-10-12 UTC)
Status: Test / **frontend Chromium + actual Windows Native paired-sampling exact-head success**; full five-workflow check documented separately
Project: `11576865/Quick-Automatic-Hardsub-Encoder`, draft/unmerged PR #104
Exact QHE head at verification: `ca7c9261d1e6065e8357aa39149ddbe3a4790670`

## Dedup
Existing `inbox/tests/2026-10-12-qhe-manual-candidate-session-atomicity-and-cancellation.md` proves *pure evidence registry lifecycle* plus real Windows paired replay; `inbox/tests/2026-10-12-qhe-native-bridge-paired-x264-x265-comparison.md` proves *12 actual hosted Windows FFmpeg source/SSIM samples*. This Test records the **new consumer Manual UI mode, one-chart semantics, accessibility, browser visual fixtures, and their specific gaps** rather than duplicating those proof layers.

## Actual UI code and acceptance

- `src/manual-transcode-compare-ui.js` is mounted by `src/transcode-calibration-panel.js`. The existing pure-transcode one-encoder quick curve, Native CQ calibration, VBR verification and formal bitrate adoption remain in place. An explicit opt-in action runs a bounded comparison of `libx264` and `libx265` with `medium` preset, identical two two-second source windows and CRF 18/28/40 (maximum 12 actual samples). Windows-only; primary v:0 SDR 8-bit `yuv420p`, original geometry and frame rate, no video filters or unmirrored advanced flags.
- The very first actual Native result provides origin, FFmpeg runtime and source-backed SSIM reference identity; the first receipt is reused for the first slot of the ordinary `runManualPairedSweep`. Preflight requires `compileTask` + Native encoder validation for both candidate configurations.
- Uses the existing **one Manual `#taskEfficiencyChart` SVG**, switched between single-encoder curve and cross-codec **one upper-envelope projection**. No second slider/chart and **no automatic codec, CRF or bitrate adoption**. Mode-specific legend labels distinguish original fitted curve vs candidate upper envelope and hide irrelevant single-encoder controls.
- Mobile/touch/keyboard alternative comparisons use an expanded accessible text list at the exact selected video budget, with per-branch fitted quality and conservative sample bound. The audio copy / attachments / container-size budget is explicitly **not represented**; it is a video-only projection, not a whole-file output promise.
- Stop requests are cooperative: Native encode in flight may finish; its late result is rejected, incomplete CQ windows cannot enter the recommendation, and prior fully complete settings are retained only within unchanged source/protocol. Exceeding bounded reported native encode cost or mismatching source/reference invalidates or refuses evidence rather than treating it as valid.
- Changing SSIM target alone preserves compatible expensive measurements. Source/task changes invalidate evidence. No dual mutable source-of-truth UI and no change to task schema v4 or Stream Copy cutting.

## Browser fixture and independent visual review

`scripts/check-curve-design.cjs` mounts the actual Manual pane with **synthetic/mocked Native transport responses** (not actual local FFmpeg), runs a complete 2-codec/3-quality/2-window comparison, verifies exactly **one Manual SVG**, two candidate text rows, correct graph legend, keyboard adjustment, zero `hooks.applyQuality/Bitrate` calls, retention on threshold-only change, and rejection of unsupported source pixel format without stale fitted curve. It generates desktop (1280px) and mobile (390px) screenshots and verifies no global horizontal overflow. The earlier synthetic line-chart fixture is removed *before* the Manual screenshots, avoiding misleading double-chart evidence.

Frontend Test at exact head `ca7c9261d1e6065e8357aa39149ddbe3a4790670`, run `38274835109`: **SUCCESS**. Independently inspected previous head's desktop and 390px screenshots in this conversation, found misleading inclusion of a separate fixture and visible single-mode controls; fixed both. Latest exact-head browser check is passing; the new screenshots should be reviewed against production materials before merge. Container visual snapshots are not a physical device test.

`src/curve-chart-svg.js` also changed a potentially misleading vertical axis from `平均样本 SSIM` to `短样拟合 SSIM`, because fitted source metric can reflect minimum/worst-window quality rather than literal mean. Test asserts the corrected label.

## Distinct real Native evidence

Windows Manual paired codec acceptance on exact head `ca7c9261d1e6065e8357aa39149ddbe3a4790670`, run `38274835098`: **SUCCESS**. It continues to run 12 real Windows hosted FFmpeg/x264/x265 short-sample encodes with source-backed SSIM, through Native Bridge, receipt validation, session registry and one common evidence-bounded upper envelope, on a synthetic FFV1 source. This is **not** actual end-user interaction against a user film.

Also exact head: Windows Stream Plan v4 runtime acceptance `38274835099` success; UIGS Evidence Coverage `38274835096` success. Windows local smoke `38274835197` was running when this record was authored and must be checked for a full five-workflow claim.

## Open acceptance boundary
The consumer UI's Native transport and Windows backend are independently exercised at controlled levels but the entire browser-to-native user flow is not yet field-accepted on a real Windows workstation. No AV1/GPU, HDR/VFR, long films, measured audio copy total-size budget, field device, hard end-to-end wall-clock cancellation or cross-codec formal VBR adoption has been proven. PR #104 remains draft/unmerged. Do not change Canonical.
