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
