# Candidate: Container inventory diffs should compare stable content identity, not presentation order

Status: **Candidate / reusable UI + verification pattern**
Date: 2026-10-04
Project context: `11576865/ASS-Workbench-Android` soft-mux / MKV container workflow design

## Observation

Container-editing interfaces become hard to understand when they primarily explain the operation in prose while showing only the target track. The user needs to see the container as an inventory of media resources and understand what the planned operation changes.

A second risk appears when before/after comparisons use list position or transient UI ordering. Track order may change even when content identity is preserved, and multiple tracks may share the same codec or language.

## Candidate rule

For non-destructive container editing and remux workflows:

- render the container's detectable contents as a first-class inventory, including all supported video, audio, subtitle, attachment/font, chapter, and other resource classes;
- keep unknown or unsupported resource types explicit instead of dropping them or guessing;
- represent action-heavy operations with compact icons when the action is conventional, while retaining accessible labels/tooltips and textual state for ambiguous domain semantics;
- distinguish baseline scan, planned state, and verified output scan; a planned result must not be presented as an observed container fact;
- compute added / removed / retained / modified resource states from a defined stable identity or matching policy, not from row number or visual order;
- when identity is ambiguous, surface `unknown` / `unresolved` rather than manufacturing a diff;
- after remux/write-back, re-scan the actual output container and compare the verified inventory against the baseline and intended mutation before publish.

A useful conceptual split is:

```text
Baseline inventory (observed)
        +
Planned mutation (intent)
        ↓
Predicted inventory (derived)
        ↓
Actual output inventory (observed)
        ↓
Verified diff
```

The UI should make the verified inventory and diff primary, while moving explanatory prose behind contextual disclosure.

## Why it is reusable

The pattern applies to MKV/MP4 remuxers, archive editors, package managers, project asset bundles, database migration previews, and other tools that modify collections while trying to preserve unrelated members.

## Evidence status

This entry comes from a design requirement and established non-destructive / evidence-level project principles. It has not yet been validated by a completed ASS-Workbench implementation or user study.

Do not promote to Canonical from this single design observation.
