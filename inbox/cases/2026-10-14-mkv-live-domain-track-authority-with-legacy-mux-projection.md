# Case: bounded live domain ownership while retaining a proven legacy execution projection

Date: 2026-10-14  
Status: **Case / product feature submitted — exact-head CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#127 — live ContainerProject source-track authority](https://github.com/11576865/MKV-Fast-Muxer/pull/127)  
Base: merged `main@1583570d59234a965c180b22a8fc24707703a24e`.

## Problem

Previous P1 slices added `ContainerDocument` read-only projections, detached `ContainerProject` export/import, three-way conflict preview and a guarded restore transaction (merged #125). However ordinary UI editing still directly mutated the legacy FFmpeg-facing `trackState`. Review-only projects and an occasional restore action do not establish a writable domain source of truth. A wholesale rewrite risks losing already working streaming mux, batch, font, original source track and P0 EBML guard semantics.

## Bounded feature change

PR #127 implements `src/live-source-track-authority.js`. After the real source is scanned, one live, immutable `ContainerProject` becomes **authoritative only for existing source audio/subtitle**: `include`, `title`, `language`, `default` and `forced`. Commands compile *all* updates against the same immutable source owner before atomically materializing the existing legacy `trackState` fields for the unchanged FFmpeg execution path. The File must be the same JavaScript object reference that actually completed the scan, not merely a new object with identical name, size or mtime. Stale live projection, unsupported fields, mixed invalid edits and preserve-all mode fail closed.

The main workbench now routes source inspector fields, traditional track form `input/change`, bulk language/Default/inclusion, and metadata reset through that command path. Verified detached import replay/undo explicitly reseeds the owner from the authorized post-operation track state. High-frequency typing compacts bounded domain history without discarding current effective field values; this is not a durable authenticated chronological edit log.

**Scope exclusion:** advanced source dispositions (`original`, `commentary`, `hearingImpaired`), ordering, attachments, external tracks, chapters, Tags, resource-only outputs and batch JobPlan remain legacy-owned; the general Matroska writer and known #77 loss of complex Chapter/Tag semantics are not fixed. Product authors must not call this full P1 or a single domain writer for the entire app.

## Tests and observed evidence

- New Node tests validate real source projection + domain project generation, atomic multi-track changes and failed mixed edits, same-display File identity refusal, legacy bypass/drift refusal, preserve-all/no-op, 150-character input beyond the bounded history length, bulk inclusion/disposition rules, and unchanged legacy advanced/order/attachment fields.
- An isolated execution of actual modules (`ContainerDocument` + `ContainerProject` + command owner + `buildOutputComposition`) passed: 150 live title edits, source audio exclusion, atomic invalid edit refusal, and expected output audio/subtitle counts. Source JavaScript syntax checks passed.
- New real Chromium scenario performs a scanned two-audio/one-subtitle MKV workflow with bulk language and Default, normal source title edit, subtitle include toggles, actual MKV writer output and **independent ffprobe** verification of delivered title/language/flags/track count. Existing source inspector, attachment, batch and P0 suites are unchanged.
- **PR #127 exact-head Node/Vite/Chromium pending**. No CI pass or user-device/cross-player correctness is claimed yet.

## Deduplication and reuse hypothesis

Foundry `inbox/cases/2026-10-14-mkv-verified-source-delta-export-and-atomic-replay.md` covers detached source-project recovery. This Case concerns **ordinary live editing ownership** and compiler-to-executor projection; it does not duplicate the previous proof. Existing Candidate `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` proposes preserving validated legacy workflows during domain generalization; this PR supplies a concrete, narrower implementation case, not sufficient evidence to promote a new Canonical rule.

Potential cross-project invariant (only a hypothesis until independently corroborated): to migrate an existing editor without duplicating write authority, specify a bounded domain-owned field set, require every user-facing entry to route through one transaction, validate the executable projection against the immutable owner, and keep the legacy executor as a generated view until actual output parity is proven.

## Reconciliation with independent P1 large-file hash release (2026-10-14)

Evidence update: PR #126 (cancellable large-file full SHA-256) and PR #127 (the live domain owner described above) each passed its **own exact-head Node/build/real Chromium E2E** and GitHub Pages deploy checks. PR #126 was squash-merged as `main@bdcdf6887725ff3eb563f4d2d55baf8b9b014c00`. The subsequently attempted merge of unchanged green PR #127 failed with a GitHub HTTP 405 **merge conflicts**, due to overlapping main workbench, E2E and task-state files; it was not a functional test failure.

Rather than force-push an unrelated whole-file version or rerun separate CI after each minor change, the next bounded integration work unit created [PR #128](https://github.com/11576865/MKV-Fast-Muxer/pull/128) directly from merged #126 main. It replayed all **13** source `main.js` hunks, **2** browser E2E hunks and **1** README hunk from PR #127 only after each old-context block was uniquely matched on the new main (no ambiguous locations). The previously green domain module, test and design record were added unchanged. The task-state JSON was reconciled semantically rather than choosing either stale version. Static JavaScript syntax checks passed for the combined source and tests, and both functional E2E scenarios are present in the new suite. The original PR #127 was closed explicitly as **superseded by #128**, not merged or abandoned for product reasons.

**Combined exact-head CI remains Pending** at this entry; two independent green predecessor suites are not proof of a new combined head. This is a concrete case of integration conflict under parallel feature branches and is consistent with existing Foundry `inbox/cases/2026-10-04-ass-mkv-stacked-pr-consolidation.md` and Canonical `governance/AGENT-EXECUTION.md`. It neither creates a new Canonical requirement nor claims Matroska preservation beyond the P0 guards.
