# Observation: A green exact-HEAD PR may become unmergeable when its branch ref advances without PR metadata/CI alignment

Date: 2026-10-15
Status: Observation / project-specific GitHub execution evidence (NOT Canonical)
Project: `11576865/MKV-Fast-Muxer`
Case: Mainline Convergence 001 — https://github.com/11576865/MKV-Fast-Muxer/issues/152

## Directly observed facts

1. PR #150 was an open Draft, then explicitly marked Ready, still reporting head SHA `bd70554d2e7c97cd9814c8d12ff7de8be6ff2928`. The exact-head Browser E2E workflow run `38617379805` and Pages run `38617380268` reported success, including 593/593 Node tests.
2. During the integration attempt the actual remote branch `feat/ten-round-p3b-save-only-retry-20261015` had advanced to `0f76649abab27ce3c76ab300e968714ef612a564` (one extra commit with changes only in `.uigs/tasks/...json` and `acceptance-ledger.json`), yet PR metadata continued to identify older `bd70554d...` as the PR head.
3. A guarded GitHub merge with `expected_head_sha=bd70554d...` returned **409 Head branch is out of date**. Current main was still the expected original `fefd97e...` when checked immediately afterwards. Thus the rejected merge was not correctly characterized as a concurrent change to main.
4. The ledger advanced the number of `partial` items from 9 to 10. Subsequent PR #151 also contained a repair for a hard-coded nine-partial test assumption. The newer #150 branch ref had **no exact-head workflow run** in the checked snapshot; a previous green run is not transferable simply because the latest delta appears documentation-only.
5. No forced merge or blind overwrite was performed. A distinct validated earlier stack #149 (exact Browser E2E run `38615849094`) was merged as `8b8ec0e30908a3960da5f9f26f6acf7444ecb60c`, preserving useful R2–R6 work while R7 stayed isolated.

## Reusable, narrowly scoped observation

When GitHub pull-request head metadata, direct branch ref and an exact-head CI result do not agree, the safe integration action is to **stop**, read the raw branch ref and compare commits, then reacquire a coherent exact-head test and compare-and-swap merge authorization. Never silently substitute a prior green run or merge without an expected head identity. The mismatch may be transient GitHub API refresh, a concurrent push, or another integration issue; this observation does not establish which infrastructure component caused the inconsistency.

## Related Foundry knowledge — no duplication

- `inbox/observations/2026-10-04-collapse-stacked-pr-chain-by-retargeting-top.md` already documents validated stack consolidation.
- `inbox/candidates/2026-10-02-single-authority-midflight-duplicate-work.md` already covers ownership conflicts.
- `inbox/candidates/2026-10-04-interrupted-session-reconcile-before-reimplementation.md` already requires resumption reconciliation.
- This record contributes one concrete stale-PR-metadata/branch-ref mismatch and guarded 409 refusal, not a new general framework or Canonical revision.

## Evidence and boundaries

- PR: https://github.com/11576865/MKV-Fast-Muxer/pull/150
- Previously passing exact-head workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38617379805
- Branch-extra commit: https://github.com/11576865/MKV-Fast-Muxer/commit/0f76649abab27ce3c76ab300e968714ef612a564
- Mainline accepted R2–R6: https://github.com/11576865/MKV-Fast-Muxer/pull/149
- Status/continued obligations: https://github.com/11576865/MKV-Fast-Muxer/issues/152

One incident, descriptive observation only. No claim that a Canonical workflow is changed or that PR #150 is accepted.
