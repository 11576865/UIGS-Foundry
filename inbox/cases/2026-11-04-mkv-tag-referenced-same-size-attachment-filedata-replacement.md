# Case: Matroska TagAttachmentUID-linked payload may be replaced safely without orphaning the reference when FileUID is preserved

Date: 2026-11-04
Status: **Case / independently verified on one native MKVToolNix-authored fixture; complete product CI pending; not Canonical**
Product: `11576865/MKV-Fast-Muxer`
Draft implementation PR: https://github.com/11576865/MKV-Fast-Muxer/pull/236
Exact head: `908756c1ec5a25b8265bae7ea6a76dc52b326966`
CI targeted step: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41703427923
Evidence artifact: `p2-mkvtoolnix-referenced-attachment-uid-evidence` ID `13264467077`, includes a JSON report and both real output MKVs.
Report verdict: `SCOPED_TAG_UID_PRESERVATION_PASS`.

## Prior-art and existing-product boundary

The 2026-10-14 sibling Case `inbox/cases/2026-10-14-mkv-existing-attachment-same-size-filedata-preservation.md` requires *no* TagAttachmentUID target for a simple source-confirmed same-length FileData replacement. This remains the existing default and ordinary unreviewed eligibility boundary. It is not evidence that a referenced UID must always become an orphan when **only** payload bytes are replaced.

MKVToolNix mature `mkvpropedit` supports selecting an attachment by exact UID and replacing it. Reference source design is used as the comparison baseline, not copied into the browser product. The current extension differs from general attachment replacement: the replacement stays at the original byte offset, its length is equal, `FileUID` and its Tag Targets are not edited, and an extra explicit permission bit is needed to change the referenced object's content.

The new implementation affects only `src/p2-existing-mkv-writer-router.js` and `src/existing-mkv-same-size-attachment-replace.js`:
- user operation still needs `approveSourceModification:true`, plus `approveReferencedTagTargetReplacement:true` when the target has any inspected incoming `TagAttachmentUID` edge;
- source graph must be fully inspected; each target edge must resolve to the expected exact attachment; default denial remains;
- non-equal-size changes are denied for referenced targets regardless of extra approval, so no adjacent-Void/tail/SeekHead fallback;
- created output is a separate Blob, original source unchanged; the writer and the common route separately check untouched protected EBML bytes, attachment UIDs/other payloads and exact graph edges;
- no UI control is added and no new general Matroska writer is claimed.

## Independent real-file experiment

Test script: `scripts/p2-mkvtoolnix-referenced-uid-differential.mjs`
Source: independently authored `p0-independent-attachmenttag.mkv` with two attachments and a `TagAttachmentUID` pointing at the selected attachment, not its decoy.
Baseline source SHA-256: `2debfa01b107314f5c1640538e222737d4370a3fe5ed668e9ff57f1f47a9276d`.
External reference: `mkvpropedit v82.0 ('I'm The President') 64-bit` on a private copy of the exact same source file.
Product: `prepareRoutedAttachmentReplacement` + `executeRoutedAttachmentReplacement` on the original immutable Blob.
Selected source attachment FileUID: `13819251715060858038`.
Both output extracted FileData SHA-256: `9d73896a4663702cfa218a582ca2e607d64e3ce8fedf1ca1da3cebe426e3713e`.
Other attachment extracted SHA-256 (both unchanged): `590c43c27f736e168f2ed9d4b985033f4957d4b5d835a627767e3ccdeb04cfe5`.
Native and product output independently passed equal Tag XML, physical target graph edges, and ffprobe packet/PTS/data hashes; test recorded `sourceUnmodified:true`.
Negative check: `defaultDenied:true` when no extra referenced-target approval. Unit tests also assert non-equal-length changes remain refused.

The staged output is **one fixture and one same-byte-count edit**, not complete Matroska preservation proof. No live user UI path, current upstream MKVToolNix Codeberg source integration, generalized UID rewrites or player/device matrix was tested. `mkvpropedit v82` is the native test environment baseline, not proof of current upstream behavior.

## Deduplication / reconciliation

- Sibling 2026-10-14 same-size Case remains valid for unreferenced edits and prior released UI; this Case is an explicit **reviewed same-UID referenced-target exception** with stricter acceptance tests.
- 2026-10-15 Candidate `mkv-multiple-bounded-writers-one-router-with-output-oracle.md` covers selecting among four backend envelopes, not referred attachment byte updates.
- 2026-11-04 Candidate `multi-writer-fallback-requires-typed-capability-refusals.md` covers error fallback classification, not TagAttachmentUID graph preservation.
- 2026-11-04 Test `softmux-mkvtoolnix-same-input-attachment-replacement-pending.md` covers unreferenced same-source differential, not the extra referenced-UID authorization case.

**Review status**: the named targeted CI step has passed and artifact is read, but full Chromium E2E exact-head `41703427923` is still in progress. Do not mark product PR accepted, ship to users, merge, or update a Canonical norm on the strength of one targeted sample.
