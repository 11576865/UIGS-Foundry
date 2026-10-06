# Durable Agent Execution and Recovery

Status: **Canonical**  
Adopted: 2026-10-07  
Authority: explicit user authorization to make long-running engineering work recoverable and to prevent interactive sessions from remaining alive until timeout.

## Purpose

Complex engineering work must remain correct even when an interactive agent session, connector, browser, local runtime, or external CI job fails.

The system therefore optimizes for **durable eventual completion**, not for the unrealistic requirement that one agent session remain alive until an entire project is finished.

## Core model

An interactive agent is a disposable worker.

Durable state belongs in persisted engineering artifacts such as:
- commits;
- branches;
- pull requests;
- repository task-state records;
- CI artifacts and logs;
- issues or explicit Pending records.

Conversation memory, hidden reasoning, temporary filesystem state, and unpushed edits are not authoritative project state.

## Completion states

### Work Unit Complete

A coherent bounded unit of implementation, investigation, repair, or documentation has reached its intended local result.

### Durable Checkpoint

The useful result is recoverable independently of the current agent session.

For repository work this normally requires:
- a pushed commit;
- a branch or PR that identifies the work;
- an updated durable task-state record when the parent task spans multiple work units.

A session should prefer creating a durable checkpoint before entering another failure domain.

### Agent Execution Complete

The current interactive turn has safely finished its bounded work.

This is the default stopping point after a durable checkpoint has been submitted.

It does **not** require external asynchronous systems to have finished.

### Pending External Validation

One or more external systems are still queued, running, unavailable, or awaiting human/device evidence.

Examples:
- CI;
- emulator/device regression;
- native probes;
- render/encode jobs;
- deployments;
- code review;
- Foundry collection, triage, proposal generation, or report generation.

Pending external validation does not keep the interactive turn alive.

### External Validation Complete

The required external evidence has subsequently completed and has been observed.

### Project Complete

All planned work units and required validation for the project-level goal are complete.

Project Complete is a project state, not a requirement for one agent turn.

## Work-unit rule

Open-ended instructions such as "continue", "keep improving", "finish the project", or "fix everything" must be interpreted as project goals, not as permission for an unbounded interactive turn.

Before implementation, identify the next coherent work unit.

A work unit should have:
- a bounded scope;
- a concrete deliverable;
- a durable checkpoint;
- an explicit next state.

After the checkpoint is submitted, a new unit belongs to a later turn unless the remaining work is clearly short, local, and does not cross another failure domain.

## Checkpoint rule

Create or refresh a durable checkpoint:
- after a coherent fix or feature slice;
- before starting long external validation;
- before moving into another subsystem;
- before cross-repository work;
- before a potentially destructive or hard-to-reverse operation;
- whenever substantial useful work would otherwise exist only inside the current session.

The purpose is not to maximize commit count. The purpose is to bound the amount of useful work that can be lost with one session.

## External-job rule

For jobs whose completion is not known to be immediate:

1. start or locate the job;
2. optionally perform one immediate status read;
3. if it remains queued/running, record **Pending External Validation**;
4. stop the interactive turn.

Open-ended status polling is prohibited by default.

A user may explicitly request synchronous waiting, but that request does not override platform/session limits and must not make uncommitted useful work the only copy of project progress.

## Repair-generation rule

If an already-visible external failure is directly attributable to the current work unit:
- inspect the failure;
- perform one bounded repair generation;
- checkpoint and push the repair;
- mark the next external validation generation Pending;
- stop.

Repeated fix -> wait -> fail -> fix loops belong to separate resumable turns.

## Durable task state

A project goal expected to span multiple work units should maintain a machine-readable task-state record conforming to:

`schemas/agent-task-state.schema.json`

Recommended location in a participating product repository:

`.uigs/tasks/<task-id>.json`

At minimum, the state records:
- goal;
- current bounded unit;
- completed units;
- next units;
- branch / PR when applicable;
- latest durable commit;
- external validation states;
- blockers;
- update timestamp.

The task state is a recovery index, not a substitute for source code, tests, PR history, or CI evidence.

## Resume protocol

On "continue" or any recovery turn:

1. read the durable task-state record if one exists;
2. inspect the recorded branch/PR and latest durable commit;
3. verify that repository reality still matches the state record;
4. choose the next unfinished bounded unit;
5. update stale state before doing unrelated rediscovery.

Conversation history may provide useful context, but it is not the primary recovery mechanism.

## UIGS Intake boundary

UIGS Intake remains required after substantial reusable engineering work, but it is bounded post-processing.

Product-side work may:
- decide that no reusable knowledge appeared;
- update one narrow existing record;
- emit one bounded intake packet;
- mark a Foundry write as Pending.

Product-side work must not, by default:
- wait for Foundry CI;
- chase collection -> triage -> proposal -> report chains;
- repair unrelated Foundry failures;
- promote knowledge to Canonical as part of product delivery;
- reopen the completed product task.

Foundry automation and later Foundry work own those downstream lifecycles.

## Reliability target

The architecture should aim for:

1. **No acknowledged durable work is lost when a session dies.**
2. **An interrupted task can be resumed from persisted repository state without relying on hidden session state.**
3. **Asynchronous external work never requires an unbounded interactive polling loop.**

It must not claim that a single interactive session can be guaranteed to survive every external failure.

## Relationship to earlier candidates

This Canonical policy incorporates and supersedes the execution guidance from:
- `inbox/candidates/2026-10-02-bounded-long-running-status-polling.md`;
- `inbox/candidates/2026-10-02-branch-submission-default-execution-boundary.md`.

Those records remain as provenance for the observed failure mode and the user's repeated execution-boundary requirement.
