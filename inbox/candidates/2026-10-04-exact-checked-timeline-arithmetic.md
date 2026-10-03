# Candidate: Use exact checked arithmetic for persisted timeline transforms

Status: candidate
Date: 2026-10-04
Domains: timeline-editing, numeric-safety, batch-authoring, persistence

## Summary

When an editor transforms persisted integer timeline coordinates, floating-point intermediates and unchecked fixed-width arithmetic can silently change or wrap values even when the source timeline itself is valid.

For persisted time transforms, arithmetic should preserve the integer time model as long as the requested mapping is rational/integer-expressible, and overflow should be reported before mutation.

## Candidate rule

1. Keep integer/rational timeline transforms in exact arithmetic rather than routing them through floating-point intermediates.
2. Check derived values after addition, subtraction, multiplication, and division; validating only the input operands is insufficient.
3. Preserve the operation's documented rounding/truncation semantics explicitly.
4. Reject results outside the persisted time type's representable range instead of allowing wraparound or saturation.
5. Keep preflight pure so overflow cannot partially mutate a batch.
6. Add regression values above 2^53 and near the integer type's extrema; ordinary small values do not expose these defects.

## Evidence

ASS Workbench Android PR #95 previously implemented batch timing scale as:

`origin + ((value - origin).toDouble() * numerator / denominator).toLong()`

This could lose millisecond precision above 2^53 and could overflow before or after conversion. Batch time shifting also used unchecked `Long` addition.

The correction uses exact `BigInteger` arithmetic for Shift/Scale Timing, preserves truncation semantics for rational scaling, clamps only the already-defined negative-time case, and fails closed when a derived result exceeds `Long.MAX_VALUE`.

Regression coverage includes an exact timestamp of `9_007_199_254_740_993` ms and overflow cases near `Long.MAX_VALUE`.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #95
- evidence level: concrete precision/overflow defect + checked-arithmetic correction + regression tests
- deduplication: searched UIGS-Foundry for exact timeline arithmetic, floating-point time transforms, and checked overflow; no direct duplicate found
- status rationale: reusable engineering candidate; not Canonical from one project observation

This is a Candidate only. It is not Canonical.
