# Case — FIXED V1.1 precise-timing scene as layout-only projection of the live editor

Date: 2026-10-16
Status: **Work Unit Complete / Durable Checkpoint / Pending External Validation**
Product: https://github.com/11576865/ASS-Workbench-Android
Draft stacked PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Head SHA: `66ea0389ef8ddc96e8600263dad814ad755a4a56`
Parent branch: `feat/r3-fixed-visual-layout-20261014` (PR #148)
Frozen design: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=85-3
Related case: `inbox/cases/2026-10-16-ass-fixed-v11-first-compose-grid-slice-stacked-pr149.md`

## Owner instruction
The user said “继续” after approving and receiving the first native wide Event grid slice. The next pending bounded task recorded in the product repository was: integrate professional FIXED timing workscene with session state continuity, then consider 1024×768 drawer. SPATIAL UI remains deferred and all spatial code is protected.

## Implementation in source
1. `app/src/main/kotlin/io/github/assworkbench/app/ui/FixedV11WorkspaceTabs.kt`: a **presentation-only** `SUBTITLE_EDIT / PRECISE_TIMING` mode with two visible wide FIXED task-scene tabs. This is neither a new Tool ID nor an editor host, and callbacks only update local saveable mode. Included read-only `FixedV11TimingContext` reporting bound Event Start/End/duration and media PTS; missing binding safely reports absence rather than inventing target.
2. `R3FixedLayoutPolicy.kt`: optional `timingPriority=false` argument keeps old geometry by default. When timing priority is on, media gets at most 34% of remaining wide pane height and **the same `ModernTimelinePane`** gets the rest. Hidden preview stays hidden; no new playback time source or mutation.
3. `ModernEditorScreen.kt` `FixedWorkspace`: `rememberSaveable(state.workspaceSessionId)` owns presentation-mode identity. Shows task tabs in wide UI, passes timingPriority to existing geometry, and inserts read-only context above the **same `movableInspector`**. The change does **not** call `onActiveTool`, change ToolInstance/Binding, save raw text, or alter Focus/Selection.
4. `R3FixedLayoutPolicyTest.kt`: JVM regression assertions for geometry budget, timeline priority, media visibility and preserved HIDDEN preference.
5. `FixedV11WorkspaceTabsInstrumentedTest.kt`: Compose test for tab navigation, retained sibling draft input, and missing-binding read-only status. This is a **shell-level** test, not full `InlineEventEditor` lifecycle proof.
6. `.uigs/tasks/ass-fixed-v11-android-implementation-20261016.json`: updated durable task, next units, blockers and latest head.

## Validation and boundaries
Commit comparison of the PR head against R3 parent reported eight changed files limited to FIXED source/tests and task record; no SPATIAL files modified. Native Kotlin build, emulator instrumentation, real media/libass, IME/rotation draft retention, waveform seeking/PTS, source screenshot parity, and real tablet interaction are **pending**. One immediate GitHub Actions query for head `66ea0389` returned no PR-triggered workflow runs; absence of a run does not establish a pass. PR #149 remains draft stacked on draft #148, not merged into main.

## Reusable bounded candidate
Task-scene switching in specialized editors should often be modeled as a **layout projection** over a stable editor and ToolInstance, not a tool replacement. A separate read-only time context may explain the selected/bound event while keeping write operations with the original inspector and shared timeline. This separates user visual organization from editing/undo lifecycle. This concrete implementation is a project Case, **not an automatic UIGS Canonical rule**; full runtime state-survival tests are still required.

## Intake dedup
Searched Foundry for:
- `FIXED V1.1 professional timing scene same inspector identity Compose timingPriority`
- `R3FixedLayoutPolicy read only timing PTS saved draft switching`
- `ASS FIXED V1.1 PR149 second native timing unit`

No duplicate of this implementation slice. First Event grid Case is adjacent, not a duplicate. Current status Pending external CI/visual/device validation.
