# Candidate: Validate derived numeric state after composition arithmetic

Status: candidate
Date: 2026-10-04
Domains: semantic-authoring, numeric-safety, geometry, generated-effects

## Summary

Checking that user-supplied numeric parameters are finite does not guarantee that the values produced by a composition are finite or representable.

Finite coordinates, scales, rotations, durations, or offsets can overflow when they are added or multiplied. Generated authoring should validate the derived state before serializing it into canonical data.

## Candidate rule

1. Validate both source values and operation parameters at their semantic boundary.
2. Re-check every derived coordinate/state that results from potentially overflowing arithmetic.
3. Never serialize `NaN`, `Infinity`, wrapped integers, or silently saturated values into canonical project data.
4. Preserve legitimate boundary values such as zero when the underlying format permits them; do not “stabilize” them with hidden epsilon clamps.
5. For generated identifiers, check allocation capacity before incrementing the current maximum.
6. Fail before mutation if a referenced base object required for composition (for example a Style) cannot be resolved exactly.
7. Add boundary regressions for zero, very large finite values, overflow, and exhausted identifiers.

## Evidence

ASS Workbench Android PR #93 review found several derived-state hazards in FX authoring:

- reflected Y coordinates could overflow after adding an otherwise finite offset;
- source Scale Y of zero was silently rewritten to `0.001`;
- reflected Scale Y and Rotation X were not re-checked after multiplication/addition;
- entrance two-thirds timing used overflowing `duration * 2`;
- generated Event IDs used unchecked `maxId + 1`;
- effect authoring could resolve a case-mismatched Style or fall back to generic defaults rather than requiring the exact referenced Style.

The corrections preserve valid zero/off-screen geometry, use overflow-safe timing arithmetic, validate derived finite geometry, fail closed on exhausted Event-ID space, and require the source Style reference to resolve exactly.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #93
- evidence level: multiple concrete numeric/reference boundary defects + corrections + regression tests
- deduplication: searched UIGS-Foundry for derived-value finite checks, ID exhaustion, and unresolved base-style composition; no direct duplicate found
- status rationale: reusable authoring-safety candidate; not Canonical

This is a Candidate only. It is not Canonical.
