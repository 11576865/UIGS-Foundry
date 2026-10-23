# Test: visible Guided per-stream editor must not inherit hidden/no-op assertion

Date: 2026-10-23
Status: OBSERVED CI FAILURE / one bounded test repair committed / repaired head CI PENDING
Product: QHE https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/130
Source: `src/media-workspace.js`, `scripts/check-workbench-basic.cjs`, `scripts/check-wu11-guided-mixed-audio-ui.cjs`

## Deduplication and authority

Searched Foundry for `Hidden guided projection cannot alter the audio plan`, explicit Guided exposure and separate approval gate. No matching specific Test. Related existing QHE general Case `inbox/cases/2026-10-13-qhe-report-baseline-cannot-be-replaced-by-scoped-ci-delivery.md` documents integration/real-browser/Native evidence limitations; this Test adds a distinct **observed UI invariant migration failure**, not a proposal to change Canonical.

## Directly observed failure

At QHE PR #130 old exact head `e3c328f49affbf0f48efb9bc7748de9d718d7319`, full frontend [run 39912565784](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39912565784) failed at `check-workbench-basic.cjs:50`:

`AssertionError: Hidden guided projection cannot alter the audio plan`; expected empty form value `''`; observed source-authoritative plan `[{"sourceOrdinal":0,"action":"flac","range":"trim"},{"sourceOrdinal":1,"action":"copy","range":"trim"}]`.

The product intentionally newly exposes the one existing per-stream audio editor in Guided. A real UI change to `.v3-audio-plan [data-audio-field="0"]` now modifies the formal form owner. The old no-op assertion is no longer the intended behavior, whereas its original safety concern remains: **an edit must not implicitly authorize Guided→Manual handoff or launch an executable job**. This failure is test-contract drift upon intentional UI expansion, not proof that real Native encoding failed.

## One bounded repair

QHE repair `2a14d882cb6184d7538b9da1ca2cfc6e474d32b5` replaces the stale negative no-op expectation with direct assertions: selected `flac` must reach the one formal `audioPlan`; `#guidedMixedAudioConfirm` remains unchecked; the task execution count stays 0. It does NOT weaken separate existing negative tests for old source, unknown copied-audio costs, Copy lock or stale VBR proof. A product task checkpoint records the prior head failure and repaired head pending.

## Evidence and limits

On old exact head, 9 of 10 workflows were SUCCESS, including WU01 true Chromium Guided mixed-audio DOM workflow and CPU handoff, Windows smoke and UIGS Coverage; full frontend failed on this old expectation. The post-repair exact-head full frontend and affected workflows were **not yet evaluated** at the time of this intake. Do not claim the repaired PR merged, real user's Windows→Native single session proven, or B02/B04/B11 complete. No Canonical changes.

## 2026-10-23 repaired-generation CI counterexample: omitted owner button in reduced browser fixture

At QHE PR #130 head `1b09c5ac7838febdbaba189f03c0d3068f185423`, full frontend [run 39953246427](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39953246427) still **FAILED** at `check-workbench-basic.cjs:58`, but for a new, concrete reason: Playwright's `locator('#guidedMixedAudioConfirm').isChecked()` timed out after 30 seconds. The reduced `/basic-fixture` had `<section id="planCard"></section>` without the production `#guidedToManual` button. The production implementation creates its approval checkbox only as an accessory to that button, so no checkbox could exist in this reduced fixture. This is **missing required fixture DOM**, not a failed Native backend or proof that the production click is absent in the actual app.

One bounded repair committed to QHE as `ffa1ade0de442a4aa6536b0a9fee570342479a4b`: include the real `#guidedToManual` control in the reduced fixture `#planCard`. Keep the exact assertions that an explicit edit reaches the one formal per-stream owner, that consent remains unchecked, and that no task executed. The change does not alter product runtime or relax preservation/budget gates.

Evidence status: **previous exact-head frontend failure observed / repair committed / repaired exact-head CI PENDING**. The prior Windows smoke, audio lock, task matrix and UIGS successes cannot be substituted for post-repair full frontend. No Canonical promotion.

## 2026-10-23 exact-head third counterexample: shared audio plan contaminates next browser scenario

