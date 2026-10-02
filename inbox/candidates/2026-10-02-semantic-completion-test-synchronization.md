# Candidate: Synchronize asynchronous UI tests on semantic completion and isolate presentation cases

Status: candidate
Date: 2026-10-02
Domains: reliability, testing, interface-grammar

## Summary

When an instrumentation test crosses asynchronous persistence/recovery work and then changes a large UI presentation, synchronize on the **semantic completion condition** of the asynchronous work rather than using fixed sleeps or treating popup/navigation timing as proof of application-state corruption.

For cross-presentation invariant tests, prefer one clean test case per presentation instead of a long serial traversal through many presentations.

## Evidence

ASS-Workbench-Android PR #61 originally exercised several presentation changes in a single Activity session. Early failures were repeatedly attributed to popup/menu discovery and asynchronous recovery timing rather than to the canonical document, Focus, or Undo/Redo invariants being tested.

The test was restructured so that each presentation begins from a deterministic Recovery fixture and:
1. creates a canonical edit and pre-existing Undo history;
2. waits until RecoveryStore's durable journal actually contains that edit;
3. switches to exactly one presentation;
4. verifies canonical Event text, Focus identity, and history;
5. exercises Undo/Redo.

This separates asynchronous journal completion from presentation navigation and makes a red result attributable to one presentation.

## Candidate rule

- Synchronize asynchronous work using an observable semantic completion predicate when one exists.
- Avoid arbitrary sleep as the primary synchronization mechanism.
- Do not interpret navigation/popup discovery failures as domain-state failures.
- For heterogeneous UI presentations, isolate each presentation in its own deterministic test case unless state carry-over is itself the invariant under test.
- Keep domain invariants and navigation mechanics separately diagnosable.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#61`
- test: `PresentationStateSmokeInstrumentedTest`
- evidence level: repeated emulator failures followed by test restructuring around RecoveryStore durable state and per-presentation isolation

This is a Candidate only. It is not Canonical.
