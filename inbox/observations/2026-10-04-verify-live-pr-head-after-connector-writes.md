# Observation: Verify the live PR head after sequential connector writes

Date: 2026-10-04
Status: Observation
Domains: GitHub workflow / branch state / concurrent automation / submission boundary

## Observation

During ASS Workbench Android PR #95 work, three connector-created commits formed a valid linear chain:

- `a5294f5...` — add shared top-level override semantics;
- `ca931ba...` — use direct-tag semantics in Batch HasTag;
- `258b883...` — regression coverage.

The commits existed in GitHub and each pointed to the previous commit as parent, but a later PR read showed the live PR head had returned to the earlier `0ea1ce8...` commit.

The branch was restored with a non-force fast-forward ref update to `258b883...`, after which the PR head matched the intended chain again.

## Practical implication

A successful file-write response proves that a commit object was created, but in workflows where another writer/automation may touch the same branch, it does not permanently prove that the PR still points at that commit later.

For multi-agent or connector-driven branches, a final lightweight PR-head verification after the intended write sequence can detect lost branch advancement without requiring CI polling.

## Limits

This is one observed branch-state incident. The cause was not established; it could involve another writer, automation, or connector/ref timing. It must not be promoted to Canonical from this observation alone.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #95
- restored head: `258b8837c0fa11cdb24aa16497af9098bd199a36`
- correction: non-force fast-forward `update_ref`
- deduplication: searched UIGS-Foundry for branch rewinds, concurrent writers, and PR-head verification; no direct duplicate found
