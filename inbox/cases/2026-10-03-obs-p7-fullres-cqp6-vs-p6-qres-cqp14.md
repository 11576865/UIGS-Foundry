# Case: OBS 4K60 NVENC AV1 P7 Full-Resolution CQP6 did not increase reported lag versus P6 Quarter-Resolution CQP14

Date: 2026-10-03
Status: Case
Scope: OBS recording / NVENC AV1 / extreme-quality profile stability

## Source evidence

Two consecutive completed recordings on the same OBS session and 3840x2160 60 FPS pipeline:

Recording A:
- NVENC AV1
- CQP 14
- P6
- HQ
- quarter-resolution multipass
- B-frames 4
- B-ref mode 2
- look-ahead 8
- AQ on
- rendering lag: 10 frames (0.1%)
- encoding lag: 10 frames (0.1%)

Recording B:
- NVENC AV1
- CQP 6
- P7
- HQ
- full-resolution multipass
- B-frames 4
- B-ref mode 1
- look-ahead 8
- AQ on
- rendering lag: 10 frames (0.1%)
- encoding lag: 10 frames (0.1%)

## Interpretation

In this paired run, the much more aggressive P7 + full-resolution multipass + CQP6 profile did not produce higher OBS-reported rendering or encoding lag than the preceding P6 + quarter-resolution + CQP14 profile.

This is evidence that the extreme profile is operationally viable on this hardware/workload sample. It is not proof of general stability because:
- the content was not guaranteed frame-identical;
- B-ref mode also changed;
- GPU utilization, encoder utilization, bitrate, storage throughput and temperatures were not logged;
- both runs reported a small nonzero 0.1% lag level.

## Reusable implication

Do not assume P7/full-resolution multipass is too heavy purely from preset labels. Validate with real workload counters. When two profiles show identical lag counters, prefer empirical evidence over theoretical caution, while still requiring longer worst-case tests before declaring a stable production default.

Do not promote to Canonical from this single case.
