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

## Scope

The adapter is intentionally conservative. It does not automatically convert every push, pull request, issue, or release into knowledge. CI failures are machine events with a clear evidence artifact; higher-level reusable meaning still requires triage.

Additional event types may be added later when they have a reliable signal and acceptable noise level.

## Failure semantics

- If the source adapter cannot persist its packet, its workflow is red.
- If Foundry cannot collect one source, the collector run is red.
- Missing uigs-outbox before the first event is not an error.
- Imported packets remain Pending.
- Canonical promotion is never automatic.
