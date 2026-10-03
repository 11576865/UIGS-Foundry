# Case: Re-land stale ASS Timeline Dock from current main

Date: 2026-10-04
Status: Case / stale-branch semantic reintegration
Project: 11576865/ASS-Workbench-Android

## Trigger

The open Timeline Dock PR #82 still represented useful product behavior, but its branch had diverged from current main:

- head: `feature/timeline-dock-workspace`;
- ahead of main: 1 commit;
- behind main: 26 commits;
- the older `integration/timeline-dock` ancestry was substantially further behind.

The feature was not present in current main, so it was neither safe to discard as obsolete nor safe to treat the stale branch tree as current authority.

## Reconciliation

The resumed work first inspected current main, the open PR, earlier Timeline Dock integration history, and the current presentation registry.

A fresh branch was then created from current main:

`feature/timeline-dock-workspace-v2`

Only the semantic delta was replayed:

- `TIMELINE_DOCK_EXPERIMENTAL` registration;
- the persistent Preview + Timeline presentation;
- bounded vertical resize and stable snap policy;
- explicit expand/collapse control;
- one continuously mounted `ModernTimelinePane`;
- registry tests;
- presentation-state invariant coverage;
- 240-ledger traceability updates.

The resulting diff remained feature-sized: seven files, with no whole-tree replacement of newer mainline code.

## Replacement boundary

Replacement PR #98 was opened from current main as a draft. The stale PR #82 was explicitly marked superseded and closed rather than kept as a second active authority.

CI is asynchronous and was left running after submission rather than polled until completion.

## Reusable evidence

This is a second project-level instance of the existing Candidate rule:

**Re-integrate stale feature branches as semantic deltas onto current authority.**

It independently supports these practices:

1. inspect existing implementation and branch ancestry before writing;
2. preserve current main as authority;
3. replay feature intent and tests instead of stale file versions;
4. inspect final diff size/surface as a corruption guardrail;
5. supersede the stale PR once the current-main replacement exists;
6. stop at the submission boundary while CI remains asynchronous.

## Evidence boundary

This Case strengthens an existing Candidate with an independent ASS Workbench example. It does not by itself promote the rule to Canonical.
