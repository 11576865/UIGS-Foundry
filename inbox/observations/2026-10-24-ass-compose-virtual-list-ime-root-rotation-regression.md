# Observation / Case — Native Compose lazy directory and stale IME root across responsive hosts

Date: 2026-10-24
Status: **Observed native regressions; candidate repair pushed; external validation PENDING**
Source project: [ASS-Workbench-Android](https://github.com/11576865/ASS-Workbench-Android)
Source branch: `feat/fixed-v11-event-grid-20261016` / [Draft PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149)
Failed exact-head run: [40074615531](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40074615531) at `63377555d867567d675241b00c9476c8f4a93ea9`.
Candidate repair: [a24e4b688d46385c6e52d52421bff79737fcefdc](https://github.com/11576865/ASS-Workbench-Android/commit/a24e4b688d46385c6e52d52421bff79737fcefdc).

## Direct evidence vs hypothesis

- Full Android connected suite at the tested head: **187 tests, 4 failures, 0 errors, 0 skipped**; Kotlin/JVM source CI succeeded and both strict native tablet screenshot gates succeeded. This observation concerns only two failures and does not declare the suite green.
- Tool directory: `batchDraftAndReviewedPreviewFollowSameInstanceAcrossMainAndCanvas` failed with “Expected exactly 1 node” on `tool-BATCH` when `performScrollTo()` was called on an item not present in the Compose semantics tree. Production directory presents grouped tools in a `LazyColumn`; the test helper attempted to scroll the uncomposed child. Source-grounded remediation is to scroll the **owning lazy collection** via `performScrollToNode(hasTestTag(...))`, and stabilize filtered list position when query changes. This is a **hypothesis** until the new exact-head emulator result.
- IME rotation: `inspectorDraftSurvivesToolSwitchAndRotation` timed out after 5 seconds reading a captured Espresso root's `WindowInsets.Type.ime()` during a responsive host change. Candidate remediation checks the live Activity root, inspects the focused popup before accepting a no-IME state, and still rejects visible/unknown IME after unsuccessful close. The relationship between stale root and timeout is inferred from control flow, not yet independently reproduced with focused insets diagnostics.
- Two **different, unresolved** failures in the same run remain: pinned spatial rail action `取消驻留` not displayed; `geometry-scale-x-1-value` disposed during `performTextReplacement`.

## Reusable engineering boundary

When an action target is virtualized in a `LazyColumn`, navigation/testing should resolve its owning scrollable collection, not require a node that has not yet been composed. Asynchronous query updates can change the item population and invalidate a previously retained scroll position. After activity/host replacement, stale View references must not be used as the sole authority for present-day IME visibility.

This is a specific observation/candidate test pattern, **not an established Universal or Canonical UI rule**, because the attempted repair has not yet passed exact-head instrumentation. Do not mark either failure resolved before external evidence.

## Foundry dedup

Searched `Compose LazyColumn semantics virtualized scroll search keyboard`, `LazyColumn virtualized search scrollToNode`, `IME stale WindowInsets detached root` and similar terms. No exact matching record found; adjacent canvas/camera and draft-ownership records address different behavior. This record does not change Canonical specifications.

## 2026-10-25 continuation — Event navigator row detaches across responsive host recreation

A distinct exact-head failure was observed at ASS branch `184403cbc649c19926348d623477bd121fc0969a`, [Android emulator run 40105502278](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40105502278). Source/JVM [40105502131](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40105502131) succeeded, while the emulator editor-regression suite emitted an XML receipt with **28 tests / 2 failures / 0 errors / 0 skips** before job failure. The two native tablet screenshot evidence jobs passed separately; no full-suite success or visual parity can be inferred.

The rotation scenario changed window size/density to tablet and back, re-entered the subtitle navigator, waited for `event-row-1` to exist, then called `performScrollTo()` on that row. The logged failure was **"The node is no longer in the tree"** for precisely that tagged row at `EditorRegressionInstrumentedTest.kt:926`; the last-known semantics still contained the expected Event #1 and text. Existence before an action did not guarantee that the target remained a stable scroll authority across responsive host recreation.

Product-side proposed correction [5037c4dd](https://github.com/11576865/ASS-Workbench-Android/commit/5037c4dddb924dda9d53df84ced96341bace24a6) tags the owning Event `LazyColumn` as `event-results-list`; instrumented repair [db4bd189](https://github.com/11576865/ASS-Workbench-Android/commit/db4bd189a8d641ad1762c678f31ee7583bff5882) uses `performScrollToNode(hasTestTag("event-row-1"))` on the list, then still demands that the actual Event row be visible and clickable and that the correct editor draft survives. This does not skip the navigation or relax document-preservation assertions.

The second failed case (`batchKaraokeRevealControlsStayPreviewOnlyUntilCommit`) was listed with an empty failure detail in the compact receipt and is **not diagnosed or marked repaired**. The current row-navigation change remains a candidate until exact-head Android emulator evidence is available. Related prior observation on the tool-directory lazy list and IME stale roots is close enough to extend this record rather than create a duplicate. Canonical remains unchanged.

## 2026-10-25 continuation — Zero-height Event viewport in exact emulator semantics

Exact prior head `e7010ee93459a155a6dd6b5830635ae11b032e1d`, emulator [40135667260](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40135667260) yielded 191 tests / 26 failures; among them, `inspectorDraftSurvivesToolSwitchAndRotation` failed with `No node found that matches TestTag = 'event-row-1' in scrollable container` after compact/landscape/tablet size and density transitions. The owning `event-results-list` semantics had bounds `l=128, t=911, r=861, b=911` px, **zero viewport height**, despite collection info rowCount=2 and vertical scrolling semantics. The previous `performScrollToNode` target change did not restore a nonzero viewport. This evidence is distinct from the 23 other invalid pinned-catalog scroll operations in the same run.

Source review found `EventWorkspace`'s LazyColumn used `Modifier.weight(1f)` for `r3Chrome` but `Modifier.fillMaxSize()` in other hosts. It is nested below a navigator header and result actions, within finite adaptive inspector/list panes. Product repair [578da44f](https://github.com/11576865/ASS-Workbench-Android/commit/578da44f4285af675ed9f6e423298c5664620b99) uses `weight(1f)` consistently for the real Event list, allocating the remaining constrained Column height instead of asking non-R3 variants to fill the parent's entire maximum. This is a layout hypothesis grounded in code and failure semantics; it is **not yet a demonstrated root-cause closure**.

Regression strengthening [f33ee695](https://github.com/11576865/ASS-Workbench-Android/commit/f33ee69568580f9bf31cbb1a2601237cf5598565) explicitly requires the real `event-results-list` to be visible and have `boundsInRoot.height > 0` after viewport/density reset, before performing the existing real row scroll/click/inspector draft restoration check. This keeps rather than suppresses assertions.

Separately, exact previous head `d5285374617bcc68e4c5c0bd08f80195731603ef` [source run 40176279488](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40176279488) failed at `compileDebugAndroidTestKotlin`, with one compiler issue: a missing `assertIsDisplayed` import in `FixedV11PageChromeInstrumentedTest.kt:36`; emulator run `40176279531` therefore stopped at prebuild (no executable device suite). Import fix [6c04069a](https://github.com/11576865/ASS-Workbench-Android/commit/6c04069ae01be0ee86a6bc9b8d7c732cce368b5b) restores the intended assertion. No claim of 23/26 regression recovery can be made on an Android build that did not compile.

Classification: same ASS Compose responsive navigation failure family; existing Observation extended, no duplicate Candidate, no Canonical promotion. New exact-head CI and emulator evidence PENDING.

## 2026-10-26 continuation — compact outer viewport reentry

Evidence at ASS branch `ddcf1ac593fbd7e31402a47201b66b3d9bcacdaa`: [FIXED source/JVM run 40190966030](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40190966030) **success**; [Android Emulator Regression run 40190966056](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40190966056) **failure** with **191 tests / 5 failures / 0 errors / 0 skipped** in its full connected receipt. The prior 23 invalid pinned-catalog scroll errors did not recur. Both full-size PNG evidence checks **failed** because a complete R3 PNG was absent; there is no current visual acceptance at this SHA.

The rotation test `inspectorDraftSurvivesToolSwitchAndRotation` still fails at `EditorRegressionInstrumentedTest.kt:924`: `event-results-list` **not displayed** after moving from expanded tablet back to compact window. Earlier run `40135667260` recorded zero-height clipped bounds for the same Event list. The inner `LazyColumn.weight(1f)` change by itself did not establish that the *outer compact scroll viewport* brought the navigator into view. Source `FixedWorkspace` puts the preview/preview-size controls before a bounded editor pane inside a vertical `fixed-content-flow` scroll. When returning to the SUBTITLES task after responsive host reconstruction, the navigator can exist but remain wholly clipped by that outer scroll.

Production follow-up [c47d12f7](https://github.com/11576865/ASS-Workbench-Android/commit/c47d12f78bf87018e1db7e24dec6cbcfc5177519) changes COMPACT `FixedWorkspace` to retain its actual outer `ScrollState`, wait for a positive measured max scroll when SUBTITLES is requested, and scroll to the editor content. It does not fake Event rows or alter ASS data, focus, undo/redo, or drafts. The prior rotation regression already asserts an *actually displayed* positive-height Event viewport, real row activation, and draft persistence; new exact-head emulator results are pending.

A separate SPATIAL tool-picker failure at the same run (`unifiedCanvasCanOpenNativePositionEditorWithoutASecondPrecisionUi`) had an explicit `hideKeyboard()` between searching POSITION and selecting `tool-POSITION`, despite that shared modal being an IME-owned, virtualized LazyColumn. Instrumentation [c4cab947](https://github.com/11576865/ASS-Workbench-Android/commit/c4cab9474b3d64f57dbf45b1e6dc9e727ff73159) now uses `performScrollToNode(hasTestTag("tool-POSITION"))` on `tool-results-list` without dismissing the search IME, retaining the actual POSITION editor and precision-mode assertions. That is a test-driver repair, not a separately verified production bug fix.

**Status:** source-diagnosed candidate corrections, latest exact-head CI and emulator PENDING; SPATIAL pin and Transform controls remain open. Existing Observation extended after deduplication, Canonical unchanged.
