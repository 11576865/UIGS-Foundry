# Observation — Global ffprobe packet interleaving is not per-stream payload preservation

Date: 2026-11-03
Status: **Candidate observation from a real browser/native failure; exact-head corrected CI pending**
Domain: Matroska Stream Copy output evidence, test-oracle construction and cross-container attachment reuse.

## Observed actual failure

Product branch [PR #231](https://github.com/11576865/MKV-Fast-Muxer/pull/231) adds a user-visible operation: import A.mkv and B.mkv, open A's AttachedFile via seek-based EBML inspection, include its FileData directly in B's ordinary browser output. The actual Chromium writer **finished successfully and delivered a new MKV with one ordinary attachment**, and the browser test had already verified the real attached FileData by `mkvextract`.

However, exact-head original CI run [41663297511](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41663297511) failed in the new end-to-end suite at assertion `selected B track compressed payload unchanged`. The test compared source and output `ffprobe -show_packets -show_data_hash sha256` returned **global row order** (video+audio interleaved) as a single sequential list. Failure diff showed the same packet hash strings moved relative to other entries, rather than solely new hash strings. This is consistent with a legitimate muxer rewrite of cross-track interleaving, not proof of content alteration.

## Reusable method

For a *no-media-edit* Stream Copy expectation, compare **ordered packet payload hash sequences independently per stream** and check the corresponding stream-scoped PTS/DTS with an explicit timebase tolerance. Keep codec and track identity checks separate. Never equate differences in arbitrary global audio/video packet interleaving with content loss, and never weaken validation to mere count, file playability or unordered packet multiset without further evidence.

This method does not automatically prove preservation under track reordering, same-type/same-codec track swaps, packet duplicate hashes or altered per-stream order. More complex cases require explicit stream identity mapping (e.g. TrackUID when appropriate) and independent packet/timeline evidence.

## Fix and pending result

Changed actual test `tests/e2e/cross-source-attachment-reuse-scenario.mjs` to group ffprobe packet rows by stream_index before comparing per-stream ordered `data_hash` arrays and PTS/DTS differences (<= 0.0011 seconds in the named short fixture). Product corrected commit `3b610eb91b0af609048ef1651fdbb3394ff5e81c`. **Full browser CI [41664141973](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41664141973) pending** at observation time. Do not assert a verified PASS until the exact new run completes.

No production writer modification was required to address this particular test-oracle problem; not a Canonical change. If corrected CI reports per-stream mismatches, investigate as possible production bug, not further normalize away.

## Accepted outcome — exact corrected head (2026-11-03)

The corrected stream-scoped per-track payload and PTS/DTS audit passed the **entire** [Browser CI 41664141973](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41664141973) for product [PR #231](https://github.com/11576865/MKV-Fast-Muxer/pull/231) exact head `3b610eb91b0af609048ef1651fdbb3394ff5e81c`, including real A.mkv→B.mkv attached-file output native evidence upload; S12 large-media scoped and Pages build also succeeded. Merged to `main@ef786241eb1dbde00793049631eb0c3d96eeb70a`.

The earlier global `ffprobe -show_packets` order false-positive is confirmed: the real browser output preserved each B stream's compressed packet SHA sequence and PTS/DTS within the named ≤1.1 ms tolerance while changing interleaving order between streams. This is a bounded real-world positive validation of per-stream comparison, not a general guarantee for other codecs, track reorder, or timestamp remapping. Keep as Observation; no single-case Canonical rule change.


## 2026-11-05: S02/S04 actual output stream identity evidence (CI pending)

**Dedup/Intake:** Continue this pre-existing stream-identity and independent-oracle Observation. There is no new general policy; do not promote it to Canonical. The owner-approved 1.0 strategic direction requires actual delivered MKV evidence, but S01–S14 detailed acceptance and release candidate remain unapproved/unfrozen.

Product [Draft PR #245](https://github.com/11576865/MKV-Fast-Muxer/pull/245) at exact code head `c4cc76cc1fea9cda12ae0d0e15d21d9326c407cc` adds **only test + CI artifact upload**. Existing actual Chromium output scenarios are extended to independently native-check selected stream compressed payload via `ffmpeg -i input -map 0:[stream] -c copy -f hash -hash SHA256 -` for **each specific corresponding source/output stream**, not the global interleaved packet order. User-facing source-track selection, audio reorder and bulk language/Default are confirmed against separately demuxed output codec/order/metadata. MP4→MKV SSA/SRT/WebVTT scenario distinguishes its explicitly declared subtitle conversion from unchanged video/audio compressed bytes, separately demuxes SSA/SRT text and retains an independent millisecond WebVTT SubRip text/timing oracle. It will upload actual MKVs, reports, per-operation JSON receipts for independent reread rather than rely on CI green alone.

**Scoped-oracle limits:** Hash of an aggregated per-stream compressed byte sequence is strong evidence that compressed bytes were not re-encoded, but by itself does **not** prove original per-packet boundaries, PTS/DTS/timestamp identity, attachment or Chapter/Tag preservation, actual player presentation, or all supported combinations. Retain existing finer packet/timeline and P1 semantic oracles rather than replacing them. No product UI/Writer/Reader change. Release statuses S02/S04 remain UNASSESSED.

**Evidence status:** `Pending CI` for exact PR #245 head. Browser E2E [#41975705591](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41975705591) was running at Intake (syntax, unit, build, native P1 and S10/S03 already green); Pages [#41975705526](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41975705526) SUCCESS. Do not claim the new S02/S04 runtime hash assertions or archives passed until complete.


## 2026-11-05: S02/S04 native source-to-output proof completed and merged

**Deduplicated closeout** of the preceding `Pending CI` entry in this Observation, **not** a Canonical promotion.

[Product PR #245](https://github.com/11576865/MKV-Fast-Muxer/pull/245) exact code head `c4cc76cc1fea9cda12ae0d0e15d21d9326c407cc` passed [full Browser E2E #41975705591](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41975705591), [Pages #41975705526](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41975705526). Product PR was squash-merged to **`main@c5259ec9dc66777aa8403f42795dabe7b4063d28`**, confirmed against the live main ref and actual scenario source. No runtime product code changed, only existing Chromium tests and artifact upload instructions.

**Direct ZIP and native media reinspection**:
- S02 actual archive `s02-multiformat-source-codec-and-native-output`, artifact `13392147260`: `additional-formats.mkv` 186,551 bytes, whole-file SHA-256 `ae2e7dd230ea42cf7e15ba814c4d4eea7b58511d2a71ddc0331c3b50ea646e32`. Native local `ffprobe`: MPEG4 video, AAC audio, 3 subtitle streams (ASS, SubRip, SubRip); local native FFmpeg per-selected-stream SHA-256 re-computation matches source-hash receipt for video `d6272b7be5c77cbc7ebeba62fd05881796787d307474d2671d7bd95ed2f74bc0` and audio `9bdca3a93fd00afa530cd614e04cdf84086d2bb07913516b0d4c2b170109be36`. The passing Browser E2E separately demuxes SSA and SRT actual text and the WebVTT→SubRip millisecond-overlap text/timing oracle. Report and receipt agree with output file hash.
- S04 actual archive `s04-source-track-attributes-order-native-output`, artifact `13392326640`: **three independently extracted and checked actual MKVs**. Original-track selection output 942,611 bytes SHA `ac9a0828c64f109764ec9bbf15e3b5a3374a622143cf85ccca16c766009e8e60` (retained Opus + video copy, excluded AAC, explicit audio/subtitle metadata and Forced); reordered original audio output 967,935 bytes SHA `8bf035e424a24334099bf83bd120dd9755e5d8b3f0cc75e4515195d485e2173d` (Opus then AAC); bulk-language/default output 967,932 bytes SHA `ca08f84361d8431922796d755508e160ae0d0e7052ffca2191d93111c2eba974` (AAC then Opus, both zho, first Default). For each, independent local `ffprobe` checks actual stream presence; local native FFmpeg computed output video and corresponding AAC/Opus per-stream compressed hashes **all exactly equal** the browser receipt's source per-stream hashes. Output reports, where included, were checked against actual file SHA.

**Evidence limitation:** These ZIPs contain downloaded **output** files but not original source media. Equality to **input** compressed bytes is an assertion tested in the exact full browser run; direct ZIP reinspection independently repeats **output** hashes and their consistency with browser's input claims, not a second external source rehash. An aggregated `-f hash` per stream proves ordered compressed-bytestream correspondence in the tested fixture but does not replace per-packet boundary/PTS/DTS assertions, subtitle rendering, Chapter/Tag UID verification, arbitrary codec/timebase claims or a frozen 1.0 candidate. Therefore the specific S02/S04 evidence task is **scoped PASS / merged**, broader release acceptance still UNASSESSED.

**Intake resolution:** Prior PR #245 `Pending CI` -> **Closed / verified**. Keep existing Observation as the home for independent stream-identity proof; do not create a second rule or modify Canonical.


## 2026-11-05: Release ledger reconciled without status promotion

**Product evidence provenance repair:** The actual S02/S04 [PR #245](https://github.com/11576865/MKV-Fast-Muxer/pull/245) native-output test work was merged at `main@c5259ec9dc66777aa8403f42795dabe7b4063d28`. The test success must no longer be described in the 1.0 release ledger as a complete lack of source/format/track evidence. In docs-only [PR #246](https://github.com/11576865/MKV-Fast-Muxer/pull/246), merged at **`main@e908a04d11c0ea6098c5b7709b1470034d81179e`**, three existing `implementationEvidence` sections (S01, S02, S04) were updated with code-head SHA, actual Browser run, native artifact IDs/receipts and specific still-open gaps; no other scenario or release-authority object was altered. Before writing, programmatic structural diff independently verified all 14 `status`/formal `evidence`/ `verifiedCommit` untouched, owner contract still `PENDING_OWNER_REVIEW`, `release.candidateCommit=null` and JSON formatting/structure valid; after merge, GitHub main JSON was reread and retained those invariants.

**Reusable process distinction:** A source-grounded *scoped product CI acceptance* should update the ledger's implementation discovery and resolved open gaps, **without** asserting owner contract approval, frozen release-candidate evidence or formal scenario PASS. Conversely, leaving stale "no evidence" statements after actual output success misrepresents project completion. This documents a bounded reconciliation method, not a new Canonical norm. No new test, writer or release authorization came from docs-only PR #246.
