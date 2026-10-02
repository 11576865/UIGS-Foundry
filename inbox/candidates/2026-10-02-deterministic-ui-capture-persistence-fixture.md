# Candidate: Deterministic UI capture fixtures must own their persistent preconditions

Status: candidate
Date: 2026-10-02
Domains: reliability, interface-grammar

## Summary

A deterministic UI screenshot/capture test must not depend on process-shared persistence being left in the expected state by test ordering.

If the captured UI requires persisted recovery/session data, the capture test should establish that persistence state itself and then load it into the live product state before waiting for visual readiness.

## Evidence

ASS-Workbench-Android's Android production-UI capture test originally relied on the debug Activity startup to seed RecoveryStore and then clicked the normal recovery UI.

After an additional presentation regression case was added, the presentation invariants themselves all passed, but the visual capture test intermittently timed out waiting for the expected two-Event document.

RecoveryStore is process-shared and earlier instrumentation cases can schedule asynchronous recovery writes. Therefore test ordering/timing can disturb the startup persistence precondition even though the product UI under capture is unchanged.

The capture fixture was changed to:

1. clear the shared recovery journal;
2. write the deterministic fixture;
3. synchronously restore that exact fixture into the current EditorViewModel;
4. wait for semantic identity (Event IDs and exact text), not only event count;
5. capture the real Android compositor.

## Candidate rule

For production visual capture and other deterministic UI fixtures:

- own all persisted preconditions inside the capture fixture;
- do not treat test ordering or a previous test's cleanup as part of the fixture contract;
- after seeding persistence, synchronize the live product state to that seed before visual readiness checks;
- use semantic identity checks, not only coarse counts or fixed delays;
- keep the fixture path debug/test-only when the behavior under test is the production UI rather than recovery UX itself.

This complements the existing semantic-completion synchronization and automated-production-visual-evidence candidates. It does not change Canonical guidance.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- PR: `#71`
- head: `c230659f68fb84edf55b330496f643ef5761a020`
- failing evidence: PR #69 Android Emulator Regression run `36999110222`
- evidence level: repeated CI failure plus fixture-isolation implementation, validation pending

