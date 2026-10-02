# Candidate: Bounded resource projection across a UI stability boundary

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, reliability, operations

## Summary

When a presentation-neutral UI contract sits in front of a stateful editor, native bridge, renderer, or resource subsystem, it should expose the smallest stable **summary/projection** needed by presentations rather than handing UI code the underlying resource objects or transport handles.

Typical safe projections include:

- counts and stable identity;
- busy/available/error status;
- selected resource identity where that identity is already part of domain state;
- immutable diagnostic snapshots;
- bounded revision numbers.

The UI contract should avoid exposing:

- filesystem/content URIs when presentations do not need persistence authority;
- imported resource objects merely so UI can reach through to internals;
- native bridge or renderer handles;
- mutable collections that alias the underlying state owner;
- complete transport payloads when a summary is sufficient.

## Evidence

ASS-Workbench-Android UI Contract Slice D adds bounded presentation-facing summaries for fonts/resources, MKV container state and renderer diagnostics.

The projection includes font counts/import status/revision, packaging-selection count, fallback family, renderer diagnostics, container attached/name/loading, track count/selected track number, attachment counts and write-back status.

It deliberately omits the container URI, FontAsset objects, complete track payload and native bridge handles. Renderer diagnostics are copied into a new list so presentation code cannot retain a mutable alias to the EditorState input.

Canonical ownership remains in EditorViewModel / container bridge / renderer subsystems.

## Candidate rule

For UI stability boundaries around resource-heavy or native-backed subsystems:

1. Project bounded state summaries instead of exporting subsystem objects.
2. Keep persistence handles and native runtime handles behind the owning service/model unless the presentation truly owns that operation.
3. Copy mutable diagnostic/status collections at the boundary.
4. Prefer counts, stable IDs, revisions and explicit availability/busy/error states over arbitrary object graphs.
5. Add write actions only as named domain intents; do not expose generic mutation of projected state.
6. Treat the projection as a view of canonical state, never as a second resource registry.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#77`
- head at intake: `b2985472bf3bf9fda4027a6eac470c3e75f41041`
- files: `EditorUiContract.kt`, `EditorUiContractTest.kt`
- evidence level: implementation plus CI in progress

This is a Candidate only. It does not modify Canonical guidance.
