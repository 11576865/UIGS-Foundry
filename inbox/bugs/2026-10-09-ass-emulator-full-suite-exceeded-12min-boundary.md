# Bug: ASS full Android instrumentation suite exceeded its 12-minute boundary

Status: Bug
Lifecycle: recorded
Date: 2026-10-09
Project: ASS-Workbench-Android
Evidence: PR #136, Android Emulator Regression workflow 37581619425, job 112662366594 (2026-10-07).

## Observation

- PR #136 changes only `AGENTS.md` and does not modify app/test sources.
- Android CI succeeded; the Android Emulator Regression job failed.
- The four independently invoked focused parameter-projection class runs emitted XML with zero test failures.
- The following full `connectedDebugAndroidTest` suite started at 06:32:42Z and hit the script's 12-minute timeout boundary around 06:44:39Z.
- The process exited with code 124 and diagnostic text `instrumentation timed out or was killed`.
- The diagnostic `dumpsys activity lastanr` reported no ANR since boot.
- Partial test-runner logs show several finished editor regressions, but no complete XML report for the full suite.

## Evidence boundary

This is an incomplete-run timeout, not a known assertion failure. The most recently captured test names are not enough to name a specific hanging test reliably; test logcat tails are partial and not an authoritative complete test order.

The observation does not prove that `AGENTS.md` caused the timeout. Root ownership remains unknown: instrumentation driver, test deadlock, device responsiveness, or other lifecycle interactions.

## Next diagnostic slice

1. Re-run only the failed workflow job on the same head (requested on 2026-10-09).
2. If reproduced, capture process and instrumentation thread dumps at timeout, the authoritative current test name, and individual test/class isolation.
3. Keep the fixed 12-minute gate and fail closed. Never mark a timeout as passing just because earlier focused tests emitted green XML.

No Canonical promotion.