# Case / Bug Evidence — FIXED V1.1 first full Android emulator suite: two test semantics errors and five unresolved regressions

Date: 2026-10-17
Status: **Source fixes committed; emulator revalidation Pending; do not promote to Canonical**
Product: https://github.com/11576865/ASS-Workbench-Android
Draft stacked PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Tested head: `a79e8c20ea112cf8c2f3ed9f9c9f1b192be31ab0`
Actual emulator CI: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38906758867
Editor regression job: `116992666366`
Native screenshot: `ASS.R3.FIXED.PRODUCTION_REFERENCE.png` was validated, size 145269 bytes, 1600×960, SHA-256 `26ee6884ae28449e661121bcf9cf3fad711a06a4198e348a4bdf2c62be5f7d7c` (image not asserted to be downloaded or individually inspected outside job)
Source compile/JVM CI at same original head: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38906758860 (SUCCESS)
Scoped source fixes: `14c7f4ca6d8f79891f546624d0b1e4755e5765eb` and `a29a42ce1bc779837d835881688eb2c7e3f81ce9`
Durable task checkpoint: `c46d721e018c46d076444972fb068b4ad21abb98`

## Observed facts (not interpretations)
Existing emulator job successfully prepared native MKV bridge, prebuilt app and instrumentation APKs, started emulator, and executed the R3 strict visual-capture test. The capture log explicitly recorded R3_INSTRUMENTATION_SUCCESS, R3_NATIVE_CAPTURE_VALID with SHA and R3_CAPTURE_EXIT_STATUS=0. Each of four parameter projection test families finished with zero failures. The mandatory full AndroidTest suite then reported **171 tests, 7 failures, 0 errors, 0 skipped**, causing entire workflow FAILURE. The separate emulator-evidence job succeeded at reading failure evidence; this cannot turn the editor-regression failure into a pass.

New FIXED V1.1-owned failures (2):
- `FixedV11EventGridInstrumentedTest.wideGridExposesEventTimesStyleAndTextWithoutAddingEditorState`: `assertIsDisplayed` on the structural fields `Row` semantics tag reported non-displayed despite the tagged event row being displayed. Corrected test to assert structural Row exists in unmerged semantics and retain/extend independently painted Event #39, time, Style and text visibility assertions. **No production UI change.**
- `FixedV11WorkspaceTabsInstrumentedTest.readOnlyTimingContextDoesNotInventMissingEventTarget`: the UI **actually contained** `媒体 PTS 80800 ms · 时间轴与视频共享时钟` in the failure's Compose semantic dump. Original `assertTextContains("80800 ms")` in this version matched exact by default, so changed to `assertTextEquals` with the full observed label. No app state, clock or rendering change.

Other live failures (5, attribution pending; NOT dismissed):
1. `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation` — 5s Compose condition timeout.
2. `EditorRegressionInstrumentedTest.spatialWorkspaceExposesBoardAndNativeEditorWithoutMovingWorldNodes` — unpin `取消驻留` not displayed.
3. `EditorRegressionInstrumentedTest.batchActionsRemainAboveVisibleKeyboardAcrossMainAndCanvas` — `tool-BATCH` absent.
4. `EditorRegressionInstrumentedTest.batchUsesSharedResultsAndRequiresFreshPreviewAfterScopeChangeAcrossHosts` — `tool-BATCH` absent.
5. `UigsToolInstanceVisualCaptureInstrumentedTest.capturePinnedDuplicatedAndResizedPositionSurfaceLandscape` — `tool-POSITION` absent.

These could be upstream R3 surface changes or affected by FIXED rollout; establish baseline attribution with exact parent commit before modifying production behavior. User has deferred SPATIAL UI work, and no SPATIAL production code was changed in this bounded unit. Do not disable these tests or claim compatibility.

