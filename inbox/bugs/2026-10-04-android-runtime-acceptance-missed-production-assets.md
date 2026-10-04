# Bug: Android runtime acceptance packaged code without production web assets

Date: 2026-10-04
Status: Bug
Lifecycle: regression-verified
Scope: Android emulator acceptance / packaged runtime dependencies / production asset staging

## Symptom

An Android emulator acceptance test reached the real EncodeService and failed a hardsub case with:

`内置 Noto Sans SC 回退字体不可用`

The application code and FFmpegKit runtime were present, but the APK built by this dedicated acceptance workflow did not contain the production web asset tree that normally carries the bundled fallback font.

## Cause

The normal Android build path performs two production-staging steps before assembling the APK:

1. fetch the pinned Noto Sans SC fallback font into `public/vendor/fallback-fonts`;
2. build the Web UI and copy `dist/` into `android-native/app/src/main/assets/www/`.

The emulator acceptance workflow generated only its test fixtures and then invoked Gradle directly. It therefore tested a packaging variant that omitted a required production runtime dependency.

## Fix pattern

Runtime-backed acceptance must reproduce the packaging prerequisites of the production build, not only compile the same Kotlin/Java code.

For this project the acceptance workflow now:
- downloads the same pinned fallback font;
- builds the Web assets;
- stages `dist/` into the APK asset tree;
- asserts the fallback font exists at the exact runtime asset path before starting the emulator.

## Reusable implication

A runtime acceptance test is authoritative only for the artifact it actually constructs. If the test path omits production packaging/staging steps, a failure may diagnose the test artifact rather than the product runtime.

Prefer one reusable packaging step or explicit parity assertions between production build and acceptance workflows.

Do not promote to Canonical from this single bug observation.


## Validation evidence

Quick-Automatic-Hardsub-Encoder PR #61 merged after Android Stream Plan v4 emulator runtime acceptance run 37206272016 completed successfully. That workflow stages the production Web assets and pinned fallback font before assembling the Android test artifact, then executes the real MainActivity + EncodeService matrix and independently verifies exported outputs.

This regression evidence verifies the packaging-parity repair for the acceptance path; it does not imply arbitrary device/OEM acceptance.
