# Bug: Raw regex cleanup can corrupt nested semantic payloads

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: structured editing / ASS transforms / destructive cleanup / raw preservation

## Symptom

A structured “clear overrides” action can remove managed-looking tags from inside a nested semantic construct even when that construct is not owned by the action.

In ASS, a raw regex over an entire override block can match tags inside `\t(...)` payloads. Removing only the nested property tag may leave a malformed or semantically changed transform wrapper.

Example shape:

`{\fs56\t(0,500,\fs80\bord8)}Text`

A regex-based Style-inheritance cleanup that removes every `\fs` / `\bord` substring can accidentally rewrite the transform payload instead of only clearing direct static overrides.

## Failure mechanism

The cleanup operated on raw override-block text and recognized managed tags by spelling, not by syntax ownership / parenthesis depth.

That conflated:

- direct Event/span overrides owned by the Style-inheritance action; and
- nested transform payloads owned by Animation.

The UI could therefore claim a Style reset operation while silently modifying another editor domain.

## Mitigation implemented

ASS Workbench Android PR #99 replaces regex-based stripping with the shared top-level override semantic projection.

- direct managed tags are removed structurally by source ranges;
- later direct span overrides can still be cleared;
- nested `\t(...)` payload tags remain byte/semantically preserved;
- unknown tags remain preserved;
- empty override blocks created by direct-tag removal are cleaned up;
- UI copy explicitly says direct overrides are cleared while Transform animation remains.

Regression coverage verifies that direct `\fs`, `\bord`, scale/color overrides are removed while nested transform payloads and unknown tags survive intact.

## Reusable lesson

Do not implement semantic cleanup by regex over a container that can embed another semantic language or ownership domain.

Resolve ownership first, then remove only the owned syntax nodes/ranges. If nested semantics are not owned, preserve them intact or fail closed.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #99
- evidence level: concrete cross-domain mutation defect + structural correction + regression coverage
- deduplication: searched UIGS-Foundry for regex override cleanup, nested transform corruption, and Style inheritance payload preservation; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
