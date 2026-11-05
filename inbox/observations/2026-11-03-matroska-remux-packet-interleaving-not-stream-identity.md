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
