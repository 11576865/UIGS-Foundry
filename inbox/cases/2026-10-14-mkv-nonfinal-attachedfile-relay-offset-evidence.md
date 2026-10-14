# Case: Non-final AttachedFile resize requires proving position deltas of later original attachments inside a relocated master

Date: 2026-10-14
Status: **verified in exact-head full Chromium and native three-attachment MKV; merged scoped capability; not Canonical**
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
PR: [#140](https://github.com/11576865/MKV-Fast-Muxer/pull/140)
Classification: Case, not Canonical.

## Gap after verified source-indexed relay PR #139

The independently verified source-indexed chained SeekHead relay [#139](https://github.com/11576865/MKV-Fast-Muxer/pull/139) allows growing the FileData in the original **last** AttachedFile of a non-terminal Attachments master. A previous implementation asserted the target must be last, because it had no explicit proof accounting for other attachments that would shift **inside the relocated appended master** after an earlier payload resized. That restriction blocked editing an otherwise unreferenced first/middle FileUID.

## Scoped extension and preservation formula

Keep exactly the already proven original source eligibility: finite Segment, one original nonterminal Attachments, correct original direct SeekHead index, enough old master byte span for same-size SeekHead relay, complete TagAttachmentUID graph, a unique actual target UID, no CRC in selected AttachedFile or affected Attachments master, valid original VINT capacities, no unknown top-level EBML and no FFmpeg remux or source overwrite. Select the target by the **exact original FileData byte offset and byte length**, not filename or child index; require exactly one FileData in each original AttachedFile before matching.

Let `R = original EOF - original Attachments master start`, the relocation displacement of its unmodified bytes, and let `Δ = new selected FileData byte length - old FileData byte length`. For each original attachment other than the selected target:

- If its original data offset is **before** the selected FileData offset, its new data offset must equal `original offset + R`.
- If its original data offset is **after** the selected FileData offset, its new data offset must equal `original offset + R + Δ`.
- The selected target's new FileData offset is `original offset + R`, and its new content length and SHA must match the selected replacement.
- For all untouched attachments, FileUID, name, MIME, description, original FileData size and SHA must match precisely. All original top-level Cluster/Cues/Tracks/Chapter/Tag source bytes and offsets must remain fixed, and the original TagAttachmentUID graph must be semantically unchanged.

This distinguishes **permitted position change inside a rebuilt master** from forbidden movement of unrelated original top-level byte ranges. It does not permit modifying an UID-targeted attachment or infer general index repair.

## Submitted independent acceptance

One full-product PR #140 extends the source-bound frozen File grant / explicit review UI, adds Node growth and shrink tests with a free first attachment followed by a Tag-linked second, and a real browser test on a native MKVToolNix-authored **three-attachment** source: first Tag-referenced; middle unreferenced **target**; third untouched later attachment. The real browser output must be independently recognized by `mkvmerge -J`; `mkvextract` must prove exact first/third original FileData, changed middle bytes, nested Chapters and targeted Tags; `ffprobe` must prove identical compressed packet SHA/timestamps, and the original source must remain byte-identical. At Case writing, Node/build have passed but **full Chromium and native output acceptance are still in progress**. No delivered feature claim or Canonical change is justified before that proof.

## Deduplication

Foundry searches for `nonfinal AttachedFile original UID relocation offset after target payload`, `middle FileData source indexed SeekHead Matroska native`, and `original later AttachmentUID content offset delta proof` found only the earlier relay Case, not a matching case recording internally shifted later AttachedFile offset proofs. This is distinct from original top-level preservation; record as a project-specific Case, not a Canonical norm.

## Independently verified final evidence and source-UID incident

The exact-head full [Actions #38577634115](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38577634115) completed **SUCCESS** at [bdd03c2](https://github.com/11576865/MKV-Fast-Muxer/commit/bdd03c20889cdcbb4ee71a0046c535685fa86741), including **549/549 Node, Vite and all real Chromium**. Its named real-output verdict is:

`P0/P2-N2 NONFINAL FileUID original 3 attachments → relayed SeekHead with later FileData moved internally + native Chapters/Tags/UID/FileData/ffprobe full PASS`

The source was independently native MKVToolNix/mkvpropedit-authored with **three existing attachments**; the first was linked by TagAttachmentUID, the second unreferenced (selected), and the third also unreferenced but **physically later** in the original Attachments master. The browser generated and downloaded a real MKV via the source-indexed relay. Native `mkvmerge -J` found all three FileUIDs and metadata; `mkvextract` independently verified original first and third FileData SHA and intended second replacement, nested Chapter and targeted Tag XML; `ffprobe` established identical original packet bytes and PTS/DTS. Source SHA remained unchanged. The merged product [PR #140](https://github.com/11576865/MKV-Fast-Muxer/pull/140) is [010e29f](https://github.com/11576865/MKV-Fast-Muxer/commit/010e29f22679ff3e09f91aaca6068a38dff9da10).

Two earlier red runs [38575500069](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38575500069) and [38576340090](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38576340090) failed before writing due to the test's own invalid native TagAttachmentUID target: first an incorrect TargetTypeValue (fixed to 20), then `JSON.parse(mkvmerge -J)` silently **rounded an original uint64 FileUID**, causing a Tag referencing the wrong UID even though native tag XML had an AttachmentUID element. The fix was to **reuse the existing** `parseMkvmergeJsonWithExactUids`/`exactPositiveUid` adapter, and independently extract source Tag XML to check the exact original UID before browser testing. This is a recurrence of the existing [precision-loss Bug](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/bugs/2026-10-12-mkvmerge-json-uint64-uid-precision-loss.md), not a novel general writer safety rule. No Tag/reference refusal gate was weakened.

**Case stays below Canonical**; verified only for original nonterminal SeekHead-indexed Attachments with sufficient relay budget and valid VINT, source <=60MiB, data <=4MiB, no affected CRC, unknown top-level EBML or referenced target. No generic source index/CRC/UID rewrite authority.
