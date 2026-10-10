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

## 2026-10-10 fixed inspector draft owner across ToolInstance switches — Pending CI

Source: [ASS-Workbench-Android product PR #143](https://github.com/11576865/ASS-Workbench-Android/pull/143), merged into the **unmerged** UI redesign #138 branch at `fb26119c5483e593bfa78c85d7e88f8878783ebf`.

The prior Android regression in run `38032992080` explicitly failed `inspectorDraftSurvivesToolSwitchAndRotation` at the first check after TEXT → EFFECTS → TEXT, **before the orientation change**: the uncommitted `WORKBENCH` payload was absent. The fixed workspace's single mutually exclusive Event Inspector keyed its saveable editor buffer by `ToolInstance.id + Event.id`; tool selection changed that identity even though the Event draft belonged to the fixed inspector slot. The source patch supplies a stable `fixed-inspector + Event.id` saveable scope only in this mutually exclusive fixed-mode presentation.

Do **not** apply the same key globally to all spatial ToolInstances: multiple concurrently mounted editors can legitimately target the same Event and then Compose `SaveableStateHolder` would reject duplicate registrations (separate recorded Bug in `inbox/bugs/2026-10-10-ass-spatial-saveable-holder-duplicate-render-keys.md`). This distinction refines the existing component-continuity Candidate: retention scope should follow the intended **semantic draft owner and concurrent presentation slot**, not automatically the current tool ID or globally the Event ID.

New Android regression asserts that TEXT → EFFECTS → TEXT preserves the unsaved body and canonical ASS Event remains unchanged until Apply. This patch is **Pending External Validation** in Android CI/Emulator/Fontconfig and does not establish rotation/tablet device parity or general Canonical policy.
