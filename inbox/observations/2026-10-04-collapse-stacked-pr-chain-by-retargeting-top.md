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
