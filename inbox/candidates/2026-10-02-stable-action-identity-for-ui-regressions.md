# Candidate: Instrumentation tests should target stable action identity, not localized display text

Status: candidate
Date: 2026-10-02
Domains: reliability, interface-grammar

## Summary

For UI regression tests, the locator for a semantic action should be tied to the action/object identity (for example a stable test tag) rather than localized visible text or incidental merged-semantics structure.

Visible labels are presentation content. They may change with localization, conflict state, copy editing, layout composition, or semantics merging even when the actionable control and product behavior are unchanged.

## Evidence

ASS-Workbench-Android repeatedly observed the same Emulator regression around the Event text apply action:

```
Action performScrollTo() failed
Text contains '应用正文'
merged tree: 0
unmerged tree: 1
```

The product control remained present, but the regression located it by Chinese label. The same button may also display `以草稿覆盖` when an external conflict exists, making the label even less suitable as stable identity.

PR #66 changes the actual actionable Button to expose `event-apply-text-{eventId}` and updates four draft/lifecycle regressions to target that identity. Product commit semantics are unchanged.

## Candidate rule

For durable UI regression locators:

1. Prefer a stable identifier attached to the actionable control itself.
2. Include object identity in the identifier when multiple instances of the action can coexist.
3. Do not use localized copy as the primary locator for a product invariant.
4. Do not treat `useUnmergedTree` or longer waits as substitutes for a missing semantic identity.
5. Keep visible-text assertions for copy/accessibility validation, separate from action targeting.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- reproducing PR/run: `#61`, workflow `36988558266`
- failing test: `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation`
- fix under validation: `#66`
- fix head at capture: `8aa27d9bb0fb28d2c2de965d6959257037032ac9`
- evidence level: repeated emulator failure + implementation-level identity fix; fix CI pending at capture time

This is a Candidate only. It is not Canonical.
