# Bug — R3 Android screenshot gate falsely accepted a 52-byte non-PNG

Date: 2026-10-14
Classification: Bug / test-evidence integrity; **not** an Android production UI bug.
Source: ASS-Workbench-Android Draft PR #148 (run 38522507918, editor-regression job 115715275138).
Status: Fix candidate committed on `feat/r3-fixed-visual-layout-20261014`; **Pending exact-head CI** and real PNG proof.

## Actual observed failure

For GitHub Actions Emulator Regression on PR #148 head `d88c24423b17194746e78e73f5a5c3f9abf45a90`:
- Log printed `Override size: 1600x960`, `Override density: 160`.
- Targeted `UigsVisualCaptureInstrumentedTest#captureR3FixedReferenceWhenExpanded` reported `org.junit.AssumptionViolatedException: R3 three-column reference requires expanded window`.
- Shell then printed **`R3_NATIVE_CAPTURE_PRESENT: ... size=52`** and **`R3_CAPTURE_EXIT_STATUS=0`**. The 52-byte output was not a real 1600x960 PNG and is not valid screenshot evidence.
- The earlier full emulator suite timed out (exit 124) and had no XML result, so workflow nevertheless failed; the false-positive R3-capture line would have misled review if read without the context.

## Root conditions

1. `wm size 1600x960` and `user_rotation 1` alone do not guarantee a reported 1180dp+ LANDSCAPE content configuration on the portrait-native Pixel 6 emulator. The Kotlin capture test previously used `assumeTrue`, allowing a skipped test.
2. Capture script treated a successful shell command or a non-empty redirected output file as proof of a screenshot; `adb exec-out run-as ... cat ...` can emit plaintext failure messages. Original `if ! ... || [[ ! -s output ]] ; then ... else PRESENT` logic additionally had the wrong Boolean semantics.

## Correction committed to product PR #148

- Kotlin capture test explicitly requests `SCREEN_ORIENTATION_LANDSCAPE`, waits for real landscape configuration, and uses a detailed hard `check(...)` if the expanded width/height is absent. No silent assume-skip.
- Emulator uses 960x1600 portrait-native override, rotates to landscape, sets 160dpi, then restores display metrics.
- Strict Python validator `tools/verify_r3_png_capture.py` checks PNG signature, IHDR dimensions 1600x960, chunk CRCs, IEND, decompressed pixel size and scanline filters. Fails closed on short, text, corrupt or rotated outputs.
- `tools/test_verify_r3_png_capture.py` provides five regression cases: valid PNG, 52-byte-ish run-as text, 960x1600 dimensions, damaged CRC and truncated file. Android CI runs these before building.
- Dedicated screenshot attempt moved **before** the long suite to avoid getting starved by 35-minute workflow budget. The full suite remains a mandatory independent gate.
- Product commits at least: `ab72453c`, `52c7bfdf`, `f3e81069`, `d82ea7b4`, `dbd4991c`; latest observed exact head `dbd4991c85c0c3958368bb7fef0bd9e4c11a10ba`.

## Evidence levels

A PNG passing file validation proves only that a decodable correctly sized compositor bitmap was collected; **not** that it matches R3 design, carries a genuine playing video, or has preserved all historical capabilities. The existing debug fixture uses two recovered subtitle lines, no video and renderer disabled. Actual R3 visual comparison with reference assets and media still awaits follow-up evidence. PR #148 stays Draft.

## Reusable lesson (Observation from a Bug)

Device geometry must be asserted at the Activity configuration *after* orientation and density changes, and screenshot authenticity requires a parser / decoder rather than non-emptiness or command exit status. Capture condition, artifact integrity and visual similarity are **three distinct gates**; never conflate them.

## Dedupe & promotion

Searched UIGS-Foundry for `R3_NATIVE_CAPTURE_PRESENT 52 size false positive adb exec-out run-as`, `PNG capture test artifact misclassified shell precedence screenshot`, and `emulator wm size landscape orientation pixel6 R3 capture`; no exact duplicate found. Record as Bug with verification pending; no Canonical change based solely on this observation.

## Follow-up evidence & repair, 2026-10-14 later window

At product PR #148 commit `dbd4991c`, run `38533498685` job `115750818069` completed **the single expanded R3 compositor test successfully** (`tests=1 failures=0 errors=0 skipped=0`) after correcting orientation and fail-closed assumptions. The debug test wrote a file with Android `UiAutomation.takeScreenshot()`, but the runner's `adb exec-out run-as io.github.assworkbench.app cat files/...` exported a short / invalid payload. The stricter validator correctly printed `R3_NATIVE_CAPTURE_INVALID`, so the screenshot was **not accepted**. Later projection sub-suites were green (9,3,7,3 tests) but the full emulator suite reached the deadline, with no XML, and remained failed.

