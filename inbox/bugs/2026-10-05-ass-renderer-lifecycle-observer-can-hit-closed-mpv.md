# Bug: ASS renderer lifecycle can observe a closed mpv instance during font-revision recreation

Date: 2026-10-05
Status: Bug
Lifecycle: recorded
Project: ASS-Workbench-Android
Evidence: PR #119 Android Emulator Regression run 37212798394

## Failure

A repository-wide emulator regression run failed only in:

- test: `RendererLifecycleInstrumentedTest.fontRevisionRecreatesNativeMpvCore`
- exception: `java.lang.IllegalStateException: this Mpv is closed`
- origin: `io.github.yuroyami.libmpvkt.Mpv.observeNode`

The same run reported 69 tests total with exactly one failure. `EditorRegressionInstrumentedTest` itself completed 33/33 successfully.

PR #119 changed only `.github/workflows/branch-hygiene.yml`, so there is no direct source-file ownership path from that PR's delta to renderer lifecycle code.

## Counter-evidence

A later ASS PR #116 emulator regression completed successfully while exercising the same repository test suite. This means the observation is not enough to classify the failure as a deterministic product regression.

## Interpretation boundary

The evidence is consistent with an intermittent lifecycle/race condition where an observer coroutine remains active across mpv core teardown/recreation, but that root cause is not yet proven.

Do not suppress or quarantine the test from one observation. First require either:
- a reproducible ordering that closes the old mpv instance while an observer is still collecting, or
- repeated CI/device evidence showing the same stack.

## Next diagnostic slice

Capture the renderer core generation/identity, close/recreate ordering, observer job cancellation/join timing, and font revision that triggered recreation. The regression should prove observers from generation N cannot call into a closed instance after generation N+1 becomes authoritative.

No Canonical promotion.
