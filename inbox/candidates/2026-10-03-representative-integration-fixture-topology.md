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


## Device-acceptance extension — package the representative topology with an independent verifier

Quick-Automatic-Hardsub-Encoder PR #56, merged as `f2c1e5b004b44c3f5179a45c4ae194ce9ca051b8`, extends the representative-fixture pattern from hosted integration testing into a reproducible real-device acceptance handoff.

The project now generates one canonical multi-stream fixture containing:

- two video streams with different dimensions/frame rates;
- two audio streams;
- one soft-subtitle stream;
- one attachment;
- chapters and container metadata.

The same pack carries a fixed eight-case device matrix and an **independent output verifier**. The verifier reads the actual exported files and checks stream inventory, packet-duration behavior, Stream Copy packet hashes, hard-subtitle frame changes, preserved container assets, and full A/V decodeability.

A separate reference-output builder runs the shared task compiler against desktop FFmpeg and feeds those outputs through the same verifier. This proves that the fixture and verifier are internally usable before a human/device run, but the documentation explicitly keeps that evidence below real Windows Native / Android device acceptance.

Reusable refinement:

1. A representative fixture intended for device acceptance should be shipped as a **portable acceptance pack**, not just as test code embedded in CI.
2. The pack should bind together the source fixture, exact task cases, expected output identities, and an independent post-hoc verifier.
3. Reference-executor success should validate the fixture/verifier pair but must remain a lower evidence tier than the platform/device execution being accepted.
4. Device outputs should be verified from exported artifacts, so the acceptance claim is tied to the final product output rather than only to UI state or task-launch success.
5. A single topology-rich fixture can efficiently exercise stream selection, mixed operation policies, independent time domains, remux/transcode composition, and container-asset preservation when scale is not causal.
6. Artifact naming or a manifest should make each device result traceable to one exact acceptance case.

This strengthens the existing Candidate. It does not change Canonical guidance and does not make hosted CI equivalent to field-device evidence.


## Runtime-backed extension — same acceptance pack through the product's native host

Quick-Automatic-Hardsub-Encoder PR #57, merged as `a9be63cb0097d61301887679943c98882fc50c69`, runs the same eight-case Stream Plan v4 acceptance pack through the real Windows Native Bridge on a GitHub-hosted Windows runner.

The execution path is materially stronger than calling desktop FFmpeg directly:

```text
canonical fixture
  -> schema-v4 structured task request
  -> Windows Native Bridge HTTP contract
  -> Native task parser / capability checks
  -> Bridge-owned FFmpeg job
  -> Bridge terminal output validation
  -> final output artifact
  -> independent acceptance verifier
```

The independent verifier then checks the exported job artifacts for stream identity/count, hard-sub frame changes, independent video/audio packet durations, packet hashes for Stream Copy, remux/container identity, preserved soft subtitles and container assets, and complete timed-stream decodeability.

Reusable refinement:

- reuse the **same fixture + case manifest + external verifier** when moving from a lower evidence tier to a stronger runtime tier; changing the test oracle at the same time weakens comparability;
- runtime-backed acceptance should enter through the product's real host/parser/job lifecycle rather than invoke the underlying library directly;
- final acceptance should inspect host-produced artifacts outside the host's own validator, so one implementation bug cannot simultaneously create and certify the same false result;
- CI-hosted native runtime evidence is stronger than parser/build/reference evidence but remains below a real user/device field run;
- an automation-only local startup seam (for example a local-process initial fixture argument) is preferable to adding a remote path-injection API solely for CI.

This is additional Candidate evidence only. It does not promote the rule to Canonical and does not relabel a hosted Windows runner as field-device evidence.
