# Candidate: Bound status polling for long-running external jobs

Status: historical candidate — incorporated into Canonical `governance/AGENT-EXECUTION.md`
Date: 2026-10-02
Domains: operations, reliability, agent-workflow

## Promotion note

On 2026-10-07, the user explicitly authorized the execution-reliability change that promoted this guidance into the Canonical durable agent execution policy.

This file remains as provenance for the original failure observation. For current execution behavior, follow `governance/AGENT-EXECUTION.md` and root `AGENTS.md`.

## Summary

For long-running CI, build, deployment, render, test, or other external jobs, an interactive agent should not keep a conversation turn occupied by repeatedly polling branch/job status until completion.

The interaction should instead use bounded observation: start or inspect the job, perform only a small finite number of status reads when useful, and return control to the user while the job remains pending.

## Evidence

During ASS-Workbench-Android work, the user reported that some builds can run long enough that continuous branch/build status checking risks conversation timeout or an apparently stuck turn.

The current project also relies on multiple independent validation pipelines, so waiting synchronously for every status transition is not required to preserve the engineering evidence model.

This is a reported interaction/operations failure mode, not yet a quantified platform timeout threshold.

## Original candidate rule

For external operations whose completion time is not known to be short:

- do not enter an open-ended polling loop inside one conversation turn;
- after triggering or locating the job, use at most a bounded number of immediate status checks;
- if status is still pending / queued / in progress, report that state and end the turn;
- check again only on a later explicit user request, a later project step that requires the result, or a user-approved scheduled/conditional watcher;
- do not continuously compare branch heads merely to wait for CI completion;
- separate "job has been started" from "job has completed and passed" in reports;
- if a result is required before a destructive or irreversible action, stop before that action rather than blocking indefinitely.

## Scope

Applies to:
- GitHub Actions / CI
- Android emulator and native probe workflows
- release builds
- long encodes or renders
- deployments
- cloud jobs and similar asynchronous external work

Does not prohibit a single status read or a short, explicitly bounded follow-up check when completion is expected imminently.

## Provenance

- source repository context: `11576865/ASS-Workbench-Android`
- source: direct user feedback during 2026-10-02 engineering work
- evidence level: user-reported operational failure mode / process candidate