QHE PR #130 exact head `60d3f7548d185ad9986f8896454c298113510064` full frontend [run 39953955003](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39953955003) **FAILED** at `scripts/check-workbench-basic.cjs:156` on `Full audio is independent of trimmed video`: expected original `expectedAudioDuration=2`, observed `1`. The first Guided scenario now correctly lets the user change the shared formal `audioPlan`; this previously hidden/no-op change persisted into an **independent later Transcode trim scenario**. The later test had assumed global audio settings and thus accidentally used the earlier source-scoped per-track trim strategy. This is an observed **test scenario isolation / shared state persistence** counterexample, not evidence that FFmpeg encoded a source incorrectly. The audio-duration contract should not be weakened to expect 1 second.

One bounded repair commit `6779608fb04b6aaf6ce1c517fbd681e8cdf75c7a`: immediately after testing explicit Guided plan modification does not auto-authorize or run, click the **production** `恢复全局音频策略` control in the same Chromium DOM to clear audioPlan and mustCopyAudioOrdinals. Assert both empty, approval still unchecked and zero execution, *then* enter separate Copy/Transcode cases and retain the original `expectedAudioDuration=2` check. This is explicit cleanup, not fabricated browser behavior or suppressed assertion.

Status: fixed PR branch committed; post-repair exact-head CI pending and **PR #130 not yet merged**. Prevent accidental generalization: this finding suggests scenario cleanup when a new UI affordance intentionally persists shared form state; it does not by itself establish a cross-project Canonical rule.

## 2026-10-23 fourth exact-head CI counterexample: reset control exists but is not user-visible in Guided

QHE PR #130 exact head `47fddd33ae4012ce94fe9594e70b56d3c1b9ab13` full frontend [run 39970406401](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39970406401) **FAIL**, again in `check-workbench-basic.cjs:64`. Playwright resolved `details.media-audio-plan>summary` but could not click: the original form-owned underlying `<details>` was not visible in the Guided visual projection. The test tried to reset the user-explicit Guided audio edit through the *hidden owner node*, not the user-accessible V3 audio projection. Nine other targeted workflows were SUCCESS on the failing head (including real-browser WU01, Windows local smoke, UIGS).

Repair `e9e74295f12b37854ce12c51b04b0e5677f51726` preserves the change's effect and no-auto-approval assertions in Guided, then switches to Transcode and uses the **visible** `.v3-audio-plan>summary` / `[data-audio-reset]` control to reset the single authoritative form plan before the following unrelated copy/transcode cases. It checks empty `audioPlan` and Copy lock, no approval and no executed task, while preserving the independent 2s-audio-duration versus 1s-trim assertion. This distinguishes **DOM existence** from **user visibility/operability**: tests must use a visible projection when the data owner is intentionally hidden.

Repair exact-head external CI remains **PENDING**; no automatic promotion to product-complete or Canonical. This extends the same Test rather than creating a duplicate.

## 2026-10-23: cancelled browser validation before any browser assertion is not a failing app regression

At QHE PR #130 head `f61060e10b01f94adfd1c70c0acd204cb129ca07`, exact-head **full frontend SUCCESS** [run 39971653592](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39971653592), as were Windows smoke, WU03–WU08 targeted suites and UIGS coverage. The WU01 real CPU/FFmpeg handoff subjob passed. But WU01 [run 39971653418](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39971653418) ended **CANCELLED**, because `real-browser-handoff` spent its 15-minute cap installing Playwright Chromium system dependencies from a slow Ubuntu/Azure apt mirror (the log was still downloading font packages). No actual Guided UI click/compilation test executed on that job attempt.

GitHub's `rerun_workflow_job` accepted a **single cancelled job retry** on the exact same source commit, with new browser job `120487899714` initially QUEUED and CPU success retained. The product PR stayed **unmerged**, as required by the exact-head gate. Recovery evidence is also stored in PR #130 comment `6367999143`; no product commit was added that would invalidate successful exact-head checks.

Generalizable, limited test interpretation: distinguish **setup-phase CANCELLED/TIMEOUT** from an application assertion failure and from a verified test PASS; use the job's last reached step and relevant external apt/download evidence, rather than inferring product state from the whole workflow badge. This remains a specific Test observation with external validation pending, not a Canonical change.
