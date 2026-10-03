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