A second extraction-path repair was committed to the same Draft branch, `2aed1586` and `0c7ba6c1`: the debug-only capture test now mirrors the original PNG to `targetContext.getExternalFilesDir("uigs-capture")` for ADB retrieval and outputs bounded, 900px, compressed JPEG review chunks tagged `R3_PREVIEW_JPEG` to logcat (same compositor bitmap; lower-resolution review only). The shell first attempts the external debug mirror with strict PNG validation, then app-private `run-as` fallback; failure prints bounded file-byte and path diagnostics. A JPEG thumbnail or target test green result **does not** satisfy the full-resolution 1600×960 PNG requirement. Exact-head Android CI `38540873674` passed; emulator `38540873687` and Fontconfig `38540873673` still in progress at last observation. Status **Pending screenshot extraction + visual diff**, with PR remaining Draft.

## 2026-10-14 19:35+08 — Exact cause and third recovery implementation

Checked PR #148 head `0c7ba6c196344744130a626c36cc32deb0a1d96c` Emulator run `38540873687`, editor-regression job `115775453129`. Expanded compositor test itself succeeded, **1/0/0/0**; Android log recorded `R3_NATIVE_FILE:/storage/emulated/0/Android/data/io.github.assworkbench.app/files/uigs-capture/ASS.R3.FIXED.PRODUCTION_REFERENCE.png:bytes=146689`. But `adb exec-out cat /sdcard/Android/data/io.github.assworkbench.app/...` returned no file, and `adb shell run-as io.github.assworkbench.app` reported **`unknown package`** after Gradle connected instrumentation finished. So this is principally an extraction-lifetime bug (test host removed before adb retrieval), not a failed screenshot encoding test.

The same logged compositor JPEG thumbnail was reconstructed from 12 correctly ordered `R3_PREVIEW_JPEG` chunks (900px wide). Visual inspection disclosed a system alert **`Pixel Launcher isn't responding`** over the UI, real black preview because the debug host has no attached media, and actual fixed three-pane content beneath. This is not a design-compatible clean native screenshot; accepting only geometry/CRC would miss the occlusion.

Follow-on PR #148 commits `8c6c6f74`, `46d1e179`, `7f5e2898`, `42ce5f98`, `f2764089`, `7d7b57a4`:
- Android instrumentation streams the original PNG into bounded indexed Base64 Android logcat lines before the app/test package is removed, with filename, exact byte count, SHA-256 and chunk count envelope; thumbnail remains strictly supplemental.
- `tools/extract_r3_png_logcat.py` reconstructs **one** full PNG only if count/index ordering/completeness/base64/byte count/SHA agree; `verify_r3_png_capture.py` continues verifying PNG signature, CRC, exact 1600x960 and image stream. Five+ focused negative regression cases in `tools/test_extract_r3_png_logcat.py` run in Android CI; the test workflow now checks both extract and decode validators.
- `run_emulator_regression.sh` clears and enlarges logcat, keeps ADB paths as fast-path, falls back to strict logcat envelope after Gradle returns. Captures remain a separate gate.
- UI instrumentation rejects R3 screenshots if Android's foreground accessibility root package is not the target app (system ANR/permission overlay).
- All remain **Pending exact-head Android CI / Emulator / Native PNG proof** at time of update. This does not establish video/render fidelity or complete historical capability parity; **no Canonical change**.

Transferable evidence rule learned from the second observation: **capture lifetime vs extraction lifetime matters** in instrumentation tests that uninstall packages; recovery channels must preserve bitmap identity across test-runner shutdown. Moreover, valid image bytes and correct viewport are insufficient if a non-product system modal visually occludes the target.

## Third observed failure and revised transport (2026-10-14 late)

Product Draft PR #148 later head `eb5caf5d7cc1b4d04f70093a47554a88f6b4955d` (Android CI and Fontconfig green, emulator run `38566426393` red) improved capture instrumentation:
- Target Android compositor actually generated a 1600×960 PNG of **163,932 bytes** and R3 focused instrumented test returned **1 test, 0 failures**.
- After `connectedDebugAndroidTest` returned, app-specific external mirror and `run-as` failed (52-byte non-PNG), consistent with the debug package having been removed.
- `R3_PNG_BEGIN` declared **79** ordered 2,800-character base64 chunks, but logcat preserved only indices **0–52**, never `R3_PNG_END` (seen across repeated diagnostic log dumps). This is demonstrated missing data, **not** a decoder implementation bug; the strict parser correctly rejected it as incomplete. Logcat transport cannot be treated as reliable for this complete PNG.
- Full emulator suite timed out independently after focused projection tests succeeded; R3 source-code compile success alone is not an emulator pass.

