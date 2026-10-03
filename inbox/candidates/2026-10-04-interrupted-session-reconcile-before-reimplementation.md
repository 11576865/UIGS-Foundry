# Candidate: Interrupted engineering sessions must reconcile existing work before reimplementation

Status: **Candidate / user-established engineering workflow**
Date: 2026-10-04

## Trigger

The user explicitly established a continuation rule for repository work after a conversation/session timeout or restart:

When work resumes, do not assume the requested feature is still unimplemented and do not write the same code again by default. First inspect the previous conversation requirements and the repository's current state to determine whether the requested functionality was already implemented, partially implemented, submitted in a branch/PR, merged, superseded, or blocked.

## Reusable workflow rule

For resumed engineering work after interruption, timeout, model/session restart, or handoff:

1. recover the prior user request and acceptance criteria from conversation/project context;
2. inspect the relevant repository state before editing:
   - current main/base;
   - open and recently merged PRs;
   - relevant feature/integration branches;
   - recent commits;
   - existing files/tests/docs implementing the requested behavior;
3. classify each requested capability as:
   - already implemented;
   - partially implemented;
   - implemented but not integrated;
   - superseded by newer work;
   - not implemented;
   - unknown / insufficient evidence;
4. continue only from the missing or broken portion;
5. do not recreate a second implementation merely because the previous execution context is gone;
6. if existing work is present, prefer verification, integration, repair, or completion over duplicate rewriting.

## Why this generalizes

Agent/session state is ephemeral while repository state is durable. Treating a new session as a blank implementation state creates duplicate code paths, conflicting authorities, redundant PRs, regressions, and false claims that work is new.

The durable source of truth for continuation is therefore the combination of:
- prior user intent / acceptance criteria;
- current repository history and branches;
- tests and evidence already present.

## Relationship to the asynchronous CI boundary

This rule complements the existing Candidate **Branch submission is the default execution boundary for asynchronous CI**.

That rule says not to burn the session polling external validation after submission. This rule says that when a later session resumes, it must first reconcile what the earlier session already produced instead of starting the implementation again.

## Evidence boundary

This rule originates from an explicit user workflow requirement in an active engineering project. Treat as Candidate process knowledge. Do not promote to Canonical solely from this instruction.


## Continuation planning

Reconciliation also applies before choosing the **next** engineering task, not only before editing a file.

After an interrupted or resumed session, inspect open/merged PRs and explicit branch ancestry/dependencies before proposing new implementation. If existing work already forms an ordered stack, prefer closing, rebasing, integrating, validating, or superseding that stack over starting another parallel implementation.

This prevents a resumed session from misclassifying integration debt as missing product capability.
