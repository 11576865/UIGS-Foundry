# Bug: Browser E2E referenced selectors that were never part of the production UI contract

Date: 2026-10-06
Status: Bug
Lifecycle: validation-pending
Scope: browser E2E / UI contract / selector ownership / integration tests

## Symptom

Quick-Automatic-Hardsub-Encoder PR #65 added a Browser E2E case for the Stream Plan v4 UI → task boundary.

The frontend/unit/integration suites passed, but the Browser E2E step failed with a 30-second Playwright timeout while waiting for:

`#taskPlanStreams`

The same test also referenced:

`#taskPlanRange`

Neither selector exists in the production media workspace.

## Actual production contract

The current plan summary already exposes the same user-visible semantics through existing nodes:

- `#taskPlanOutput` contains the selected video-stream summary;
- `#taskPlanNote` contains independent video/audio range policy.

Production code renders, for example:

- `视频 #0 / #1` in `#taskPlanOutput`;
- `视频IN/OUT · 音频完整` in `#taskPlanNote`.

The E2E test invented more specific selector names instead of asserting against the current production contract.

## Failure mechanism

The product behavior under test was present, but the test encoded a DOM contract that the product never declared.

This converts a useful integration test into a false red:

`valid product behavior -> fictional selector -> locator timeout -> CI failure`

The failure therefore does not establish that Stream Plan v4 lost UI → task wiring.

## Repair submitted

PR #65 commit `a63c7b32921b13e7cb33fce01aef8defe7bbe547` changes the E2E assertions to:

- read stream selection from `#taskPlanOutput`;
- read independent range semantics from `#taskPlanNote`;
- keep the stronger task-object assertions unchanged.

Fresh CI is pending at intake time.

## Reusable lesson

End-to-end tests should assert against **existing production-owned UI contracts**, not selectors invented solely for the test.

When a test needs a more specific machine-readable surface, either:

1. use an already stable production selector/state;
2. explicitly add a production test hook/semantic contract as part of the feature;
3. or assert the resulting task/state directly.

A locator timeout on a nonexistent selector must be classified as a test-contract defect before it is treated as a product regression.

## Evidence boundary

This is one concrete Browser E2E defect with a submitted repair. It is Bug evidence, not a Canonical rule.

## Provenance

- project: `11576865/Quick-Automatic-Hardsub-Encoder`
- PR: #65
- failing run: Test frontend #326 / run 37318417780
- failing job: frontend / job 111790956162
- repair revision: `a63c7b32921b13e7cb33fce01aef8defe7bbe547`
- deduplication: Foundry search for stale/nonexistent Playwright selectors and UI-contract equivalents returned no direct match
