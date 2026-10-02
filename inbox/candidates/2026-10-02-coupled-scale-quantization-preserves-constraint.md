# Candidate: Coupled scale quantization must preserve the active constraint

Status: **Candidate / implementation + unit-test evidence**
Date: 2026-10-02

## Observation

When X/Y scale is proportion-locked, independently rounding X and Y to a snap grid can violate the very ratio constraint the user explicitly enabled. This is especially visible for non-square starting scales such as 120:80.

## Reusable rule

Quantization is subordinate to the active manipulation constraint.

For proportion-locked scale:
1. identify the driver axis (explicit X/Y mode, or the dominant normalized movement for XY mode);
2. quantize the driver value;
3. derive the coupled axis from the original ratio;
4. apply bounds by constraining the shared scale factor, not by clamping the two axes independently.

For unlocked scale, X and Y may be quantized independently.

## Example

Initial scale:

`X = 120, Y = 80` (ratio 1.5)

With X-driven 25-point snap, a raw X near 142 becomes:

`X = 150, Y = 100`

not:

`X = 150, Y = 75` or `X = 150, Y = 100` by unrelated independent rounding logic.

The essential invariant is that the enabled ratio constraint survives quantization and boundary handling.

## Why this generalizes

This applies to constrained resizing in vector editors, CAD, motion graphics, image editors, layout tools, and any direct-manipulation system combining:
- coupled parameters;
- explicit lock/constraint state;
- snapping or quantization.

## Validation notes

ASS-Workbench-Android now tests:
- non-square ratio preservation;
- single-axis locked driving;
- explicit percentage-point snap;
- ratio preservation under snap;
- ratio preservation at scale bounds.

## Evidence boundary

The optimal snap step values and the choice of driver axis are product-specific interaction policy. This candidate only asserts the ordering of constraints and quantization.

Do not promote to Canonical from this implementation alone.
