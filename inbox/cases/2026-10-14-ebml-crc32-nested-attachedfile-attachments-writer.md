# Case: CRC-bearing existing Matroska attachment mutation requires bounded source validation and inner-before-outer output recomputation

Date: 2026-10-14
Status: **verified exact-head independently native CRC-32 output; merged project Case, not Canonical**
Product branch: [MKV-Fast-Muxer PR #141](https://github.com/11576865/MKV-Fast-Muxer/pull/141)
Classification: Case, not Canonical.

## Problem and source constraints

The delivered nonterminal source-indexed relay [#139](https://github.com/11576865/MKV-Fast-Muxer/pull/139) and later original AttachedFile offset audit [#140](https://github.com/11576865/MKV-Fast-Muxer/pull/140) refused CRC-32 inside the affected `AttachedFile` or enclosing `Attachments`, since their original CRC values would be invalidated by a changed FileData. This prevents some otherwise structurally eligible Matroska sources from a non-remuxing reviewed edit. A successful EBML parse or source SHA alone does not prove CRC validity.

A scope-qualified candidate writer now accepts one source CRC-32 (ID 0xBF, four bytes) in each modified Master only if the CRC child is the **FIRST ordered child (mandatory in RFC 8794 §11.3.1)** and after checking the **original** CRC32 over the full parent Master data excluding the **complete CRC-32 child element** (header and value). CRC-32 is ISO-HDLC/IEEE, stored little endian in EBML. Malformed, duplicated or mismatched original CRCs refuse; unknown or unbounded scope refuses.

When the selected FileData changes length inside a newly appended copy of the existing Attachments, recompute the **selected AttachedFile CRC first**, then the **parent Attachments CRC** over data that include the updated child CRC bytes. CRC child payloads that lie after resized FileData must move by the exact data-length delta in the appended new master, and the emitted CRC value is then verified. Do not change original source CRCs; existing unrelated original top-level Cluster/Cues/Chapters/Tags/seek offsets and UID target graph stay governed by #139/#140.

## Evidence and independent acceptance

[PR #141](https://github.com/11576865/MKV-Fast-Muxer/pull/141) integrates source-bound actual File grants, reviewed FileUID selection, bounded chunked CRC-32 calculation, original/produced nested CRC validation, positive grow/shrink and bad original CRC refusal tests.

A test-only independent original source fixture begins from native MKVToolNix/mkvpropedit two-attachment Matroska (one UID-tagged, one editable; nested Chapters and real codec packets) and reclaims exactly **12 bytes of free FileData** to insert one 6-byte AttachedFile CRC and one 6-byte parent Attachments CRC **without changing original top-level bytes or offsets**. That native source must still parse externally. After real Chromium output, independent **Python zlib.crc32** (separate implementation) verifies both source and resulting parent/child CRC coverage; native `mkvmerge`, `mkvextract`, `ffprobe` verify Chapter/Tag/UID/other FileData and all media packet hashes/timestamps. Any red stage is a pending failure, not delivery.

At intake checkpoint, Node/build are green and full real Chromium/native output is **still running** in [Actions #38582367728](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38582367728). Do not mark accepted or merge before exact-head independent proof.

## Reuse boundary and dedup

The operational insight is **coverage order**: when integrity checks nest, validate each original protected scope and rebuild inside out, using a parser independent of the data mutation. This is a candidate project Case, not generic permission for all CRC-bearing EBML, and **not** an automatic Canonical rule. Limits include original correct SeekHead, bounded source <=60MiB and payload <=4MiB, no CRC repair outside affected AttachedFile/Attachments, no missing/stale index, no unknown EBML/UID retarget or arbitrary byte shifts.

Dedup search against UIGS-Foundry: `EBML CRC32 nested AttachedFile Attachments independent zlib Matroska`, `CRC-32 parent master child order recheck writer`, `CRC original verified before rewrite crc32 EBML` returned no direct duplicate; earlier Cases describe source-indexed no-CRC writer, not new CRC field mutation.

## Normative CRC child order correction (not Canonical promotion)

The first product run [38582367728](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38582367728) succeeded against a **non-compliant** test source that placed otherwise numerically correct CRC-32 elements at the end of their Masters. A normative check of [RFC 8794 §11.3.1](https://www.rfc-editor.org/rfc/rfc8794.html#section-11.3.1) confirmed a CRC-32 child **MUST be first**. The product code added `RELAY_CRC_MUST_BE_FIRST_CHILD`, the source fixture prepends both CRCs, and the independent Python oracle rejects late CRC. Node tests now include valid CRC values in late positions as negative samples. Acceptance must be based on a **new exact-head conforming-source CI**, not on the initial green run. This is project-specific evidence and does not auto-change Canonical.

## Verified final external output evidence (2026-10-14)

The **compliant-source** final PR head [3f18a73](https://github.com/11576865/MKV-Fast-Muxer/commit/3f18a7341a26afe0b01e1a5076d0254024c65c32) completed [Actions #38583859923](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38583859923) **SUCCESS**: 552/552 Node tests, build, full Chromium and the named native-output oracle:

`P0/P2-C ORIGINAL native CRC32 Attachments + AttachedFile → Chromium changed FileData → INDEPENDENT Python zlib nested+parent CRC32 + mkvmerge/mkvextract/ffprobe PASS`

The approved source layout began with actual MKVToolNix/mkvpropedit original attachments, targeted AttachmentUID Tags, nested Chapters and codec packets. A transparent source-fixture transformation financed one original 6-byte CRC child in AttachedFile and one original 6-byte CRC child in enclosing Attachments using 12 original selected FileData bytes, retaining original top-level offsets and total bytes. Both CRC children were **first** as required by RFC 8794; independent Python zlib authored/checked both original CRCs. Chromium changed free FileData and downloaded a new MKV; Python zlib again verified both resulting CRCs independently. Native mkvmerge/mkvextract and ffprobe audited original UID, linked other attachment data, Chapter/Tag XML and compressed packet SHA/timestamps. Real browser UI also asserted the presence of **two recomputed/rechecked CRC scopes**. Original source remained unchanged.

[PR #141](https://github.com/11576865/MKV-Fast-Muxer/pull/141) merged into main at [b809701](https://github.com/11576865/MKV-Fast-Muxer/commit/b8097016185f82430fc9e518545992764d7e3f0a). **Superseded first green run** #38582367728 used noncompliant CRC placement and is intentionally not acceptance proof; a later exact-head successful run with first-child CRC fixture provides conformance evidence. This is limited to original existing correct direct SeekHead/known Attachments and affected AttachedFile CRC scopes, not arbitrary EBML CRC or general Cues/SeekHead/Chapter/Tag repair. Classification stays **Case**, no Canonical modification from one project artifact.
