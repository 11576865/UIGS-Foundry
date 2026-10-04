# Observation: Collapse a stacked PR chain by merging the validated root and retargeting the top PR

Status: observation
Date: 2026-10-04
Domains: engineering-process, git, stacked-prs, integration

## Situation

ASS-Workbench-Android had a linear stack:

- PR #103 -> main
- PR #104 -> #103 branch
- PR #105 -> #104 branch
- PR #107 -> #105 branch
- PR #110 -> #107 branch

The root PR #103 had fresh successful Android CI, Emulator Regression, and Fontconfig probe evidence. The intermediate stacked PRs had no independent workflow runs because they targeted feature branches rather than main.

## Action

1. Mark the validated root PR ready and merge it into main using a merge commit so the feature head remains in main ancestry.
2. Retarget the top PR directly to main.
3. Verify GitHub recomputes the top PR as clean/mergeable and that the resulting diff contains the combined remaining stack.
4. Close the now-redundant intermediate PRs as unmerged/superseded.
5. Mark the consolidated top PR ready so main-targeted CI can run asynchronously.

## Result

- PR #103 merged to main at merge commit d6d5c359c60e63aba19e55aad859ab22eef94f58.
- PR #110 was retargeted to main and recomputed as mergeable/clean.
- PRs #104, #105, and #107 were closed as redundant intermediate stack layers.
- PR #110 became the single active UI/spatial integration PR for the remaining 50-file combined delta.
- Separate Matroska branches (#108/#109/#106) became non-mergeable against the advanced main and require an explicit current-main reconciliation rather than blind merge.

## Reusable lesson

For a strictly linear stacked PR chain, once the dependency root is validated, preserving its ancestry with a merge commit can make it possible to collapse the remaining stack by retargeting only the top PR to main. This reduces PR bookkeeping without replaying each intermediate feature separately.

Do not apply this mechanically when branches are not a strict ancestry chain or when parallel branches supersede/modify overlapping files. Those require semantic reconciliation.

## Evidence boundary

This is one successful project case, not a Canonical rule. Repository branch protection, CI triggers, merge strategy, and conflict behavior can differ.

No Canonical promotion.


## Extension: parallel stack consolidation

The same ASS integration pass also had a parallel Matroska branch family that could not be represented by simple stacked retargeting.

A clean consolidation path was:

1. replay the latest Matroska-owned blobs onto current main as one explicit current-main branch;
2. verify the resulting PR is independently mergeable against main;
3. open a temporary branch-to-branch integration PR from that consolidated Matroska branch into the existing top spatial integration branch;
4. let GitHub perform the normal three-way merge and confirm it is clean;
5. merge that temporary PR into the integration branch, close the now-redundant Matroska PR, and leave one final main-targeted integration PR.

This avoided manually reconstructing a cross-domain merge when GitHub's three-way merge could already prove the two current-main deltas were compatible.

Use this only when both sides have been reconciled to the same current-main base and the temporary integration PR is clean/mergeable. A dirty integration PR still requires semantic conflict resolution rather than force-merging.
