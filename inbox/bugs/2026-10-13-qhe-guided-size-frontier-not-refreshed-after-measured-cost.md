# Bug: QHE Guided size frontier can keep an obsolete auxiliary-cost coordinate after source measurement

Date: 2026-10-13
Status: Source-inspection observation; fix committed in draft QHE PR #105; latest exact-head UI/Native acceptance pending
Domain: QHE / shared task workbench / decision projection / state invalidation

## Observed boundary
QHE Guided ASS's size curve originally used an estimated audio bitrate and fixed reserves, whereas Manual already used measured per-stream packet costs and the authoritative whole-file ledger. QHE commit `90f4162dfd23e93e527ca601f1c92eb2720d53ad` connects Guided's projected size frontier to the existing `wholeFileLedger` and `projectWholeFileFrontier` where copied-packet evidence is available; otherwise copy costs remain labelled estimates.

Source inspection of that continuation exposed a second, distinct lifecycle gap: Manual's `#taskMeasureBudget` updates private `budgetEvidence` and invalidates Manual transcode curves, but did not notify Guided to re-render its own already-shown budget coordinates. Thus the display could remain on a premeasurement estimate even after the source-owned ledger was available, until another Guided interaction caused a refresh. This is an inferred UI effect from the event chain, not an observed physical-device screenshot.

## Correction in QHE
- `2f730325f618648d6d3acd0e654b699037741304`: add `onBudgetEvidenceChange` callback from the shared workbench on measurement completion/failure and media source updates; Guided recomputes the size preview and plan from current evidence.
- New `src/guided-budget-ui-wiring.test.mjs` verifies notification wiring; new test added to `.github/workflows/test-frontend.yml`.
- Evidence stays source-identity-scoped. Reprojection must not be called new CQ/SSIM measurement or a final-byte verification.
- Prior QHE commit `90f4162`: three pure whole-file projection tests passed in hosted frontend run `38410971561`. The later refresh commit has a separate exact-head CI run and remains subject to its own status.

## Reusable engineering rule (provisional)
When an input measurement changes an authoritative resource-cost ledger, notify every dependent decision projection/view, not only the measurement-owning panel. Preserve still-compatible raw video measurements; invalidate derived certification/adoption when its budget inputs change. Treat source changes as cost-provenance invalidation rather than silently retaining prior measured costs.

## Dedup
Related but not duplicate: `inbox/candidates/2026-10-10-measurement-identity-must-exclude-decision-and-presentation-inputs.md` separates raw measurement identity from budget projection; `inbox/observations/2026-10-13-qhe-guided-manual-intent-handoff.md` covers explicit intent handoff. This Bug records the concrete cross-view notification omission and bounded correction.
No Canonical change or full initial-version acceptance. End-user browser, Windows Native, long-form and physical device checks remain independent.

## Additional dependency invalidation: user audio edits and restored configurations (2026-10-13)

QHE PR #105 continuation identified the same cross-view invalidation failure for a *different trigger*: Manual form `invalidateCompiledPlan` did not notify Guided when audio strategy, selected track, audio range, bitrate, channels, sample rate or audioPlan changed; `applyConfig` silently changed these inputs too. Source measurement itself could remain valid, but Guided's derived whole-file video bitrate / size projection needed recomputation.

Corrections: QHE `0a4f08ab58a50af65f9435fb892fd5d6364e137e` adds the notification after audio-field invalidation and configuration application. `a41be90e8067826735a2dc7b7a2dcb5591ef5ac8` adds a wiring regression. `deae2bf` / `ee9ab66` extend the production-workspace Chromium fixture to dispatch real DOM audio edits and click configuration restore, asserting notification and no encode side effects. Exact-head hosted CI is pending at the time of intake; do not claim a browser PASS until observed.

Dedup: extend this existing Bug rather than creating a second cross-view refresh Bug. The general rule applies whenever a derived decision projection depends on mutable, user-owned auxiliary inputs—not only on measured-evidence arrival.
