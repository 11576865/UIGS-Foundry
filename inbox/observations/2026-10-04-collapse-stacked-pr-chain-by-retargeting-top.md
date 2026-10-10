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


## Extension: exact-tree reconstitution for a divergent PR stack — CVS (2026-10-11)

Project: `11576865/Character-Voice-Service`  
Aggregation PR: https://github.com/11576865/Character-Voice-Service/pull/21  
Input PRs: #14, #15, #16, #17, #18, #19, #20  
Status: **Integration PR submitted; integration CI and mergeability not yet verified.**

CVS had seven open stacked PRs. Each source PR head had one successful
`CVS tests` GitHub Actions run, with successful Linux `test` and Windows
`windows-script-audit` jobs. However #16 was cut from an earlier #15
commit and **did not inherit three later #15 commits**. The substantive
v1.1 single-reference-per-generation-revision behavior was restored in
#18 and carried through #20, with stricter testing. The #20 documents
also corrected a late #15 documentation newline-escape artifact.

Simply retargeting the top PR and trusting its nominal base relationship
would not prove that all later upstream changes were represented.
A distinct consolidation approach was used:

1. Compare the **current main** against the final top-of-stack head and
   enumerate the 22 modified/added paths, checking there were no deletions
   or unrelated baseline changes.
2. Create a new Git tree from current main, replacing exactly those 22
   paths with their **Git blob SHA identities from the top branch**.
3. Commit that tree with **main as its single parent**, preserving one
   independent integration commit and avoiding the divergent 63-commit
   ancestry in the proposed merge.
4. Verify complete tree equality rather than relying only on the
   difference listing: the reconstructed integration tree and the top
   source commit both yielded Git Tree SHA
   `73f404ae65b73f0a7ce3c22821fca2c190443708`.
   The new commit is `1ba3904f91d79714428348cbf6bc809a715d8474`
   and the original top source is
   `a037b63724c5619c8c8a035da6ee755ab3e5efb6`.
5. Open PR #21 **directly against main**, retaining the seven source PRs
   for provenance until the new combined PR passes CI and is merged.

**Evidence boundary:** Git Tree SHA identity proves byte-for-byte Git
tree equivalence at these two commits, not that the source stack's
runtime behavior is correct. All source workflow runs were green; the
new main-targeted integration PR has **Pending CI**. The create-PR
response reported `mergeable=false`; this is **not** treated as
evidence of confirmed conflict or success without GitHub recomputation.
No source PR was prematurely merged or closed.

This method complements, rather than supersedes, the prior single-root
merge/retarget and current-main semantic-delta approaches: exact-tree
reconstitution is suitable when an already reviewed final tree is the
intended product state, but the branch ancestry is divergent and direct
PR stacking creates review or merge ambiguity. It preserves Git file
content, **not individual commit ancestry**, so original PR links must
remain available for granular review.

Dedup: existing records cover stacked-PR collapse, content-equivalent
ancestry merge and post-sync diff auditing; this is an incremental
**Observation** about exact full-tree identity and a fresh main parent,
not a new Canonical rule. No Canonical promotion.
