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

## 2026-10-10 complementary inverse: end editor-draft ownership at session boundary — Pending CI

Source: ASS-Workbench-Android [PR #140](https://github.com/11576865/ASS-Workbench-Android/pull/140), merged into the **unmerged** UI redesign PR #138 branch at `92ccaba3cb1d36eea6cbc31144d14d464aff3e15`.

The continuity rule has an inverse: preserve a UI draft while the semantic workspace owner remains stable, but do **not** allow that draft to cross into a new project session just because the new project reuses the same Event ID. An unkeyed root `rememberSaveableStateHolder()` cached InlineEventEditor buffers under ToolInstance/Event-ID keys rather than project/session identity. Reusing those identifiers across documents could inadvertently resurrect a previous project's unsaved buffer.

The submitted patch keys the holder on `workspaceSessionId` and adds an instrumentation regression using two sessions with the same Event ID. It also annotates the existing orientation/tablet-size regression with stage-specific draft-payload and Apply-button checks. A previous emulator run `37984011960` reported a failure in `inspectorDraftSurvivesToolSwitchAndRotation` without diagnostic XML content and included `adb: device offline`; that failure is **not** proven to originate from session collision or draft loss. The related non-diagnostic emulator evidence boundary is already documented in `inbox/observations/2026-10-04-android-emulator-offline-before-code-change.md` and is not duplicated here.

**Evidence:** project source patch and proposed tests only; latest Android CI, emulator and real-device acceptance **Pending External Validation**. No Canonical promotion.

## 2026-10-10 fixed-inspector tablet relayout: dirty draft reparenting — Pending CI

Source: ASS-Workbench-Android [PR #144](https://github.com/11576865/ASS-Workbench-Android/pull/144), merged into the **unmerged** Draft UI redesign PR #138 at `800a662e892be84293b53431ca6b85f0cf108429`. Connected evidence: [Android emulator run 38050733194](https://github.com/11576865/ASS-Workbench-Android/actions/runs/38050733194).

**Observed defect, not a hypothetical UI guideline:** Within one document session, an uncommitted Event #1 text buffer survived TEXT→EFFECTS→TEXT and initial phone-landscape configuration. After the test changed Android display size to 1920×1200 and density to 160, the three-pane inspector displayed the unmodified canonical `Recovered line` instead of the uncommitted `Recovered line WORKBENCH`. The failure occurred at `tablet-landscape` before Apply; data continuity, not merely navigation, was lost. The run reported 16 tests / 2 failures; its interrupted coverage must not be equated to a full earlier 120-test run.

**Source mechanism under investigation:** `FixedWorkspace` invoked one semantic inspector from three distinct Compose composition branches (COMPACT, DUAL_PANE, THREE_PANE). A plain composable lambda can be disposed and recreated across a profile switch, even though both the inspector and document-session owner remain the same. The repair remembers one `movableContentOf<Modifier>` inspector identity and calls it from each layout branch; `rememberUpdatedState` supplies current tool/Event callbacks. A strict existing connected test additionally checks the unchanged workspace session ID, distinct from draft survival.

**Evidence boundary:** PR #144's new-head Android CI, Emulator Regression and native probe are **Pending External Validation** (runs `38061223365`, `38061223380`, `38061223374`). The cause and patch are code-grounded, but not yet emulator-verified. No ASS canonical Event, domain ToolInstance or Undo history is mutated by the layout change. This extends the existing stable-component-identity Candidate; it must not be promoted to Canonical from one observation. Remaining viewport-history/IME/visual tests are independent.
