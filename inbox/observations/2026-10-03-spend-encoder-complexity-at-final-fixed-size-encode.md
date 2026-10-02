# Observation: Spend encoder-complexity budget at the constrained final encode, not the near-transparent capture

Date: 2026-10-03
Status: Observation
Scope: OBS/NVENC capture / fixed-size final encode / B-frame references / preset selection

## Observation

When a workflow records a very high-quality intermediate (for example low-CQP NVENC AV1) and later re-encodes to a fixed output size, additional encoder-complexity features have different value at each stage.

At the near-transparent capture stage:
- P6 -> P7 usually has diminishing visible benefit when quantization is already very low;
- enabling B-frame references can improve temporal prediction and compression efficiency, but its main benefit is often smaller files / more efficient coding rather than obvious visual changes at the same low CQP;
- a stable capture with zero dropped frames is more valuable than marginal rate-distortion gains.

At the final fixed-size encode:
- preset quality and reference structure matter more because the encoder is operating under a real bit budget;
- slower presets and stronger temporal reference structures can convert the same target bitrate/file size into better retained detail.

## Reusable implication

For two-generation workflows:
1. Use a sufficiently high-quality, operationally stable capture/intermediate.
2. Reserve the most expensive encoder-search/analysis settings for the final size-constrained encode where they improve rate-distortion efficiency under a fixed budget.
3. Do not sacrifice capture reliability to gain marginal P6->P7 or B-ref improvements at an already near-transparent source stage.

Do not promote to Canonical from this single observation.