Product follow-on fix in same PR (commits `d469e2c4`, `f339384e`, `6ca63b6a`, `705f64af`) changes the dedicated screenshot stage:
1. `gradle :app:assembleDebug :app:assembleDebugAndroidTest`;
2. `adb install -r -t` both exact-head debug/test APKs;
3. run exactly one test via `adb shell am instrument -w -e class ... -e r3StrictCapture true`; require **explicit 1-test JUnit pass and instrumentation success marker**, not just shell exit 0;
4. **before uninstall** retrieve app-private screenshot via `adb exec-out run-as ... cat ...`, then run strict PNG validator;
5. reset temporary density/orientation; original projection/full suite still run unchanged and remain mandatory.

This is a fix **candidate**, not verified until exact-head emulator output confirms the direct transport and preserves screenshot authenticity. Latest CI head `705f64af28e0fbdade9937fb5a4230db578e30d9` Android CI **success**; Emulator `38579751530` and Fontconfig `38579751484` were in progress at this observation.

Native screenshot thumbnail (decoded from 18 complete `R3_PREVIEW_JPEG` chunks in the failed-run log) shows real R3 three-column blue/cyan layout, but debug fixture contains two subtitle events with renderer disabled, so the video region shows renderer-safe-mode notice and cannot be compared as real media against the city-video R3 reference. **Valid screenshot capture, target app screen, genuine playing media, and design pixel parity remain independent gates.**

Intake: this is a continuation of the same evidence-integrity Bug, **not** a new Canonical or separate duplicated Candidate.

## 2026-10-14 · Headless accessibility root false-negative and guarded fallback

New PR #148 exact-head `705f64af28e0fbdade9937fb5a4230db578e30d9`:
- Android CI run `38579751468` and Fontconfig `38579751484` passed.
- Emulator `38579751530`, job `115906919972`, failed R3 targeted capture with `R3_NATIVE_SCREEN_OCCLUDED: foreground window belongs to <none>` because `UiAutomation.rootInActiveWindow` was null. This is not evidence of an actual foreign ANR window: it is **insufficient to decide ownership**.
- Original full suite also had `batchUnknownStyleAndNegativeMarginFailBeforePreview` recorded in its timed/partial XML; exact assertion and baseline attribution not yet established.

Product code fix in commit `5a026b8a3bfb751dcb0e33aecc6ead8c19c8ca97` adds independent `decorView.hasWindowFocus()`, `isShown`, and Activity lifetime checks when and only when the accessibility root is unavailable. If non-null root belongs to another package it is still rejected; a null root with unfocused/hidden target is rejected. Additional regression commit `b9706eed9ce082c2e884153be848d9f9d524971f` tests valid target root, null-root focused fallback, unfocused fallback rejection, foreign launcher overlay rejection, and hidden target rejection.

Separately recovered the **complete earlier Android compositor PNG** from run `38558602308` (74 ordered R3_PNG chunks, 154648 bytes, SHA-256 `3fabb1af9fe79a5155e8104f1938814cb934ed26308954902d7bd223fda8be38`) and reviewed it next to local R3 reference. It contains an actual 1600x960 native three-pane FIXED layout, but black renderer-safe-mode video and two-event test data, not matching the city-video and densely populated event-list design; therefore it cannot certify R3 pixel parity or media operation. This is observational visual evidence, not a product pass.

At this update `b9706eed` Android CI run `38586229141` passed; latest Emulator run `38586228927` and Fontconfig run `38586229417` still in progress. **Status remains Pending exact-head native capture/Emulator and visual diff.** Do not merge PR #148 or promote Canonical based on a passing Kotlin build.

## 2026-10-14 late follow-up — emulator screenshot compilation starved 180s budget

At newer exact head `b9706eed9ce082c2e884153be848d9f9d524971f`, Android CI run `38586229141` and Fontconfig run `38586229417` were **successful**, but Emulator run `38586228927` failed (source job `115929172498`). Its `R3_INSTRUMENTATION_SETUP_FAILED` follows 180-second `gradle :app:assembleDebug :app:assembleDebugAndroidTest` in the **running emulator** session; no targeted R3 capture method ran. Four earlier scoped projection suites succeeded (9/3/7/3 tests), while full `connectedDebugAndroidTest` then timed out with no isolated XML result. Capturing this as a **new failure mode of the existing R3 evidence gate**, not a visual-fidelity pass.

