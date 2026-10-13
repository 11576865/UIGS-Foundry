# Case: Untrusted source attachment recovery requires proof, consent and cross-object atomicity

Date: 2026-10-14  
Status: **Case / implemented in PR; exact-head CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
Feature PR: [#131 — verified source attachment draft recovery](https://github.com/11576865/MKV-Fast-Muxer/pull/131)  
Base main: `13968cd141be2790713ae347c364e48e60e6a797` (merged #130).

## Prior observed gap

The previous Case, `inbox/cases/2026-10-14-mkv-source-attachment-live-domain-ownership-not-writer-authority.md`, recorded how the real inspector, attachment list and bulk actions became one immutable `ContainerProject` edit owner. However exported projects still had **no portable scan-based attachment edit intents**, even when the currently inspected editor had renamed an attachment, changed MIME or excluded one. Consequently a user could export a realistic-looking final attachment object yet could not recover those edits safely. This is distinct from Matroska writer/AttachmentUID preservation (#77) and from live editor ownership.

## Scoped implementation

PR #131 introduces separate original scan attributes (`name`, `mime` and original inclusion) for verified source attachments, then exports current-minus-observed synthetic `set-attribute`/`include` intents. These intents are effective state deltas, **not a signed/authenticated edit chronology**. Source-attached and external font resources are explicitly distinguished by source binding.

On imported JSON, existing strict v1 parser and reverse chain audit run before a source-bound three-way preview. Attachment restoration requires complete current-source SHA-256 match, source ID and object ID alignment, successful ffprobe scan, stable stream index/type and **exact original ffprobe stream object identity**, allowed field and safe name/MIME values, baseline old-value agreement, selective editing mode, and user's explicit confirmation. Imported bytes are otherwise read-only.

A single prepared edit may modify audio/subtitle tracks **and** existing source attachments. Before any mutation, final apply verifies every target still has its recorded pre-edit state; if a single attachment changed since preview, the entire mixed transaction fails without modifying any track. Guarded undo similarly refuses to clobber newer track or attachment edits and reverts both groups together. No File object, byte data, FFmpeg writer permission or output is granted through the detached project. Metadata modifications to an excluded attachment remain refused, avoiding silently hidden edits.

## Tests/evidence boundary

- Actual isolated execution of the real `ContainerDocument`, `ContainerProject`, strict JSON import/audit, conflict preview, and apply/undo modules **PASS** for a mixed one-track, two-attachment, four-intent transaction. A stale edited attachment correctly blocks the whole transaction and leaves the audio track unchanged; both receipts report no File write or mux.
- Node tests submitted for source attachment baseline export/strict import, both attachment-only and mixed atomic apply, inverse conflict, changed ffprobe stream reference, missing digest/proof, preserve-all, excluded metadata, dangerous filename and unsupported reorder.
- Existing real Chromium fixture extended: actual MKV attachment rename/MIME/drop → export JSON → reset source editor → inert import → full-source SHA → explicit apply → guarded undo → explicit re-apply → actual MKV remux → independent ffprobe attachment count/name/MIME and unchanged original source bytes.
- Changed JavaScript syntax checks passed. **PR #131 exact-head full Node/build/Chromium CI is Pending**, so no integrated acceptance, device/performance guarantee or generic Matroska fidelity claim exists yet.

## Separation of authority and deduplication

The adjacent live-owner Case proves only that a user action can safely change a local *semantic edit plan*. This Case adds an independent **portable-restoration** contract. Neither gives a general Matroska writer license: AttachmentUID references, targeted Tags, nested Chapters, unknown EBML elements and issue #77 structural loss remain subject to independently verified writer checks. Source track-order recovery is still unsupported and disclosed separately.

Potential transferable pattern: when a detached document requests a cross-object edit, validate source-byte/object/old-state identity and the whole prepared mutation set before committing any executable projection, and guard the inverse against newer user changes. This is recorded only as a Case while exact-head CI and other project corroboration are pending. Do not promote or edit Canonical.
