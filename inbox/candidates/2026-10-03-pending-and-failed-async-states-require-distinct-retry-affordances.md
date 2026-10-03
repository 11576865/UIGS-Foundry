# Candidate: Pending and failed async states require distinct retry affordances

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, interaction-state, reliability
Evidence type: state audit plus user-facing failure path

## Summary

An asynchronous operation that is still pending and one that has already failed must not share the same disabled UI state.

A failed terminal state should expose the failure and an explicit retry path when retry is valid.

## Evidence

Quick-Automatic-Hardsub-Encoder used the absence of a successful Native input probe as one combined state. Both:

- probe still running; and
- probe finished with `ok:false`

made the source-analysis button disabled with the label “正在读取视频参数…”.

After a probe failure, the UI could therefore look permanently busy and offered no retry action.

PR #41 now distinguishes:

- no result yet → pending, disabled, “正在读取视频参数…”;
- failed result → retryable, enabled, “重试读取视频参数”;
- successful result → normal source-inspection / subtitle-analysis action.

## Candidate rule

For retryable async operations:

- represent pending and failed as separate states;
- pending may suppress duplicate execution;
- failed must not continue to present itself as pending;
- show the failure reason in the local context;
- when retry is valid, expose an explicit retry affordance without requiring unrelated state changes;
- state-transition tests should cover pending → failed → retry → success.

## Scope

Applies to source probes, validation, remote lookup, import, synchronization, preview generation, upload/download and other retryable async operations.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #41 `Stabilize Windows Native sessions and workflow state`, merged as `04bdf5764a4850a931cf93bec80de423de97afb8`; earlier PR #35 was superseded and closed
- evidence level: code-audited terminal-state defect plus regression contract

This is a Candidate only. It is not Canonical.
