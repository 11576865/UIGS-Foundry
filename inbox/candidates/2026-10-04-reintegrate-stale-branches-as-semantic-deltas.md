# Candidate: Re-integrate stale feature branches as semantic deltas onto current authority

Date: 2026-10-04
Status: Candidate
Scope: branch integration / long-lived PRs / evolving architecture

## Observation

A long-lived feature PR can become unmergeable even when the feature itself is still valid, because current main has independently changed the same high-authority files.

In Quick-Automatic-Hardsub-Encoder, the Bink 2 adapter branch predated later Windows history, timeline, output verification, bridge endpoint, and capability-contract work. Copying the old feature files wholesale would have reintroduced obsolete versions of those systems.

## Candidate principle

When current main has evolved substantially, treat current main as the authority and replay the stale branch as a **semantic delta**, not as a file-version authority.

A safe integration sequence is:

1. create a fresh branch from current main;
2. identify the stale PR's changed files and intended behavior;
3. apply non-conflicting hunks only where their old context still matches uniquely;
4. resolve changed authority surfaces additively, preserving current-main behavior;
5. verify that both the new feature markers and the newer main markers remain present;
6. inspect the resulting diff for suspicious whole-file replacement or unexpectedly large churn;
7. open a replacement PR and supersede the stale one.

## Why this matters

Textual conflict resolution can be syntactically successful while semantically regressing newer architecture. The risk is highest in central files such as application state, API routers, bridge/server entry points, CI workflows, and shared UI shells.

Diff-size inspection is also a useful guardrail: a feature expected to add a few hundred lines but suddenly showing thousands of additions is evidence of integration corruption even before CI runs.

## Evidence boundary

This comes from one concrete stale-PR reintegration. It should remain Candidate until repeated across projects or independently validated.

Do not promote to Canonical from this single case.


## Independent follow-up evidence

ASS-Workbench-Android later reproduced the same integration shape with Timeline Dock:

- stale PR #82 remained behaviorally useful but was 26 commits behind current main;
- current main did not yet contain the feature;
- a fresh current-main branch replayed only the Timeline Dock semantic delta and tests;
- the resulting replacement PR #98 stayed feature-sized and preserved newer mainline authority;
- the stale PR was then closed as superseded;
- asynchronous CI was left pending after submission rather than actively polled.

This provides a second project-level example supporting the Candidate. It still remains Candidate; no automatic Canonical promotion follows from the additional case.


## PR-continuity variant: rebuild the existing head on current main

ASS-Workbench-Android PR #131 provided a narrower variant of the same rule. The feature itself was one commit ahead, while `main` had advanced four commits and only one changed regression-test file overlapped the feature surface.

Instead of opening another replacement PR, the integration rebuilt the PR head directly from current `main`:

- exact feature blobs were reused only for paths unchanged by newer `main`;
- the one overlapping regression file was replayed as a semantic hunk onto current `main`;
- the rebuilt head became one commit ahead / zero behind `main`;
- the existing PR number and review context were retained.

This refines, rather than replaces, the Candidate sequence: a fresh replacement PR is useful when history/ownership is badly tangled, but PR continuity can be preserved when the semantic replay is small, auditable, and the head can be reconstructed deterministically from current authority.

This remains Candidate-level guidance. It is not a Canonical promotion.


## Tree-consolidation variant: collapse historical branch stacks without changing the final tree

ASS-Workbench-Android PR #129 exposed a second PR-continuity case. The branch was already zero commits behind current `main`, but its history still carried more than 180 accumulated integration commits even though the actual PR tree differed from `main` in only 16 files.

The integration boundary was reduced by reconstructing the **current branch tree** directly on top of current `main`:

1. verify the PR head is zero behind current `main`;
2. enumerate the actual changed paths from the current head;
3. reuse the exact current-head blobs for those changed paths;
4. use current `main` as the base tree for everything else;
5. create one consolidation commit and move the existing PR head to it;
6. verify the resulting PR is one commit ahead / zero behind and the changed-file set is unchanged.

This is different from replaying an old feature snapshot: the source of truth is the already-reconciled **current PR tree**, not historical commits. It is useful when semantic reconciliation has already happened but the branch still contains a large, noisy integration history.

Safety boundary: this requires a stable observed head and a final race check before rewriting the ref. It must not discard concurrent updates, and it does not justify rewriting a branch whose tree has not already been reconciled against current main.

This remains Candidate-level guidance, not Canonical.
