# Candidate: Synchronize Compose popup semantics before querying tagged menu items

Status: candidate
Date: 2026-10-02
Domains: reliability, interface-grammar

## Summary

Android Compose instrumentation tests that interact with popup/menu content should separate **popup synchronization** from **node-tree selection**. Do not assume that forcing `useUnmergedTree = true` makes a popup item more discoverable.

A robust test should:
1. trigger the popup from a stable control;
2. wait until the intended popup item is discoverable in the semantics tree mode actually used by the component;
3. only then click the item;
4. wait for the destination surface/invariant before asserting product state.

## Evidence

ASS-Workbench-Android PR #61 added a cross-presentation canonical-state smoke test.

- First attempt clicked the top-bar menu and immediately queried `workspace-mode-toggle`; the item was not yet available.
- Second attempt added synchronization but forced `useUnmergedTree = true`; the wait itself timed out at `switchPresentation():95`.
- Existing stable editor regression tests interact with the same `workspace-mode-toggle` / UI Variant Lab using the default semantics query mode.

The failure therefore belongs to test synchronization/tree-selection behavior, not to canonical editor-state loss.

## Candidate rule

For popup/dropdown UI tests:
- synchronize the popup opening explicitly;
- use the narrowest semantics-tree mode proven for that component;
- treat merged vs unmerged tree as a component-specific test contract, not a universal “more visibility” switch;
- keep product-state assertions separate from popup-discovery failures.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#61`
- first failing workflow: `36973306283`
- second failing workflow: `36974168155`
- second failing head: `61bd466acbdc458d0db395f85eb32ff0bc56ee79`
- evidence level: repeated Android emulator instrumentation evidence plus comparison with existing passing regression tests

This is a Candidate only. It is not Canonical.
