# Candidate: Do not synchronize an open PR branch by transiently resetting it to its base

Status: candidate
Date: 2026-10-02
Domains: operations, reliability

## Summary

When an open pull request branch must be rebased/rebuilt onto a newer base, avoid a synchronization procedure that temporarily force-resets the PR head to exactly the base commit and only afterward re-adds the branch changes.

GitHub may close a pull request when its head becomes identical to the base. Later commits on the branch do not necessarily reopen that pull request automatically.

## Evidence

During ASS-Workbench-Android stabilization work, PR #61 and PR #62 were both force-reset to the then-current `main` as the first step of rebuilding their low-conflict diffs. At the instant the head and base became identical, both PRs were automatically closed with zero commits / zero changed files. Their intended commits were subsequently recreated on the same branches, but the PRs had to be explicitly reopened.

No product changes were lost, but the operation created avoidable coordination noise and could have caused a missed CI/review cycle.

## Candidate rule

To refresh an active PR branch:
- prefer merge/rebase/cherry-pick operations that keep at least one intended branch change present throughout the update;
- if history must be rebuilt, create the rebuilt commit/tree before moving the public PR ref;
- if a transient base-identical reset is unavoidable, explicitly verify PR state afterward and reopen if necessary;
- do not infer that subsequent pushes will automatically restore the PR to open state.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull requests: `#61`, `#62`
- base commit at reset: `235f9c8d89408ea6832a87c05398c594462e03a1`
- rebuilt heads: `513fcb5b624298894e51debf414e77d282abab3a`, `bfd3c2e2fa47ec2e7ba7bc4d05b782b735f75e66`
- evidence level: directly observed repository state transition

This is a Candidate only. It is not Canonical.
