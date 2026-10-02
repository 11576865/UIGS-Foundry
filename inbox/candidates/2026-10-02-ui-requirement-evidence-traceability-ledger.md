# Candidate: Separate requirement completion from evidence coverage in large UI experiment ledgers

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, operations, reliability

## Summary

A large UI experiment/specification list should not be tracked with one scalar "done / not done" field.

Maintain a per-requirement traceability ledger that separates:

- implementation state (Implemented / Partial / Planned / Blocked);
- current code or authoritative PR;
- concrete product Surface / production realization;
- automated regression evidence;
- Production Visual Evidence;
- device/runtime evidence;
- known blockers and missing semantics.

A presentation-level smoke test or a family-level implementation is evidence about that presentation/family, but does not automatically prove every requirement grouped beneath it.

## Evidence

ASS-Workbench-Android has a 240-item experimental UI specification. Several 12-item families already correspond to production experimental presentations, while later families are only partially represented by existing timeline/editor/font infrastructure.

During the 2026-10-02 inventory pass, treating a registered presentation as equivalent to "12/12 requirements complete" would have hidden explicit gaps such as:

- Tool Instances draft-conflict handling;
- Glass automatic avoidance of the active subtitle;
- Edge Bookmark continuous rail scrubbing and full custom group naming;
- Subtitle Object continuous radial-scrub invocation;
- Precision Lens device-dependent compositor capture;
- Timeline Dock not being present in the current-main presentation registry.

A conservative 240-row ledger was therefore created with independent implementation and evidence columns rather than deriving completion from PR titles or family membership.

## Candidate rule

For large UI plans or experiment registries:

1. Preserve each original requirement as a stable traceability ID.
2. Record implementation state independently from visual/device evidence.
3. Do not promote a whole requirement family because a presentation exists or its root smoke test passes.
4. Treat current-main code and explicitly authoritative PRs as stronger implementation evidence than historical branches.
5. Historical prototypes may support provenance but must not be labeled current authority.
6. Upgrade status only when the missing semantics for that requirement are closed and a repeatable verification path exists.
7. Keep Production Visual Evidence and device/runtime evidence as separate dimensions; CI green is not a substitute for either.

## Relationship to existing Foundry knowledge

This complements, rather than replaces:

- `OPS.UIGS.CROSS_LAYER_EVIDENCE_RESOLVER`, which links Patterns, Surfaces, Production Realizations and visual evidence;
- `REL.CAPABILITY_PROVEN_BY_OUTPUT`, which requires real output evidence for runtime capabilities;
- `Automated Production Visual Evidence Capture`, which defines visual evidence levels.

The additional observation here is the **requirement-level traceability boundary**: family/presentation evidence must not be silently inherited as proof for every child requirement.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- source plan: `ASS-Workbench-Android_超级激进UI实验清单_2026-10-02.txt`
- traceability PR: `#70`
- traceability commit: `fe9a977636d4827fb88f615ae54e3bd9ec12daea`
- evidence level: planning/traceability implementation plus repository-state audit

This is a Candidate only. It does not modify Canonical guidance.
