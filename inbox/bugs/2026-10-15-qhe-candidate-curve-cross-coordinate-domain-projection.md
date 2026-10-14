# Bug: Branch candidate fits leak video-payload x coordinates into whole-file budget plot

Date: 2026-10-15
Status: FIX-SUBMITTED / exact-head CI pending
Project: [QHE PR #103](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/103)
Mainline convergence: [#106](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/106)
Candidate fix SHA: `743c437c7b74a3fbd391c0dec8bffd2e239f0188`

## Evidence and narrowed diagnosis
The complete Chromium suite [run 38642019614](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38642019614) failed in the *existing Manual* dual-codec comparison: measured evidence reported completed, but the two `#taskCompareCandidates li` rows were never rendered, even after a 15-second wait. A separate synthetic candidate-curve fixture was isolated to run only after the Manual lifecycle; failure persisted. This ruled out synthetic test DOM contamination and a mere slow render.

Manual's `currentFrontier()` uses `projectWholeFileFrontier()` for whole-file budgets. That function spreads `...frontier` into the projected wrapper, overriding total min/max/evaluate/sampleCurve, but it did **not** override newly introduced `sampleBranchCurves`. This method was therefore inherited with its **video-payload-byte x coordinates**. The graphical `buildSizeFrontierPlot` expects all candidate point targets in the same **whole-file-byte** domain and calls the projected fraction mapping. The mismatch can prevent candidate plot construction before `showResult()` reaches candidate-row publication. Both code paths and exact failure boundary were inspected; full post-fix CI is required to confirm resolution.

## Proposed fix / regression
In `src/whole-file-frontier.js`, define an explicit projected `sampleBranchCurves` callback. Convert each original video point using the same `videoBytesToTarget` projection as existing evidence points, filter against the projected shared range, and avoid exposing the method when the underlying frontier does not support it. `src/whole-file-frontier.test.mjs` adds a two-branch contract proving projected x values use whole-budget coordinates.

Do not 'fix' by removing the candidate list assertion, turning video-byte points into whole-file decisions, or reverting verified product plans. Remain fail-closed if independent Native evidence / task identity is absent.

## Reusable engineering pattern
Whenever a domain wrapper spreads a source object and replaces its primary coordinate system, audit **every inherited plotting, cursor, alternative candidate and sample callback** for coordinate provenance. Sharing a method that silently speaks a different axis creates failures that may surface several downstream UI steps later, not at the projection boundary.

## Deduplication / authority
Searched Foundry for `whole-file-frontier`, candidate curve projection mismatch and cross-coordinate axes; no matching Bug. Related earlier Candidate on one curve and branch comparisons does not record this projected-method leak. Case/Bug only; do not promote Canonical automatically.
