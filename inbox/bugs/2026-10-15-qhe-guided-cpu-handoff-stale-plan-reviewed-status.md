# Bug: QHE Guided→Manual handoff falsely marks an unvalidated plan as checked

Date: 2026-10-15
Status: **FIX-SUBMITTED / exact-head Chromium confirmation Pending**
Project: [QHE PR #105](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105)
Tracking: [QHE Mainline Convergence #106](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/106)
Code fix SHA: `b7b27740cf02d3bc7aceb802a242cca4c5e6d4cf` (later integration HEAD also includes this change)

## Symptom and reproduction
Real production workspace mounted by `scripts/check-whole-budget-ui.cjs`, in the full Chromium `Test frontend` run `38638032330`, fails at the immediate post-handoff `data-plan-checked` assertion:
- Before handoff, source/plan has a reviewed task;
- `#guidedToManual` copies new Guided CPU parameters into authoritative Manual form;
- Status text correctly says the CPU plan requires re-verification and ASS/VBR sample receipts do not transfer;
- **But the plan review still displays checked** (`true`, expected `false`).

## Cause
`src/media-workspace.js` calls `compileGuidedCpuHandoff` and `commitGuidedCpuHandoff` (safe proposal/readback compile), then sets `currentPlanTask=applied.task` and calls `syncTaskReview()`. The review model treats a populated `currentPlanTask` as independently checked although the authoritative `prepare() + hooks.validate()` preflight for the changed Manual parameters has not run. This promotes a compilation/projection fact into a stronger verification claim.

## Correction and required evidence
At `b7b27740`, the handoff continues to preserve applied form fields, compiled task preview, policy and nontransferred evidence warnings, but sets `currentPlanTask=null` before `syncTaskReview()`. Re-checking the plan through `#taskInspect` still follows the normal preparation and validation gate. The existing Chromium script asserts `data-plan-checked=false` immediately after handoff, then `true` after explicit inspection.

**Do not declare the fix accepted until the new exact-head full browser CI passes.** Native output and field device acceptance remain separately scoped.

## Generalizable failure mode
A projected or compiled task is not necessarily a validated task. If review badges are derived from an object whose presence conflates “compiled” with “passed independent preflight”, cross-view/plan handoffs can present a stale-success state. Derive visible assurance from an explicit proof receipt bound to the current task identity/revision, not merely a non-null plan.

## Deduplication / governance
Search terms: QHE `currentPlanTask`, `data-plan-checked`, stale review handoff, compiled versus independently validated. Existing Foundry records on Guided VBR adoption and source-selection invalidation are adjacent, but do not describe this exact review-state overclaim. Keep this as a Bug/Case candidate; no automatic Canonical modification.
