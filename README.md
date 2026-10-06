# UIGS-Foundry

UIGS-Foundry is the cross-project knowledge, governance, reporting, and reference-implementation layer for the user's software projects.

UIGS originally means User Interface Grammar System. Interface Grammar remains a first-class domain, but Foundry is broader: it also governs reliability, architecture, operations, failure knowledge, evidence, automated reporting, and non-monotonic knowledge revision.

## Model

- Product repositories are the execution plane and remain authoritative for shipped code, runtime behavior, project-specific tests, releases, and device results.
- Foundry is the knowledge/control plane.
- The atomic epistemic unit is a **Claim**, not a document.
- Evidence supports, contradicts, scopes, or tests Claims.
- Pattern/Policy/Bug/Case/Test/Lesson/UI records are higher-level views/packages around Claims and evidence.
- Evidence flows up; scoped guidance flows down.
- Capture is cheap; promotion is gated; authority is reversible.
- Canonical maturity does not override current contradiction, staleness, or quarantine.
- Knowledge may be added, revised, contracted, deprecated, or superseded.

Read `governance/EPISTEMIC-MODEL.md` for the knowledge model.

## Structure

- governance/ — highest-level charter, authority, epistemic model, promotion/revision, reporting, and execution rules.
- knowledge/ — Claim, Evidence, and Knowledge Change records.
- domains/interface-grammar/ — reusable UI grammar, patterns, platform realizations, expected effects, and validation.
- domains/reliability/ — stress testing, regression, red reasons, failure injection.
- domains/architecture/ — reusable integration and lifecycle architecture.
- domains/operations/ — GitHub/CI, agent collaboration, release/resource policies.
- schemas/ — machine-readable records and intake packets.
- intake/ — capture and routing policy.
- outbox/ — durable Pending intake collected from project-side adapters.
- projects/ — manifests describing how repositories participate.
- reports/ — generated and curated reports.
- inbox/ — unpromoted observations and candidates.
- harvest/ — targeted cross-repository archaeology and evidence-acquisition queue.

## Durable project intake

Participating repositories can emit immutable Pending packets to a local `uigs-outbox` branch. Foundry collects them without requiring a cross-repository PAT. See `outbox/README.md`.

Read `AGENTS.md` before modifying Foundry.
