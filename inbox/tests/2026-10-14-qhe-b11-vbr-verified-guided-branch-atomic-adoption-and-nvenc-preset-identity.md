# Test — Guided frontier branch must not become a formal task before rendered-reference VBR verification

Date: 2026-10-14
Product PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Product exact-head commit: `653c37b0c897544e7faec88f76e669673c51e6b3`
Status: implementation committed; exact-head Node/Windows/Browser external acceptance **Pending**
Affected requirements: B04/B11/B12, partly B15; initial V1 remains incomplete.

## Observed contract gap
Existing Guided RD frontier UI directly changed `selectedCodec` and sometimes `guidedOutputSize` when the user clicked a recommendation. The Guided ASS Native VBR short-window verifier added earlier tested only the already-selected branch. This allowed a fitted CQ recommendation to change the formal selection **without** checking that recommended codec/resolution's actual ASS-rendered VBR output in its source/reference domain.

A separate issue appeared in the prior B11 receipt: actual Guided NVENC production uses preset p7 while the Native receipt copied the general UI preset (often medium). A truthful receipt must describe the **executed** preset.

## New test boundary
1. Clicking the recommendation creates an immutable pending proposal without changing codec, size or formal Native request.
2. Each admission rechecks source/render-reference identity, current shared-budget coordinate, branch identity, proposed VBR bitrate and preset, plus the original selected branch. Changing any invalidates the proposal.
3. Run real two-window Native ASS-rendered FFV1-reference VBR on the **proposed** candidate, not the incumbent; independently check source/runtime/staged ASS digest/font digest/encoder/rate/window/SSIM.
4. Only an explicit user confirmation after a passing certificate may write selection. First compile hypothetical executable plan; then change selected codec/geometry once, compile actual plan, compare executable fields (including video bitrate, byte target and audio costs). On any mismatch restore old codec and geometry; a failed rollback is an explicit failure.
5. Fitted/nonexecuting frontier predictions may vary after incumbent changes. Do not compare whole diagnostic objects as if they were executable task fields.
6. Guided real NVENC preset is p7 (with its Guided VBR flags) even if a UI profile mentions a different preset; Native receipt and JS verifier must check actual executed `p7`. For pure software use the actual requested/fallback software preset.
7. Neither a short-window SSIM pass nor a committed selection is proof of whole-movie quality, strict byte ceiling, two-pass behavior or completed output delivery.

## Evidence
- `src/guided-branch-adoption.js`, `src/guided-branch-adoption.test.mjs`
- `src/main.js`: staged proposal, candidate-specific Native VBR verification, explicit confirmed atomic adoption, resolved candidate container
- `src/guided-native-vbr-verification.js`, `src/guided-native-vbr-verification.test.mjs`: `expectedPreset` proof including NVENC p7
- `windows/native-bridge.ps1`, `windows/guided-rendered-sample-evidence.ps1`, `scripts/check-guided-vbr-evidence.ps1`: true executed preset in receipt and offline fixture correction
- `.github/workflows/test-frontend.yml`: new Node tests in draft-fast and full suite.
- **Bounded local evidence:** 18 retrieved-source JavaScript behavior tests passed in an isolated V8 evaluator; 12 source wiring checks passed and main JS syntax parsed. This is not full Node import, Native or browser acceptance.
- At one immediate workflow read after head update there were no runs yet. Record external CI and actual Windows/FFmpeg/NVENC/browser acceptance as Pending.

## Nonpromotion, dedup
Searches: `Guided recommended codec verified transactional adoption rollback`, `QHE staged branch vbr validation`, `native NVENC preset p7 receipt actual versus requested`, `candidate cannot auto-commit before verification`. Related existing B11 Native rendered-reference Test concerns the evidence source and encoder flag contract, not a user-initiated branch-stage -> verification -> rollback-safe selected-state transition. This is a separate Test/engineering case. Do **not** promote a single implementation observation to Canonical.

## Still open
Native real GPU acceptance, full browser selection/transaction, complete cross-UI Manual/Guided authoritative task compiler and persisted source/parameter identity, resized high-density ASS, two-pass and strict full-file result attestation, all initial version acceptance B01–B25 / A01–A10.
