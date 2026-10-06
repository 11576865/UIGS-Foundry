# Project Adapter Protocol

Status: implemented baseline
Date: 2026-10-02

Each participating product repository exposes .uigs/project.json and .github/workflows/uigs-intake.yml.

The adapter currently provides two intake paths:

1. Automatic CI failure capture for explicitly tracked workflows.
2. Manual workflow_dispatch emission for an Observation, Candidate, Bug, Case, Test, or Lesson.

A project adapter writes only to its own uigs-outbox branch. It never needs credentials that can write to UIGS-Foundry.

## Durable path

product workflow or manual dispatch
-> UIGS Intake Adapter
-> immutable JSON packet
-> source repository uigs-outbox/packets
-> Foundry scheduled collector
-> outbox/pending
-> triage and deduplication
-> structured knowledge record

## Interactive-agent execution boundary

Participating repositories should expose a root `AGENTS.md` that applies the Canonical policy in `governance/AGENT-EXECUTION.md`.

The source-side contract is:

1. Treat an interactive agent session as a disposable worker.
2. Convert broad/open-ended goals into bounded work units.
3. Persist a pushed checkpoint before long or external validation when safe.
4. After a coherent work unit is durably submitted, external CI/emulator/render/deployment/Foundry work may remain Pending.
5. Do not keep the current conversation turn alive by repeatedly polling asynchronous work.
6. For multi-unit goals, keep a durable task state under `.uigs/tasks/<task-id>.json` conforming to `schemas/agent-task-state.schema.json`.
7. On continuation, recover from the task state + branch/PR + latest durable commit before relying on conversation memory.
8. UIGS Intake may emit one bounded packet or update one narrow record, but downstream Foundry processing is a separate lifecycle.

A source adapter is therefore a persistence bridge, not a reason for a product-side interactive agent to wait for Foundry processing.

## Scope

The adapter is intentionally conservative. It does not automatically convert every push, pull request, issue, or release into knowledge. CI failures are machine events with a clear evidence artifact; higher-level reusable meaning still requires triage.

Additional event types may be added later when they have a reliable signal and acceptable noise level.

## Failure semantics

- If the source adapter cannot persist its packet, its workflow is red.
- If Foundry cannot collect one source, the collector run is red.
- Missing uigs-outbox before the first event is not an error.
- Imported packets remain Pending.
- Canonical promotion is never automatic.
- Failure or delay in downstream Foundry processing does not reopen an already completed product-side agent work unit.

## Invariant evidence coverage

A product repository may expose a source-owned `.uigs/invariants.json` manifest and an `invariant_evidence` entry in `.uigs/project.json`.

The manifest is not a claim that the product is bug-free. It records the critical invariants the project currently intends to prove and the evidence boundaries required for each one.

Recommended execution path:

`source invariant -> source/test/workflow evidence -> UIGS Evidence Coverage workflow -> failure -> existing Intake Adapter -> Pending packet`

The initial validator supports three deterministic source-repository checks:

- `pattern`: required source/test/workflow text exists;
- `capture_equal`: captured contract values agree across producers/advertisers/consumers;
- `capture_in_integer_set`: a current version captured from one source is included in a consumer's accepted-version set.

Required evidence levels are explicit per invariant. A green ordinary CI suite does not satisfy an invariant whose declared evidence level is absent.

This mechanism is intentionally source-owned: the product repository remains authoritative for its implementation and tests, while Foundry owns the reusable manifest semantics and validator. Missing invariant evidence may fail CI and therefore enter the existing Pending intake path. It does not trigger automatic Canonical promotion.
