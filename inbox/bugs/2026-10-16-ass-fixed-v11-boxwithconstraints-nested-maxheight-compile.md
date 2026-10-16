# Bug — FIXED V1.1 compact-layout nested Compose receiver breaks Android Kotlin compilation

Date: 2026-10-16
Status: **Repair Committed / External Validation Pending**
Product: https://github.com/11576865/ASS-Workbench-Android
Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Affected branch: `feat/fixed-v11-event-grid-20261016`
Failing CI: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38885202379
Job ID: `116921246085`
Failing tested head: `b61de8748872043c9700698df93c127d09ef0f0d`
Source repair commit: `324b50d7e2d34448be065e1aabd2f80aa379d420`
Task/checkpoint commit: `77ed585480bea5510ee23ff54612e9bb4f748b38`

## Reproduction/evidence
PR-triggered `FIXED V1.1 Branch Validation` completed with **failure**, in step `Compile Android and all instrumentation sources` while running `:app:compileDebugKotlin`. Job logs report exactly two Kotlin diagnostics:
- `ModernEditorScreen.kt:1351:41` — `'val maxHeight: Dp' cannot be called in this context with an implicit receiver. Use an explicit receiver if necessary.`
- `ModernEditorScreen.kt:1366:51` — same diagnostic.

These are references to `maxHeight.value` from a nested `Column` / `Box` composition inside the outer `BoxWithConstraints` of FIXED's compact-tablet two-pane video/timeline. The compiler cannot resolve the outer implicit `BoxWithConstraintsScope` receiver at the inner call site. Core Kotlin compilation had already proceeded; app compile failed and JVM tests were skipped. The observed error is a compile-time receiver scope error, not evidence of video/libass or ASS domain failure.

## Bounded repair
Changed only `app/src/main/kotlin/io/github/assworkbench/app/ui/ModernEditorScreen.kt`:
1. Capture `val availableHeightDp = maxHeight.value` directly in the outer `BoxWithConstraints` scope.
2. Replace the nested `maxHeight.value * 0.43f` media-height cap with `availableHeightDp * 0.43f`.
3. Replace the nested `maxHeight.value < 620f || imeVisible` timeline compact flag with `availableHeightDp < 620f || imeVisible`.

No Feature/Tool IDs, Binding, Focus/Selection, document drafts, renderer or SPATIAL host were changed. Root-height semantics are preserved at the same numeric value.

## Verification boundaries and next step
The failing run is real evidence; the repair is source-level only. No passing post-repair compile result was observed, and no emulator, screenshot or physical tablet tests were run in this unit. Product AGENTS execution rule calls for one bounded repair and no polling the new generation. The next work unit must inspect one authoritative post-repair exact-head CI result (and address a visible new failure only in its own bounded unit).

## UIGS dedup and status
Searched Foundry for `ASS FIXED V1.1 maxHeight nested Compose receiver CI 38885202379`, `BoxWithConstraints maxHeight cannot be called with implicit receiver Kotlin nested Row`, `ASS Android PR149 compile receiver scope failure`. No matching prior report. The earlier stacked-PR workflow trigger observation is adjacent but not duplicate. Record this as a **Bug**, not Canonical. Do not generalize a one-time incident into a universal architecture rule without broader test evidence.
