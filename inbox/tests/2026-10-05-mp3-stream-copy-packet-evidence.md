# Test: MP3 stream-copy import needs packet-level evidence across plan, save, and output

Status: **Test / Pending external CI**
Date: 2026-10-05
Project evidence: `11576865/ASS-Workbench-Android` PR #129, stacked on PR #124

## Purpose

Validate that a generic-media import can be promoted from “stream-copy compatible” to an executable capability without collapsing source parsing, execution readiness, and output verification into one claim.

This test specializes the existing Candidate:

- `2026-10-05-media-import-capability-stages-must-not-collapse.md`

and complements:

- `2026-10-03-container-editing-ui-may-mask-transactional-rebuild.md`
- `2026-10-04-container-inventory-stable-identity-diff.md`

It does not create a new Canonical rule.

## Test model

For compressed packet stream-copy, evidence is checked at three boundaries:

1. **Plan-time normalization**
   - Android `MediaExtractor` reads the selected source Track.
   - The adapter emits a deterministic bounded packet bundle (`AWPKT001`) without decoding or re-encoding.
   - The plan pins:
     - extractor Track index,
     - Matroska CodecID,
     - sample rate,
     - channel count,
     - packet count,
     - whole-bundle SHA-256,
     - logical packet-content SHA-256.

2. **Save-time re-normalization**
   - The original URI is demuxed again.
   - Bundle SHA, logical packet-content SHA, sample rate, channel count and packet count must all match the plan-time evidence.
   - Any drift fails closed before Matroska writing begins.

3. **Output verification**
   - The resulting MKV is re-opened.
   - The added Track must have a fresh destination TrackNumber / TrackUID and the intended codec/metadata.
   - A native `digest-track` pass recomputes a digest over actual output block:
     - timecode,
     - payload length,
     - payload bytes.
   - Output packet count and digest must equal the plan-time logical packet evidence.

## Why whole-file SHA alone is insufficient

A temporary packet bundle is an execution representation, not the source media itself.

A whole-bundle SHA proves that the staging artifact did not change, but it does not directly prove that the final container preserved the same packet payload/timestamp semantics after muxing.

Therefore the test distinguishes:

- **bundle identity**: execution artifact bytes;
- **logical packet identity**: timestamp + payload semantics;
- **container identity**: destination Track identity and metadata.

## Negative cases

The native protocol tests reject:

- packet bundle SHA drift;
- trailing bytes after the declared packet count;
- non-monotonic packet timestamps;
- invalid packet metadata;
- unsupported packet-audio codec mappings.

These are fail-closed conditions.

## Bounded-memory requirement

The Matroska merge must not materialize the entire external compressed stream in memory.

The packet source participates in the existing k-way merge as a streaming reader that retains only the current head block per source.

This is a test requirement, not merely a performance optimization, because full-file buffering would make “generic media import” unsafe for large assets.

## Current implementation evidence

PR #129 implements the first executable adapter:

- standalone MP3 / `audio/mpeg`;
- destination Matroska CodecID `A_MPEG/L3`;
- Android `MediaExtractor` packet demux;
- no `MediaCodec` decode/re-encode step;
- plan/save dual normalization evidence;
- native streaming packet-source merge;
- post-write packet digest verification;
- native negative tests;
- Android Emulator regression containing a real MP3 bitstream fixture.

AAC, FLAC, video adapters and transcoding remain out of scope.

## Evidence boundary

At intake time PR #129 is open and mergeable, but repository CI has not run because the current workflows filter pull requests to `main`, while #129 is intentionally stacked on feature branch #124.

Therefore this record is **Pending external CI**. It may be promoted from Test/Pending only after the stacked work reaches a CI-triggering boundary and the relevant Android/native regressions pass.
