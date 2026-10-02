# Knowledge lifecycle and promotion

Status: **Canonical**

Lifecycle:

`observed -> candidate -> experimental -> validated -> canonical`

Side states: `pending`, `rejected`, `deprecated`.

- New material normally enters as Observation, Case, Bug, Test, Lesson, implementation reference, or Candidate.
- A working implementation is not by itself proof of a universal rule.
- A screenshot is evidence of appearance, not proof of behavior.
- CI success is not equivalent to device validation.

## Gates

**Experimental:** clear semantics, intended scope, and at least one implementation or reproducible case.

**Validated:** repeatable evidence and explicit constraints. Cross-platform claims require evidence from every platform claimed.

**Canonical:** stable semantics, provenance, appropriate validation, known failure boundaries, and an explicit promotion decision.

Explicit user authorization may approve a governance promotion; scope and rationale must still be recorded.
