# Candidate: Foundry operationalization phase

Status: candidate
Date: 2026-10-02

## Rationale

The initial cross-repository archaeology has produced enough structure and evidence that the next priority should shift from manual harvesting to operating the Foundry as a live cross-project control/knowledge plane.

## Proposed phase order

1. **Stabilize the schema and registry contracts**
   - validate provenance, lifecycle/status, catalog references and project manifests;
   - add machine checks for stale/duplicate IDs and unsupported promotion.

2. **Install project-side adapters**
   - each participating repository exposes a small .uigs/project manifest and high-value event sources;
   - product repositories remain execution authorities.

3. **Automate intake without automating Canonical promotion**
   - PR/CI/issue/release events can emit Observation/Bug/Test/Case/Candidate packets;
   - failed Foundry writes become durable Pending/Outbox entries.

4. **Build report generation**
   - generate cross-project inventory, red-reason, release-readiness, reliability coverage and knowledge-reuse reports from structured records.

5. **Make Interface Grammar consumable**
   - add searchable aliases, platform realizations, visual baselines/showcases and reference demos so agents can resolve natural-language UI requests to concrete patterns.

6. **Continue targeted archaeology only where it fills known evidence gaps**
   - use harvest/coverage.json as the queue rather than scanning repositories indefinitely.

## Key decision

Do not spend the next phase maximizing record count. Optimize for whether Foundry can reliably:
- ingest new evidence;
- deduplicate it;
- preserve provenance;
- generate useful reports;
- return reusable guidance to another project;
- expose failure/Pending states when automation cannot complete.

This candidate does not change Canonical governance by itself.
