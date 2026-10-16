# Case / Candidate — FIXED V1.1 first native Compose subtitle-grid slice on stacked R3 branch

Date: 2026-10-16
Status: **Work Unit Complete / Durable Checkpoint / Pending External Validation**
Product: https://github.com/11576865/ASS-Workbench-Android
Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Branch: `feat/fixed-v11-event-grid-20261016`
Parent: `feat/r3-fixed-visual-layout-20261014` (draft PR #148)
Latest durable commit: `a5340129aee9579b260010835d4de7e7fd909386`
Figma FIXED baseline: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=85-3

## User intent and previous decision
After user froze Tablet FIXED V1.1 as the implementation baseline and postponed SPATIAL UI, they approved starting the first bounded Android implementation slice. Prior R3 PR #148 already hosts the actual FIXED 3-pane live video/transport/timeline/inspector and contains draft ownership protections. New V1.1 changes must not duplicate or discard that working infrastructure.

## Actual output
- `app/src/main/kotlin/io/github/assworkbench/app/ui/FixedV11EventGrid.kt`: a native Material3 wide-window table header and compact event row, rendered from stable Event ID, start/end, Style and visible text. Focus and selection are highlighted; QC issue count opens the existing diagnostic list. No new viewmodel/state owner.
- `ModernEditorScreen.kt` `EventWorkspace`: only `r3Chrome` wide FIXED path uses this new table presentation. Preserves the same `LazyColumn` and key={event.id}, existing `EditorViewModelUiActions` focus/select action, filtered order, long-press range container and previous narrow `ModernEventRow` branch.
- `app/src/androidTest/kotlin/io/github/assworkbench/app/ui/FixedV11EventGridInstrumentedTest.kt`: Compose check for table fields and tap/long-press callback forwarding.
- `.uigs/tasks/ass-fixed-v11-android-implementation-20261016.json`: durable scope, completed/next units, draft PR, exact branch/commit and open validation boundaries.
- PR #149 is draft and **stacked on #148**, not merged into main. Pending dependency resolution acknowledged.

## Explicit evidence limits
Source files and commits have been persisted. A one-time GitHub Actions query for final commit returned no pull-request-triggered workflow runs yet. This is not a CI pass and does not prove buildability. Emulator, actual media/libass, keyboard/draft lifecycle, exact 1440/1024 screenshots and tablet input remain **Pending External Validation**. User should not be told the full V1.1 UI is now implemented: this is only the first event table slice. The separate SPATIAL host and historical canvas features remain untouched.

## Reusable candidate learning
A new design baseline does not justify making duplicate event state or rebuilding live video/timeline. For a high-density professional UI, add a *presentation-only row variant* over the current event owner and keep stable Event IDs, filter ordering, click/long-press selection behavior, and independent inspector draft state. Work on one coherent branch/PR, connect automated input tests, and leave CI exact-head evidence explicitly pending. This is a bounded Case/Candidate, **not** a modification of UIGS Canonical.

## Dedup
Searched `FIXED V1.1 Compose professional subtitle table preserved existing EventWorkspace callbacks`, `ASS Workbench R3 stacked PR view-only subtitle event grid selection behavior` and `2026-10-16 FIXED V1.1 Android native first slice event table`. No matching Foundry record. Prior `inbox/cases/2026-10-16-ass-fixed-v11-frozen-baseline-spatial-deferred.md` documents the Figma/scope decision, not this native code implementation.
