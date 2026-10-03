# Candidate: Monitor loss must not release long-job ownership

Status: candidate
Date: 2026-10-03
Domains: reliability, long-running-jobs, interaction-state
Evidence type: code audit plus deterministic regression

## Summary

Losing the status channel for a long-running task is not evidence that the task ended.

A client may stop or bound status polling after repeated failures, but it must not release task ownership, clear recoverable job identity, or re-enable conflicting input mutations unless the backend job is known to be terminal.

## Evidence

Quick-Automatic-Hardsub-Encoder guided Native monitoring previously retried failed status reads indefinitely.

A naive alternative would be to abandon the job after a retry limit, but that would allow a second task or input mutation while the original Native encode could still be alive.

PR #43 now:
- bounds consecutive status-read retries to five;
- stops hot polling after the threshold;
- preserves `state.nativeJobId`;
- preserves the persisted recovery key `nativeEncodeJobId`;
- keeps input/config mutation locked;
- instructs the user to keep the Bridge alive and reload to reconnect.

A dedicated VM regression asserts that monitor loss does not clear ownership.

## Candidate rule

- status-channel failure and task termination are distinct states;
- bounded polling is acceptable, but ownership must persist while task liveness is unknown;
- preserve the durable/recoverable task identifier across monitor loss;
- do not enable a competing task or mutate execution inputs merely because observation failed;
- surface a reconnect/recovery instruction rather than a false terminal state;
- release ownership only on an authoritative terminal state, explicit abandonment policy, or verified backend absence;
- regression tests should separate “cannot observe” from “task ended”.

## Relationship to existing Foundry knowledge

Related:
- `REL.SINGLE_OWNER_LONG_JOB`
- `REL.DURABLE_STAGING_FOR_LONG_JOB`
- `inbox/candidates/2026-10-02-bounded-long-running-status-polling.md`

This Candidate focuses specifically on the ownership semantics when bounded monitoring gives up.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #43 `Stabilize input lifecycle and native picker identity`
- evidence level: code-audited failure path plus deterministic VM regression

This is a Candidate only. It is not Canonical.
