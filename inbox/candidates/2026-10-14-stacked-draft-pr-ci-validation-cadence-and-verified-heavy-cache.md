# Candidate: Stacked draft PR CI should separate fast feedback from full release gates

Date: 2026-10-14
Status: Candidate / QHE implementation submitted, runtime acceptance Pending
Domains: operations, engineering evidence, reliability

## Trigger and scope
On QHE stacked draft PR #105, `pull_request.paths` evaluates paths in the PR diff against its base rather than just the newest commit. A task-record-only update can therefore continue to schedule the full Windows/Android/VVC matrix whenever those paths remain changed in the draft PR. This is especially expensive for long integration stacks.

Exact observed bottleneck: Windows VVC run [38440266547](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38440266547) spent about 4m49s fetching/verifying an isolated FFmpeg/libvvenc archive out of about 5m34s total. Actual QP/bitrate/ASS verification was about 16s. One run is not a statistical performance guarantee.

## Proposed reusable boundary

1. During draft development, run a targeted fast code/test/build job and retain lightweight evidence/invariant checking.
2. Preserve all heavy Native, emulator, browser and codec acceptance jobs, but automatically execute them at Ready for Review and required mainline/release checkpoints; also permit explicit dispatch when GitHub supports it.
3. Full-test status must remain separate: a skipped heavy Draft job is NOT a passing validation, and a passing fast job is not full acceptance.
4. Cancel superseded runs of the same workflow/PR/ref, while retaining exact-head full validation requirements before merge.
5. For large third-party toolchains, resolve a trusted release asset's SHA-256, key the cache by that immutable digest and verify the downloaded/cached archive before extraction. A missing or mismatched digest must fail closed; a cached binary must not be treated as proof of runtime correctness.
6. Commit and checkpoint coherent work before async CI; do not replace durable agent-execution policy with one giant uncommitted coding session.

## Concrete proposed product implementation
QHE staged branch `feat/qhe-ci-batched-validation-20261014` based on #105 head `039079a` edits eight relevant workflows, the Windows VVC asset installer, adds docs and a durable task record, and is intended to fast-forward PR #105 (Draft). `Test frontend / draft-fast` runs targeted model regressions plus production build; eight full jobs are gated until Ready/dispatch, Windows local-smoke branch-push duplication is removed, and the VVC archive uses digest-scoped `actions/cache@v4` plus runtime digest checks.

No performance improvement or CI correctness is claimed until actual exact-head runs and a warm-cache cycle are inspected. Mandatory tests for this Candidate: (a) draft-fast runs, (b) heavy jobs do not run during draft synchronizations, (c) Ready for Review schedules complete acceptance, (d) manual dispatch is available where workflow resides on default branch, (e) cold/warm cache both pass real execution and corrupted cache is rejected.

## Existing knowledge and dedup
Checked Foundry queries for `draft CI gating`, `pull_request.paths cumulative PR`, `ready_for_review`, `checksum toolchain cache`: no directly matching record found. Related:
- `governance/AGENT-EXECUTION.md` is existing Canonical durable checkpoints / asynchronous waiting boundary; this Candidate does not amend it.
- `inbox/observations/2026-10-14-qhe-vvc-ci-toolchain-provisioning-dominates-runtime.md` records the particular observed timings, not the proposed operational design.

Do not automatically promote this single implementation attempt to Canonical.
