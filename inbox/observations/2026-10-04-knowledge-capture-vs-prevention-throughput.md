# Observation: Knowledge capture throughput can exceed prevention throughput

Date: 2026-10-04
Status: Observation
Scope: UIGS Foundry / engineering knowledge lifecycle / reliability

## Observation

UIGS-Foundry currently captures reusable defects and engineering lessons faster than those records are consolidated into validated, executable prevention mechanisms.

At the observed snapshot:

- `inbox/bugs`: 15 retained Bug records;
- `inbox/candidates`: 126 Candidate records;
- `inbox/observations`: 17 Observation records;
- `inbox/cases`: 8 Case records;
- durable outbox Pending packets: 217 at the observed snapshot; these are durable intake storage and may already have triage records;
- catalog: 62 reusable entries, including 43 experimental and 15 validated entries.

The Bug directory is cumulative evidence, not an open-defect tracker: several Bug records already include an implemented mitigation or repair PR. Therefore Bug-record count must not be read as unresolved-product-bug count.

## Reusable implication

A knowledge system can become strong at detection and memory while still being weak at prevention if:

1. intake grows faster than triage/promotion;
2. Candidate knowledge remains prose rather than executable checks;
3. projects evolve faster than validated rules are propagated back into CI, contracts, linters, schemas, or test harnesses;
4. repaired Bug records remain intentionally retained as historical evidence.

Operational maturity should therefore be measured separately across:

- detection;
- durable capture;
- deduplication/triage;
- validation/promotion;
- executable enforcement;
- recurrence rate.

A rising Bug/Candidate count can indicate improving observability rather than declining product quality. Raw Pending count alone is not backlog because packets remain in durable Pending storage after triage; untriaged packets, unresolved review/proposal work, and repeated bug families are stronger indicators of governance or prevention lag.

## Evidence boundary

This is a current cross-project operational observation from UIGS-Foundry state, not a Canonical maturity model.
