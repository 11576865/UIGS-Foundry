# Candidate: Keep batch edit intent in the UI contract without hoisting editor-local drafts

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, product-architecture, reliability

## Summary

When a professional editor exposes rule-based batch operations through a stable UI contract, separate three concerns:

1. canonical selection-derived **batch intent** (for example, whether the default scope is the current Selection or all Events);
2. typed **write target** metadata derived from canonical identity plus Tool Binding;
3. editor-local Filter / Transform draft state.

The first two may cross a presentation-neutral UI boundary. The third should remain presentation-local until the user explicitly commits the recipe.

## Evidence

ASS-Workbench-Android UI Contract Slice E introduced:

- a bounded batch intent projection derived from canonical Selection;
- a typed Workspace write-target identity distinct from its display label;
- a contract action for committing an `AssBatchRecipe`;
- no global copy of the RuleBatchPane Filter / Transform draft.

This preserves one canonical document authority while allowing multiple presentations to consume the same stable intent and commit surface.

## Candidate rule

For rule-based or bulk-editing tools:

- project only stable domain intent across the UI contract;
- keep filter/transform form drafts local unless cross-presentation draft continuity is an explicit product requirement;
- type the write target separately from human-readable scope text;
- derive write target from canonical identity + Binding instead of storing a second mutable target;
- send the final batch recipe through one domain commit path so the operation remains one undoable transaction;
- do not collapse Focus, Selection, Binding, Write Target and draft state into one generic "current context" object.

## Relationship to existing Foundry knowledge

This complements `UIGS.WORKSPACE.SCOPE_TRANSPARENCY`. That pattern explains WHO / WHERE / HOW MANY and requires derived-only scope metadata. This candidate adds the contract-boundary observation that a batch editor's local recipe draft should not be promoted merely because the commit action is presentation-neutral.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#80`
- branch: `refactor/ui-contract-write-target-slice-e`
- evidence level: implementation + unit/instrumentation CI in progress

This is a Candidate only. It does not modify Canonical guidance.
