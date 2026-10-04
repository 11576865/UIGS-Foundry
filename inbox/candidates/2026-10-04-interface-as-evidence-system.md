# Candidate: Interface as an evidence system

Status: candidate
Date: 2026-10-04

## Summary

Users respond not only to what an interface visibly shows, but also to what they infer is happening behind it.

Reusable model:

`Observable Evidence -> Inferred Hidden State -> Interpretation -> Response`

## Candidate rule

Treat actual system state and user-inferred state as separate variables.

- Operational semantics: what the system is doing.
- Interpretive semantics: what the user believes is happening and why.

Labels, provenance, progress indicators, delay explanations, verification markers, and similar cues can alter the inferred hidden state even when the underlying output is unchanged.

Design and testing should therefore verify both the state machine and the evidence presented to users.

## Evidence boundary

This is a conceptual interaction hypothesis, not an empirical universal. The direction and magnitude of attribution effects require testing in each context.

This is a Candidate only. It is not Canonical.
