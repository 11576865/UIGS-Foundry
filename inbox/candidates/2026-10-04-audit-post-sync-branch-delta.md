# Candidate: Audit post-sync branch delta for unrelated main regressions

Status: candidate
Date: 2026-10-04
Domains: git, branch-integration, CI, engineering-process

## Summary

A feature branch can report `behind_by = 0` after merging current main and still contain stale or deleted versions of files that the feature did not intend to change.

This can happen when a prior manual/conflict-resolved merge constructs a tree that records main as a parent but accidentally preserves the feature branch's older copy of unrelated files. Git ancestry then says the branch contains main, while the effective tree silently regresses main behavior.

## Candidate rule

After synchronizing a long-lived or manually merged feature branch with main:

1. Do not treat ancestry alone (`behind_by = 0`, merge-base, or a successful merge commit) as proof that the branch preserved the main baseline.
2. Compare the resulting branch tree against current main.
3. Classify every remaining changed file as either intentional feature delta or suspicious unrelated drift.
4. Any unrelated modified/deleted file should be restored from main before CI is treated as meaningful feature validation.
5. Re-run CI only after the post-sync delta contains the intended feature surface.
6. Prefer this audit especially after hand-built merge trees, conflict resolution, cherry-pick stacks, or branches that crossed several concurrent PR merges.

## Evidence

While synchronizing ASS Workbench Android PR #84 after PR #86 merged, the branch reached `behind_by = 0`, but the post-sync compare still showed:

- `VideoPreview.kt` modified relative to current main
- `FrameTransportTest.kt` deleted relative to current main

Neither file belonged to the spatial-reflection-fade feature. They were stale transport-baseline artifacts preserved by an earlier branch merge. Restoring both files from current main reduced the compare set to the intended FX/UI/test/documentation files before the new CI run.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #84
- evidence level: concrete branch-integration fault detected and corrected before merge
- deduplication: searched UIGS-Foundry for post-sync delta / unrelated main regression guidance; no direct duplicate found
- status rationale: reusable engineering-process candidate; not enough cross-project evidence for Canonical

This is a Candidate only. It is not Canonical.


## Additional stacked-branch regression observation — CVS PR #18 (2026-10-10)

A different integration window was observed in `11576865/Character-Voice-Service`:

- The source branch of [PR #15](https://github.com/11576865/Character-Voice-Service/pull/15) contained a late amendment to the Evaluation Registry: schema v1.1 permits **one** reference per `generation_revision`.
- Descendant PR #16 was created from a **specific earlier commit** of that branch, before the amendment. PR #17 inherited the stale Evaluation Registry file. Code inspection showed the actual file in #15 enforcing `len(references) == 1`, while #16 and #17 still allowed arbitrary nonempty reference lists.
- [PR #18](https://github.com/11576865/Character-Voice-Service/pull/18), stacked on #17, restores the omitted contract and adds write-time plus read-time regression coverage.

This is a distinct source-level example of **branch ancestry being a snapshot, not a live dependency**. A PR targeting an upstream feature branch does not mean its head automatically receives later commits to that branch. Before merging a stack, audit changed contract files and replay necessary upstream fixes into descendants or reconcile the branches explicitly.

The fix is submitted but full CI and final merge reconciliation are Pending. This augments the existing Candidate about branch-delta auditing; no new Canonical rule or duplicate Candidate is created.
