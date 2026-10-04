# Candidate: Source-bound resource actions must not execute against display-only output snapshots

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #102

## Observation

A resource-oriented editor may display an inventory derived from a newly verified output while the active source handle still points to the original input artifact.

That creates an evidence/identity hazard: a row visible in the UI can describe the verified output without being addressable in the currently open source. Actions such as Extract, Remove, Replace, or Edit Metadata must not silently use that display row against the old source.

## Candidate rule

Separate:

- **working source identity** — the artifact resource operations actually read or mutate;
- **displayed inventory evidence** — baseline, current-source, predicted, or verified-output state;
- **mutation plan** — pending changes to be applied to the working source;
- **non-mutating resource reads** — extraction/export operations.

Reusable constraints:

1. Non-mutating Extract/Export is not a container mutation and should not enter the mutation plan or dirty/write-back state.
2. Source-bound actions must resolve resource identity against the actual working source, not merely against the inventory currently displayed.
3. If the UI switches to a `VERIFIED_OUTPUT` inventory without switching the working source to that output, source-bound resource actions should be disabled or explicitly redirected.
4. Metadata-only edits are mutations even when payload bytes are preserved; verification should confirm identity/payload invariants separately from metadata changes.
5. Read-only extraction may have its own concurrency/busy state so it cannot be confused with transactional write-back.

## Implementation evidence

PR #102:
- adds streaming attachment extraction as a read-only operation;
- keeps extraction outside `ContainerEditPlan`;
- introduces a separate extraction busy state;
- disables source-bound attachment actions on a verified-output inventory until that output is reopened as the working source;
- treats FileName / FileDescription edits as explicit mutations and verifies UID/MIME/payload-size preservation after remux.

## Evidence boundary

This is implementation-backed in one resource-oriented container editor. Exact source-handle and snapshot mechanics vary by product.

Do not promote to Canonical from this evidence alone.
