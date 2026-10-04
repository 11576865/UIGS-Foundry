# Observation: Treat Android Emulator device-offline failures as infrastructure evidence before editing product code

Date: 2026-10-04
Status: Observation
Domains: Android, instrumentation, CI diagnostics, emulator reliability
Source: 11576865/ASS-Workbench-Android PR #95, Android Emulator Regression run #482

## Trigger

A branch with a successful Android CI run failed its emulator regression after only two instrumentation tests executed.

The failing XML reported an empty failure body for an existing, unrelated test:

- `EditorRegressionInstrumentedTest.groupedNavigationAndGeometrySectionsPreserveDocument`

The job tail then reported:

- `adb: device offline`
- uninstall failure for the test package
- only a partial instrumentation result set

The new PR-specific batch-Karaoke instrumentation test had not yet executed.

## Observation

When an Android instrumentation run terminates with an empty or non-diagnostic test failure, a partial suite, and an explicit `adb: device offline` / emulator teardown failure, the evidence does not yet localize the fault to product code.

Editing production or test semantics immediately would risk reacting to infrastructure noise.

A safer first response is:

1. separate the failing test identity from the infrastructure termination evidence;
2. check whether the changed feature's tests actually executed;
3. verify whether the emulator/device became unavailable;
4. re-run the failed emulator job unchanged before changing code;
5. only treat the failure as product evidence if it reproduces with a healthy device or yields a deterministic assertion/stack trace.

## Evidence boundary

This is a single observed CI incident. It does not establish that all `device offline` failures are harmless, nor that the named existing test is always flaky.

The observation only supports an evidence-ordering rule: infrastructure loss plus incomplete diagnostics should be reproduced before product code is modified.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #95
- branch revision: `56284433f18016d4ba58fab3aeecec1cd9205c7e`
- Android CI #857: success
- Emulator Regression #482: failure with partial suite + `adb: device offline`
- action taken: rerun the failed emulator job without code changes
- deduplication: searched UIGS-Foundry for Android Emulator / device-offline / connectedDebugAndroidTest infrastructure guidance; no direct duplicate found

This remains an Observation. It is not Canonical.


## Refinement — unrelated existing UI failure with empty diagnostics

A later ASS Workbench Android case broadens the evidence pattern without removing the original device-offline condition.

PR #127 (Position XY projection) had Android CI and Fontconfig green while Android Emulator Regression #608 failed. The instrumentation XML contained 15 executed tests, with one failure in the pre-existing `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation`. Its `<failure></failure>` body was empty. The PR-specific `WorkspacePositionProjectionInstrumentedTest` did not execute in that run.

There was no deterministic assertion/stack trace localizing the failure to the Position XY change. Therefore the first action remained an unchanged rerun of the failed emulator job rather than product-code mutation.

Refined triage rule:

- identify the exact failing test and whether it belongs to the changed feature;
- inspect whether the feature-specific connected test actually executed;
- distinguish a non-diagnostic existing-test failure from deterministic feature evidence;
- rerun unchanged when the failure is empty/non-localized and the changed feature was not exercised;
- mutate product or test semantics only after a healthy rerun reproduces a deterministic, attributable failure.

This refinement does **not** assert that every unrelated or empty test failure is infrastructure noise. Reproduction on a healthy device still overrides the provisional classification.

Evidence:
- project: `11576865/ASS-Workbench-Android`
- PR: #127
- failing workflow: Android Emulator Regression #608
- existing failing test: `inspectorDraftSurvivesToolSwitchAndRotation`
- PR-specific connected test did not execute
- action: rerun failed emulator job unchanged
