# Test: QHE Guided Native completed budget receipt survives web UI reload

Date: 2026-10-14 (Asia/Shanghai)
Status: Specific Windows Native runtime step PASS and recovery helper tests PASS; latest exact-head full CI pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder, draft PR #105
Head at first report: `430c58257361c9203f8fb454a8e94199cb6b0f52`

## Problem being tested

Before this continuation the browser-only `nativeJobProjection` represented the requested whole-file target, planned bytes and policy. Completed Native jobs survived page refresh by `jobId` but their original target, planned-vs-actual error and strict proof were absent on the recovered UI. A page reload must not turn a plan estimate into a claimed native strict verification.

## Bounded production tests

- `src/native-guided-budget-recovery.js` normalizes a completed job receipt from Native status. It rejects unknown/non-completed states and invalid numbers. Native-source `strictVerified` plus within-target actual bytes are necessary before showing 'strict byte ceiling verified'; transient plan can never assert this.
- `src/native-guided-budget-recovery.test.mjs` tests pure normalization, over-budget actual bytes, missing Native proof, mismatch/stale transient job, and uses `node:vm` to actually execute the `recoverNativeJob` production method after simulating a page reload and a single Native status query.
- `src/main.js` attaches planned whole-file bytes to the legacy Guided Native execution request. Normal completion and recovered completion both render `formatCompletedGuidedNativeBudget` and attach the resulting comparison to the completed artifact.
- `windows/native-bridge.ps1::Get-JobStatus` now returns `budgetProjection` on both the first completed status and repeated completed-job status after the existing strict output byte/hash gate. The projection is associated with the Bridge-owned completed job.
- `scripts/check-guided-budget-native.ps1` sends planned bytes and original target, runs real Windows Native two-pass and strict x264/ASS jobs on a CI-generated short source, compares Native response projection against the input, re-queries completed status and checks receipt stability.
- `src/ui-shell.test.mjs` was updated to assert recovered budget logic rather than obsolete transient-only `sizeError` and `actualBytes>projection.budgetBytes` source expressions.

## CI observations

The prior frontend check on `40fe91f` failed **only** at an outdated `ui-shell.test.mjs` assertion; `node --test src/native-job-monitor.test.mjs src/native-guided-budget-recovery.test.mjs` completed SUCCESS. The `8724a80` frontend run similarly passed new native recovery tests and failed on another older `ui-shell` assertion, subsequently updated in `430c582`.

Windows local smoke `38436001776` completed its `Exercise real guided Windows Native two-pass and strict byte ceiling` step with SUCCESS after the new budget receipt and repeated status contract was registered. At initial recording overall workflow and newest HEAD CI were not final; do not equate step success with full all-platform acceptance.

## Evidence scope

These are hosted tests on CI-generated short software-x264 data. They do not prove Native Bridge process restart (job state is still in the process), a physical Windows workstation, exported-file user playback, arbitrary long-film target-size accuracy or full actual SSIM quality; output stays subject to source/stream and byte validation. A successfully completed non-strict output below target is still not strict delivery verification. This Test is complementary to the source-cost provenance test `inbox/tests/2026-10-13-qhe-windows-guided-ass-source-bound-copy-audio-budget.md`. No Canonical promotion, main merge or release.

## Code exact-head 429de52 confirmation

The QHE source implementation at `429de527dd57b09f5441a7d21f119d5307b15af7` subsequently passed the **entire hosted frontend workflow** `38436582969`, including the native recovery pure/VM tests, source-text UI shell tests, FFmpeg integrations and Chromium browser checks. The same source HEAD's `Windows local smoke` workflow `38436583069` completed **SUCCESS**, including the actual Guide ASS two-pass/strict completed budget receipt and repeated-query consistency step. Windows Manual paired, Stream Plan v4, device fixture, Compile Android and UIGS evidence also passed at that code head. VVC and Android emulator independent runs were still in progress at this observation.

A subsequent ledger-only update `0bb95d855aae231f0c746fc439be1f8947dd3fcd` restarts the nine workflow gates; its exact-head results must be checked independently. Page reload and Native Bridge process restart remain distinct acceptance scenarios.