Product PR #148 commits `43111277` and `6166ee53` moved the exact-head debug + AndroidTest APK prebuild to a dedicated GitHub Actions step **before** the emulator is launched, and changed the screenshot stage to install those binaries directly without compiling within a 180-second device budget. This eliminates the identified setup-timeout coupling but must be validated by subsequent exact-head emulator CI. Latest observed head `6166ee53c868c6e977e8103297692e060c4ac8bf` had Android CI `38590886616` **success**, while Emulator `38590886531` and Fontconfig `38590886649` were still running at time of update.

Transferable scope: separate host compilation, emulator start, instrumentation execution, bitmap authenticity, and image-to-design review into independent evidence gates. A failed test-APK setup must not be misreported as a failed visual comparator; the earlier valid debug-fixture compositor image is still not a real-video R3 parity receipt. Existing Bug record extended; Canonical unchanged.

## 2026-10-15 extension: false red from actual terse runner + package signature conflict

Exact-head product PR #148 `6166ee53c868c6e977e8103297692e060c4ac8bf` CI receipts: Android CI `38590886616` success; Fontconfig `38590886649` success; Emulator `38590886531` failure. Detailed emulator job `115945810631` confirmed:
- Direct `am instrument -w -e class ...#captureR3FixedReferenceWhenExpanded` produced the **actual API 35 terse output** `io.github.assworkbench.app.UigsVisualCaptureInstrumentedTest:.`, `Time: 14.74`, `OK (1 test)`, without the verbose `INSTRUMENTATION_STATUS: test=...` or `INSTRUMENTATION_CODE: -1`. Existing `verify_r3_instrumentation.py` incorrectly rejected it with `the requested R3 test is absent`. Native test logcat independently showed 1/1 tests passed and R3 compositor PNG file approx 163,738 bytes saved on-device, but host had not yet retrieved/validated the full image.
- After the direct APK instrumentation, subsequent Gradle `connectedDebugAndroidTest` returned `INSTALL_FAILED_UPDATE_INCOMPATIBLE`, because a package with a different signing certificate remained installed. This invalidates the later regression receipt, even though screenshot test itself finished.

Product commits:
- `3c69e845` enhances validator to accept **exactly one** terse `Class:.` + `Time` + `OK (1 test)` format ONLY for the expected `UigsVisualCaptureInstrumentedTest`, while preserving verbose full-identity validation and failing closed on error markers.
- `d3d27551` adds real terse format fixture and negative cases (unrelated class, missing dot, missing time, multiple tests); existing verbose negative cases retained.
- `0b9a27ba` uninstalls the direct test and target APKs **after** screenshot extraction and **before** Gradle's normal reinstallation, avoiding Android signing conflicts and isolating fixture state.

Verification scope: latest exact-head `0b9a27ba8af49bac265963f0818ea30cbbd75f92` Android CI `38604521014` success at last check; Emulator `38604521032` and Fontconfig `38604521029` still in progress. A recovered complete on-device **JPEG thumbnail** from the earlier emulator log shows actual Compose three-column debug fixture with a black media/renderer-unavailable surface, not real video. This enables a preliminary gap audit against the R3 concept but **not** full-size PNG validity, no display-bound calibration, no real-media and no visual acceptance.

Intake: this is the same R3 evidence integrity failure family, append to existing Bug instead of new Canonical or duplicate Observation. Remains Pending exact-head emulator and native image examination.


## 2026-10-23 — headless emulator foreground/IME evidence (same R3 capture lineage)

**Source:** ASS Workbench Android stacked Draft [PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149), exact pre-fix head `b4abfff89ffc8e70cc3f9d7d771f3f48cde92735`.

