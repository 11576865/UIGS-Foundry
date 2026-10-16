# Case / Candidate — FIXED V1.1 compact tablet drawer reuses one EventWorkspace under IME pressure

Date: 2026-10-16
Status: **Third native implementation work unit source-complete; External Validation PENDING**
Repository: https://github.com/11576865/ASS-Workbench-Android
Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Branch: `feat/fixed-v11-event-grid-20261016`
Exact checkpoint SHA: `8fe30e703e75d31147461deb2a68a99d8ea29976`
Base dependency: `feat/r3-fixed-visual-layout-20261014` / draft PR #148
Frozen FIGMA FIXED page: `85:2`; compact scene: `85:942`; drawer scene: `85:1237`.

## User goal and bounded scope
Owner said “继续” after the wide native Event-grid and professional timing-scene slices. Resume the next recorded unit: 1024×768 FIXED grid drawer, touch selection, keyboard pressure and draft continuity. Explicitly do NOT update SPATIAL UI or delete spatial model/domain code.

## Actual source changes
- `FixedV11CompactEventDrawer.kt`: Material3 `ModalNavigationDrawer` wraps the existing `EventWorkspace` list as an on-demand surface. An explicit accessible “字幕列表” opener and “关闭” action, finite-height LazyColumn host, selected/total counts, and state outside the drawer. No duplicated Event snapshot.
- `ModernEditorScreen.kt`: replaces the DUAL_PANE permanent subtitle-list column with two editing panes (actual `WorkbenchPreview`/player and `ModernTimelinePane` on left; the same existing `movableInspector` on right). The original `EventWorkspace` is rendered only inside the drawer; for logical tablet widths 720–1179dp it renders the existing `FixedV11EventGridRow` and header. Selected Event focus closes the drawer; long-press multi-selection stays open. Narrow COMPACT and wide THREE_PANE fallback branches remain.
- `FixedV11CompactDrawerPolicy.effectiveProfile`: when the drawer is already open and logical tablet width is within 720–1179dp, it remains mounted despite IME-induced `AdaptiveWorkspacePolicy.COMPACT` height classification. As soon as the drawer closes the actual adaptive profile returns. This is a **presentation-only** change, not a persisted snapshot or modified Binding/Focus.
- `FixedV11CompactDrawerPolicyTest.kt`: pure JVM tests for keyboard compaction, drawer closure and refusing to force phone/wide UIs into dual pane.
- `FixedV11CompactEventDrawerInstrumentedTest.kt`: Compose test shell opens/closes, displays same grid, long-press and focus callback behavior, sibling text draft still exists across drawer transition. Does **not** fully emulate `InlineEventEditor`, physical keyboard or renderer.

## Source evidence and safety limits
GitHub compare against R3 base returned 18 commits ahead and 11 files changed across three units: FIXED UI source/tests and `.uigs/tasks/ass-fixed-v11-android-implementation-20261016.json`, no `InfiniteCanvasHost` or SPATIAL files. PR #149 remains draft and stacked on #148. Exact-head `8fe30e70` Actions and combined-status checks both returned zero runs/statuses at the time of inquiry. **DO NOT claim compilation success or runtime compatibility**. No APK, screenshot or real-device evidence produced.

The Figma reference is 1024×768 *design pixels*; native policy uses **logical dp** and adaptive width/height, not physical device pixels. Actual landscape devices and IME changes must be tested. Inline text-editor saveable state, focus, selection, media PTS and undo are expected to remain stable by code ownership, but this expectation needs actual editor integration instrumentation. More width/keyboard corner cases may emerge in device testing.

## Bounded reusable knowledge, not Canonical
A feature-dense tablet subtitle navigator can be moved to an overlay **only if** it remains a single navigation/data owner and the underlying editor/timeline/inspector stay composed; keep the overlay anchored across IME-induced resize to avoid destroying a filtered list mid-input. Use explicit open/close and tested touch handling. This is one concrete product Case/possible Candidate, not proof of a universal cross-product UI rule. Do not auto-promote Canonical.

## Intake dedup
Queried Foundry for `ASS FIXED V1.1 1024 event drawer IME policy same EventWorkspace`, `FixedV11CompactEventDrawer single owner draft keyboard` and `ASS PR149 compact subtitle grid modal navigation`; no exact prior case. Earlier PR149 Event grid and timing scene Cases are adjacent units, not duplicates.
