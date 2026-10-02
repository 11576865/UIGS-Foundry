# Candidate: Foundry as cross-project guidance and control plane

Status: candidate
Date: 2026-10-02

## Proposal

UIGS-Foundry should be evaluated not only as a UI knowledge repository, but as the highest cross-project **guidance, knowledge-governance, and reporting layer** for the user's software projects.

It must not become a monorepo or a second implementation source of truth. Product repositories remain authoritative for executable code, project-specific state, tests, releases, and runtime behavior.

Foundry becomes authoritative only for cross-project knowledge classes that have been explicitly promoted to Canonical status.

## Control-plane model

Product repositories are the execution plane.

Foundry is the control / knowledge plane:

- collect evidence and reusable lessons from project repositories, CI, bugs, reports, and development conversations;
- normalize them into Observation / Candidate / Case / Bug / Test / Rule records;
- maintain cross-project principles, schemas, naming, evidence levels, and promotion rules;
- generate and maintain reports from machine-readable project facts;
- detect duplicated lessons, recurring failures, policy drift, and missing validation;
- provide reusable patterns, policies, test recipes, and reference implementations back to projects.

Evidence flows upward; guidance and reusable mechanisms flow downward.

## Automated reporting candidate

Foundry should eventually support generated reports such as:

- project state / engineering completion report;
- architecture and dependency report;
- CI red-reason and reliability report;
- regression and stress-test coverage report;
- GitHub Actions resource / storage / cost guardrail report;
- release-readiness report;
- known limitations and unresolved evidence report;
- cross-project reusable-knowledge report;
- design / UI conformance report;
- agent-collaboration and repository-coordination report.

Generated reports should be derived from structured facts and provenance where possible, rather than hand-maintained prose that silently becomes stale.

## Governance boundary

The highest guidance layer should be intentionally thin.

It defines:
- scope and non-goals;
- source-of-truth ownership;
- evidence levels;
- provenance requirements;
- Candidate -> Validated -> Canonical promotion;
- conflict and override rules;
- change-control requirements;
- generated-report rules.

It should not directly prescribe every UI value, platform implementation, test case, or project-specific detail.

## Existing principles

Existing cross-project project principles are primary source material. Foundry should consolidate and operationalize them rather than invent a competing doctrine.

Single observations may create candidates or evidence, but must not silently rewrite Canonical rules.

## Naming question

If Foundry becomes the highest cross-project engineering layer, the current expansion "User Interface Grammar System" may become too narrow for the umbrella. Preserve the Interface Grammar concept, but decide separately whether UIGS remains the umbrella name or becomes one domain beneath Foundry.

## Next validation work

- inventory all active repositories;
- define the project manifest each repository exposes to Foundry;
- define provenance and source ownership schema;
- define the report-generation schema;
- define policy inheritance and project-specific override rules;
- define read-only intake versus automated write-back boundaries;
- validate the model against ASS-Workbench-Android, Character-Voice-Service, MKV-Fast-Muxer, Quick-Automatic-Hardsub-Encoder, and HSR-Voice-Archive-Builder.
