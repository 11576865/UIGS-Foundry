# Candidate: Terminal job status reads must be idempotent and independent of disposed runtime handles

Status: candidate
Date: 2026-10-02
Domains: reliability, operations, agent-workflow
Evidence type: direct bug diagnosis and implementation repair

## Summary

A long-running job API must treat terminal state as a durable snapshot rather than re-deriving it from transient runtime objects such as Process, thread, session, socket, Activity, or worker handles.

After a job reaches a terminal state, repeated status reads and downstream actions such as publish/export must be safe even if the runtime handle has already been disposed or detached.

## Evidence

Quick-Automatic-Hardsub-Encoder Windows Native stored a completed job and its verified staging output, but `Export-Job` called `Get-JobStatus` again before publishing. The old status path touched the job Process object before checking the already-recorded terminal state. The Process had been disposed after finalization, and the observed save workflow failed after successful encoding/verification with a PowerShell `op_Subtraction` overload error on the status/export path.

The repair resolves `completed`, `failed`, and `cancelled` snapshots before touching the Process handle. A completed snapshot also verifies that its staged output still exists and is non-empty before allowing export.

## Candidate rule

For long-running job state machines:

- persist an explicit terminal state and the minimal terminal result needed by later actions;
- status reads after terminal transition must be idempotent;
- terminal status reads must not require access to disposed runtime handles;
- publish/export/retry actions should consume the terminal snapshot and staged artifact, not restart or reconstruct the execution lifecycle;
- if a terminal snapshot references a missing staged artifact, transition to an explicit failure/recovery state rather than silently reporting success;
- regression coverage should include repeated status reads after completion and publish/export after the execution handle has been disposed.

## Scope

Applies to subprocess-based encoders, build jobs, renderers, background services, workers, deployment tasks, and similar asynchronous job systems.

## Related Foundry knowledge

- `REL.SINGLE_OWNER_LONG_JOB`
- `REL.DURABLE_STAGING_FOR_LONG_JOB`
- `REL.VERIFY_THEN_PUBLISH`
- `inbox/candidates/2026-10-02-long-job-stage-observability-and-completion-handoff.md`

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- source workflow: Windows Native verified-output export
- repair branch: `fix/task-handoff-progress-save`
- evidence level: direct user-observed failure + source-level fault path + regression guard

This is a Candidate only. It is not Canonical.
