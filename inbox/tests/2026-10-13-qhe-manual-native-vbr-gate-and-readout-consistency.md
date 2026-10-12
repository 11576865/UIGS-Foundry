# Test: QHE Manual multicodec recommendation VBR confirmation, source receipts and UI state consistency

Date: 2026-10-13 (Asia/Shanghai)
Status: **Test / draft evidence**, exact final-head all-workflow CI checkpoint pending when written
QHE draft PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
Distinct from: `inbox/tests/2026-10-12-qhe-native-bridge-paired-x264-x265-comparison.md` (actual x264/x265 CQ), `inbox/tests/2026-10-13-qhe-manual-comparison-one-chart-browser-and-native-separation.md` (UI comparison without VBR).

## New implementation to verify
- `src/manual-transcode-vbr-verification.js` checks all paired short windows with real Windows Native `windows-native-exact-vbr-v1` receipts. CQ receipts cannot be repackaged as VBR; checks full source/runtime/SSIM-reference/filter identity, actual codec/encoder/preset, disabled multipass, exact requested bitrate and window, complete unique samples and finite quality/video byte observations.
- `src/manual-transcode-compare-ui.js` adds an **explicit, read-only** `实测验证当前推荐编码器的 VBR` action at the currently selected video-only budget. Validates the matching formal bitrate-mode task and real Native candidate capability before sampling. A successful verification shows minimum window SSIM and measured mean bitrate but **does not call task apply/encoder switch hooks**. Failures, source/reference drift, target SSIM changes and graph-budget changes revoke the old pass; a Native provenance conflict also invalidates the earlier CQ session.
- The chart-level readout and status text reflect the same current VBR certificate. A prior browser capture exposed contradictory text (top said VBR passed, chart said unverified); fixed with certificate identity bound to selected bytes, codec branch, target, requested bitrate and source key, and a browser keyboard-movement regression.
- Separate model/unit tests `src/manual-transcode-vbr-verification.test.mjs`, wired into `.github/workflows/test-frontend.yml`.
- Browser Chromium integration `scripts/check-curve-design.cjs` uses **mocked Native transport** to check actual UI behavior. A first browser test run failed because the simulated receipt omitted `multipass`; the simulated data was corrected, not the strict validation.
- Actual Windows Bridge CI `scripts/check-manual-native-paired.ps1` now executes 12 real CQ trial encodes (x264/x265) **plus two real x264 bitrate-mode encodes** using 600 kbps and identical 1.5-second source windows on one generated synthetic FFV1 source, then `scripts/verify-manual-native-paired.mjs` admits the returned bitrate-mode receipts via the same VBR module. This checks actual FFmpeg execution, not only a fake result.

## Already observed Windows real-media evidence
Previous exact PR head `e5dc43ec1a30e2d66db69a0b441b294fdc6f2b5b`, Windows Manual paired codec workflow `38277777275` SUCCESS:
- Two real VBR samples at 600,000 bps requested, source-backed per-window SSIM around 0.99926 and 0.99924; summary minimum approximately **0.99923** (do not infer these values for arbitrary media).
- Proposed test SSIM target 0.90 passed. Full-length mux output filesize, physical GPU, audio preservation and actual formal task adoption **not tested**.
- Frontend CI `38277777273` SUCCESS after correcting the mocked receipt; Windows Stream Plan v4 acceptance `38277777278` SUCCESS; UIGS coverage `38277777318` SUCCESS. The latest UI consistency fix was made later and requires a new final-head rerun.

## Acceptance boundaries
No hidden auto-switch, no automatic adoption of recommended bitrate/codec, no final-size guarantee. The VBR pass attests only the two short measured windows at declared rate, not CQ/VBR equivalence or long-video quality. A subsequent explicit, **atomic codec+encoder+preset+rateMode+bitrate handoff** with final task validation and independent encoded-artifact verification remains necessary before presenting the workflow as complete. Keep Candidate/Test, not Canonical; PR #104 stays draft/unmerged pending owner and device review.


## Final exact-head verification checkpoint (after readout-certificate fix)

QHE draft PR #104 SHA `c2f3cbf638aa30caf540aadd468bf5a8c8113bdd`, all five workflows completed **SUCCESS**:
- Test frontend `38278213258`: Node native VBR admission tests; Playwright real Manual UI with mocked Native transport; one shared SVG, explicit VBR verification action, no `applyQuality`/`applyBitrate` invocation, consistent after-pass readout, and revoked pass after keyboard budget movement.
- Windows Manual paired codec acceptance `38278213526`: 12 **real** x264/x265 FFmpeg CQ samples plus two **real** x264 VBR samples and Native receipt validation on one FFV1 synthetic source. At requested 600000bps and test threshold .90, VBR SSIM summary minimum approximately .99923 (fixture-specific).
- Windows local smoke `38278213254`, Windows Stream Plan v4 `38278213362`, UIGS Evidence Coverage `38278213284`: all success.
- Frontend artifact `11759389135` included standalone 1280px desktop and 390px mobile Manual comparison screenshots. Both independently visually reviewed in this conversation: the former contradictory chart/status VBR state is corrected; there is one chart, visible candidate text and no global horizontal overflow. These are browser-mocked data screenshots, not Windows physical-user transcoding evidence.

This record's CI status is **complete**. Candidate adoption/whole-file validation is still **pending**; PR remains Draft/unmerged.
