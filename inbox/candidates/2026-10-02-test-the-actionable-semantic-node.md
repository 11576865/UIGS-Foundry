# Candidate: Test the actionable semantic node

Status: candidate
Date: 2026-10-02
Domains: reliability, interface-grammar

## Summary

UI automation should attach and target stable test semantics on the element that actually owns the user action, not merely on an outer visual/layout container.

A parent Surface or container may be visible and tagged while the real click action belongs to a nested button. Calling `performClick()` on the tagged container can therefore succeed syntactically without exercising the product interaction.

## Evidence

ASS-Workbench-Android PR #63 / #67 exposed this with the Edge Bookmark workspace:

- the outer Edge handle Surface had tags such as `edge-handle-top`;
- the actual `onClick` belonged to the nested `IconButton`;
- Emulator regression #270 clicked the outer tagged node and timed out waiting for `edge-layer-top`;
- the implementation added explicit actionable tags such as `edge-toggle-top` / `edge-toggle-bottom`;
- the rebuilt PR #67 passed Android Emulator Regression #280.

## Candidate rule

For automated interaction tests:

1. Put the stable test identifier on the node that owns the action semantics.
2. Keep layout/visual container tags separate from action tags.
3. Use container tags for presence, geometry, and composition assertions.
4. Use actionable tags for click, toggle, drag, input, and other interaction assertions.
5. When a test times out after an apparently successful interaction, inspect the semantics owner before increasing timeouts.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- failed integration: PR #63, Emulator Regression #270
- validated rebuild: PR #67, Emulator Regression #280
- merge commit: `da5670a408ca97a31900f71f8026d1c6079d6a3e`
- evidence level: CI-validated Android Compose instrumentation

This is a Candidate only. It is not Canonical.
