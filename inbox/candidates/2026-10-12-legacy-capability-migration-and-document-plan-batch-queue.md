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
