# Bug — FIXED V1.1 AndroidTest import breaks stacked CI and emulator prebuild

Date: 2026-10-17
Status: **One source repair committed / post-fix external validation PENDING**
Product: https://github.com/11576865/ASS-Workbench-Android
Stacked Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Tested head: `c46d721e018c46d076444972fb068b4ad21abb98`
Failing source CI: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38928965389
Failing emulator workflow: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38928965421
Bounded fix: `139afdfadd3c81d2bff6566f074d2fcd999bf9f4`
Durable task checkpoint: `90633f8a965b59781fcba40835adfe143561b72e`

## Verified failure
Prior emulator run #38906758867 had executed a full 171-test Android suite, with seven failures including two assertions in newly authored FIXED V1.1 tests. Subsequent assertion changes included an invalid top-level Kotlin import `import androidx.compose.ui.test.assertExists` in `FixedV11EventGridInstrumentedTest.kt`.

In post-assertion exact-head GitHub Actions `FIXED V1.1 Branch Validation` #38928965389, step `Compile Android and all instrumentation sources` failed in `:app:compileDebugAndroidTestKotlin` with `FixedV11EventGridInstrumentedTest.kt:6:33 Unresolved reference 'assertExists'`. The prebuild step of `Android Emulator Regression` #38928965421 failed on precisely the same compilation diagnostic. Emulator KVM/setup/test suite was skipped in the latter run, so this is **not** a new runtime test observation.

## Repair applied
Only removed the invalid top-level import from the Android test file. The existing `SemanticsNodeInteraction.assertExists()` method call remains inside the unmerged-tree tagged node assertion; no assertions or other regressions were disabled or weakened, and no production `ModernEditorScreen` or SPATIAL files changed.

## Evidence boundaries
The repair was committed to the same stacked FIXED feature branch; the follow-up CI/emulator result was deliberately **not** polled under repository AGENTS.md bounded-unit rule. The prior full emulator suite's five other failures (inspector draft/rotation timeout, spatial unpin visibility, BATCH entries twice, POSITION entry) remain open until a green AndroidTest compile and targeted emulator evidence. Prior tested source/JVM at `a79e8c20` did pass; current head does not yet have a claimed passing run.

## UIGS intake / dedup
Foundry searched `FixedV11EventGridInstrumentedTest invalid top-level assertExists import AndroidTest compile CI 38928965389`, `ASS workbench 38928965421 emulator prebuild same assertExists unresolved`, and `Compose SemanticsNodeInteraction assertExists member import Kotlin` with no matching exact Bug. Adjacent prior emulator seven-failure Case documents why the assertion was modified, not the faulty import. This is a bounded Bug/learning about API/member vs import ambiguity in Compose tests, **not** a Canonical amendment.
