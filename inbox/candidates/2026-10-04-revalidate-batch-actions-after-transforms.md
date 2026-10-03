# Candidate: Revalidate batch actions after earlier transforms and fail atomically on invalidation

Status: candidate
Date: 2026-10-04
Domains: batch-editing, preflight, compatibility, atomicity, UI-contract

## Summary

A batch filter can establish that an item is compatible before transformation, but earlier actions in the same recipe can invalidate that compatibility before a later action executes.

Treating the later action as a silent no-op preserves data safety but violates the user's recipe intent: the item may still receive earlier actions while the later requested action is skipped, producing a partially applied semantic transaction.

## Candidate rule

1. Distinguish filter-time eligibility from action-time compatibility.
2. When a later action owns constrained properties or semantics, revalidate against the current intermediate item after all preceding actions.
3. If an item passed the filter but becomes incompatible because of earlier actions in the same recipe, do not silently skip only the later action.
4. Fail the recipe preflight atomically unless the product explicitly models and surfaces per-action partial execution as an intentional policy.
5. Preview must surface the failure without mutating canonical state.
6. Commit must rerun the same preflight and refuse canonical mutation if the recipe is no longer valid.
7. Initial heterogeneous incompatibility may still be handled by an explicit compatibility filter when that is the documented batch policy.

## Evidence

ASS Workbench Android PR #95 adds Karaoke reveal to the general Filter → Transform → Preview → Commit batch engine.

The initial implementation:
- filtered Events using Karaoke reveal compatibility,
- then rechecked compatibility in the Karaoke action,
- but returned the current Event unchanged if an earlier action had introduced a conflicting blur/geometry override.

That protected the Karaoke-owned property but could still commit preceding actions, silently producing a partially applied recipe.

The correction now:
- keeps initial incompatibles filtered out,
- throws on action-time invalidation for a previously matched Event,
- catches the failure in Preview and displays it,
- reruns the same preflight at Commit,
- and prevents any canonical mutation from the invalid recipe.

A regression test covers a recipe where a numeric blur override precedes Karaoke reveal and verifies that preview fails while the source document remains unchanged.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #95
- evidence level: concrete semantic defect found during batch-composition review + implementation correction + regression coverage
- deduplication: searched UIGS-Foundry for filter/action invalidation, batch preflight, and partial-apply atomicity; no direct duplicate found
- status rationale: reusable cross-project batch-editing principle; not promoted to Canonical from a single project observation

This is a Candidate only. It is not Canonical.
