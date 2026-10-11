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
