# Bug: Infinite canvas surfaces can remain viewport-clamped under a bounded Compose parent

Date: 2026-10-04
Status: Bug / fix submitted, CI validation pending
Source: 11576865/ASS-Workbench-Android PR #88

## Symptom

The infinite-canvas instrumentation test created a world-space surface with width 900 dp on a phone viewport. At emulator density, the expected measured width was 2362 px, but the semantics layout width was exactly 1080 px: the physical viewport width.

This proved that the surface was still inheriting a bounded parent measurement constraint even though its geometry model allowed larger world-space sizes.

## Root cause

A child surface using `requiredSize(...)` / `wrapContentSize(unbounded = true)` is not sufficient if the direct world container itself measures children under viewport-bounded constraints. Overflow may render conceptually outside the viewport, but the child's measured layout contract can still collapse to the viewport bound.

For a true spatial workspace, clipping and measurement are separate concerns.

## Fix pattern

Use a finite viewport layer that clips presentation, with an inner world layout that measures direct surface children using unbounded max constraints:

- viewport remains finite and clips drawing;
- world layer reports the viewport size to its parent;
- world surfaces are measured with `Constraints.Infinity` for width/height;
- camera transform / offsets decide what portion is visible;
- surface geometry is therefore not silently rewritten or measured down to viewport dimensions.

PR #88 fix commit: `bcd09b9fab4d998ea0b2d711b6f951ae2ee6a553`.

## Regression invariant

A world-space surface wider than the physical viewport must retain its requested measured size. The viewport may clip it visually, but must not force the surface measurement to equal the viewport width.

The instrumentation test `InfiniteCanvasInstrumentedTest.surfaceMeasurementIsNotClampedToThePhoneViewport` is the current regression gate.

## Evidence boundary

The initial failure is confirmed by Android Emulator Regression: expected 2362 px, measured 1080 px.

The fix has been submitted but its replacement CI run is still pending at the time of this record. Do not promote to Canonical until the regression is green and the behavior is validated in the integrated spatial workspace.
