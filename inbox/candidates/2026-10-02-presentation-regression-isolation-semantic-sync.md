# Candidate: Isolate UI presentation regressions and synchronize on semantic completion

Status: candidate
Date: 2026-10-02
Domains: reliability, interface-grammar

## Summary

When a UI regression traverses multiple presentation modes while background persistence or recovery work is still asynchronous, one long multi-presentation test can make failures difficult to attribute.

Prefer one independent test case per presentation from a deterministic baseline, and synchronize asynchronous side effects using a **semantic completion condition** rather than a fixed sleep.

## Evidence

ASS-Workbench-Android PR #61 originally exercised several experimental presentations in one Activity session. Repeated failures occurred around popup navigation before the canonical-state invariant itself, and state from the previous presentation plus asynchronous recovery journal writes could contaminate the next step.

The test was restructured so that Canvas, Pager, Spatial, Tool Instances, Glass Layered, Precision Lens, and Subtitle Object each run as an independent test case. Each case:

1. restores a deterministic Recovery fixture;
2. establishes Focus and a canonical document edit;
3. waits until RecoveryStore actually contains that edit;
4. switches exactly one presentation;
5. verifies canonical text, Focus identity, Undo availability;
6. executes Undo/Redo to prove the history remains operational.

This narrows the Red Reason to one presentation and avoids using an arbitrary delay for recovery I/O.

## Candidate rule

For regression tests spanning presentation modes or asynchronous persistence:

- start each presentation case from a deterministic baseline when cross-case state is not itself under test;
- wait on the domain-level completion condition (journal contains expected edit, transaction reaches committed state, etc.) instead of sleeping for a guessed duration;
- keep navigation failures distinguishable from domain invariant failures;
- verify operational history with Undo/Redo, not only a boolean availability flag;
- combine presentations into one continuous scenario only when continuity itself is the behavior under test.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#61`
- head: `87340ef80790e8d8bd209c3cd81785189e48be91`
- evidence level: implementation plus Android instrumentation gate in progress; prior failing attempts established attribution problem

This is a Candidate only. It is not Canonical.
