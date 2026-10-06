# Candidate: Branch submission is the default execution boundary for asynchronous CI

Status: **historical candidate — incorporated into Canonical `governance/AGENT-EXECUTION.md`**
Date: 2026-10-02

## Promotion note

On 2026-10-07, the user explicitly authorized the execution-reliability change that promoted this boundary into the Canonical durable agent execution policy.

This file remains as provenance for the original user-established workflow and its later reinforcement. For current execution behavior, follow `governance/AGENT-EXECUTION.md` and root `AGENTS.md`.

## Trigger

During ASS Workbench Android work, the user explicitly established a process boundary: after code changes are complete and the branch/PR has been submitted, the assistant's active work for that turn ends. The assistant should not remain in a polling loop waiting for CI, emulator, renderer, or other asynchronous workflow completion.

## Reusable workflow rule

For repository work with asynchronous CI:

1. finish the requested code or configuration change;
2. commit/push the branch and create or update the PR;
3. report the submission point and any workflow status already available at that moment;
4. if checks are still running, mark them as **Pending CI** and stop;
5. resume only when the user explicitly asks to inspect a failure, continue after CI, or handle a new result.

Do not spend the remainder of the turn repeatedly polling long-running workflows unless the user explicitly requests synchronous waiting.

## Why this generalizes

The rule applies to coding agents, release automation, documentation PRs, test-fix workflows, and other asynchronous engineering systems. It separates:
- **agent execution completion**: artifact/branch/PR has been submitted;
- **external validation completion**: CI or review later reports a result.

This reduces idle polling, wasted tool/runtime budget, and unnecessary follow-up churn while preserving a clear handoff point.

## Exceptions

Continue past branch submission only when:
- the user explicitly asks to wait for or monitor CI;
- the task definition itself requires a completed external result before it can be considered submitted;
- an immediately available failure is already known and the user requested it to be fixed in the same turn.

## Evidence boundary

This began as one explicit user workflow preference in an active engineering project and was later reinforced by repeated failure observations. The current authoritative rule now lives in `governance/AGENT-EXECUTION.md`.

## Reinforcement — 2026-10-04

The user explicitly reinforced the execution-boundary rule with a failure mode to avoid: **do not keep checking progress until the conversation/session times out**.

Operationally, once the requested code/configuration/document work has been submitted and no immediately actionable failure is already present, the agent must stop active polling. A running CI job is reported as Pending CI; it is not a reason to consume the rest of the session.
