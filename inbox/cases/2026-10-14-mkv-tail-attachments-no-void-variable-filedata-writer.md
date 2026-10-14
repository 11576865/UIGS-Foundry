# Case: No-reserved-Void Matroska FileData resize via terminal Attachments master and fixed-width parent SIZE updates

Date: 2026-10-14
Status: **verified real Chromium/native artifact and merged product capability (bounded), not Canonical**
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Product PR: [#138](https://github.com/11576865/MKV-Fast-Muxer/pull/138)
Classification: Case, not Canonical.

## Distinction from existing Cases

Previous verified P0/P2 Cases cover an *equal-length FileData byte splice* ([#136](https://github.com/11576865/MKV-Fast-Muxer/pull/136)) and a *variable-length FileData with original directly adjacent EBML Void* ([#137](https://github.com/11576865/MKV-Fast-Muxer/pull/137)); neither changes the original Segment or parent Master size. A different original source eligibility condition permits resizing without any original Void:

**The original, single Attachments master is the final top-level Segment child, and the chosen unreferenced FileUID belongs to its final AttachedFile.**

With a finite Segment length and sufficient original EBML SIZE VINT widths, a writer may modify precisely the encoded SIZE fields of FileData, AttachedFile, Attachments and Segment, plus the target FileData payload. The total file length and size of these four nested elements change; all original pre-Attachments top-level positions/bytes, Cluster packet locations, SeekHead/Cues, nested Chapters, Tags and previous attachments remain unchanged. The Attachments *start position* remains identical, so existing top-level SeekHead references to that master still resolve at the same location. The target's own later metadata fields may move within the same AttachedFile, but their values and UID relations must survive.

## Strict boundaries

The operation must refuse non-final Attachments, ambiguous/multiple Attachments masters, target that is not the final AttachedFile, TagAttachmentUID references to the chosen target, incompletely enumerated UID graph, CRC in modified ancestors, unknown top-level EBML, arbitrary extra children in affected masters, unknown length, original VINT insufficient for the new size, source or replacement changes, same-size requests and unverifiable final output. The concrete research/product guard is <=60MiB source and <=4MiB one replacement. Never fall back to FFmpeg remux or overwrite a source path.

A real user UI must select current actual FileUID and new File, explicitly confirm and bind a frozen non-serializable plan to genuine captured File instances. Re-verify actual picker contents via SHA-256 before executing and before downloading; check source and payload again after local output byte/inventory proofs.

## Submitted test architecture, not yet accepted

[PR #138](https://github.com/11576865/MKV-Fast-Muxer/pull/138) contains the bounded source reader/writer, workbench UI, synthetic grow/shrink/negative tests and full real Chromium native output audit. The native source begins as MKVToolNix/mkvpropedit-authored Matroska with two existing attachments, targeted TagAttachmentUID, nested Chapters and real codec packets. Since many such files do not naturally place Attachments last, a **test-only source transform** preserves original preexisting top-level positions by replacing the old Attachments slot with same-length Void, appending the exact original Attachments master at Segment EOF, and updating SeekHead's attachment index if its original SeekPosition capacity fits. Where a narrow SeekPosition cannot encode the new offset, the test-only transform replaces the now-invalid specific Seek entry with a same-length universal Void; SeekHead is optional but must not retain stale references. Native MKVToolNix must parse that *new prepared source* before Chrome edits it. The browser's downloaded real MKV is independently evaluated using native `mkvmerge -J`, `mkvextract` chapters/tags/attachments, and `ffprobe` original packet hashes and times.

A first [full CI 38558866210](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38558866210) completed Node **545/545** and build green but the real browser scenario failed *in test-fixture preparation* at `TEST_TAIL_SEEKPOSITION_OVERFLOW`: an original MKVToolNix SeekHead entry used too few integer bytes to point to the relocated test attachment. The next test-only preparation patch [416f7f2](https://github.com/11576865/MKV-Fast-Muxer/commit/416f7f288cbdc0fa43d91a6d725938cf8d5522c7) avoids leaving an invalid pointer, while keeping all original protected byte offsets. **Current exact-head real browser and external native verdict pending**; neither Node green nor preparation fix proves the actual writer.

## Reusable hypothesis

At least three different source-specific writer classes exist for one business-level action "replace attachment": exact data size, data length financed from an original adjacent Void, and data length paid for by growing a **terminal** EBML hierarchy. They require distinct size/offset/reference audits, but all may preserve original media packets and nested chapter/tag structures without stream remux when their specific eligibility tests pass. This is a testable Case, not permission to build or declare a general EBML writer.

Deduplication: project Foundry search for `final Attachments master Segment size width no Void existing MKV FileData`, `terminal Attachments independent structural resize SeekHead Cues` and `Matroska no Void final attached file size field rewrite` surfaced the two earlier non-equivalent preservation Cases but no direct duplicate. Do not auto-promote to Canonical from this work item.

## Final independently verified acceptance and two negative attempts (2026-10-14)

Actual completed exact-head [Actions 38560282611](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38560282611) returned **SUCCESS: 545/545 Node, Vite build, every real Chromium scenario**. The browser test log contains:

`P0/P2-T tail no-Void FOUR SIZE FIELD real browser output + native MKVToolNix chapters, targeted Tags, FileUID, FileData and ffprobe packet audit PASS`

[PR #138](https://github.com/11576865/MKV-Fast-Muxer/pull/138) merged to main at [c769a847](https://github.com/11576865/MKV-Fast-Muxer/commit/c769a847b7e12023024fd01b4a931e5f6ed61925). The source remained untouched. The independent native output check recovered the original nested Chapters and targeted Tags XML, retained the first TagAttachmentUID-linked FileData and its UID, observed the free last FileUID's new file bytes, and matched all compressed media packet hashes/timestamps with the independently native-parsed input. The actual user-facing writer did not change original SeekHead/Cues or move existing protected top-level byte ranges.

Two earlier exact-head **red browser runs** were part of the same strict acceptance, not successes:

1. [38558866210](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38558866210): the **test-only** source rearrangement tried to encode a final Attachments SeekPosition inside the original MKVToolNix `SeekPosition` field, whose original width was too narrow (`TEST_TAIL_SEEKPOSITION_OVERFLOW`).
2. [38559509527](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38559509527): a same-sized Void replaced the unrepresentable original Seek entry, but native `mkvmerge -J` then found **zero** attachments. Our internal parser seeing the trailing master was not sufficient to claim externally discoverable valid metadata.

The independently reviewed [test-only final source preparation 45da93c](https://github.com/11576865/MKV-Fast-Muxer/commit/45da93c8d9f90535efd3090d9334d085ed067157) used a **chained SeekHead relay**: the original narrow SeekHead index still targeted the exact original Attachments offset, now occupied by an equal-sized second SeekHead; the second contains a sufficiently wide SeekPosition to the unchanged Attachments master moved to Segment EOF. Native `mkvmerge -J` then recognized the prepared input, and independently verified the browser's real output. This is a *test-source construction workaround* demonstrating a valid index topology; it is **not a shipped general SeekHead relocation implementation**. A source with ordinary non-final Attachments remains refused by production code.

**Reusable evidence-qualified conclusion:** Source-local structural byte proof alone cannot substitute for external semantic discoverability. A spec-legal incomplete index can make an EBML object visible to an in-house exhaustive scanner yet invisible to native consumers; independent native tooling is therefore a separate acceptance oracle. This is one confirmed Case, not sufficient for Canonical promotion. Remaining unverified: arbitrary non-terminal attachment resizing, generic CRC repair, UID retargets, unknown EBML, >60MiB streaming and broad player compatibility.
