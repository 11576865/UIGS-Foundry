# Test — Guided ASS native exact VBR must use the rendered reference and formal encoder flags

Date: 2026-10-14
State: QHE PR #105 code submitted; real Windows Native/Node exact-head CI Pending
Product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `9763eb9edad6d8c65724a17db3f81516297b430d`
Requirements: B04/B11/B12/B13/B15; all remain partly open.

## Newly isolated failure mechanism

An exact bitrate short sample that reuses *Manual source-only* SSIM against a Guided ASS encode (or that reuses Manual's different NVENC VBR parameters) is NOT evidence about the formal Guided ASS rendering/encoding plan. Even the same source scene timestamps and codec do not repair the incompatible quality reference/parameter contract.

### Test contract
- Windows Native must require the combined opt-in `sampleExact`, `guidedRenderedReference`, `withSubtitles`, `measureSsim` and positive bitrate, and reject mixed Manual/Guided flags.
- Build a subtitle-rendered FFV1 sample from the **same staged ASS and selected fonts**, rather than compare to the unfiltered source. Compare actual encoded VBR video against this reference by SSIM, including bicubic upsampling where the full Guided output uses a smaller output size.
- Match existing formal **Guided** single-pass encoder settings, not Manual exact VBR flags: Windows NVENC Guided p7 + tune + vbr + maxrate + bufsize, or software chosen preset + b:v.
- Receipt validates source and runtime stat identity before/after Native work and staged ASS UTF-8 SHA-256 and selected font content digest before/after; context: receipt SHA is a fingerprint of staged files, *not* all possible libass/system font fallback behavior, and cannot prove unchanged source bytes when file stat metadata is forged.
- Frontend independently hashes the exact shifted ASS sent for each window, validates that digest, pairwise Native font hash/source/runtime identity, encoder, preset request, bitrate, duration/position, video packet bytes, SSIM, and the **Guided rendered reference domain**.
- Admission is short-window only. A user must explicitly confirm a passing receipt on the **current** Guided plan; confirmation does not auto-change an encoder/bitrate, grant a strict byte ceiling, certify two-pass operation, or prove a whole-movie SSIM.

### Code and bounded tests
- `windows/guided-rendered-sample-evidence.ps1`, `windows/native-bridge.ps1`, `src/guided-native-vbr-verification.js`, `src/main.js`.
- `src/guided-native-vbr-verification.test.mjs`: 8 source-equivalent isolated V8 behavioral tests passed; missing/mismatched receipt, source drift, wrong reference, fonts, geometry, windows, threshold and strict/two-pass rejection all covered. Main JS syntax was parsed in V8; NOT a full Node/Browser runtime pass.
- `scripts/check-guided-vbr-evidence.ps1`: independent Windows PowerShell staged-ASS/font/source mutation tests.
- `scripts/check-guided-budget-native.ps1`: existing Windows localhost synthetic actual-FFmpeg smoke extended with **two real Guided ASS VBR samples** and an independently SHA-256-hashed reference. It is newly authored but hosted execution is Pending.
- Draft-fast/full frontend and Windows local smoke workflows wired to these checks; after the one immediate PR-head workflow query no run was yet recorded, therefore **Pending External Validation**, not PASS.

### Dedup and promotion rules
Existing `inbox/tests/2026-10-14-qhe-b11-guided-ass-rendered-quality-evidence-invalidation.md` addresses stale render state *between* calibrations and usage. Existing `inbox/tests/2026-10-14-qhe-b15-manual-guided-shared-paired-risk-windows.md` addresses shared *sample position* but incompatible reference domains. This is a distinct native encoder+rendered-reference+asset-digest *receipt validation* case. No automatic Canonical promotion; no complete B11/full theoretical initial version claim.

### Pending field acceptance
Exact-head Node/build; Windows hosted PowerShell syntax, offline receipt mutation oracle and actual FFmpeg 2-window Native localhost run; real user ASS+fonts, high density, scaled output, hardware NVENC, audio/full-budget formal output, Android/browser, long-form and physical playback evidence. Full Guided/Manual shared branch transaction and final-file gates remain incomplete.
