# Bug: Android Stream Plan v4 emulator tail verification rejects V4D-06

Status: bug
Date: 2026-10-04
Project: Quick-Automatic-Hardsub-Encoder
Evidence: PR #58 workflow run 37190815690

## Failure

The Android emulator runtime acceptance reached the real EncodeService execution path and failed one case:

- case: V4D-06
- observed terminal state: failed
- message: 成品视频 packet 末端异常：输入视频约 6.021 s，扫描末端 5.033 s
- expected test terminal state: completed

The Gradle/Android test infrastructure itself built and launched successfully; the failure occurred inside the runtime-backed acceptance assertion after execution.

## Interpretation boundary

This proves a mismatch between the current Android runtime output and the verifier's expected packet-tail coverage for V4D-06. It does not by itself establish whether the defect is in:
- EncodeService trimming/range execution,
- output mux timing,
- packet-tail scanning,
- fixture assumptions,
- or the verifier tolerance.

The emitted evidence artifact was still uploaded by the workflow.

## Next diagnostic slice

Compare V4D-06's canonical video range, generated ffmpeg command, output duration/last packet PTS/DTS and the independent host verifier's expected terminal boundary. Avoid weakening the assertion until the execution-vs-verification ownership is identified.

No Canonical promotion.
