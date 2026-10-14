# Case: Original non-terminal Matroska Attachments can be relocated without shifting protected top-level objects by a same-span chained SeekHead

Date: 2026-10-14
Status: **verified project-specific Case: full real Chromium and independent native MKV output PASS; merged to main; not Canonical**
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Product branch: [PR #139](https://github.com/11576865/MKV-Fast-Muxer/pull/139)
Classification: Case, **not Canonical**.

## Distinct source layout and observed technical gap

The three verified source-specific operators #136 (equal-sized FileData), #137 (FileData + directly adjacent original Void, preserved combined span) and #138 (FileData growth in the original final Attachments master, four parent size patches) cannot write a real **non-terminal** Attachments master whose FileData grows beyond local capacity. Naively moving following Clusters/Chapters/Tags/Cues risks original byte offsets and index relationships, while FFmpeg remux has a documented #77 loss of nested Chapters and UID-targeted Tags.

The project earlier needed a **test-only** chained SeekHead relay merely to construct an authentic terminal Attachments source that native MKVToolNix could actually inspect. Removing the original Seek entry made its exhaustive custom reader see an object that native `mkvmerge -J` did not discover. This new project block is the first *candidate product writer* applying that same index topology directly to **an unmodified, independently authored original non-terminal MKV**.

## Scoped relocation operator, not generic rewriting

Only for a single original Attachments master with a well-formed direct SeekHead `SeekID=Attachments`, `SeekPosition` exactly matching its old Segment-relative byte offset, a master big enough to hold an equally sized relay SeekHead and legal Void, a finite Segment and sufficient original parent size-VINT capacities: 

1. Keep every old Cluster, Cues, Chapter, Tag, Tracks and other top-level protected object in place, unchanged.
2. Replace original Attachments master byte-span by a valid **same-byte-length SeekHead** that points at the appended modified master.
3. Change each original direct SeekHead entry's **SeekID bytes only** from Attachments to SeekHead, leaving its original (possibly narrow) `SeekPosition` untouched, where it now points to the relay.
4. Append the original Attachments master copied with only original fixed-width FileData, AttachedFile, Attachments size fields and the selected new FileData contents changed; grow the original Segment size by the entire appended master byte count.

Thus *original non-Attachments and non-SeekHead top-level byte positions and commitments* need not change; the old SeekHead's only permitted delta is precisely specified SeekID bytes. Native tools must follow the chain to the appended Attachments, and an independent oracle must prove exact original nested Chapters, Target Tag identities, linked FileData and all compressed packet hashes/timestamps, not merely a custom EBML scanner verdict.

Fail closed on no original index, malformed/stale or alternate index, CRC in altered masters/SeekHead, unknown top-level EBML, ambiguous UID graph, TagAttachmentUID-targeted selected FileUID, non-final selected AttachedFile, inadequate original slot or VINT capacity, source/replacement selection changes and unverified output. Current research implementation bounds source <=60MiB and selected new payload <=4MiB, retains real private File grants in a frozen/WeakMap plan, and only allows explicit user-reviewed manual download of a new MKV. Does not overwrite source or fall back to FFmpeg.

## Submitted acceptance evidence and status

One integrated [PR #139](https://github.com/11576865/MKV-Fast-Muxer/pull/139) includes writer, reviewed UI, synthetic adversarial positive/negative tests, real Chromium scenario against original MKVToolNix/mkvpropedit-authored **non-terminal** Attachments, independent native `mkvmerge -J`, `mkvextract` original nested Chapters/Tags/attached bytes and `ffprobe` packet SHA/times, plus responsive tablet evidence. At this initial checkpoint, **Node and build succeeded, full browser/native proof still in progress** in [CI 38566327194](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38566327194). Do not report delivery before green.

## Deduplication and inference boundary

Search in Foundry for `indexed nonterminal Attachments chained SeekHead relay relocation MKV`, `Matroska original SeekID Attachments to SeekHead same offset byte-span writer`, `source-specific relocation original Cues Cluster immutable seekhead chain` found no duplicate. Previous verified Case concerns **preparing terminal source as a test fixture**, not producing new user-requested non-terminal output. This Case is distinct, provisional and must remain non-Canonical even if one product-head artifact later passes. General SeekHead/Cues rewriting, arbitrary shifts, CRC repair, wider EBML unknown-element preservation, and all-player compatibility remain unproved.

## Final exact-head production evidence (2026-10-14)

[Exact-head full CI #38566327194](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38566327194) succeeded, including **547/547 Node tests, build, all real Chromium E2E tests**. The browser log explicitly records:

`P0/P2-N real ORIGINAL NONTERMINAL Attachments → CHAINED SEEKHEAD → Segment tail variable FileData browser output + independent native Chapter/Tag/UID/Cues-packet audit PASS`

The source was the original independent MKVToolNix/mkvpropedit-authored complex Matroska, not a source pre-transformed by the previous terminal-attachment testing helper. The user-reviewed browser operation generated a real downloaded MKV. Independent native `mkvmerge -J` discovered both original FileUIDs at the appended Attachments master via the chain, `mkvextract` recovered identical nested Chapters and targeted Tags XML and preserved the original tag-linked attachment bytes while reading the new free attachment payload, and `ffprobe` matched all original codec packet SHA/timestamps. The source remained unchanged, including its originally protected media byte ranges.

[PR #139](https://github.com/11576865/MKV-Fast-Muxer/pull/139) merged to `main` at [4db7eee](https://github.com/11576865/MKV-Fast-Muxer/commit/4db7eee026aff7fabed0b566bc38715c3fb45f9c). This verifies one source-indexed nonterminal writer class, **not** arbitrary SeekHead/Cues offset rebuilding, missing-index rescue, CRC repair, non-last AttachedFile modification, unknown EBML, targeted-UID reassignment or broad playback conformance. Keep historical P0 #77 fail-closed behavior. **Case remains non-Canonical.**
