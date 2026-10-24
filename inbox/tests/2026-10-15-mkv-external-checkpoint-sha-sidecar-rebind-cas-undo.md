# Test · Portable external metadata checkpoint requires current byte rebind and revision-bound inverse

Status: **Test Candidate / Product PR Submitted / exact-head CI Pending**. Not Accepted, not Canonical.
Date: 2026-10-15
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/144
Exact submitted product head: `a305dde5486c068f689d45f340dfdd457e02c5b8`
Depends on PR #143 live one-document authority and parent #142 P0 protection.

## Prior knowledge and distinct gap

Foundry already records `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md`: same filename/size/mtime cannot substitute exact browser File reference for **current-session** metadata editing. `inbox/cases/2026-10-14-mkv-verified-source-delta-export-and-atomic-replay.md` covers source-MKV track/attachment replay based on full-source SHA. Those cases do not cover **multiple external audio/subtitle Files plus optional sidecar** across a session restart, with imported checkpoint JSON, explicit consent and revision-bound inverse.

## Submitted scoped regression gate

New `src/portable-external-project-recovery.js` exports only allowlisted per-external-track metadata, current `File` full SHA-256 and optional subtitle sidecar full SHA-256. JSON neither carries browser File grants, writer rights nor outputs. Imported JSON is untrusted, rigidly parsed and inert. Preparing recovery checks each current File name/size, full bytes digest, exact live `File`/sidecar/format/identity references after every await, the unified immutable ContainerProject identity and revision. Mismatched content, changed File inventory, concurrent edits and malformed schema refuse.

A **separate checkbox + Apply click** dispatches the whole recovered external metadata delta through the actual unified transaction. Undo is valid only against the exact Project object revision resulting from this apply; later edits or File changes invalidate it. This is not a generalized persistent Undo journal.

### Required tests

- Node `tests/portable-external-project-recovery.test.mjs`: successful export/parse/prepare/apply/inverse, altered File byte and sidecar byte, same-looking new File, malicious grant key, unknown field, hash-time field mutation, stale plan, no implicit consent.
- Chromium `scenarioExternalCheckpointRecoveryRealMux`: MP4 + FLAC, export/download JSON, change title, inert import, SHA verify, checkbox approval, apply, undo, second prepare/approve/apply, **real finished MKV**, native independent `ffprobe` reads recovered external audio title.
- PR #143's mixed source/external actual MKV scenario and all legacy P0/Batch/P3 regressions must remain green.

**None of these new exact-head CI or native output verdicts is yet confirmed**. This entry is a pending Test, not proof.

## Dedup / limits

Searched `SHA-256 sidecar recovery explicit consent undo`, `external metadata checkpoint`, `rebind exact File digest user confirmation`, `portable project multi source recovery`. Related exact File identity and source-MKV SHA cases are not duplicate of the **external sidecar + cross-session metadata + consent + CAS undo** test class.

Outside scope: source and external changes combined into one all-or-nothing portable replay; font File regrant; serialized browser handles; durable undo after page refresh; new Chapter/Tag writer. No Canonical promotion.

## 2026-10-25 S09: single portable carrier without combined authority (Pending CI)

Product [PR #202](https://github.com/11576865/MKV-Fast-Muxer/pull/202), head at intake `cc7f1a7dacaf9628d07811af76ace61b0ddb5a37`, adds one `softmux-workspace-recovery-bundle-v1` JSON containing an inert detached source-track/attachment draft and an optional inert external-audio/subtitle/sidecar checkpoint. This addresses the real user burden of separately exporting/importing two checkpoint files for a single workbench session. The bundle delegates parsing of each nested component to its **existing strict standalone parser**, rejecting unknown top-level keys, invalid nested schema, forged SHA/metadata, over-budget content and malformed JSON. Only after BOTH validate does the UI replace either pending-review draft.

**Crucial limit:** A single delivery package is not a single authority or transaction. The actual source File and external File/sidecar objects must be freshly granted after refresh, verified against the nested full-byte hashes, reviewed and explicitly applied **separately** using the pre-existing recovery paths. Neither bundle import nor complete nested parser validation changes the executable mux plan, applies edits, restores fonts, grants writer permission or simulates atomic rollback.

Node regressions cover valid dual packaging, optional external content, malicious unknown fields, false nested SHA, malformed nested content, size and JSON rejection. A real Chromium mixed source+ASS+font workbench scenario exports the bundle, imports it and asserts both scopes remain awaiting independent consent and cannot alter the actual plan; invalid nested external metadata rejects the whole import and retains the prior staged checkpoints. **Exact-head Node/build/Chromium CI is pending at this intake, not accepted evidence.**

**Deduplication:** This extends this existing Test because it composes the same already-recorded external checkpoint with the existing source verified-delta restore; it does not assert or introduce a universal `multi-domain atomically restorable project` rule. No Canonical promotion.

**2026-10-25 S09 identity/UI correction:** Product head `32dabe2dab2a984b436c37ebfb1713e1ce3b02a6` avoids clearing existing *applied* source/external undo receipts when merely importing another inert bundle. Existing revision/source guards continue to control eligibility. Latest exact-head CI pending. Foundry Validate was already red on dozens of unrelated historical Bug records lacking required Lifecycle metadata, so this Test proposal must remain Pending rather than being mislabeled accepted or altering Canonical.\n