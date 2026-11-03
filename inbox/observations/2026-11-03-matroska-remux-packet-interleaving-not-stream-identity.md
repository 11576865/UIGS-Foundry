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
