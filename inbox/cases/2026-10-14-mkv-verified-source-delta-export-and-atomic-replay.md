# Case: Portable edit restoration requires a source baseline, correct ID translation, and atomic live-owner validation

Date: 2026-10-14  
Status: **Case / implementation submitted — exact-head CI Pending**  
Product: [MKV-Fast-Muxer PR #125](https://github.com/11576865/MKV-Fast-Muxer/pull/125)  
Main baseline: `6d3f88a4ae7c0c67c7c058c3422ac4e32213b235`  
Development branch: `feat/p1-verified-track-transaction-20261014`

## Actual engineering observations

1. The previous `ContainerProject` JSON exported a detached final object snapshot with `editIntents: []`, even when the **real legacy source-track editor** had changed values. Strict re-import, SHA verification and conflict preview could all work while the ordinary user still had no recoverable edit delta. Repair: preserve both observed scan-time original field values and current effective editor values; export a **bounded, coherent scan-to-current delta**. Do not label these synthetic revisions an authenticated chronological edit log.
2. Source object IDs in the live `ContainerDocument` were source-scoped raw composition IDs; imported `ContainerProject` edits used **stable hashed IDs**. A naive map keyed by `liveProjection.objects[].id` caused `TRACK_REPLAY_UNSUPPORTED_OBJECT` despite a valid source and edited track. Repair: reconstruct the exact ordered domain projection and map domain IDs to the current live source objects. This mismatch was identified by actually running the new module functions in a lightweight isolated V8 smoke; static parsing alone did not catch it.
3. A successful read-only three-way conflict preview must **not** mutate state. Actual restoration requires an additional explicit user confirmation, immutable File reference continuity at commit, verified whole-file checksum commitment, inspected source, selective edit mode, exact old-value parity in the mutable owner, a narrow field allowlist, and prevalidation of **all** target tracks before synchronous mutation. No FFmpeg command or file write is authorized by a JSON document.
4. An inverse transaction may undo those restored values only if every touched live track still equals the transaction's saved `after` values. If a user changed any participating track later, refuse the **entire undo** rather than overwrite a newer edit.
5. Product-side work consolidated code, Node tests, browser E2E and docs on one branch before opening one PR. Existing Browser E2E workflow triggers on PR/main, not intermediate branch commits; full external validation remains asynchronous. This applies the **already Canonical** execution boundary rather than proposing a new CI policy.

## Evidence scope

- New modules and bindings: `src/container-project-restore.js`, `src/container-document.js`, `src/container-project.js`, `src/main.js` (PR #125).
- Browser scenario exercises real scanned MKV → source title edit → generated revisioned JSON → re-import/hash → explicit apply → guarded undo/reapply → actual browser mux → independent ffprobe output check and unchanged original source bytes.
- Modified JS syntax checks and an isolated exported-module source-delta/import/prepare/apply/undo smoke passed during authoring; actual PR Node/build/full Chromium results are **Pending** at this observation point.
- No evidence of complete single-writer ContainerProject migration, >64 MiB digest support, arbitrary EBML editing, chapter/Tag retention, user-device acceptance or generalized cross-project applicability yet.

## Dedup / boundaries

- Existing Foundry Test `inbox/tests/2026-10-14-mkv-detached-project-intent-chain-semantic-review.md` covers internal JSON coherence **without replay**. This Case adds usable editor delta export, cross-namespace ID mapping, explicit atomic replay, and guarded undo. Do not rewrite the earlier Test as a universal execution authorization.
- Existing Canonical `governance/AGENT-EXECUTION.md` already establishes branch/PR durable checkpoints and default no-poll async CI. No new Canonical policy is proposed.
- Keep this product-linked Case until exact-head evidence is observed; do not automatically promote to Candidate/Canonical based on a single implementation.
