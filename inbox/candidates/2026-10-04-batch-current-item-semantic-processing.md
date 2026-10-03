# Candidate: Pass the current batch item directly to semantic predicates and transforms

Status: candidate
Date: 2026-10-04
Domains: batch-processing, editor-performance, semantic-authoring

## Summary

A batch engine that already iterates over the current object should not make each semantic predicate/action re-resolve that same object by ID or rebuild the entire collection merely to call a per-object compiler.

Doing so can turn an intended O(N) batch pass into O(N²) work and obscure which object state the action is actually validating after earlier transforms.

## Candidate rule

1. Treat the current batch item as the authoritative per-item input for predicates/actions.
2. Pass immutable shared document/context separately when semantic resolution needs styles, metadata, or other global state.
3. Avoid per-item `find(id)`, full-list `map`, or temporary whole-document reconstruction when the current item is already available.
4. When actions are sequential, semantic compilation must consume the current transformed item, not silently re-fetch the original item from shared context.
5. Preserve an ID-based convenience overload only at API boundaries where callers genuinely have an ID rather than an object.
6. Verify complexity with code-path structure or measurement before claiming performance magnitude.

## Evidence

ASS Workbench Android PR #95 initially had multiple nested collection operations in Karaoke batch processing:

- compatibility re-found the Event by ID and then planning re-found it again;
- batch planning associated IDs with plans by repeatedly resolving each Event;
- the Karaoke action rebuilt the whole Event list for every target just to substitute the current transformed Event before invoking the compiler.

The correction adds direct-`AssEvent` planner/compatibility overloads and passes the current transformed Event through the batch loop. Shared Style/document context remains separate. This removes repeated full-list scans/copies from the per-item Karaoke path.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #95
- evidence level: concrete nested-scan/copy code path + implementation correction; no formal large-N benchmark yet
- deduplication: searched UIGS-Foundry for current-item batch APIs, nested lookup, and O(N²) per-item semantic compilation; no direct duplicate found
- status rationale: reusable batch-engine performance/correctness candidate; not Canonical

This is a Candidate only. It is not Canonical.
