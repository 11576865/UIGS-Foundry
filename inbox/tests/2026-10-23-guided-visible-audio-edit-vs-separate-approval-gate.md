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
