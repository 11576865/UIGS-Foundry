# Case: Same-size FileData replacement is a distinct existing-container editing capability

Date: 2026-10-14
Status: **Case / independently verified in one real-browser and MKVToolNix-authored fixture; merged product scope**
Product: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Feature PR: [#136](https://github.com/11576865/MKV-Fast-Muxer/pull/136)
Not Canonical.

## Concrete gap

Previous Matroska #77 independently demonstrated that conventional FFmpeg no-edit remux can erase nested ChapterAtom/ChapterUID-targeted Tags. The browser workbench had read-only existing-attachment UID impact, plus a separate narrow *add new Attachments into pre-reserved Void when source had no attachments* path. A user with an MKV **already containing attachments** could inspect impact but not safely modify even one attachment byte.

## Distinct bounded writer class

A replacement that changes exactly `AttachedFile/FileData` **payload bytes, with identical byte length**, is a distinct structural edit. A new Blob can be assembled from an immutable original prefix, replacement bytes and original suffix, leaving original EBML element headers, SeekHead/Cues, Cluster packets and positions, Chapters, Tags, attachment FileUID/filename/MIME and all other attachments at exactly the old byte offsets. This differs from adding new elements, rewriting IDs, or re-muxing entire streams.

Such a patch is not automatically safe. The **particular FileUID must have no TagAttachmentUID Target**, original source and output must be fully scanned, CRC in the affected Attachments hierarchy must be refused (a byte change would otherwise invalidate it), source unknown top-level EBML and incomplete UID graph must block, new data size must match exactly, and source/replacement content must be reverified immediately before and after writing. The concrete implementation is limited to <=60 MiB sources and <=4 MiB single payloads, with genuine frozen source-session plan privately holding File grants.

The UI offers original FileUID choices, visibly disables referenced UID targets, requires explicit risk review and produces **a separately downloaded new MKV** after local SHA-256/byte-offset and other-attachment verification; source overwrite and FFmpeg fallback are forbidden.

## Independent acceptance oracle, not a hypothetical model

Submitted Node adversarial corpus includes nested Chapters, a TagAttachmentUID pointing at another attachment, unchanged protected object commitment checks, wrong-size and no-op refusal, duplicate FileUID, unknown top-level EBML, CRC and forged-plan refusal.

Submitted real browser acceptance uses MKVToolNix/mkvpropedit-authored original with two existing attachments, target relationship plus nested Chapters; it replaces the **unreferenced** item. It then independently runs native mkvmerge/mkvextract/ffprobe to check the two original FileUIDs and metadata, XML of all Chapters and Tags, non-targeted and targeted FileData, stream packet and timestamp hashes, and unchanged original source.

**Submission is not output proof.** No exact-head full CI verdict was available at Case creation. The strict existing raw preservation comparator still returns a blocked/not-generally-authorized status even when this limited operator's new Blob passes local checks.

## Distinguishing hypothesis (not Canonical)

Writer capability should be typed by **which byte ranges can change without requiring graph-wide structural updates**. An equal-size FileData patch can be independently evidenced without asserting a general EBML editor or relaxing the existing preservation preflight; any length change, UID retargeting, CRC or unknown structure creates a distinct writer class requiring new proofs.

This Case is **not** a duplicate of the previous [source no-edit preservation oracle](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md): the prior record concerns no-edit detection and adding new attachment bytes to previously empty Attachments space; this one concerns preserving a pre-existing *attachment inventory and UID graph* during a payload replacement. Never auto-promote to Canonical on a single product observation.

## Verified result (2026-10-14)

**Actual output proof, not just plan submission:** [full exact-head Actions 38535796837](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38535796837) completed successfully with **539/539 Node tests, Vite build and complete real Chromium**. The raw Chromium log explicitly records:

`P0/P2 same-size existing attachment replacement + independent external chapter/tag/UID/packet/FileData audit PASS`

The independent source was `mkvmerge`/ `mkvpropedit`-authored with **two existing attachments, a TagAttachmentUID target to the first and nested Chapters**. The browser refused a wrong-size replacement, disabled the referenced attachment, required fresh review, produced a real downloaded MKV, and separate native `mkvmerge -J`, `mkvextract` chapters/tags/attachments and `ffprobe` packet-data SHA compared output to source, confirming the non-targeted new bytes and unchanged targeted FileData, original structural XML and media packets. Source file size and exact byte commitments were retained.

[PR #136](https://github.com/11576865/MKV-Fast-Muxer/pull/136) was merged to main at [17ff592](https://github.com/11576865/MKV-Fast-Muxer/commit/17ff592ae33e6dc70d3696ea0724577eae649d56), and the artifact/contract documented in [P0/P2 same-size write capability](https://github.com/11576865/MKV-Fast-Muxer/blob/main/docs/P0-P2-SAME-SIZE-EXISTING-MKV-ATTACHMENT-REPLACEMENT-20261014.md).

**Boundaries unchanged:** no general Chapters/Tags/reference rewriting, varint-length modification, SeekHead/Cues recompute, CRC repair, source overwrite, >60MiB real-source testing or multi-player/device compatibility proof. The FFmpeg-preservation regression #77 remains a separate protected risk. **Do not promote this single verified product Case to Canonical.**
