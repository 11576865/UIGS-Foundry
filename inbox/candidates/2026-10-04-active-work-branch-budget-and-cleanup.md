# Candidate: Active work branch budget and post-merge cleanup

Status: candidate
Date: 2026-10-04
Domains: engineering-process, git, branch-hygiene, cross-project

## Trigger

Multiple repositories accumulated dozens to more than one hundred historical feature/fix/UI branches even when few or no pull requests remained open. The branch list stopped representing current work and made repository state harder to reason about.

## Candidate rule

For project repositories, treat branches as temporary execution artifacts rather than durable project records.

### Default branch budget

- Exclude the default branch and intentionally long-lived release/reference branches.
- Keep at most **8 active work branches per repository** by default.
- "Active work branch" means a non-default branch that still contains unique unmerged work or backs an open/in-progress pull request.
- If the repository is already above the budget, do not create another work branch until the current task has checked whether it can reuse, consolidate, or retire an existing branch.
- The budget is a workflow guard, not a reason to delete evidence or unique work blindly.

### Branch creation gate

Before creating a new branch:

1. Check whether an existing open branch already owns the same task line.
2. Prefer updating/reusing that branch when semantic ownership is the same.
3. For stacked work, prefer a single top integration branch once lower layers are validated.
4. Do not create parallel "re-land", "rebase", "current-main", "v2", "v3" branches without closing/superseding the previous attempt as part of the same operation.

### Terminal state

After a PR is merged:

- delete the merged head branch by default when tooling/repository policy permits;
- otherwise mark it as cleanup-pending and remove it at the next branch-maintenance pass.

After a PR is closed without merge:

- if superseded and all unique work is represented elsewhere, delete the branch;
- if unique work remains, keep it only with an explicit reason.

### Cleanup priority

When branch count is high, classify branches in this order:

1. fully merged into default branch -> safe deletion candidate;
2. superseded by a newer branch/PR with equivalent or stronger content -> delete after semantic verification;
3. unique unmerged commits -> retain or re-land before deletion;
4. intentional release/reference branches -> retain.

## Acceptance criteria

- New work does not create a branch when a same-purpose active branch already exists.
- A repository above 8 active work branches triggers consolidation/cleanup before another work branch is created.
- Merged PR head branches do not remain indefinitely without an explicit retention reason.
- Closing a superseded PR and leaving its branch behind is treated as incomplete cleanup.
- Historical branch-count reduction never deletes unique commits merely to satisfy the numeric budget.

## Scope and exceptions

Long-lived branches such as release/version lines, protected integration branches, and explicitly documented evidence/reference branches are outside the active-work budget.

Repositories may temporarily exceed the budget during a bounded integration event, but the same work item must include consolidation back toward the budget.

## Evidence boundary

This is a user-requested workflow guard and a Candidate, not a Canonical specification. The numeric budget may be revised after observing real multi-repository workload.

No Canonical promotion.


## 2026-10-05 cross-repository reconciliation evidence

A branch-budget audit across Character-Voice-Service, MKV-Fast-Muxer and HSR-Voice-Archive-Builder found several branches that still reported unique commits against current main even though their useful behavior had already landed through a clean successor or a stronger later implementation.

This adds an important distinction to cleanup priority step 2:

- **Git uniqueness is a retention signal for automation, not a semantic ownership claim.**
- Before re-landing an old branch, inspect successor PRs/current-main behavior and identify whether any capability delta is genuinely absent.
- If the capability is already represented, record the supersession and avoid manufacturing a duplicate current-main replay solely because `ahead_by > 0`.

The audit annotated the relevant closed PR threads so future continuation work has a durable successor trail.

This remains Candidate evidence; no Canonical promotion.


## 2026-10-11 MKV post-merge branch classification

