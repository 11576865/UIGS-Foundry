# Bug: HSR full MKV FFmpeg mux leaked subprocess progress pipes

Date: 2026-10-14
Project: `11576865/HSR-Voice-Archive-Builder`
State: **Fixed, exact-head real FFmpeg regression and Chromium CI verified**
Severity: bounded lifecycle/resource leak; no demonstrated corruption or user data loss
Area: FFmpeg process ownership, progress reporting, long-running archive jobs

## Observation

The genuine >4 MiB PNG / full Matroska real-media integration run exposed Python `ResourceWarning: unclosed file` messages from `app/archive_bundle_exporter.py` when the `subprocess.Popen(..., stdout=PIPE, stderr=PIPE, text=True)` object exited without explicitly closing both pipes. This was visible in the successful real-FFmpeg test logs at [HSR media run 38443137095](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38443137095), `libass-artifact` job; a green exit alone does not prove absence of resource warnings.

A failure or exception raised by a progress callback could also bypass normal cleanup and leave the child FFmpeg writer running until it exits independently. The previous code consumed progress and called `wait()` but did not own child streams in a structured context.

## Bounded fix / validation

- Product `main` commit [`64cab090e8983d9e348e9245f625d6db92e915a8`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/64cab090e8983d9e348e9245f625d6db92e915a8) now wraps the FFmpeg process in `with subprocess.Popen(...) as proc:`; the process context closes stdout/stderr even on encode errors. If an exception occurs during progress, a running child receives `terminate()` before the exception propagates.
- The real-media acceptance [HSR browser/libass run 38443474566](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38443474566) completed successfully, including a 5+ MiB valid PNG → FFmpeg decode → H.264+FLAC+ASS MKV → saved-image reuse. The libass job log had **zero `ResourceWarning` entries** after the patch versus observed entries in the prior run.
- Exact-head [Python 3.11/3.12/3.13 + Termux 38443474435](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38443474435) and [Pages 38443473452](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38443473452) were also successful; latest `main` was compared as identical to the fixed commit.

## Reusable boundary

A process returning exit code 0 can coexist with unclosed stream handles. Long-lived application encoders must own and close child standard streams on normal completion **and failure/cancellation**, and run tests should check emitted warnings as well as output validity. A `Popen` context manager is a minimal pattern for structured cleanup; stderr-heavy backpressure and exact cancellation latency are still distinct performance/fault-injection test subjects.

Intake: searched Foundry for HSR FFmpeg Popen/unclosed-pipe duplicates; no matching existing Bug found. This is a single verified project bug, **not** grounds to change Canonical automatically.
