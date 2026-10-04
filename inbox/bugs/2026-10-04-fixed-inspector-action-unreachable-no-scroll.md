# Bug: Fixed inspector blocks can make lower actions unreachable even when tests try performScrollTo

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: mobile UI / inspector layout / Compose testing / progressive disclosure

## Symptom

A tool inspector can render a large fixed-height parameter block above its content list. On smaller viewports, lower controls in that block may fall outside the visible area even though the list below is scrollable.

A Compose UI test may expose the architecture problem as:

`Semantic Node has no parent layout with a Scroll SemanticsAction`

when it calls `performScrollTo()` on one of those lower controls.

## Failure mechanism

The target control is visually below the fold, but it is not actually a descendant of a scrollable layout. The adjacent `LazyColumn` does not make sibling controls scrollable.

Adding `performScrollTo()` in a test cannot repair a production hierarchy that offers no scroll semantics for that node.

## Fix pattern

ASS Workbench Android PR #86 changed the Karaoke FX author block from an always-expanded parameter form to progressive disclosure:

- title + compact summary + Preview / Apply remain visible;
- advanced numeric parameters move behind an explicit “调整参数” expansion;
- the default collapsed surface fits the fixed inspector region;
- instrumentation now asserts the actions are directly displayed instead of pretending the fixed block is scrollable.

## Reusable lesson

When a mobile inspector contains both an always-visible editor header and a separately scrollable content list:

1. budget the non-scrollable header for the smallest supported viewport;
2. keep the primary action reachable without relying on sibling scroll containers;
3. put advanced controls behind progressive disclosure or place the entire inspector in a real scrolling parent;
4. treat `performScrollTo()` failures as possible production-layout evidence, not merely test syntax failures.

## Evidence

- project: `11576865/ASS-Workbench-Android`
- PR: #86
- failing emulator evidence: Android Emulator Regression #450, new Karaoke FX instrumentation test
- repair: compact collapsed FX parameter surface + direct visibility assertions
- deduplication: searched UIGS-Foundry for fixed inspector / no-scroll-semantics / progressive-disclosure equivalents; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
