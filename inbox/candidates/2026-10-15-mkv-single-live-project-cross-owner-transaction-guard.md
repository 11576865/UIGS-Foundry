# Candidate · A live project may unify two bounded domain adapters only with cross-owner precommit proof

Status: **Candidate / Product PR submitted / exact-head CI Pending**, not Accepted, not Canonical.
Date: 2026-10-15
Product: [11576865/MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
PR: [#143 — Round 2/10 shared live ContainerProject](https://github.com/11576865/MKV-Fast-Muxer/pull/143)
Submitted head: `b9cf928f5fd044c0a3f4d34d8cd70fe8f44bcaa1`
Stacked baseline: Round 1 [#142](https://github.com/11576865/MKV-Fast-Muxer/pull/142), head `85cc5c143e1e56ac77c7b848ba9ee02158199739`.

## Boundary and observed architectural problem

The existing MKV live source-track/attachment session and the external audio/subtitle/font session each owned their own immutable `ContainerProject`. Each individually enforced exact File references and a domain-to-FFmpeg projection, but two separate documents existed for one user's composed MKV. Editing one subset did not intrinsically verify the other subset's current authorization and execution projection.

In a migration where both adapters must remain, **one** `ContainerProject` can hold both subsets of semantic objects. The individual executors may continue to use existing bounded rows. Every exposed mutation should validate *both* bounded owners first, then publish the new immutable revision to both references only after a successful delegated domain transaction. This prevents a command on one side from ignoring a known drift on the other side.

## Submitted implementation / pending proof

- New `src/live-container-workspace-authority.js`: exact source/external subset reconciliation, shared immutable project reference, one edit dispatcher for source fields/source attachments/source order/external metadata/font mode, and cross-domain read-before-write consistency checks.
- `src/main.js` uses this dispatcher at actual authoring actions and verifies a shared project immediately before single-task FFmpeg execution. Existing legacy mux writer and frozen batch runner do not change.
- New Node `tests/live-container-workspace-authority.test.mjs` includes foreign-domain direct row mutation, identical-display replaced File, no-source document, new font File rebind, and history compaction negative/positive controls.
- New browser `scenarioSharedContainerProjectRealMux`: real source Matroska plus external FLAC, ASS and font -> mixed edits -> real finished MKV -> external native ffprobe checks.
- **Full PR-head Node/Vite/Chromium CI not yet observed**; none of these checks can be marked accepted from source code alone.

## Limits and falsifiers

This does *not* establish global cross-task/BatchJobPlan ownership, detached external File grant recovery, arbitrary Matroska Chapters/Tags writing, source identity backed by new cryptographic evidence, or safe multi-file atomicity. Rebinding an actual File inventory intentionally establishes a new session document; its history is not durable Undo.

Future test failures that falsify the candidate:
- Main UI keeps writing directly to one owner's executor rows without the dispatcher.
- A drifted source track still permits an unrelated external metadata edit.
- A replaced same-name File preserves authorization without an actual current session-bound reference.
- New mixed actual-output Chromium shows unexpected source/new title, disposition or attachment payload.
- Parent #142 P0 CI red or missing, rendering stacked integration unsuitable for merge.

## Foundry dedup

Search: `one immutable ContainerProject multiple owner`, `single live document source external track`, `cross-domain state drift edit authority`, `split owner source external domain`.
Related Cases:
- `inbox/cases/2026-10-14-mkv-live-domain-track-authority-with-legacy-mux-projection.md` — the original source track adapter, not cross-owner transaction.
- `inbox/cases/2026-10-14-mkv-source-attachment-live-domain-ownership-not-writer-authority.md` — source attachment migration.
- `inbox/cases/2026-10-14-mkv-batch-recipe-v2-explicit-review-to-frozen-per-output-job-plan.md` — external batch plan trust boundary, not unified single-task owner.

Distinct new narrow principle: **cross-owner drift refusal and one shared semantic revision while existing adapters coexist**. Not enough evidence to modify Canonical standards.
