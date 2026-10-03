# Bug: JVM regex tests can miss Android ICU pattern syntax failures

Date: 2026-10-03
Status: Bug
Scope: Kotlin / Java regex portability / Android instrumentation / shared domain code

## Symptom

A regex used in shared Kotlin domain code passed JVM unit tests and the Android build, but failed at runtime on the Android emulator with:

`java.util.regex.PatternSyntaxException: Syntax error in regexp pattern`

The pattern was:

`\{[^}]*}`

The unescaped closing brace was accepted by the host JVM regex engine used by unit tests, but rejected by Android's ICU-backed `java.util.regex.Pattern` implementation when the code path executed in instrumentation.

## Concrete evidence

ASS Workbench Android PR #84, Android Emulator Regression run #438:

- Android CI and JVM unit tests passed.
- The production-renderer instrumentation test `captureSpatialReflectionFadeRuntimeLandscape` executed the shared `AssFxComposition.overrideBlocks` helper on-device.
- Android threw `PatternSyntaxException` at the regex constructor before rendering.
- The fix changed the pattern to `\{[^}]*\}`, escaping both literal braces.

## Reusable lesson

For regex used in Android runtime code:

1. Do not treat host-JVM regex acceptance as proof of Android runtime compatibility.
2. Escape paired literal metacharacters explicitly even when one engine tolerates an ambiguous form.
3. Keep at least one Android instrumentation path that executes regex-heavy shared-domain parsing used by production UI/rendering.
4. When CI differs between JVM tests and instrumentation, inspect the runtime regex engine before classifying the failure as renderer/UI flakiness.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #84
- failing workflow: Android Emulator Regression #438
- failure: `PatternSyntaxException` in `AssFxComposition.overrideBlocks`
- repair commit: `46cfd8df3a70e716bd8f55521008fd1c055d77e6`
- deduplication: searched UIGS-Foundry for Android ICU / JVM regex brace portability; no direct duplicate found

This is a Bug record, not a Canonical rule.
