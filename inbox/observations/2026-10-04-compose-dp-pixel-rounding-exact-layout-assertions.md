# Observation: Exact UI pixel assertions must mirror framework unit-conversion rounding

Date: 2026-10-04
Status: Observation
Source: 11576865/ASS-Workbench-Android PR #88, Android Emulator Regression run 37142645921

## Trigger

After the infinite-canvas viewport-clamp bug was fixed, the regression no longer measured the surface at the phone viewport width. Instead, the only remaining failure was:

- requested world-space width: 900 dp;
- test expectation: 2362 px;
- Compose semantics measured width: 2363 px.

The test computed the expected width with:

```kotlin
(900f * density).toInt()
```

which truncates fractional pixels. Compose's dp-to-pixel layout conversion rounds to the nearest integer pixel.

## Observation

When an instrumentation test asserts an exact measured pixel size derived from dp, it should use the same rounding semantics as the UI framework rather than an ad-hoc truncation rule.

For positive Compose dp values, a suitable equivalent is:

```kotlin
(900f * density).roundToInt()
```

or the framework's own dp-to-pixel conversion helper where practical.

A one-pixel discrepancy caused solely by mismatched unit-conversion rounding is a test-contract error, not evidence that the production layout is still viewport-clamped.

## Scope

This observation is about exact layout assertions that cross logical-unit and physical-pixel domains. It does not justify adding broad tolerances to tests that should be exact, and it does not weaken the underlying invariant that a world-space surface may measure wider than the viewport.

## Evidence boundary

This is currently a single Compose/Android case. Record as Observation only; do not promote to Canonical without repeated evidence across projects or frameworks.
