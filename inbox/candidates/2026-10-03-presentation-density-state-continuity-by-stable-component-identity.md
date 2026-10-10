# Candidate: Preserve local UI state across presentation-density changes by retaining component identity

Status: **Candidate / UI state-continuity pattern**
Date: 2026-10-03
Project evidence: `11576865/ASS-Workbench-Android`, PR #82

## Observation

ASS Workbench needed one timeline to exist in both a compact persistent dock and a larger expanded editing surface.

A tempting implementation is:

```text
collapsed
  -> CompactTimeline()

expanded
  -> ExpandedTimeline()
```

That creates two presentation subtrees around one semantic capability. Even when both read the same document state, local interaction state such as viewport center, zoom, follow-playhead, snap settings, transient disclosure, or scroll position can acquire a second owner or be lost when the subtree is replaced.

PR #82 instead keeps one `ModernTimelinePane` invocation mounted and changes only presentation constraints:

```text
same Timeline pane instance
  + compact density / smaller height
  <-> expanded density / larger height
```

The timeline's existing `rememberSaveable` viewport/follow/snap state therefore remains attached to the same component identity while the host changes density and geometry.

## Reusable candidate

When a UI transition changes **presentation density, geometry, or disclosure** but does not change the semantic tool or its state owner:

- prefer retaining one semantic component instance and changing its constraints/presentation inputs;
- avoid conditionally swapping between parallel compact/expanded implementations when both represent the same capability;
- keep canonical/domain state outside the presentation either way;
- treat local viewport/disclosure state as one owned continuity surface unless product semantics explicitly require a reset;
- add an invariant test that the presentation transition does not mutate canonical data, Focus, Selection, or history.

This pattern is especially relevant to inspectors, timelines, tool docks, editors, preview panels, and responsive master/detail surfaces.

## Evidence

PR #82 adds:

- `TIMELINE_DOCK_EXPERIMENTAL`;
- one continuously mounted `ModernTimelinePane` whose `compact` flag and height change;
- bounded drag-resize and snap policy;
- an explicit expand/collapse control;
- `TimelineDockPolicyTest`;
- a `PresentationStateSmokeInstrumentedTest` case that checks canonical Event text, Focus, and Undo/Redo invariants across presentation entry.

## Evidence limits

At intake time PR #82 is still Draft and its current CI/Emulator/Fontconfig runs are pending. This record therefore remains Candidate and must not be treated as validated Canonical guidance.

The observation also does not claim that retaining component identity is always preferable. Replacing a subtree can be correct when the semantic tool changes, lifecycle reset is intentional, resource ownership differs, or state migration is explicitly defined.

## 2026-10-10 complementary inverse: end editor-draft ownership at session boundary — Pending CI

Source: ASS-Workbench-Android [PR #140](https://github.com/11576865/ASS-Workbench-Android/pull/140), merged into the **unmerged** UI redesign PR #138 branch at `92ccaba3cb1d36eea6cbc31144d14d464aff3e15`.

The continuity rule has an inverse: preserve a UI draft while the semantic workspace owner remains stable, but do **not** allow that draft to cross into a new project session just because the new project reuses the same Event ID. An unkeyed root `rememberSaveableStateHolder()` cached InlineEventEditor buffers under ToolInstance/Event-ID keys rather than project/session identity. Reusing those identifiers across documents could inadvertently resurrect a previous project's unsaved buffer.

The submitted patch keys the holder on `workspaceSessionId` and adds an instrumentation regression using two sessions with the same Event ID. It also annotates the existing orientation/tablet-size regression with stage-specific draft-payload and Apply-button checks. A previous emulator run `37984011960` reported a failure in `inspectorDraftSurvivesToolSwitchAndRotation` without diagnostic XML content and included `adb: device offline`; that failure is **not** proven to originate from session collision or draft loss. The related non-diagnostic emulator evidence boundary is already documented in `inbox/observations/2026-10-04-android-emulator-offline-before-code-change.md` and is not duplicated here.

**Evidence:** project source patch and proposed tests only; latest Android CI, emulator and real-device acceptance **Pending External Validation**. No Canonical promotion.
