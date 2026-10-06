# Agent protocol

This repository is a knowledge-control plane, not a dumping ground.

## Execution safety — highest priority

Interactive agent sessions are disposable workers. Repositories, commits, branches, pull requests, task-state records, and other persisted artifacts are the durable state.

1. **Persist useful work early and incrementally.** Do not keep the only copy of meaningful progress in conversation memory, hidden reasoning, a temporary worktree, or an unpushed local state.
2. **Use bounded work units.** Broad goals such as "continue improving the project" must be converted into one coherent work unit with an explicit durable checkpoint before the next unit begins.
3. **Checkpoint before crossing failure domains.** Before long CI, emulator/device tests, renders, deployments, cross-repository work, or other asynchronous/external operations, commit and push the coherent work completed so far whenever it is safe to do so.
4. **A pushed commit / branch / PR is the default execution boundary.** Once the requested coherent work unit is durably submitted and no immediately actionable failure is already known, mark the agent work complete and return control to the user.
5. **External validation does not keep the turn alive.** Pending CI, builds, emulator runs, native probes, renders, deployments, reviews, Foundry collection/triage, or promotion processing are reported as Pending and do not block Agent Execution Complete.
6. **Do not poll open-endedly.** After starting or locating an external job, perform at most one immediate status read unless the user explicitly requested synchronous waiting. If it is still queued/running, report Pending and stop.
7. **Bound repair generations.** If an already-visible failure is directly caused by the current work unit, one immediate repair generation may be performed. After re-pushing the repair, do not wait for the next validation generation; report it Pending and stop.
8. **Make interrupted work resumable from repository state alone.** For work expected to span more than one coherent unit, maintain a durable task state following `governance/AGENT-EXECUTION.md` and `schemas/agent-task-state.schema.json`.
9. **Resume before rediscovering.** On a continuation request, read the durable task state, branch/PR, and latest durable commit first. Do not reconstruct project progress primarily from conversational memory.
10. **UIGS Intake is bounded post-processing.** Intake may classify and persist reusable knowledge, but it must not reopen the primary product task, wait for Foundry CI, chase downstream automation, or silently expand into another unbounded workstream.
11. **Foundry processing is asynchronous by default.** Product-side agents may emit/update a bounded intake record or mark it Pending. Collection, triage, proposal generation, reporting, validation, and Canonical promotion are separate lifecycles.
12. **Never claim external completion without evidence.** Distinguish Agent Execution Complete, Pending External Validation, External Validation Complete, and Project Complete.

These rules take precedence over lower-level intake, reporting, validation, and workflow instructions whenever continuing those activities would risk losing already-completed work or keeping an interactive turn alive without a bounded purpose.

## Knowledge-control protocol

1. After substantial software/UI/testing/engineering work, perform a UIGS Intake Check.
2. Determine whether the new information is reusable beyond the immediate task.
3. Search existing registry and inbox records before creating a new one.
4. Record provenance and evidence level.
5. Prefer updating an existing family over creating a duplicate.
6. A single observation may create Observation, Candidate, Case, Bug, Test, Lesson, or implementation reference.
7. Do not silently promote a rule to Canonical; follow `governance/PROMOTION.md`.
8. Product repositories remain authoritative for executable implementation.
9. If a Foundry write cannot be completed, report it as **Pending**; never imply success.
10. For UI work resolve: natural-language intent -> Pattern ID -> platform realization -> expected effect -> validation contract -> known failures.
