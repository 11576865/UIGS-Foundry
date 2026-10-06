# Epistemic Knowledge Graph

This directory contains the fine-grained epistemic layer defined by `governance/EPISTEMIC-MODEL.md`.

## Layout

- `claims/` — propositions whose support, scope, assumptions, maturity, and authority can change.
- `evidence/` — observations and source artifacts related to Claims.
- `changes/` — durable belief/governance change ledger.

## Important distinction

Domain records such as Pattern, Policy, Bug, Case, Test, Lesson, and UI Grammar remain useful human/agent views.

They are not the atomic truth-maintenance unit.

The graph underneath them is:

`Evidence -> Claim -> dependent Claim -> knowledge view`

## Migration

Migration is intentionally incremental.

Priority order:
1. Canonical knowledge;
2. Validated knowledge;
3. high-impact Experimental knowledge;
4. knowledge with recurrence/conflict;
5. the rest of the catalog.

Do not fabricate Claim/Evidence records merely to reach coverage targets. A missing graph mapping is better than invented provenance.

## Consumers

Consumers should use `tools/evaluate_epistemic_graph.py` output to determine effective authority.

A stored `maturity=canonical` Claim can still be effectively quarantined.


## Validation missions

`tools/generate_validation_missions.py` proposes the next evidence needed to resolve high-impact uncertainty. This is the Active-Learning boundary: UIGS may identify what should be tested next, but it does not silently execute experiments or rewrite mature knowledge.

## Migration visibility

`tools/generate_epistemic_migration_report.py` measures which legacy aggregate records have explicit `claim_refs`. Missing mappings are migration debt, not permission to invent provenance or evidence.
