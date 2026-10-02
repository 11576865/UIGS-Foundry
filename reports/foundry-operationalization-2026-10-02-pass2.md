# Foundry Operationalization — Pass 2

Date: 2026-10-02

## Implemented

- Deterministic Pending Triage Engine.
- Red Reason classification using source-captured workflow/job/step evidence.
- Related-knowledge hints that point to prior Bug/Test/Pattern records without claiming identity.
- Red Reason aggregate report.
- Triage schema and validation.
- Unit tests for policy, release, timeout, unknown, and manual semantic packets.
- Source-enriched intake recorded as an Experimental operations pattern.

## Classification boundary

The classifier may return `unknown` and may mark a result `needs_review`. It is not allowed to convert weak workflow-name evidence into a confident root-cause claim.

The next source-adapter revision enriches CI packets with failed job/step evidence so central triage does not need broad cross-repository log credentials.
