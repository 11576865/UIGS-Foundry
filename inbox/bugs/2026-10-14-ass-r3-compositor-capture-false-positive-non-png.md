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
