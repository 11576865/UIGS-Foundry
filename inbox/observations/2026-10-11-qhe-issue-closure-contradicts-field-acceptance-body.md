# Observation: Closed tracker state can contradict outstanding acceptance evidence

Status: Observation / needs workflow follow-up, not Canonical  
Observed: 2026-10-11  
Project: Quick Automatic Hardsub Encoder (QHE)  
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/85  
Related: PR #86 https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/86 ; PR #87 https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/87

## Observation

GitHub Issue #85 was read as `state=closed` while the same issue body's final milestone section still directs **“Leave #85 OPEN for remaining field and precision work”**. The body also retains unchecked real-media/physical-hardware matrix, cancellation and restart cleanup, audio reservation, infeasible budget explanation, recovery options, and validation work. These are **not** discharged merely by PR #86/87 synthetic Windows Native tests.

The project main commit `3dc38d08e1aad99013be7654e3d17acc8622c692` and merged PR #87 do show substantive implementation and CI success. The mismatch is a **workflow/acceptance representation inconsistency**, not evidence that the implementations failed or that their tests did not run.

## Candidate workflow guard

For milestone closure, distinguish **implementation merged**, **CI-verified** and **field accepted**. If a closed tracker still has incomplete acceptance requirements, either (a) reopen the tracker or (b) explicitly transfer each remaining obligation into an open child/follow-up issue and annotate the original closure as limited scope. A report must not infer field acceptance from the issue’s Closed badge alone.

## Verification and limits

Verified via live GitHub issue metadata and body on 2026-10-11; no user-device test or independent audit of #85’s closing rationale. This is **one project-specific observation**, not yet a repeated pattern, no automatic issue modification, and **not** a justification to revise UIGS Canonical.
