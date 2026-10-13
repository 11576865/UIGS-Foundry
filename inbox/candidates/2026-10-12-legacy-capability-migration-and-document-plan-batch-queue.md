# Candidate: Preserve validated legacy workflows while generalizing the domain — batch = queue of independently frozen document plans

Date: 2026-10-12
Status: Candidate / source-review + design decision hypothesis, implementation unverified
Product: `11576865/MKV-Fast-Muxer`
Reviewed product main: `7781a4f410a9c6edb9a1f3d056091e6ace333cc4`

## Trigger

A migration strategy previously covered a new Matroska `ContainerDocument`, subtitle-delivery specialization, validation/inspection, and UI design but omitted explicit decisions for **existing functionality**, especially the already working batch subtitle mux feature. Without a legacy capability inventory, even a technically correct rewrite could remove behaviors relied on by users.

## Product source evidence

- `src/batch.js` builds jobs from recognized **video** candidates; assigns ASS/SSA/SRT/WebVTT/PGS/VobSub subtitle tracks by stem/episode-token scoring, rejects unresolved tied matches, blocks output-name collisions, and filters jobs without any assigned subtitle.
- `src/main.js` batch intake and `syncBatchPlan()` identify content and fonts, build an asynchronous plan, block unsupported assets/ambiguous matches/pre-existing destination collisions, and support grouping font subset once per batch or per task. Independently imported audio is explicitly marked unsupported in the batch UI.
- Batch executor rewrites the single-job hidden `videoInput`, `subInput`, `fontInput`, resets track state, clicks `muxBtn`, polls `running/scanning/previewing`, fetches a completed Blob URL, writes outputs optionally via directory handle, and restores prior single-job state. This is UI automation, not a domain-level job runner. It has already needed asynchronous readiness fixes (see existing Bug Candidate).
- `src/batch-result-urls.js` and `src/batch-status.js` preserve completed downloadable outputs and distinguish cancelled/preparation-error/per-item-failure/optional save failure. These are valuable existing invariants, not disposable legacy.
- `src/output-composition.js` is only a projection of old single-job state, not yet a generalized document authority.

## Distinctions

Three superficially similar operations are not equivalent:
1. **Multi-source composition**: N input assets -> one `ContainerDocument` -> one output MKV (a single job).
2. **Bulk edit in one document**: many objects inside one document -> one logical edit action with one undo/redo boundary (not a batch queue).
3. **Batch execution**: N frozen document plans -> N independently tracked output artifact(s), with per-job preflight/audit/save states and clear resource budgets (a real queue).

There may also be a **batch inspection/audit/export** family where input sources map to inspection/extraction outputs, without any mux; those are future optional job types sharing queue infrastructure but not a reason to prematurely unify all formats into one executor.

## Candidate design and migration constraint

- Before deleting a legacy feature, classify its **user-visible behavior and evidence** as retain / merge / enhance / internal rewrite / conditional reveal / retire redundant UI / remove obsolete implementation. Retirement of a control does not justify loss of its capability.
- Preserve the legacy one-video-with-subtitles quick workflow as a selectable **batch recipe/preset** within the new queue, with equivalent name heuristics, ambiguous-match refusal, invalid-input reporting, font group/subset behavior and output retention.
- The queue operates over independently owned `JobSpec { jobId, sourceRefs, containerPlanSnapshot, recipeId, outputDestination, auditPolicy, status/evidence }`. A worker consumes an immutable prepared plan with `prepare → execute → independently audit → save/publish`, rather than mutating another workbench's DOM/file inputs or synthesizing button clicks.
- Keep recipe defaults distinct from per-job overrides and shared assets. Shared batch fonts do not automatically imply every job uses them; use explicit scope and handle font licensing/subset policies.
- Adopt conservative browser initial policy: one heavy mux job at a time; content sniff / metadata preflight may be bounded-parallel; release staging and Blob references per lifecycle. Multi-core and parallel jobs only after empirical memory/IO tests.
- Browser support is conditional: `ffmpeg.wasm` standard input limit (official FAQ 2 GB), memory-bound `fetchFile`+virtual filesystem, file-picker limited availability, permission reauthorization, and page lifecycle. Do not promise background run after browser close or resumable continuation of a partially written MKV.
- Failure/partial semantics: a completed artifact may be successful yet optional output persistence may fail; batch plan, individual statuses, file collision checks, and prior downloadable results must remain distinct. Restore or recover only verified data and never assume atomic no-clobber from File System Access.
- UI: batch has a separate professional **queue workspace** (table with target outputs, source mapping, rule status, progress, evidence), not a long disclosure beneath the single-file document view; selecting a job may open the **same domain inspector** used by a single document, without sharing mutable draft state.