[MKV-Fast-Muxer PR #73](https://github.com/11576865/MKV-Fast-Muxer/pull/73) was merge-committed to `main` (`60d41336ed7d6df5a422001289824510ea823d9e`), and [branch hygiene run 38129064307](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38129064307) succeeded, removing exactly the current merged UI feature branch. Independent post-merge main Chromium E2E (38129064341) and Pages deployment (38129064270) both succeeded, 199/199 Node tests passing.

The same audit still found four **closed, unmerged, divergent** historical PR heads with unique commits relative to the verified main:

| Retained historical head | Ahead/behind main | Closed PR | Successor/evidence |
|---|---:|---|---|
| `docs/seo-discovery-metadata-20260930` | +7 / −336 | [#25](https://github.com/11576865/MKV-Fast-Muxer/pull/25) | PR body explicitly says superseded and replayed in merged [#27](https://github.com/11576865/MKV-Fast-Muxer/pull/27) |
| `ui/mobile-tablet-density-20260930` | +4 / −336 | [#26](https://github.com/11576865/MKV-Fast-Muxer/pull/26) | PR body explicitly says responsive changes replayed in merged #27 |
| `feat/font-content-identity` | +13 / −85 | [#57](https://github.com/11576865/MKV-Fast-Muxer/pull/57) | Identically titled successor [#58](https://github.com/11576865/MKV-Fast-Muxer/pull/58) is merged; main contains `src/font-identity.js`; exact semantic parity **not yet proven** |
| `ui/mkv-workbench-action-hierarchy` | +6 / −54 | [#67](https://github.com/11576865/MKV-Fast-Muxer/pull/67) | PR marked superseded by content-first architecture; [#69](https://github.com/11576865/MKV-Fast-Muxer/pull/69) and #73 merged; exact semantic parity **not yet proven** |

These are **not** ancestry-contained branches: deleting them simply because newer features exist would risk dropping unique history. The safe next cleanup is a separate evidence/tag-based retirement review, not part of the completed #73 release. `maintenance/archive-reviewed-merged-pr-refs` is ancestry-contained but explicitly exempt from automated cleanup; `uigs-outbox` is an independent data branch and must not be mistaken for a feature branch.

This supports the existing Candidate's two-gate distinction: Git ancestry decides automatic deletion eligibility, while semantic supersession requires separate verification and a durable archive before pruning divergent history. Do not promote to Canonical from this alone.


## 2026-11-05 Softmux bulk-merge request: PR integration versus historical divergent refs

Requested scope: consolidate the accumulated branches in `11576865/MKV-Fast-Muxer`. The actionable queue contained eight open Draft PRs, not fifty-eight independent ready-to-merge product features.

- Exact-head checks and distinct task scopes supported integration of [#235](https://github.com/11576865/MKV-Fast-Muxer/pull/235) (research docs), [#236](https://github.com/11576865/MKV-Fast-Muxer/pull/236) (fail-closed writer fallback), [#237](https://github.com/11576865/MKV-Fast-Muxer/pull/237) (bounded header deduplication), [#233](https://github.com/11576865/MKV-Fast-Muxer/pull/233) (cross-source ASS/fonts), [#241](https://github.com/11576865/MKV-Fast-Muxer/pull/241) (S08 acceptance tests), and [#240](https://github.com/11576865/MKV-Fast-Muxer/pull/240) (optional BSD Foundation C/WASM reader research). Six GitHub merge API results explicitly returned `merged=true`; final observed main `45b292c5faa48f276b7b2b1f35723d7e1489782a`.
- Merging an **optional research implementation** (#240) did not enable its default production path, authorize writer operations, or establish Softmux 1.0 release acceptance. Previous exact-HEAD PR tests cannot be represented as a fresh aggregate mainline test result.
- [#234](https://github.com/11576865/MKV-Fast-Muxer/pull/234) (obsolete icon-first UI) was closed unmerged with recorded supersession by [#239](https://github.com/11576865/MKV-Fast-Muxer/pull/239); the branch was deliberately retained. #239 remains Draft because its pilot acceptance gate failed and whole-workbench UI acceptance is unfinished. This is not a claim that closure alone finishes branch cleanup.
- After these operations, the repo branch inventory listed **52 non-main refs**. Each comparison to that exact main reported `ahead_by > 0` and `behind_by > 0`, including legacy, research, test, maintenance and `uigs-outbox` data refs. This is Git ancestry divergence, **not** proof of 52 still-missing unique behaviors. None qualifies for automated ancestry-based deletion from this snapshot; semantic replacement and independent data-branch retention must be evaluated before any pruning.
- The original merged PR head refs were no longer present in the subsequent inventory. This is an observed branch-list result, not an instruction to delete divergent refs to satisfy the numeric branch budget.

**Candidate-only reuse:** distinguish the merge-ready, current exact-head PR queue from the much larger historical branch namespace; gate high-risk UI/release transitions separately; keep CI, merged-commit identity, product default enablement and release acceptance as independent statuses. No Canonical promotion. Follow-up semantic retirement of the 52 divergent refs is still pending.

## 2026-11-05 Softmux V3 draft integration: main preservation versus source branch overlay

**Scope:** Same existing product [Draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239) after six independent PRs and newer S05 main commits landed. Its old V3 branch had diverged from main by 157 commits. No new integration branch was created.

**Grounded integration diff:** Compared exact baseline `5ce85fc8` against main `3ac5310fddfb87b65ac97ed445f0aabd68699d26` and V3 `b94747590604ff502ab1d7891e188009ce0b84b7` using Git blob trees, not just PR descriptions. V3 delta: 52 changed paths (47 additions, 5 modifications), four nonidentical overlap files requiring review (`.github/workflows/browser-e2e.yml`, `src/main.js`, `tests/e2e/browser-mux.e2e.mjs`, `tests/e2e/cross-source-ass-font-bundle-scenario.mjs`). Shared S05 preservation preflight and unit test files, P3 ASS-font logic and its unit test were identical to main after staged synchronization. A text audit uncovered missing P2 native-reference workflow steps that had been added to main by #236 and were not present in V3; those were restored on V3 in `b94747590604ff502ab1d7891e188009ce0b84b7` before merge-tree synthesis.

**Result:** Built a new Git tree from the exact main tree and overlaid the reviewed 52 V3 paths, preserving 533 main-only blob paths. Created a two-parent merge commit `b8ef01b372cf2299cbc56f30e6b1b10ee457ac2f` on the SAME V3 branch (parents: V3 head then main head), updated the ref with an expected-head check. GitHub subsequently reported PR #239 `mergeable=true`, `ahead=109`, `behind=0`, still **Draft**. This is neither a user-approved visual acceptance nor a main merge.

**Execution evidence:** Earlier direct file updates to the Draft branch yielded no workflow runs visible at those exact heads, while this exact Git Data ref update was followed by distinct PR-triggered runs: [V3 pilot #41966549198](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549198), [Browser E2E #41966549260](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549260), [S12 #41966549101](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549101) **in progress** when observed. Pages [#41966549032](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549032) build passed but PR deployment was skipped. Do not infer that the particular GitHub API method guarantees triggers across all permission/token types or that CI passed: only exact observed runs are evidence.

**Candidate-level reusable method, not Canonical:** For a large, still-unaccepted UI branch, distinguish main-ancestry reconciliation from UI acceptance; audit nonidentical shared file blobs and missing mainline regression gates before constructing a two-parent integration checkpoint. Keep PR Draft even after GitHub reports mergeability. Record precise CI head and job outcomes separately. The merge tree needs fresh exact-head regression and owner-level visual review before any mainline adoption. No automated cleanup of divergent historical branches, no 1.0 release ledger advancement.
