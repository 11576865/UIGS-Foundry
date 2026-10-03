# Candidate: Model semantic compatibility as a batch filter, not an exception path

Status: candidate
Date: 2026-10-03
Domains: batch-editing, authoring-tools, heterogeneous-documents, fail-closed-design

## Summary

Bulk authoring frequently targets heterogeneous objects. A transform may be semantically valid for some matched objects and unsafe for others even though they share the same nominal type.

If incompatibility is discovered only inside the transform and raised as an exception, one incompatible object can abort an otherwise safe batch. If the transform silently coerces the object instead, data can be damaged.

A safer authoring pattern is:

- expose compatibility as an explicit semantic predicate;
- compose that predicate into the batch filter;
- make the transform itself fail-closed as a second line of defense;
- let Preview report only the objects that are both user-selected and semantically compatible;
- commit the resulting compatible subset as one ordinary transaction.

## Candidate rule

For a batch transform with object-specific semantic preconditions:

1. Implement a reusable compatibility inspection function that returns a boolean plus a human-readable reason.
2. Expose the compatibility predicate as a normal batch filter.
3. When the user enables the transform, automatically add that compatibility filter unless they explicitly choose a different policy.
4. Keep the transform itself fail-closed if invoked without the filter.
5. Do not let one incompatible object abort unrelated compatible objects.
6. Do not silently coerce an incompatible object into a different semantic model.
7. Preserve Preview → Commit semantics so the compatible subset is visible before mutation.

## Evidence

ASS Workbench Android PR #85 connects per-syllable Karaoke reveal FX to the general Filter → Transform → Preview → Commit engine.

The source file may contain:
- cumulative `\k / \kf / \ko` timing that is compatible;
- absolute `\kt` timing with different semantics;
- existing alpha/blur/transform controls owned by another effect;
- ordinary non-Karaoke Events.

The implementation adds:
- `inspectProgressiveRevealCompatibility`;
- `AssBatchFilter.KaraokeRevealCompatible`;
- a fail-closed `ApplyKaraokeRevealFx` action;
- UI behavior that automatically composes the compatibility filter when the action is enabled.

Regression tests use one heterogeneous batch and verify that only the compatible Event is affected while incompatible Events remain byte-for-byte unchanged.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #85
- evidence level: implemented domain/API/UI + regression coverage; final CI pending at intake time
- deduplication: searched UIGS-Foundry for equivalent compatibility-filtered heterogeneous batch guidance; no direct duplicate found
- status rationale: reusable batch-authoring architecture candidate; not Canonical


## Refinement — 2026-10-04

ASS Workbench Android PR #95 supersedes draft #85 after the per-syllable flip/effective-state compiler landed in main.

This adds two constraints to the candidate pattern:

8. **The compatibility predicate must be parameter-identical to the transform it guards.** If compatibility depends on duration, geometry, ownership, codec, mode, or any other transform input, the filter must receive the same spec rather than evaluating a generic/default configuration.

9. **The transform must revalidate against the object state that actually reaches it.** In an ordered batch pipeline, earlier actions may change the same object's text, style, geometry, ownership, or other preconditions after the initial filter ran. The guarded action therefore needs a second compatibility check against the current transformed object and relevant document context before applying itself.

PR #95 also demonstrates why compatibility cannot be reduced to text-only inspection when authoring semantics depend on inherited/effective state. Karaoke reveal compilation now depends on Event text plus Style alpha/scale and Event-level geometry, so the batch predicate uses the same document-aware compiler boundary as the action.

Additional evidence:
- project: `11576865/ASS-Workbench-Android`
- superseded draft: #85
- replacement PR: #95
- implementation revision: `56284433f18016d4ba58fab3aeecec1cd9205c7e`
- evidence level at intake: branch + PR + domain/UI/regression tests authored; asynchronous CI pending
- Canonical status unchanged

This is a Candidate only. It is not Canonical.
