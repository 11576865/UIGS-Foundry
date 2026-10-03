# Candidate: Representative integration fixtures should preserve production topology, not production scale

Status: candidate
Date: 2026-10-03
Domains: testing, media-pipelines, acceptance, cross-platform
Evidence type: production-derived regression matrix with Linux and Windows execution

## Summary

A regression fixture for a large or expensive production input does not need to reproduce the original file size, duration, or resolution when the defect is governed by a smaller semantic topology.

For media pipelines, a small generated fixture can still be high-value if it preserves the dimensions that actually crossed the failing boundaries: container, video codec, audio codec, task mode, requested output policy, parser version, and executor path.

## Evidence

Quick-Automatic-Hardsub-Encoder previously failed on a real MKV carrying AV1 video and ALAC audio. The observed failures involved task-schema acceptance, output-container policy, explicit audio conversion, and execution wiring rather than the source's 4K resolution or hundreds-of-megabytes size.

PR #42, merged as `d7ce66a45c8832d8a4369a1bd19cb63e8425d2bb`, adds a small synthetic AV1+ALAC MKV and runs the following real FFmpeg acceptance matrix on Linux and Windows:

- copy + Auto -> preserve MKV, AV1 and ALAC;
- copy + explicit MKV -> preserve MKV, AV1 and ALAC;
- stream-copy video/audio packet payload hashes must match the source payload prefix;
- hard-sub + explicit AAC + MKV -> H.264/AAC MKV;
- hard-sub + AAC + Auto -> H.264/AAC MP4;
- every output receives a real FFmpeg decode/packet scan;
- Windows additionally parses representative schema-v3 copy and hardsub tasks.

The fixture is only seconds long and low resolution, but it preserves the codec/container/policy topology that caused the original production defect.

## Candidate rule

When converting a production regression into automated acceptance:

1. Identify the causal topology before copying incidental scale.
2. Preserve every boundary-relevant semantic dimension: format/container, codecs, stream count, task mode, policy choice, schema/version and executor class.
3. Reduce duration/resolution/size aggressively when those dimensions are not causal.
4. Use real encoders/demuxers/muxers at least once when the defect depends on external media semantics; metadata-only mocks are insufficient.
5. Assert semantic properties of the output, not merely process exit success.
6. For nominal stream-copy, verify packet/payload identity where practical.
7. Run the same representative fixture on materially different executors/OSes when portability is part of the product contract.

## Limits

This does not replace large-file, long-duration, memory-pressure or device-performance testing when scale itself is causal. Those require separate runtime/device evidence.

This is a Candidate only. It is not Canonical.
