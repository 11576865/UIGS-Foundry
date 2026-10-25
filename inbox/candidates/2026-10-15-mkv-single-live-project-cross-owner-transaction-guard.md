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

## 2026-10-25 S09 extension: cross-domain checkpoint replay must compile before publishing (Pending exact-head CI)

Product [PR #203](https://github.com/11576865/MKV-Fast-Muxer/pull/203) upgrades the prior single JSON carrier to a **bounded one-revision recovery transaction**. Before any user-facing executor row changes, the implementation requires the current source Full SHA-256 verdict, an independently hashed external File/sidecar checkpoint, consistent exact in-session File references, original read-only source intent conflict analysis and a still-current shared `ContainerProject` generation. It performs the source replay on shallow in-memory executor shadows, compiles source track/attachment and external metadata changes into a fresh immutable project, checks mutation eligibility before publication, and exposes a **separate real confirmation** action.

The resulting single synchronous commit publishes the new project to both bounded source/external sessions alongside the actual executor rows; a scoped inverse requires that exact accepted project and external File/current-source bound references, refusing later edits. The browser workflow retains legacy single-domain recovery as a fallback and tests combined review/apply/inverse across a real reload, while keeping the actual MKV native ffprobe independent acceptance canary.

The first exact-head CI for product head `af1b83e185ce497723ddc059a2758889e3732bf3` was **red** (6 of 740 Node tests failed before media), caused by an added external witness comparison against a non-existent `ref.row` property. Existing `prepareExternalMetadataRecovery` intentionally returns *File/sidecar/format/identity* witnesses without granting a mutable row reference; the one live external domain adapter separately verifies bound executor row identity. Product head `3b0fd6113a2c37834f3ae7b8e80b3a91fc0dbbe0` removes this invalid duplicate row comparison while preserving all real identity/byte checks. **Exact-head Node, full Chromium and S12 CI are pending** at this intake. Do not carry over the earlier failing/partial status as success.

**Knowledge and scope:** This is a concrete extension of the existing cross-owner precommit guard Candidate, not a new canonical law. One-revision semantic state does not grant Writer or filesystem authority, prove physical durability, restore browser File handles after refresh, cover arbitrary Chapters/Tags/Font editing, or guarantee all possible JS runtime throws cannot occur after publication. Do not promote to Canonical on a single project instance.

### 2026-10-25 external PR review hardening (latest product head `57ab1ca1ccc6f24e91393d913daaef41395ab9e5`)

Review found two additional boundary counterexamples and required explicit tests rather than assuming the happy path:
1. **Finite semantic history vs immediate inverse:** A combined transaction could consume the 100-history-entry `ContainerProject` edit budget, leaving no capacity to undo even without intervening edits. The product now compacts semantic edit history before extending both forward and inverse edits (with existing live adapter policy semantics); a Node regression starts near this limit, verifies accepted two-domain changes and immediate whole-transaction inverse. Compaction is not audit-log durability or proof that earlier edits occurred.
2. **Late preservation-mode flip:** Preparing source edit replay in selective mode and then enabling MKV 'preserve all' can make restored source fields non-executable although external fields still take effect. Final atomic confirmation now denies `appendMode=true` in the domain API and front-end; Node regression verifies no half-commit after this mode flip.

First red CI also revealed two copies of the same mistaken assumption that external checkpoint witnesses carry mutable `row` references; the existing standalone checkpoint only serializes `File`, `sidecar`, `format` and `identity`. The new atomic recovery uses live domain verification and the actual current contextual editor row for semantic comparisons, rather than promoting a nonexistent `ref.row`.

These are **Candidate-level scoped findings** until exact-head full Node/Chromium/S12 green. Product PR #203 remains open. No Canonical alteration.
