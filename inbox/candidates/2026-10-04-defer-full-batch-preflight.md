# Candidate: Separate keystroke-time validation from full batch preflight

Status: candidate
Date: 2026-10-04
Domains: editor-performance, batch-authoring, UI, validation

## Summary

A batch-capable editor should not automatically run the full batch compiler/validator on every keystroke merely to keep an inspector button enabled.

For large selections this couples local form editing to O(N) document work on the UI thread and can turn ordinary parameter entry into selection-size-dependent latency.

A better split is:

- validate parameter syntax/ranges locally on every edit;
- optionally validate the focused/current object for immediate semantic feedback;
- run full multi-selection preflight only on an explicit Preview / Apply action;
- keep that batch preflight pure and atomic so failure cannot partially mutate the document.

## Candidate rule

For parameterized batch authoring:

1. Keep keystroke-time validation bounded independently of selection size whenever possible.
2. Use the focused/current object for contextual compatibility feedback if that is useful.
3. Treat full selection compatibility as an explicit operation boundary (Preview, Apply, Validate).
4. Full preflight must validate every target before committing any mutation.
5. Surface the failing target/reason through operation status instead of silently skipping incompatible objects.

## Evidence

ASS Workbench Android PR #86 initially recomputed `planProgressiveRevealBatch(...)` from Compose whenever a Karaoke FX parameter changed. The implementation was revised so the inspector only plans the focused Event during recomposition; the ViewModel performs full atomic batch planning when the user explicitly presses Preview or Apply.

This keeps text-field interaction independent of selection size while preserving fail-closed batch semantics.

A second occurrence appeared in ASS Workbench Android PR #95: adding Karaoke FX to the general Batch pane initially caused `AssBatchEngine.preview(...)` to rerun full compiler-backed compatibility and output generation whenever parameters changed. Review then exposed that the same O(N) recomputation already existed for the rest of the Batch pane. The correction now makes **all** batch preview explicit: parameter edits only rebuild local recipe state and validation, any recipe/document change invalidates the previous preview, Commit requires a current successful preview, and cheap filters run before compiler-backed Karaoke compatibility.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PRs: #86, #95
- evidence level: repeated implementation design correction across two authoring surfaces; no formal latency benchmark yet
- deduplication: searched UIGS-Foundry for batch-preflight/keystroke validation guidance; no direct duplicate found
- status rationale: reusable editor interaction/performance candidate; not Canonical

This is a Candidate only. It is not Canonical.
