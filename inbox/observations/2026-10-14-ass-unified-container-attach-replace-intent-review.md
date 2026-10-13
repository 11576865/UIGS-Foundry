# Observation — Unifying media-picker entry can change workspace mutation semantics

Date: 2026-10-14
Status: Observation / user-supplied patch review; not compiled, executed or field-validated
Project: 11576865/ASS-Workbench-Android
Input: ASS_Workbench_Unified_Container_UI_20261014(1).patch, six local commits, especially [PATCH 5/6] unified container loading.
No Canonical promotion.

## Source-backed observation

Previously the visible UI distinguished “打开 / 更换参考视频” (non-destructive reference-media attachment via `openPickedVideo` -> `attachVideo`) from “打开 MKV 工程” (workspace replacement/import). The new patch consolidates both visible actions to “载入容器”, routes empty-preview clicks through the same action and sends the picker callback to `openMediaContainer` instead of `openPickedVideo`. Depending on the 4-byte signature, it dispatches to `openMkvProject` or `openGenericMediaContainer`. The generic path explicitly creates `AssDocument()`, resets history, begins a new workspace boundary and resets the editing session. The hidden `attachVideo` API remains callable internally.

This is **not merely navigation deduplication**: it unifies two distinct user intents (replace the current workspace vs attach/change a reference-media source) under a destructive operation. The new confirmation dialog makes replacement explicit when a workspace exists, so source inspection alone does not prove accidental loss. It does establish an acceptance question: can users still change reference video without intentionally discarding existing ASS editing context via an accessible primary action?

Additional source-risk hypothesis: `MediaContainerRouting.detect` only positively identifies Matroska prefixes; every other prefix, including invalid data, is classified `GENERIC_MEDIA`, and the generic route resets the document before `AndroidMediaImportProbe.probe` completes. This needs fail-closed media type validation / invalid media acceptance tests before declaring the import flow reliable.

## Related Foundry records / dedupe

- `inbox/observations/2026-10-13-ass-real-android-ui-video-comparison-and-spatial-anchors.md` — semantic anchors, identity and state continuity on task switch.
- `inbox/cases/2026-10-13-ass-native-mainline-stable-host-and-compact-taskbar-rollout.md` — native UI rollout evidence boundaries.
- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` — container import projections and source identity.

These cover continuity, import organization and test status, but not the specific attach-vs-replace contract regression risk. Therefore this record is an Observation, not a duplicate Candidate or verified Bug.

## Suggested falsification tests

1. Active unsaved ASS + different reference video: determine whether “attach reference media without replacing subtitles” is still reachable and distinguish this from intentional project replacement.
2. Active saved ASS + cancel picker: document, focus, selection, draft, Undo and media timestamp remain unchanged.
3. Unsupported/corrupt content selected as a generic container: existing working document is retained until a supported-media preflight succeeds; if current behavior differs, file a verified Bug with exact input and output.
4. Matroska with zero subtitles/fonts vs multi-ASS/default track: distinguish successful empty import from unsupported file and confirm read/commit consistency.

The supplied patch contains Kotlin policy probes and unexecuted Android instrumentation but no verified Gradle, emulator, renderer or field evidence. No claim of a reproduced defect or a successful compiled UI is made.
