# Candidate: Terminal task state classification must not depend on localized message text

Status: candidate
Date: 2026-10-03
Domains: reliability, interaction-state, localization
Evidence type: code audit plus executable regression

## Summary

Machine workflow state must be derived from explicit state/status values or normalized error classes, not from localized human-readable message fragments.

## Evidence

In Quick-Automatic-Hardsub-Encoder manual Native tasks, a cancelled job could surface as the machine state `cancelled`. The workspace catch path recognized cancellation only when the error message contained the Chinese substring `取消`.

Therefore a legitimate Native cancellation could be misclassified as a processing failure.

PR #35 replaces the single localized substring test with normalized cancellation recognition and adds cancel → idle → rerun regression coverage.

## Candidate rule

- terminal state classification should use explicit machine state or a normalized error/category code;
- human-readable localized text is presentation, not control data;
- if string compatibility handling is unavoidable, normalize known machine spellings independently of locale;
- cancellation and failure must remain distinct in UI, recovery behavior, telemetry and tests;
- regression tests should include terminal states emitted in a different language/spelling from the UI locale.

## Scope

Applies to long-running jobs, build/deploy systems, media processing, file operations, network tasks, and localized applications with native/backend bridges.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #35
- evidence level: deterministic code path plus regression test

This is a Candidate only. It is not Canonical.
