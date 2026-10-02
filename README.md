# UIGS-Foundry

**UIGS-Foundry** is the cross-project knowledge, governance, reporting, and reference-implementation layer for the user's software projects.

UIGS originally means **User Interface Grammar System**. Interface Grammar remains a first-class domain, but Foundry is broader: it also governs reliability, architecture, operations, failure knowledge, evidence, and automated reporting.

## Model

- **Product repositories are the execution plane.** They remain authoritative for shipped code, runtime behavior, project-specific tests, releases, and device results.
- **Foundry is the knowledge/control plane.** It is authoritative only for cross-project knowledge explicitly promoted to Canonical status.
- **Evidence flows up; guidance flows down.**
- **Capture is cheap; Canonical promotion is gated.** A single observation may create evidence or a Candidate, but may not silently rewrite Canonical rules.

## Structure

- `governance/` — highest-level charter, authority, promotion, and reporting rules.
- `domains/interface-grammar/` — reusable UI grammar, patterns, platform realizations, expected effects, and validation.
- `domains/reliability/` — stress testing, regression, red reasons, failure injection.
- `domains/architecture/` — reusable integration and lifecycle architecture.
- `domains/operations/` — GitHub/CI, agent collaboration, release/resource policies.
- `schemas/` — machine-readable records.
- `intake/` — automatic capture and routing policy.
- `projects/` — manifests describing how repositories participate.
- `reports/` — generated and curated reports.
- `inbox/` — unpromoted observations and candidates.

The first end-to-end Interface Grammar entry is `UIGS.WORKSPACE.STICKY_SUPPORTING_PANE`.

Read `AGENTS.md` before modifying Foundry.