## Current scope and validation caveat
FIXED V1.1 owner frozen Figma implementation page `85:2` contains 1440×900 and 1024×768 target screens. R3's 1600×960 artifact validates capture transport, **not FIXED V1.1 target visual parity**. No target-size images, physical tablet report, true IME/draft scenario acceptance, or full Android instrumented suite pass yet.

A single source fix generation corrected the two V1.1 test assertions above. The follow-up exact-head CI **was not polled** in the same work unit under repository AGENTS.md async-CI rule. Next unit must check actual run and investigate remaining cases without asserting a pass.

## Reusable bounded lesson and governance
In Compose tests, a tagged structural grouping node may exist but not be an independently painted surface; distinguish semantic existence from visible user-cell assertions. Also distinguish exact vs substring text expectations, especially for provenance/PTS labels. Do not rewrite real product behavior solely to satisfy a mistaken assertion; also do not use assertion fixes to hide unrelated genuine failures. This is a verified CI-specific Case/Bug observation, **not a new UIGS Canonical rule**.

## Dedup
Foundry searched: `FIXED V1.1 Android Emulator Regression 38906758867 seven tests failed screenshot sha256`; `FixedV11EventGridInstrumentedTest structural Row assertIsDisplayed PTS assertTextContains semantics`; `ASS Workbench android actual 171 tests 7 failed pinned batch position`. A nearby 2026-10-14 R3 native-evidence Observation exists but does not cover this exact run, latest FIXED regression or two V1.1 test assertions.


## Follow-up 2026-10-17: 171/4 emulator and source width correction (not yet validated)

The post-AndroidTest-import FIXED V1.1 source CI #38930055526 **passed** at exact head `90633f8a965b59781fcba40835adfe143561b72e`. Its companion [emulator run #38930055528](https://github.com/11576865/ASS-Workbench-Android/actions/runs/38930055528) executed the full suite: **171 tests, four failures, zero errors**, down from prior seven. Prebuilt APK/native R3 capture and all four projection test families succeeded. The previous timing PTS assertion and tool POSITION / some BATCH case failures were no longer in this run's failing list; do not infer they are globally fixed.

The four remaining failures in this newer run are:
- `FixedV11EventGridInstrumentedTest.wideGridExposesEventTimesStyleAndTextWithoutAddingEditorState`: the `fixed-v11-grid-text-39` Text was not displayed (now a genuine rendered-cell visibility check, not the earlier structural Row assertion).
- `EditorRegressionInstrumentedTest.inspectorDraftSurvivesToolSwitchAndRotation`: 5-second timeout in the `hideKeyboard` helper reached via `showFixedSubtitleList`, before proving whether the draft itself survived. Do not label this a proven data loss.
- `EditorRegressionInstrumentedTest.batchDraftAndReviewedPreviewFollowSameInstanceAcrossMainAndCanvas`: tag `tool-BATCH` not found when opening the tool.
- `EditorRegressionInstrumentedTest.spatialWorkspaceExposesBoardAndNativeEditorWithoutMovingWorldNodes`: `取消驻留` control not displayed. SPATIAL production UI is explicitly out of scope for this FIXED increment.

Inspection of `FixedV11EventGridRow` showed its second `Row` (subtitle text + QC) had no `Modifier.fillMaxWidth()`, yet its text `Text` used `Modifier.weight(1f)`. This can yield zero-width text when Row measures wrap content. **One bounded production fix** adds `fillMaxWidth()` to give the weighted text definite width, preserving its strict display test and same Event/selection/data state. Product source commit `18f09bf3dbbf285028248dd6061a17eb847bfcce`; task checkpoint `8d91fc36840ec5dadc35594ec6fc06cf729baebc`. This is a hypothesis-backed remedy, **NOT YET confirmed** by a post-repair emulator result. Do not declare regression green or merge PR #149.

UIGS intake dedup queries for this exact 171/4 run, weighted Row issue and remaining IME/BATCH/SPATIAL symptoms yielded no duplicate Foundry case. Extend this existing first-emulator-suite case rather than open a duplicative report. **Canonical remains unchanged.**
