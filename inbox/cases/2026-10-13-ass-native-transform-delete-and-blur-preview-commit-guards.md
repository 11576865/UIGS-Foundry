# Case: Native ASS Transform removal and Blur interaction honor source/draft commit boundaries

Date: 2026-10-13
Status: Case / committed to Android main; Android CI and emulator acceptance Pending
Project: 11576865/ASS-Workbench-Android
Related: inbox/cases/2026-10-13-ass-native-transform-draft-survival-source-guarded-commit.md

## Trigger
The owner requested continued implementation on main. Source audit after Transform draft persistence found two unguarded paths: delete-Transform still operated directly by index despite externally changed Raw ASS or dirty sibling drafts, and Blur slider released a document edit automatically even though a separate Apply button suggested a staged preview.

## Native changes
- Added EditorViewModel.removeEventTransformIfSourceMatches with canonical Event text recheck inside document edit transaction. No current source match -> no remove, no history mutation. Existing edit history preserves Undo when matching.
- Added TransformDraftStore.hasDirtyInEvent. The visible Delete action in InlineTransformCard is disabled whenever any Transform draft in the Event is dirty, or when the selected Event source conflicts. This prevents a deletion from renumbering the target of a sibling draft. Route uses guarded ViewModel method.
- Blur ContinuousParameterControl now supplies only transient preview during slider dragging/stepping; explicit Apply is the only write boundary. The Apply control rejects invalid non-finite/non-numeric input rather than silently interpreting it as removing Blur. Legitimate empty text remains a request to clear Blur.
- Added native ViewModel guarded Blur apply and preview entry points comparing whole expected Event source to current source; stale proposals never mutate the document or render a preview over a newer canonical Event. Existing unknown tags are handled by existing domain patcher rather than a new HTML writer.
- Added Android instrumentation assertions for stale deletion rejection, unchanged unrelated overrides, Undo recovery, disabled dirty/conflict Remove control, stale Blur preview and Apply rejection. Test source is committed; these are not test-run success claims.

## Exact repository commits
bf48e22550b23300886047749891abec04af8a46 guarded Transform removal.
c4ea5de4f03592be1f06f8615064167a7d588a6d dirty-sibling finder.
97a302384124406661586d2b15a1eeb21f34e175 native disabled deletion on dirty/conflict.
93e8e9a7491277bf5bf09824121cf13b8d4a9efa deletion regression assertions.
d6c23ab06aa1e6f55324bfed58fe3e218f81902f Blur slider does not auto-commit.
94daebf41776945768537e19a17d27e98ed8f3b3 source-guarded native Blur Apply.
986e8a78345a9999a942ac700576875eb6e17d43 native explicit Apply + validation.
109d6ba9611c6f9aba30890ff30b4bb30cd1c69a source-checked Blur preview.
406f92a321cb70f000a5b2532ec7cf86993d72c8 UI preview wired to guard.
f176383c4218e407079494b9e44f62ed752bf8b5 Android regression tests.
ce9376dff05ac00ac7961fc9a9aa07597f29cb5a project progress checkpoint.

## Verification boundary
All native source and tests were committed to main via GitHub. Container Java/Kotlinc exists but no Android Gradle SDK/build cache/repository checkout; attempting git ls-remote failed because github.com DNS unavailable. No native build, JVM test run, emulator instrumented run, screenshot, or device gesture verification was performed. Do not label this work as Android-accepted.

## Reusable lesson
A control that looks like an explicit Apply workflow must not also commit during release of a continuous gesture. Editor UI preview and the final canonical authoring transaction should independently verify Event source identity before modifying any index-addressed ASS tag. Index-shifting operations must also account for outstanding sibling drafts. Rejecting an unsafe operation is preferable to silently discarding or retargeting user edits.

## Dedupe and governance
Searches: ASS Transform deletion dirty sibling drafts source guarded viewmodel; Blur slider implicit commit preview-only explicit Apply ASS Android; ASS native blur source guard stale preview transform removal. No equivalent native Case was found. No automatic Canonical promotion.