# Cross-repository Harvest

This directory defines the repeatable archaeology process used to extract reusable engineering knowledge from product repositories.

Harvest is **read-mostly**. It indexes and normalizes knowledge; it does not copy whole product implementations into Foundry.

## Signals

High-value source signals include:
- HARDENING / FAILURE / POLICY / RELEASE / DESIGN / ARCHITECTURE documents;
- deterministic fixtures and E2E scenarios;
- CI workflows and policy checkers;
- runtime registries, supervisors, discovery/reconciliation code;
- rollback/recovery and atomic-publication code;
- source identity/fingerprint logic;
- incident fixes documented in changelogs;
- UI contract tests and adaptive layout rules.

## Extraction

source artifact
-> concrete observation/case/bug/test
-> reusable family
-> Candidate/Experimental record
-> additional project evidence
-> gated Canonical promotion

Do not infer an incident merely from a defensive comment. A Bug Museum entry requires evidence that the failure actually occurred or that project history explicitly describes it as a fixed failure.
