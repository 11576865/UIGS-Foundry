# Candidate: Superseded parallel PRs should be closed or reduced to unique deltas, not conflict-merged wholesale

Status: **Candidate / reusable branch-integration pattern**
Date: 2026-10-03
Project evidence: `11576865/MKV-Fast-Muxer`, PR #57 / PR #58

## Observation

Two pull requests implemented substantially the same font content-identity feature from the same older base.

PR #58 was merged first and contained the newer implementation, including additional preflight, filename normalization, orchestration, and E2E fixes. PR #57 remained open on its older branch. Once #58 landed on `main`, GitHub reported #57 as conflicting because both branches modified the same files and concepts.

The conflict did not mean that the stale branch needed to be mechanically reconciled into `main`. Doing so would risk reintroducing an older implementation over a newer one.

## Candidate rule

When a parallel or duplicate PR becomes conflicted after another PR for the same feature has merged:

1. First classify the PR as **independent**, **partially superseded**, or **fully superseded** before touching conflict markers.
2. Compare semantic behavior and unique deltas, not only changed filenames.
3. If fully superseded, close it with an explicit pointer to the merged replacement.
4. If partially superseded, transplant only the still-useful unique delta onto a branch based on current `main`; do not merge the stale branch wholesale.
5. Treat “resolve conflicts” as an integration decision, not a textual merge exercise.
6. Re-run current tests from the current base for any transplanted delta.

A useful decision flow is:

```text
conflicted old PR
  -> compare against current main / merged replacement
  -> no unique value -> close as superseded
  -> unique value remains -> extract minimal delta onto fresh current-base branch
```

## Evidence

In MKV-Fast-Muxer, PR #57 and PR #58 both implemented content-derived font identity. PR #58 merged as `a63dec997207515d37ca26939754fd73f4367a11` and contained a more complete implementation. PR #57 subsequently reported merge conflicts. It was reviewed against the merged implementation and closed as superseded rather than force-merged.

## Scope

Applicable to parallel feature branches, duplicate bot/agent PRs, stacked changes that accidentally overlap, and repositories where multiple automation agents may implement the same task concurrently.

Do not promote to Canonical from this single-project observation without broader validation.
