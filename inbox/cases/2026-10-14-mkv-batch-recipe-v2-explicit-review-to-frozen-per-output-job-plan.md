# Case: Portable per-output media rules must be reviewed before entering a frozen job executor

Date: 2026-10-14  
Status: **Case / implementation PR #134 submitted, exact-head CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#134 Batch Recipe v2](https://github.com/11576865/MKV-Fast-Muxer/pull/134), stacked on [#133](https://github.com/11576865/MKV-Fast-Muxer/pull/133) latest external-domain cancellation repair.

## Why existing knowledge was insufficient

Batch Recipe v1 could save only task-wide preservation/subset policies; per-output subtitle titles, language and dispositions were inferred anew rather than saved as reviewed declarations. The existing frozen `BatchJobPlan` and per-output audit already execute independently, but no safe boundary linked portable per-job metadata to current real media. A document mentioning filenames is not a browser File grant and must never be treated as a historical resumable job. Foundry Candidate `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` covers the general transition from legacy mux to job ledger, not this specific portable-rule-to-session-approval boundary.

## Bounded product implementation

PR #134 adds strict, allowlisted `batch-recipe-v2` JSON (max 128 KiB; up to 100 outputs / 500 subtitle rows) storing declared source/output display names and per-subtitle file/sidecar name, format ID, title, language, Default, Forced, Original, Commentary, Hearing Impaired. All execution grants, destination directory authorization, media bytes, previous outputs and browser handles are explicitly absent. Version 1 remains compatible.

Actual UI adds independent v2 Export, Import, per-output accessible read-only review and **explicit Confirm**. Import is inert: even a fully matching current selection may not execute without confirmation. Pairing preview rejects missing/duplicate sources, subtitle or sidecar disagreement, wrong format, unresolved ambiguity and output collisions. User confirmation pins **exact in-memory source File, subtitle File and sidecar references**, not their metadata equality; approvals are revoked upon input replacement. At confirmation and all asynchronous preflight boundaries, current real FileLists are compared against pinned references again. Only after matching current media, safe output directory and the original P0 Matroska preservation guard does the approved rule create **new nonmutating per-output pairing rows** that pass into the already-validated `freezeBatchJobPlan`. The frozen executor, status ledger, final independent MKV audit and persistence states remain unchanged.

## Evidence / current acceptance boundary

- Targeted actual v2 module execution passed strict 2-output export/import/preview, current File-bound approval, distinct per-job title projection, denial after a new File object with identical metadata, and no mutation of source pairing.
- Node regressions submitted for JSON strictness and fake permissions, whole-pairing mismatch rejection, sidecar/format identity, explicit approval, entry to real frozen plan and mux-context metadata, and headless runner's separate per-output audit/awaiting-save statuses.
- Real Chromium E2E submitted: two actual episode MP4 inputs, different ASS/SRT, export/edit/import v2, premature execution denial, explicit confirmation, two real MKV outputs, independent native `ffprobe` checks per-output title/language/dispositions, and frozen-job report/output persistence distinctions.
- Static JS syntax checks for module/main/Node/browser tests passed. **Full exact-head Node/build/Chromium for PR #134 Pending**. Parent #133 had two prior Chromium failures on cancellation restart, latest bounded repair in flight; no inherited green claim.

## Deduplication / nonpromotion

Earlier Foundry batch Candidate describes planning and ledger ownership and remains separate. This Case observes a new trust boundary: a **portable recipe is a proposal; only a reselected whole pairing, actual File-reference pin, explicit human acceptance, and last-moment revalidation can produce executor-facing metadata**. No single implementation is evidence for UIGS Canonical promotion. Existing #77 complex Chapter/targeted Tag/AttachmentUID/unknown EBML remux safety is not relaxed.
