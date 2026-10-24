# Bug — ASS Text and opaque extension columns silently lose edge whitespace

Date: 2026-10-24
Lifecycle: **Source-confirmed defect; repair submitted; validation pending**
Source project: [ASS-Workbench-Android](https://github.com/11576865/ASS-Workbench-Android)
Source PR: [#149 (Draft)](https://github.com/11576865/ASS-Workbench-Android/pull/149), branch `feat/fixed-v11-event-grid-20261016`
Severity: **Data integrity / import-save round-trip fidelity**

## Direct code evidence

At the branch before repair, `core/domain/src/main/kotlin/io/github/assworkbench/domain/AssCodec.kt` parsed each comma-separated Event field with `.trim()` indiscriminately, including `Text` and unrecognized vendor-defined fields in `Format:`. The Style parser did the same to unrecognized Style columns.

This loses the first/last spaces of actual subtitle text and opaque extension values when an ASS document is opened, even if the user does not edit those fields. Once parsed, serialization cannot reconstruct the removed characters. This is not a visual padding issue: `Text` is content payload; unknown columns must not be normalized on behalf of an editor that does not understand their semantics.

The source confirms the transforming code path, but no real user file or physical-device reproduction is claimed.

## Bounded repair and falsifiable tests

Product repair: [6e698c53](https://github.com/11576865/ASS-Workbench-Android/commit/6e698c53be6f0982c6409d8f01fe8abea6a2a8dc).
Tests: [30cc5770](https://github.com/11576865/ASS-Workbench-Android/commit/30cc5770d09df1cd9336b7a7d824f64d698ffe79), refined at [dd1ffe1d](https://github.com/11576865/ASS-Workbench-Android/commit/dd1ffe1d22f23f29485428e4e48c9203f881f996).

- Normalize recognized typed ASS fields as before, but preserve `Text` and unknown Event/Style columns as raw values.
- Add parse/write/parse tests for leading/trailing spaces, literal commas, inline ASS tags, vendor extension columns, and whitespace-only text.
- Add a full five-group Event edit review → ASS serialization → reopen regression covering content, timing, metadata, Style reference, margins, unknown sections, and untouched sibling Events.
- The regression compares opaque sections semantically, ignoring only incidental section-edge blank lines; it still asserts the actual unknown payload is present.

**Evidence:** product source and test cases have been committed. Kotlin/JVM/Android CI result for this repair, external real media, and user-device acceptance are **Pending External Validation**. The exact current PR head should be used for validation. Do not count this as a passing or field-fixed issue until a relevant test receipt is available.

## Reusable engineering observation

An importer's typed-field normalization boundary must distinguish **recognized schema data** from **literal content/opaque extensions**. Applying universal whitespace trimming to a row model can silently destroy information during otherwise unrelated editing. This observation remains attached to this specific defect; it does not automatically amend UIGS Canonical specifications.

## Dedup

Searched Foundry for `ASS Text trim whitespace raw preserve`, `opaque vendor columns`, `AssCodec` and `trim()`. No exact record found. The adjacent 2026-10-24 ASS Compose lazy-directory/IME observation concerns a different interaction failure.

## 2026-10-24 implementation continuation — Android Save/Readback integration

The initial patch's GitHub Actions generation (branch checkpoint `c00c27e2`) failed **before full test execution**. Both [FIXED branch validation run 40080008476](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40080008476) and [Emulator run 40080008481](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40080008481) stopped at `:app:compileDebugAndroidTestKotlin`. Job log pinpoints `EditorRegressionInstrumentedTest.kt:2058`: Kotlin rejects an impossible `ComposeTimeoutException` type check against `Exception` (the Compose timeout is an `AssertionError`). This is an unrelated **test-harness compile blocker**; it is not evidence that the ASS parser repair passed or failed its new assertions.

Repair commit [54489d43](https://github.com/11576865/ASS-Workbench-Android/commit/54489d43a091a3f3ca501b6a01b0b88f6d614720) changes the bounded IME handling to `catch (Throwable)` but only treats the two expected transitional errors (`NoMatchingRootException` / `ComposeTimeoutException`) as acceptable **when current Activity insets prove IME hidden**. Unexpected exceptions and unknown/visible IME remain strict failures. The failure mechanism and the new guard are source-reviewed; new exact-head compilation remains pending.

Added Android instrumented integration in [a457cb9f](https://github.com/11576865/ASS-Workbench-Android/commit/a457cb9f133b73575a106d817aa8532829173a3b): the real `EditorViewModel.applyEventEditReview` performs all five groups with one Undo/Redo; `EditorViewModel.saveTo` invokes production `SafeSubtitleSave` against the existing debug ContentProvider with read-back; the test decodes and reparses the saved bytes, asserting exact `Text` whitespace/ASS tags, custom Event/Style columns, sibling Event, unknown sections, and no false dirty state.

**Status:** test source committed, JVM and Android execution PENDING. No user-file reproduction, emulator success, or Canonical promotion is inferred.
