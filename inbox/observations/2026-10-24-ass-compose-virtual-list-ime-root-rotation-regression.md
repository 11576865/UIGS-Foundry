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
