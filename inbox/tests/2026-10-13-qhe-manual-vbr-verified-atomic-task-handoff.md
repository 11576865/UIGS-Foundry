# Test: QHE Manual selected-codec VBR certificate → explicit atomic formal task handoff

Date: 2026-10-13 (Asia/Shanghai)
Status: **PASS in exact-head CI**, Draft PR, no real user-field or whole-file acceptance
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
Exact tested QHE head: `089bb6b3101a50d267fb92a3450ced3a8d314025`
Related Foundry Candidate: `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`
Prior distinct Test: `inbox/tests/2026-10-13-qhe-manual-native-vbr-gate-and-readout-consistency.md` (short-window VBR pass; **no form task handoff**)

## Purpose / novel acceptance boundary

Previous work could measure cross-codec CQ candidates, generate a single common-envelope chart and validate a chosen candidate in Native VBR mode, but **explicit formal codec+rate task adoption remained unimplemented**. This follow-up builds a guarded, synchronous transaction for the *one existing formal Manual form*, not a parallel task editor.

## Implementation under test

- `src/manual-transcode-adoption.js::commitVerifiedManualCandidate` takes one already approved H264/libx264 or H265/libx265 candidate, positive integer video bitrate, exact pre-adoption form state and source identity. Synchronously snapshots codec, encoder, preset, NVENC multipass setting, rateMode, bitrate, twoPass; rebuilds dependent select options, sets the candidate atomically, checks actual readback and recompiles the *real formal media task*. If any phase fails, it restores the previous controls and does not publish a partial changed-form event.
- `src/media-workspace.js` owns the authoritative form and emits **one** `input` event after the entire transaction succeeds, allowing existing compiled-plan invalidation/stale-artifact tracking to consume coherent final settings. There is no secondary mutable source of truth.
- `src/manual-transcode-compare-ui.js` exposes `确认写入已验证的编码方案` only after a **still-current, passed, source/runtime/reference/selected-budget/target-bound Native short-window VBR certificate**. Clicking explicitly recompiles the full formal bitrate-mode task, rechecks encoder capability asynchronously, then checks that the source, form, target and chosen budget are unchanged **after** the await. On success it invokes the atomic form method and discards the old comparison session; it does not encode or assert output correctness.
- Changing the selected video budget or SSIM threshold, or source/form identity, hides/revokes the confirm control and invalidates the former pass. CQ interpolation alone cannot enable it.

## Test cases and evidence

`src/manual-transcode-adoption.test.mjs` checks: correct atomic H265 codec+encoder+preset+bitrate-mode handoff; true rollback after injected formal compiler failure; refusal of changed source/form, invalid codec/encoder/rate, simulated encoder-selection failure with previous settings restored. A separate real `compileTask` integration confirms actual v4 HEVC target-bitrate command compilation at 850,000 bit/s.

Chromium browser test `scripts/check-curve-design.cjs` drives the real optional one-chart Manual UI with **mocked Native transport**: before explicit confirm, no form adoption hook is called; budget-keyboard movement hides confirm and revokes VBR pass; after new complete CQ/VBR confirmation, clicking the explicit button invokes adoption exactly once, switches mode from comparison, and updates the mocked authoritative task fields. This does NOT demonstrate an actual user physical Windows UI+Bridge end-to-end run.

Independent Windows hosted codec path still tests **12 real x264/x265 CQ samples + two real x264 VBR samples** from a generated FFV1 short source, same windows and Native identities. No production long-video output file is encoded by the new handoff unit test.

## Exact-head CI / outcome

QHE head `089bb6b3101a50d267fb92a3450ced3a8d314025`, all five success:
- Frontend/Chromium `38282698714`;
- Windows Manual paired-codec & VBR `38282698440`;
- Windows local smoke `38282698510`;
- Windows Stream Plan v4 runtime acceptance `38282698376`;
- UIGS Evidence Coverage `38282698373`.

The first new frontend run was red from a *test-double discrepancy*: a plain JS object did not implement HTML select option rejection. The fixture was changed to simulate encoder-option rebuild throwing on unsupported codec; production rollback guard was not loosened. Final exact-head tests passed.

Browser screenshot artifact `11762236020` was downloaded and visually checked at 390px; the UI shows one size-quality chart, VBR passing status consistent with readout and a separate explicit confirmation button. Visual image data comes from mocked Native transport, not the physical user machine.

## Non-claims and residual risk

Passing VBR on two CI short windows **does not** establish user-film quality, full-file output bytes, audio copy preservation, packaging/playback compatibility, HDR/VFR, hardware acceleration or AV1 behavior. Formal artifact encoding, independent full-output probe/packet/quality verification and Windows field-device user workflow acceptance are outstanding. User owner review and PR merge are still pending. This is Test/Candidate; **do not promote to Canonical**.
