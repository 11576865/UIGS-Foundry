# Test — source-owned FLAC encoded cache must survive final video/softsubtitle mux packet-for-packet

Date: 2026-10-14
Product: Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Product exact head: `b22f5fae2ee49d6dd3e442781729b808c89e55e8`
State: actual local Linux FFmpeg short fixture succeeded; exact-head Draft Windows/Node CI running at first query; production FLAC cached artifact handoff remains unimplemented
Requirement: B16 partial; do not close full initial version B01–B25/A01–A10.

## Dedup, difference from existing B16 entries

Existing `inbox/tests/2026-10-14-qhe-b16-source-owned-multitrack-flac-preencode-and-draft-runtime-gate.md` covers independent FLAC encode and its **audio-only** packet totals. Other B16 tests cover trim-copy observations and finished mixed output audit. None demonstrates reusing **the same already-encoded FLAC packets** as final mixed-mux inputs. This Test isolates that missing prerequisite to any future fixed encoded-audio budgeting.

## Mechanism and reusable oracle

1. Create one real source with video, two PCM audio tracks and a soft subtitle. Encode the first audio stream in full and the second for a selected trimmed interval into a Matroska FLAC cache.
2. Create one *completed* mixed Matroska with the original video and soft subtitle, but use `-map` on the **cache** and `-c:a copy` to carry the same FLAC bitstreams into the final output. Do not independently FLAC-reencode them there.
3. FFprobe each cached and completed audio stream using `-show_packets -show_data_hash sha256`. Compare **ordered** packet counts, per-packet sizes and per-packet SHA-256 content hashes, not only total bytes or a duration extrapolation. Independently verify final video, two FLAC audio streams and subtitle stream actually exist.
4. Require the original source content SHA-256, source budget measurement ID, cache artifact SHA-256, final artifact SHA-256, lossless filetime strings, exact audio source/cache/output mapping, full/trim range, rate/channels, actual final job ID and Matroska `-c:a copy` strategy. Any mismatch, duplicate/extra/missing track, order divergence, overflow or stale origin fails closed.
5. Even full equality for that completed job returns `canAuthorizeStrictBudget:false`, `canPredictNextJobSize:false` and `canRebaseWholeSourceLedger:false`. This confirms *reused audio packet payloads in one finished movie*, not future mux header/extradata/PTS/attachment overhead or final byte-ceiling guarantees.

## Code and evidence

- `src/flac-cache-reuse-contract.js` and `src/flac-cache-reuse-contract.test.mjs`
- `.github/workflows/test-frontend.yml`: six pure tests in fast/full.
- `.github/workflows/windows-b16-runtime.yml`: after real FFmpeg install, `QHE_B16_REAL_PACKET_FIXTURE=1 node --test src/flac-cache-reuse-contract.test.mjs` runs real encode/cache/final-mux and independent FFprobe packet hashes in a focused Draft runtime.
- `docs/b16-flac-cached-packet-reuse-2026-10-14.md` documents no future budget authority.
- Six actual GitHub-module isolated behavior tests PASS; JS syntax and source wiring PASS; local Linux FFmpeg 3-second real fixture gave cached and final packet sequences exactly equal (full audio 32 packets / 39300 B; trimmed audio 21 packets / 27599 B).
- Previous exact PR head `9a503bfc` had successfully completed Windows B16 real runtime including 182 s Native asynchronous packet audit, but **new** exact head `b22f5fae` Windows FLAC cached packet reuse is still running, not PASS.

## Pending / promotion policy

Production formal job must own an immutable/cache-backed audio artifact, verify source content identity and all encode options/timebase/PTS/DTS, wire actual Native output args to `-map cache -c:a copy`, and independently bound other stream costs/container overhead before any strict byte budget admission. No automatic Canonical promotion from one fixture; do not claim B16 or full theoretical V1 done.
