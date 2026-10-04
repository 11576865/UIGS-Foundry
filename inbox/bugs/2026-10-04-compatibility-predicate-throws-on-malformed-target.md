# Bug: Compatibility predicates can throw on malformed targets instead of classifying them incompatible

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: batch filtering / compatibility predicates / malformed input / fail-closed behavior

## Symptom

A compatibility predicate used as a batch filter can abort the entire filter pass when the target contains malformed or out-of-range syntax that fails during preliminary parsing.

That is different from an explicit authoring action: a predicate's job is to classify the current target, so expected target incompatibility should normally be represented as an incompatible result with a reason.

## Failure mechanism

ASS Workbench Android's Karaoke compatibility path parsed the Event once to obtain a segment count **before** entering the exception-to-incompatibility boundary.

A syntactically shaped but numerically unrepresentable marker such as an oversized `\k` duration could throw during that preliminary parse. The filter therefore did not satisfy the effective contract “target is either compatible or incompatible”.

## Mitigation implemented

PR #95 moves the full compatibility plan inside the guarded boundary and computes diagnostic segment count with a secondary guarded parse only after failure.

The direct compatibility predicate now returns:

- `compatible = false`;
- a best-effort segment count;
- a reason when available;

instead of leaking ordinary malformed-target exceptions through the batch filter.

Explicit authoring/planning APIs remain free to throw and fail closed, because they represent an operation boundary rather than a classifier.

## Reusable lesson

If an API is used as a predicate/classifier over user-authored objects, define whether malformed target data is an expected negative classification or an exceptional system failure.

When malformed target data is expected in normal editing:

1. keep all target parsing inside the classification boundary;
2. return an explicit incompatible/invalid result;
3. reserve thrown exceptions for programming/system failures or for explicit mutation/preflight APIs whose contract is fail-closed.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #95
- regression coverage: oversized Karaoke duration returns incompatible and leaves source unchanged
- deduplication: searched UIGS-Foundry for total compatibility predicates, malformed target classification, and fail-closed filters; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