- Source/JVM CI [#39723880966](https://github.com/11576865/ASS-Workbench-Android/actions/runs/39723880966) passed, but Android Emulator Regression [#39723880969](https://github.com/11576865/ASS-Workbench-Android/actions/runs/39723880969) failed.
- Strict R3 native capture observed `accessibility root=<none>`, target decor `shown=true` and `focused=false`. No valid PNG was accepted.
- Later instrumentation repeatedly raised `NoMatchingRootException` in the test helper's keyboard-hide precondition. The suite timed out with **NO XML RESULTS**; this run cannot support a complete pass/fail count for individual business tests. Device diagnostic also referenced an input dispatch timeout and Pixel Launcher as top-resumed activity, but a causal launcher defect is not yet independently established.
- Product-side scoped commits: [`677f504f`](https://github.com/11576865/ASS-Workbench-Android/commit/677f504f6c1663702da0747227583c7793ff82de) accepts missing Espresso focus root as a keyboard-hide no-op **only when Activity window insets positively show the IME is already hidden**; null/visible IME and unrelated exceptions still fail. [`9308195b`](https://github.com/11576865/ASS-Workbench-Android/commit/9308195b44b0d6dfc503083e145b99137eeffec2) allows bounded foreground settling after rotation but rechecks the original strict compositor identity gate before capture. Neither update bypasses a user-facing error or declares the actual GUI foreground-ready.
- Durable product checkpoint: [`bb0e2ce3`](https://github.com/11576865/ASS-Workbench-Android/commit/bb0e2ce3602d38fbcc8ef7de328c6cad9b0cb436).

**Reusable case refinement:** distinguish *already satisfied idempotent preconditions* (IME hidden) from missing environment readiness (foreground app ownership). A precondition helper may no-op only with positive state evidence; evidence capture and device interaction must remain fail-closed on uncertain or externally owned focus. A cascading test-harness failure without XML is not proof of dozens of independent product regressions.

**Status:** test code committed; new exact-head Android CI and native emulator results **Pending**. This is additional evidence within the existing R3 screenshot/foreground integrity family, not a second independent confirmation. No Canonical promotion.


## 2026-10-23 — valid tablet captures but oversized review transport

Same evidence-integrity lineage, deduplicated by search for `logcat PNG`.
Product [PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149)
source `020e20761b024b64502c8ea582c163db86aa2ca9` passed source/JVM run
`39956067332`. Emulator `39956067357` validated run-as compositor files:
1440×900, 134758 bytes, SHA256
`2f8be9e6b8abce36284927958a2e009c6fb4a7c4f40ce3f1ca30852711e9e472`;
1024×768, 89506 bytes, SHA256
`1e3460a7a2c9c49af7d8e56871f08423ce4fd61ae317fcadfe45347d591e89ad`.
Four projection families passed 22 tests; full instrumentation remained failed:
179 tests, 4 failures, 0 errors, 0 skipped.

The compact evidence job was readable, while downloading the full editor job
through the GitHub connector repeatedly returned internal/transport errors.
PNG bytes could therefore not be retrieved for actual design comparison.
This does not invalidate the recorded file integrity gates, and those gates
still do not establish visual parity.

Follow-on product commit
[`39ffe1a3`](https://github.com/11576865/ASS-Workbench-Android/commit/39ffe1a3604d9cbcd3ed12717983800f033bc7f9)
immediately emits an indexed bounded envelope from the runner-owned, validated
run-as file, using a distinct prefix from lossy Android logcat. Two separate
per-size evidence jobs recover the complete PNG, require its original gate
receipt, and recheck hash, byte length, CRC and decoded dimensions before
re-emitting it. Source run/attempt/tested merge SHA/head SHA and the original
regression conclusion remain explicit. Missing, damaged or oversized images
fail; no thumbnail substitution or weakened suite gate. Seven new defensive
transport tests pass locally (35 relevant Python checks total).

Status: new Android execution and bounded screenshot retrieval **Pending**.
Actual native-vs-design review remains incomplete; debug fixtures do not
establish real video/libass coverage. This is a project-specific repair candidate
within the existing Bug, not independent cross-project confirmation or Canonical
promotion.


## 2026-10-24 — completed bounded-transport generation, capture correctly rejected

Read the completed results for product source
`39ffe1a3604d9cbcd3ed12717983800f033bc7f9` (tested merge
`a0d89ca2be29a37c993db73d0756d2cacae398c7`):
source/JVM run `39971371387` succeeded; emulator `39971371534` failed.

R3, 1440×900 and 1024×768 screenshot attempts all rejected external accessibility
root `android`, target decor focused=false/shown=true. The source job's last-ANR
diagnostic recorded a preceding 14:44:15 UTC input-dispatch timeout with no focused
window and Pixel Launcher as the recorded resumed Activity. This supports an
environment-readiness failure; it does not independently determine every cause.

Projection groups passed 9/3/7/3 tests. The full suite timed out and its XML was
empty, so no full-suite count or improvement from the historical 179/4 receipt
can be inferred. Both bounded image jobs failed with no complete envelope:
the foreground gate had accepted no images to transport. This is expected
fail-closed behavior, not demonstrated image-decoder failure.

Product-side evidence and follow-up inspector work are recorded at
[`89f69e97`](https://github.com/11576865/ASS-Workbench-Android/commit/89f69e97cd001f7522eea2f45ace5622d4272626)
and `docs/FIXED-V11-EVENT-INSPECTOR-2026-10-24.md`.
The new UI package remains Pending Kotlin/Android/native visual validation.
This refines the same existing foreground/evidence Bug; no separate Candidate
or Canonical promotion.
