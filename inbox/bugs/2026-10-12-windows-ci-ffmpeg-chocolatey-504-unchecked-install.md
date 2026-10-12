# Bug: QHE Windows CI can misattribute upstream FFmpeg installation failures to media tests

Date: 2026-10-12
Status: **FIX PROPOSED in QHE PR #104**, exact-head checks still distinguish independent jobs
Severity: CI test reliability and diagnosis, not a demonstrated product encoding defect
Related QHE draft PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104

## Reproduction and evidence
A QHE Windows local smoke workflow, run `38268001600` at PR #104 head `0921499f76ddfc61fed4dee4116a2aa8fe6fbbbe`, failed in `Validate native Manual sample evidence receipts on real FFmpeg source` with PowerShell `CommandNotFoundException` for `ffmpeg`. Inspection of the **preceding Chocolatey step** revealed an HTTP **504 Gateway Timeout** from `https://community.chocolatey.org/api/v2/...` and `Chocolatey installed 0/0 packages`. The single-line `choco install ffmpeg --yes --no-progress` step had not explicitly checked `$LASTEXITCODE` and therefore workflow advanced to media tests even though required tooling was absent.

The new independent Windows Manual paired codec workflow `38268001729` was successful on the same PR head; it had FFmpeg available and actually executed 12 paired x264/x265 samples. Hence the local-smoke failure was a dependency installation/outage misattribution, not evidence of a regression in the sampling algorithm. Do not silently describe the first failed check as a codec failure.

## Bounded proposal
At head `3f1b4fbc1d6a2c02c269f920a9db92adf04a9c52`, the PR changed both `.github/workflows/windows-local-smoke.yml` and `.github/workflows/windows-manual-paired-codec.yml` to retry Chocolatey FFmpeg installation up to three times (with short backoff), **check the installer process exit code**, and fail explicitly at the dependency boundary if all attempts fail. Real sample assertions remain unchanged. This limits misleading test failures but does not remove reliance on upstream package feed.

## Verification scope
The independent paired codec test was rerun in workflow `38268364465` and succeeded at the exact updated head. Other workflows should be checked independently for complete success; a passing codec test alone does not establish a clean full PR check set. Do not update Canonical rules from this single specific incident.

## Reusable engineering observation
When external dependency setup can fail transiently and its command exit code is not guarded, subsequent domain steps can falsely carry the blame. Keep toolchain provisioning, domain-test assertions, and hosted environment failures separately diagnosable; accept success only at the exact final commit and per-workflow check results.
