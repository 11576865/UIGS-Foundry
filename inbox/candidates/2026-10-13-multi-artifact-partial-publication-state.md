# Candidate: Publication of a multi-artifact result requires per-artifact persistence truth

Status: Candidate / implementation-backed, not Canonical
Date: 2026-10-13
Domains: reliability, workflow, interface-grammar, file-output
Source project: 11576865/MKV-Fast-Muxer
Evidence: merged PR #114, https://github.com/11576865/MKV-Fast-Muxer/pull/114
Current-main confirmation: 15ca805db83e640f867bcbc6e36502d89af25f61; browser E2E run 38366667414 succeeded for that main.

## Observation

A single logical export may produce a primary result (MKV) plus a separately persisted audit report (JSON). Browser File System Access does not provide an atomic transaction covering both destinations. Publishing the primary result and then failing to write the report is a *partial publication*, not a failed media generation and not a fully saved artifact set.

In PR #114, a real Chromium batch scenario injected a report-only quota failure *after* the MKV had been committed. It asserted that the MKV remained in the simulated destination, the JSON was absent, in-memory fallback downloads remained available, and UI / terminal summary reported partial persistence.

## Candidate rule

1. Identify every artifact in the logical result set, its destination and independently verified persistence status.
2. Preflight collisions and target identity across all filenames before starting publication; recheck each target at its actual write boundary.
3. Never claim cross-file atomicity when the storage provider cannot guarantee it.
4. If the primary artifact is already committed, do not attempt unsafe rollback or deletion merely because a secondary report fails.
5. Do not create an orphan report if the primary artifact failed to save.
6. Model statuses as a structured outcome (primary persisted, report persisted, review/audit status, failures, unsaved in-memory artifacts), not one boolean success flag.
7. Bind UI and retry actions to the actual artifact identities; preserve valid already-created artifacts.
8. Regression-test success, collision-before-write, primary failure, secondary failure, and late/stale-identity conditions against a realistic storage adapter.

## Boundaries

This is a *candidate engineering pattern*, not proof of an atomic filesystem protocol, crash consistency in every browser, cross-process locking, or real-device directory persistence. The exact CI covers designated Chromium scenarios and synthetic directory failures; broader filesystem/browser acceptance remains separate.

## Deduplication

Existing Foundry Candidate `2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` already distinguishes generated artifacts, optional persistence failure and batch identity, while `2026-10-03-completed-artifact-identity-survives-current-setting-changes.md` separates old artifacts from current UI settings. This Candidate adds the independently testable *multi-artifact partial-commit boundary* (MKV saved while paired JSON fails), rather than restating queue or artifact identity principles.

No Canonical promotion is requested.
