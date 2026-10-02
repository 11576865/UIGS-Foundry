# Candidate: Re-enter semantic navigation context after adaptive layout transitions in UI regressions

Status: candidate
Date: 2026-10-03
Domains: reliability, interface-grammar

## Summary

After a responsive/adaptive layout transition, an instrumentation test must not assume that the same descendant Surface remains composed even when the underlying domain object and draft state are intact.

Re-establish the navigation context through a stable semantic entry point, wait for the target descendant to enter the semantics tree, and only then perform scroll/click actions.

## Evidence

ASS-Workbench-Android's `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation` exercises a draft through orientation change plus temporary `wm size` / `wm density` overrides.

An Emulator run for UI Contract Slice D failed after resetting the viewport:

```
Action performScrollTo() failed.
Expected exactly '1' node ... TestTag = 'event-row-1'
```

The product invariant was not shown to be broken. The compact adaptive workspace can legitimately settle on either its list page or its inspector page after the viewport reset. When it settles on the inspector page, `event-row-1` is not composed, so directly calling `performScrollTo()` targets a nonexistent descendant.

PR #79 changes the regression flow to:

1. inspect the stable `fixed-page-list` navigation action;
2. activate it when present;
3. wait semantically for `event-row-1` to exist;
4. only then scroll/click the row and continue the draft-persistence assertion.

No fixed sleep is added and product code is unchanged.

## Candidate rule

For UI tests that cross orientation, window-size, density, keyboard, split-window, foldable, or other adaptive projection changes:

- treat the post-transition presentation/page as non-deterministic unless that exact page is the behavior under test;
- navigate using a stable action identity before locating descendants that may be conditionally composed;
- synchronize on descendant existence/readiness rather than attempting scroll/click first;
- distinguish “target not currently composed” from “canonical/domain object disappeared”;
- do not solve projection uncertainty with longer arbitrary sleeps.

## Relationship to existing Foundry knowledge

This is distinct from `Stable Action Identity for UI Regressions`: that candidate addresses *which node identity* a test should target. This candidate addresses *re-establishing the correct adaptive navigation context* before that node can exist.

It also complements presentation-isolation / semantic-completion guidance: the completion condition here is the target descendant becoming available after an explicitly restored presentation context.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- observed workflow: Android Emulator Regression run `37019948521` on PR #77
- failing test: `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation`
- repair PR: `#79`
- repair commit: `972d337ccc8a898c0256117e2111be296fdb4ef2`
- evidence level: emulator failure + implementation fix under CI validation

This is a Candidate only. It does not modify Canonical guidance.
