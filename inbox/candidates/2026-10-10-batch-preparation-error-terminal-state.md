# Candidate: Batch terminal status must distinguish unexpected preparation failure from zero-job success

Status: **Candidate**, not Canonical
Date: 2026-10-10
Domains: batch orchestration, exception boundaries, state restoration, observable terminal states, UI-contract tests

## Source Observation

Project: `11576865/MKV-Fast-Muxer`
Baseline: `main@d5669c6d9bb6ebdd6843ee8c7f651902c80c4d08` (PR #65 merged; main-push Chromium Browser E2E and GitHub Pages succeeded).
Branch: `fix/batch-preparation-error-reporting`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/66
Head at intake: `e8c31d4a93ad4ac1953e886e8da37ee0abf02fe7`

A source inspection of `src/main.js` found the batch event handler placed Group font subset preparation (`buildGroupedSubsetFonts`) and parts of per-job input setup *outside* its per-item mux catch, under an outer `try/finally` with no matching `catch`. If subtitle decoding, font subsetting, or task setup threw, `finally` computed `done=0` and `failed=0` from an empty `results` array and displayed `批量完成：成功 0，失败 0` even though execution was interrupted. An async event-handler rejection could also remain uncaught. This is a **code-grounded potential failure**, with a deterministic fault-injection browser scenario added to PR #66, not a user-reported production incident.

## Candidate Principle and Fix

`finally` is an appropriate cleanup boundary, **not** a proof of success. Batch UI states should not infer successful completion merely because the number of recorded job failures is zero; unhandled failure in a preparatory stage may occur *before the first result object exists*. Distinguish:
- Normal completion: report success and failure counts.
- User cancellation: report completed and failed counts with cancellation status.
- Unhandled preparation/setup error: report `批量中断`, the cause and any already completed / per-item failed counts; retain successful downloads and optional directory-save warnings.

PR #66 adds an outer `catch` capturing the fatal error while preserving the existing restoration `finally`, plus a pure `formatBatchTerminalStatus` function with explicit `fatalError` precedence over cancellation/success. The test suite includes source-derived unit assertions and browser fault injection: after creating a real Group subset batch plan, `File.prototype.arrayBuffer` rejects reading a selected ASS during Group preparation; E2E then requires an explicit `批量中断` status and restored batch start readiness.

## Evidence and uncertainty

At intake, **5/5 source-derived V8 checks passed**, and all four touched JavaScript files passed V8 parse checks. Full repository Node tests, real Chromium E2E, and PR review remain **Pending CI**. No assertion of green CI or production resilience is made. The change improves truthful reporting of preparatory failures and retains existing completed artifacts; it does not guarantee that every conceivable restoration exception is recoverable.

Deduplication: searched Foundry for batch preparation errors / zero-job false success / Group subset failure / fatal terminal status, and found no equivalent record. This insight is separate from earlier Candidates about destination file ownership and Blob URL lifetime. **Do not promote to Canonical on this single code observation**.
