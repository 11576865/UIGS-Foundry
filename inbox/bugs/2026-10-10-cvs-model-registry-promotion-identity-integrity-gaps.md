# Bug: CVS Model Registry could promote stale assets and accept ambiguous model identities

Status: **Bug / repair submitted; CI Pending**
Date: 2026-10-10
Source project: `11576865/Character-Voice-Service`
Source fix PR: https://github.com/11576865/Character-Voice-Service/pull/18
Dependency: PR #17 -> #16 -> #15 -> #14

## Code-path findings, not a reported production incident

Source inspection of the open CVS stack identified several related integrity gaps:

1. The model-promotion handler trusted the persisted lifecycle status and Evaluation Registry decision. It **did not revalidate the currently installed manifest and all weight SHA-256 digests** immediately before installing a model as the voice default. An internal `require_evaluation=False` override could promote a stale or modified asset.
2. A Model Root scan encountering two physical manifests with the same `model_id` only rejected **different manifest SHA-256**. Two byte-identical manifests in separate directories were silently resolved by scan order, making a content ID ambiguously mapped to physical model locations.
3. `default_model_id` used an old default pointer without confirming present/nonquarantined status; `resolve_model` did not reject a quarantine flag when files happened to be restored.
4. Registry writes used a shared fixed `.tmp` filename and did not fsync the staged JSON. Process interruption and concurrent writers could collide on staging or leave weak publication guarantees.
5. A `model.json` symlink resolving outside Model Root could make `_registry_relative` throw outside the scanner's guarded block, aborting a scan instead of reporting a bad item.

## Submitted repair

CVS PR #18:
- rechecks registered model scope/voice/revision, live manifest and all artifacts before promotion, even if evaluation checking is explicitly bypassed;
- quarantines previous entries with duplicate `model_id` manifests, including byte-identical copies; reports ambiguity and returns no active default for missing/quarantined entries;
- prevents quarantined models from serving via `resolve_model`;
- writes registry snapshots to unique create-only temporary files, flushes and fsyncs them, then uses atomic replacement with cleanup on exception;
- reports out-of-root manifest symlinks in `invalid` without stopping the entire scanner;
- adds source-level regression tests for all of the above and adjusts tests using custom Model Roots.

**Important limits:** atomic file replacement does not serialize independent writers and cannot provide distributed transactions; it does not guarantee durability of the containing directory or protection against modification after the validation check. The current implementation expects serialized registry owners.

## Verification status

New tests are **committed, not reported as passed**: full pytest/Windows CI and real-runtime integrity checks remain **Pending** as of PR submission. No production asset loss, compromised voice default, or actual exploit is asserted.

## Reuse and dedup

A useful cross-project principle is to bind a promotion/activation decision to the **current physical asset's identity**, not to historic registry metadata alone; reject ambiguous physical identities even if file bytes agree.

Foundry was searched for model promotion integrity, duplicate model ID, registry atomicity, model manifests. Related entries address composite resources and persistent derived evidence, but none covered this CVS-specific **model lifecycle and physical identity** failure. This is an observed code-path bug, **not a Canonical rule**.
