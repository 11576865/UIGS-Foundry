# Observation: QHE VVC CI time dominated by toolchain provisioning

Date: 2026-10-14 (Asia/Shanghai)
Status: Observation — one exact-run measurement, not a universal CI performance claim
Domain: operations / GitHub Actions execution cost
Product: 11576865/Quick-Automatic-Hardsub-Encoder

## Evidence
- PR #105 (draft/unmerged), tested head `039079a60bd1b50502410b9b27ffdd4e0d2dfc98`.
- GitHub Actions run: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38440266547, Windows required VVC runtime acceptance, job `115444708466`.
- Job logs begin `2026-10-13T17:38:58Z` and finish `17:44:32Z`: approximately 5m34s.
- `Fetch hash-verified isolated libvvenc toolchain`: `17:39:24Z` to `17:44:13Z`, approximately 4m49s.
- `Require real QP, bitrate and ASS hard-sub bridge outputs`: `17:44:13Z` to approximately `17:44:29Z`, approximately 16s.
- Job concluded `success`; eight other tracked workflows for the same PR head also succeeded at the later status lookup.

## Interpretation and limit
For **this one observed job**, dependency provisioning was the dominant wall-clock segment, not the actual VVC/ASS execution checks. Frequent PR updates can repeat heavyweight environment preparation and increase CI resource use. This is not evidence that every VVC run has identical timing, that caching will be safe/effective, or that the workflow was hung.

## Potential improvement to evaluate
- Measure multiple job runs and distinct step durations before changing CI.
- Preserve frequent fast static/unit checks and durable work-package commits, but avoid invoking the entire expensive platform matrix after every non-critical source edit when branch protection and test coverage permit selective gates.
- Evaluate pinned, hash-verified toolchain artifact/cache reuse, securely scoped caching and reuse keys; retain trusted-source and SHA verification and never silently bypass required full runtime validation.
- Run full Windows/Android/VVC/media acceptance at meaningful integration checkpoints and required premerge/release gates.
- Do not wait/poll merely for an asynchronous CI run to complete.

## Dedup / relationship
Searched Foundry for workflow, CI cache, heavy toolchain, branch submission, test selection. Related but not duplicate: `governance/AGENT-EXECUTION.md` (Canonical durable checkpoints and asynchronous waiting boundary) and historical `inbox/candidates/2026-10-02-branch-submission-default-execution-boundary.md`. This observation concerns measured CI wall-clock allocation and potential selective validation, not a change to the existing Canonical execution boundary.

No Canonical promotion and no QHE workflow changes were performed.