## Proposed minimum regression matrix

1. Single task legacy fixture produces identical intentional video/audio stream-copy + ASS/SSA + fonts after migration (compare independent audit, not pixel-perfect file bytes).
2. Multi-episode batch maintains unambiguous filename matching and stops tied/invalid assignments without guessing.
3. Shared Group fonts, per-task subset, TTC/OTC no-subset safety; no cross-job font pollution or selection override.
4. Retained source MKV audio, subtitle, attachment, chapter/tag metadata are audited to extent supported; unknown structures reported (no blanket “preserve all” guarantee).
5. Cancel during job N preserves only completed verified outputs; optional save failure keeps usable artifact handle; repeated run does not overwrite or leak Blob URLs.
6. After queue operations, independently open single-job editor and confirm unchanged draft and input state.
7. Browser tab close/reopen restores *plan metadata* if persisted and file handles remain authorized; execution does not claim seamless resume of interrupted mux unless proven.
8. Audio-only and attachment-only Matroska are separate writer-acceptance fixtures, not silently generated video.
9. UI browser E2E checks real table selection/focus/scroll, tablet space, batch status and detailed per-job diagnostics.

## Related prior knowledge and dedup

- `inbox/candidates/2026-10-02-batch-execution-async-preflight-readiness-race.md`: observed race from reusing interactive input event handlers; existing candidate, not duplicated.
- `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md`: collision/matching safeguards.
- `inbox/candidates/2026-10-09-browser-batch-artifact-object-url-ownership.md`: blob-result lifetime.
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`: primary single-document UI and separate batch mode.
- `inbox/candidates/2026-10-03-batch-intent-vs-local-draft-ui-contract.md`: bulk-edit scope vs editor-local drafts.

This Candidate adds a **legacy capability survival and generalized queue contract**. It is not a new Canonical rule or proof of a working new batch executor.

Public references: https://ffmpegwasm.netlify.app/docs/faq/ ; https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker ; https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation


## 2026-10-12 refinement: Batch Composition Workbench, not merely a queue (Candidate-only)

The user asked what *form* the future batch experience should have, beyond preserving its old execution loop. A reviewed UI/product proposal is:

- The primary pre-execution object is an **output-target matrix**: one row per planned output `ContainerDocument`; columns contain target identity, mapped sources, planned contents, inherited/overridden rules, output destination, and readiness/evidence. A queue of execution progress is only the runtime projection after plans have been approved.
- One batch `Recipe` derives many candidate output documents (e.g., legacy episode ASS/font matching); the selected row opens the **same container inspector** used in single-document work. Sources can be imported to a shared inventory, with an explicit mapping confidence/reason and an ambiguity state. Do not make implicit filename heuristics equivalent to user consent.
- Scope precedence should distinguish `Recipe default → current batch rule → per-job override`. Display effective values and their origin. If a batch rule changes, pending plans regenerate while valid per-job overrides survive; running jobs use a frozen `JobPlan` revision. No silent loss of per-row exceptions.
- Separate three meanings often conflated as “batch”: many sources to **one** composed MKV; one document **bulk edit**; many independent target document plans to **many** output artifacts. Only the third requires a multi-job queue. One source may later have explicit multiple output variants, but there should be no automatic cross-product of sources and variants.
- Batch UI has a compact recipe bar, dominant dense task matrix, contextual selected-job inspector, and stable execution/progress rail. Source library is an on-demand drawer once files exist. Avoid many expanded job cards, long page scroll, four A/B/C/D task tabs, and duplicated per-job editable track models.
- “Run ready only” should be a visibly scoped, explicitly confirmed subset action whenever unresolved jobs remain; do not silently exclude blocked jobs, or let an ambiguous row silently choose its candidate. Standard run-all must honor whole-batch preflight gates.
- Each output keeps independent mux, audit, and save/publish results. Completed-but-unsaved differs from mux failed; after cancel or browser closure, only persisted plans and independently saved verified outputs may be considered durable. No assertion that a partly written MKV can resume at an arbitrary percentage.

Comparable existing patterns: HandBrake Queue makes source→job explicit and avoids output collisions; Adobe Media Encoder binds presets to queued jobs and can produce multiple output instances from sources. These are interaction reference cases, not evidence that an MKV browser app can copy desktop watch-folder or background-process behavior. https://handbrake.fr/docs/en/1.9.0/advanced/queue.html ; https://helpx.adobe.com/media-encoder/desktop/encoding-and-exporting/encode-export-video-audio.html

Proposed acceptance tests: 4-episode fixture with one ambiguous subtitle; change a batch rule with one per-job override; verify unchanged override and selected-row focus; consent to run exactly 3 verified outputs leaving 1 unresolved; no implicit skipping; cancel during an active job; preserve earlier saved outputs, separate audit/save statuses, and verify default single-job state is untouched. Scope: user-directed architectural proposal, not implemented/visually validated; no Canonical promotion.

## 2026-10-12 P1 implementation provenance (Pending CI, Candidate only)

Product branch: `11576865/MKV-Fast-Muxer:feature/container-document-projection-v0-20261012`.
Boundary: a **read-only source-scoped ContainerDocument v0 projection** has been committed on a product feature branch. It consumes existing owned source track edits and external resource state, projects observable source/data/chapter/tag facts separately from unverified writer preservation, and routes existing composition display through the same legacy editor actions. The existing mux command, P0 preservation preflight and batch executor are not replaced.

A stale UI selection with the same per-stream legacy index must not silently bind to a different source: the branch introduces a source-scope reconciliation helper plus Node regressions. Its file key remains name/path+size+mtime based, not content-authenticated. Duplicate projected IDs are diagnosed; this slice does not establish universally stable asset identity or full `EditIntent` / `JobPlan` authority.

**Evidence status:** code and unit tests submitted to product branch; exact-head Node, Chromium E2E, deployment and user acceptance are Pending CI/not claimed. This updates implementation provenance for the existing candidate instead of manufacturing a new or promoted Canonical rule. The prior batch queue and functional migration constraints remain unmet.

## 2026-10-12 P1 exact-head result and next submitted experiment (Candidate only)

**P1-A verified and merged:** product PR [#85](https://github.com/11576865/MKV-Fast-Muxer/pull/85), head `b7909ef13af94d09db5a34989e83229d56064ebf`, passed **235/235 Node** and complete Chromium Browser E2E + build at workflow [38224113412](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38224113412). The same PR's Pages build check passed at run [38224113547](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38224113547); deploy step was skipped, so this is **not a Pages publication claim**. Squash merge into main: `8ab92c0798f944d01dd4f3ad2fa99f409ca62219`. P0 #77 remains open; no writer/root preservation fix.

**P1-B submitted / Pending CI:** product Draft PR [#86](https://github.com/11576865/MKV-Fast-Muxer/pull/86), head `37d5607bf86bc88934f8ffe36663a84821b0d961`. Read-only `buildSubtitleEditIntentSnapshot` projects explicit external subtitle additions from legacy owned state, preserving source scope and operation ordinal; a deterministic serialized draft fingerprint invalidates on tracked source/subtitle property changes. Tests compare actual legacy `buildMuxCommand` argument arrays against staged descriptors in append-all/selective modes and reject stale revision or mismatched identity/index. Nothing in this PR replaces the writer, changes runtime staging, or promotes the weak path/size/mtime key to authenticated identity.

**Important scope distinction:** input-draft equality ≠ whole-document plan revision or execution-time freshness guarantee; FFmpeg command argument equivalence ≠ independently verified output semantic equivalence. CI of PR #86 is not yet asserted passing. Existing Candidate governance remains unchanged; no Canonical promotion.

## 2026-10-12 P1-B merged and P1-C submitted (Candidate-only)

Product PR [#86](https://github.com/11576865/MKV-Fast-Muxer/pull/86) head `37d5607bf86bc88934f8ffe36663a84821b0d961` completed **241/241 Node** and full Chromium Browser E2E including source MKV remux, P0 gate, batch and TrackUID/AttachmentUID relationship scenarios in run [38232907599](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38232907599); Pages build run [38232907606](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38232907606) also succeeded. Squash merged to main `6ca303d2b9cc5e25d120d02d0843f34a1ad759ce`.

New bounded product Draft PR [#87](https://github.com/11576865/MKV-Fast-Muxer/pull/87), head `a85d72b707bc3fdd36ecd0784212397fb511492a`, adds a **single-operation subtitle freshness witness** using browser File-object reference identity, sidecar and classification evidence, append mode and a prior draft revision. It checks freshness after async source EBML preflight **before clearing previous outputs**, then before `ffmpeg.exec`; a no-write shadow call to `buildMuxCommand` checks staged subtitle-argument parity. The existing writer, batch and P0 gates remain authoritative. At intake, exact-head Node/Chromium CI remains **Pending**, Pages build succeeded. Even if green this is only argument equivalence, not full output-artifact equivalence or universal Matroska preservation.

UIGS knowledge scope: exact File reference evidence prevents one class of same-path/name/size/mtime stale-binding errors during one operation, but does not establish durable file identity or whole-document plan revisions. No new Canonical rule.

## P1-C exact-head handoff refinement — real-browser interleaving included

The P1-C Draft PR [#87](https://github.com/11576865/MKV-Fast-Muxer/pull/87) advanced beyond its first submitted commit to `2ce950b188b543ce777ecac098f6b6f6058bd5e6`. It now includes the deterministic `scenarioP1SubtitleIntentInvalidation` Chromium E2E: hold a valid Matroska source's EBML preflight with intercepted `File.slice().arrayBuffer()`; programmatically replace the subtitle selection while inputs are disabled; require stale-intent rejection and no fresh artifact. **Exact-head CI Pending** at the time of this intake. This is one source-specific regression implementation, not a new Canonical standard or a claim of arbitrary asynchronous integrity.


## Round 2/5 frozen batch authorization + lifecycle projection (2026-10-13; Pending exact-head CI)

Implementation PR: [MKV-Fast-Muxer #105](https://github.com/11576865/MKV-Fast-Muxer/pull/105). Review boundary: `main@0c698623493713bd9686cdcd7a04da6893a31e86`; PR head after branch integration: `b7ad5f65755004f743fb6c9ad6736156a42c2fa8`.

Extends this existing Candidate without reasserting a new Canonical rule:
- Existing `buildBatchJobsFromCollected()` reviewed pairing is frozen into `batch-job-plan-v1` **after** start preflight, preserving source File references, planned sidecar inputs, output names, group/individual font settings, and generation-scoped task IDs. The snapshot owns batch policies; the legacy mux adapter no longer reads mutable batch rule controls during its job loop.
- A batch-scoped ledger models `queued / preparing / muxing / saving / succeeded / awaitingSave / saveWarning / failed / cancelled / interrupted` separately. The matrix and selected-job inspector read the ledger but never become a second editable owner of stream properties.
- Output Blob generated without a persisted destination remains **awaitingSave**, not persisted success; directory write failure is **saveWarning**, not a fabricated mux failure. Lifecycle markers are invalidated on changed batch settings, source binding or output directory.
- The old `muxBtn.click()` adapter remains. This slice implements a **frozen authorization seam**, not the full independent JobPlan executor, durable batch recipe, verified save transaction or long-lived resume. Scope of the previous design proposal remains larger than implementation.

Regression submissions: Node tests for frozen snapshot integrity, source/sidecar ownership, ambiguity/conflict refusal, legacy fallback, illegal state changes, and save warning; existing Chromium two-job scenario checks `awaitingSave` for unsaved Blob artifacts. **Both Node and Chromium exact-head CI were pending at intake.**

Deduplication: this is evidence for the existing legacy migration + queue Candidate; pairing ambiguity's direct-choice UX is recorded in the separate 2026-10-09 matching/identity Candidate. No Canonical promotion. Further proof must include exact-head CI, real output checks and eliminating the DOM click adapter.


## Round 3/5: DOM-free queue orchestration and direct artifact handoff (2026-10-13; Pending CI)

Product PR: [#106](https://github.com/11576865/MKV-Fast-Muxer/pull/106). Early work branch `feat/round3-batch-runner-direct-mux-contract`.

A specific migration seam has been implemented (without claiming full queue separation from media UI adapters):
- `runFrozenBatchQueue(plan, { prepare, execute, publish, shouldCancel, onResults, ledger })` owns serial ordering and per-job terminal transitions. This module has **no DOM references** and consumes an immutable reviewed plan.
- The existing single-task FFmpeg mux body is now an awaitable `executeCurrentMuxTask()` returning the *actual* output Blob, JSON report Blob, SHA-256 and audit status. The batch no longer simulates `muxBtn.click()` or polls mutable download links every 150 ms before fetching Blob URLs back into Blob objects.
- The batch compatibility adapter still stages each job through legacy single-file File input controls. This means `BatchRunner` scheduling is headless, but **media execution is not yet UI-independent**; the migration is not the completed proposed domain `Executor.execute(jobPlan)`.
- Node tests cover exact serial ordering, job-local failure vs batch-fatal staging, cancellation during and between jobs, terminal unsaved output identity, and mismatch of plan/ledger. Existing production Chromium mux output tests remain the deciding evidence.

Important source-coupling regression during migration: prior integration tests asserted literal `muxBtn.click()` and a loop in `main.js`; those must be moved to assertions on the new direct executor and runner module, without removing actual browser output/oracle tests. This is an implementation-coupled test refactor, **not** evidence that functional behavior is correct until E2E passes.

Status: CI on updated PR head **Pending**; do not infer green checks from early subtest results. Same existing Candidate: no new Canonical standard.


## Round 3/5 exact-head Chromium acceptance and merge (2026-10-13)

Product PR [#106](https://github.com/11576865/MKV-Fast-Muxer/pull/106), exact tested head `6b87529a2954c34333d7d2ce31c585c3ef40fdd1`, merged into main at `9c527cde58e3b0c8c27809d9573f6c7401cc5a1c`.
- [Pages build + Node tests](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38328508158): success.
- [Full Chromium Browser E2E](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38328508144): success. This is browser fixture evidence, not physical-device or arbitrary MKV preservation certification.
- Direct mux artifact return (MKV Blob, report Blob, hash, audit status) and DOM-free per-job scheduling are now integrated; synthetic mux button click and download-link polling are absent from the batch pipeline.
- A new guard refuses executor output name drift from the frozen JobPlan before publication; tests simulate mismatched names.
- Earlier Node failures exposed source-shape tests tied to the old `main.js` loop and button-click event forwarding. Corrected to assert the new runner and direct mux path without deleting real browser output checks.
- Unfinished: per-job media staging still reuses legacy single-task File inputs and FFmpeg/Wasm operation. This is not yet fully isolated `Executor.execute(JobPlan)`, independent persistent Recipe, arbitrary Matroska writer or cross-device acceptance.

Remains Candidate, not Canonical.


## Round 4/5 audit-aware task status (2026-10-13; Pending CI)

Product [PR #107](https://github.com/11576865/MKV-Fast-Muxer/pull/107) adds `auditWarning` as a distinct terminal job state when the independently executed ffprobe audit reports `warning` or `unavailable`. A generated MKV remains downloadable and is still counted as a mux success, but must not be labeled as verified; batch terminal summary counts audit issues separately from mux failures and directory-write failures. The existing `BatchRunner`/frozen plan remains the actual execution path. Behavioral tests cover pass/warning/unavailable across generated output and save conditions.

Status: implementation + tests submitted, exact-head Chromium E2E **Pending** at intake. This is a refinement of the existing batch state/evidence Candidate, not Canonical promotion.
