# Case: CRC-bearing existing Matroska attachment mutation requires bounded source validation and inner-before-outer output recomputation

Date: 2026-10-14
Status: **PENDING exact-head native Chromium / independent Python zlib output proof**
Product branch: [MKV-Fast-Muxer PR #141](https://github.com/11576865/MKV-Fast-Muxer/pull/141)
Classification: Case, not Canonical.

## Problem and source constraints

The delivered nonterminal source-indexed relay [#139](https://github.com/11576865/MKV-Fast-Muxer/pull/139) and later original AttachedFile offset audit [#140](https://github.com/11576865/MKV-Fast-Muxer/pull/140) refused CRC-32 inside the affected `AttachedFile` or enclosing `Attachments`, since their original CRC values would be invalidated by a changed FileData. This prevents some otherwise structurally eligible Matroska sources from a non-remuxing reviewed edit. A successful EBML parse or source SHA alone does not prove CRC validity.

A scope-qualified candidate writer now accepts one source CRC-32 (ID 0xBF, four bytes) in each modified Master only after checking the **original** CRC32 over the full parent Master data excluding the **complete CRC-32 child element** (header and value). CRC-32 is ISO-HDLC/IEEE, stored little endian in EBML. Malformed, duplicated or mismatched original CRCs refuse; unknown or unbounded scope refuses.

When the selected FileData changes length inside a newly appended copy of the existing Attachments, recompute the **selected AttachedFile CRC first**, then the **parent Attachments CRC** over data that include the updated child CRC bytes. CRC child payloads that lie after resized FileData must move by the exact data-length delta in the appended new master, and the emitted CRC value is then verified. Do not change original source CRCs; existing unrelated original top-level Cluster/Cues/Chapters/Tags/seek offsets and UID target graph stay governed by #139/#140.

## Evidence and independent acceptance

[PR #141](https://github.com/11576865/MKV-Fast-Muxer/pull/141) integrates source-bound actual File grants, reviewed FileUID selection, bounded chunked CRC-32 calculation, original/produced nested CRC validation, positive grow/shrink and bad original CRC refusal tests.

A test-only independent original source fixture begins from native MKVToolNix/mkvpropedit two-attachment Matroska (one UID-tagged, one editable; nested Chapters and real codec packets) and reclaims exactly **12 bytes of free FileData** to insert one 6-byte AttachedFile CRC and one 6-byte parent Attachments CRC **without changing original top-level bytes or offsets**. That native source must still parse externally. After real Chromium output, independent **Python zlib.crc32** (separate implementation) verifies both source and resulting parent/child CRC coverage; native `mkvmerge`, `mkvextract`, `ffprobe` verify Chapter/Tag/UID/other FileData and all media packet hashes/timestamps. Any red stage is a pending failure, not delivery.

At intake checkpoint, Node/build are green and full real Chromium/native output is **still running** in [Actions #38582367728](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38582367728). Do not mark accepted or merge before exact-head independent proof.

## Reuse boundary and dedup

The operational insight is **coverage order**: when integrity checks nest, validate each original protected scope and rebuild inside out, using a parser independent of the data mutation. This is a candidate project Case, not generic permission for all CRC-bearing EBML, and **not** an automatic Canonical rule. Limits include original correct SeekHead, bounded source <=60MiB and payload <=4MiB, no CRC repair outside affected AttachedFile/Attachments, no missing/stale index, no unknown EBML/UID retarget or arbitrary byte shifts.

Dedup search against UIGS-Foundry: `EBML CRC32 nested AttachedFile Attachments independent zlib Matroska`, `CRC-32 parent master child order recheck writer`, `CRC original verified before rewrite crc32 EBML` returned no direct duplicate; earlier Cases describe source-indexed no-CRC writer, not new CRC field mutation.
