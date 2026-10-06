# Knowledge lifecycle, promotion, challenge, and demotion

Status: **Canonical**

This policy is subordinate to the epistemic semantics in `governance/EPISTEMIC-MODEL.md`.

## Maturity is not current truth

The maturity ladder is:

`observed -> candidate -> experimental -> validated -> canonical`

It records governance maturity: how far a Claim has progressed through review and validation.

It MUST NOT be treated as an irreversible truth ladder.

Current usability is controlled separately by **authority** and **epistemic state**.

## Authority lifecycle

Authority is:

- `active`
- `quarantined`
- `deprecated`
- `superseded`

A Canonical Claim can therefore be:

`maturity=canonical, authority=quarantined`

without falsifying its promotion history.

## Epistemic state

Current evidence is summarized separately as:

- `unknown`
- `supported`
- `mixed`
- `challenged`
- `contradicted`
- `stale`

Consumers must use computed effective authority, not maturity alone.

## Promotion gates

**Experimental:** clear semantics, explicit scope/assumptions, and at least one implementation, reproducible case, or direct test.

**Validated:** repeatable evidence, explicit constraints, and sufficient independent support for the declared scope. Cross-platform claims require evidence for every platform explicitly claimed, unless the claim itself is platform-independent and that independence is justified.

**Canonical:** stable semantics, provenance, appropriate independent validation, known failure boundaries, explicit assumptions/scope, a declared support policy, and an explicit promotion decision.

A working implementation is not by itself proof of a universal rule.
A screenshot is evidence of appearance, not proof of behavior.
CI success is not equivalent to device/final-output validation.

Explicit user authorization may approve a governance promotion; scope and rationale must still be recorded.

## Challenge and automatic quarantine

New evidence may challenge any maturity level, including Canonical.

Automation may calculate `effective_authority=quarantined` when a Claim's configured policy is triggered by:
- active contradicting evidence;
- an undercutting defeater;
- a materially broken/quarantined dependency;
- insufficient current support after evidence becomes stale/retracted.

Automatic quarantine is a safety action, not permanent demotion. It prevents default reuse while preserving history.

Every automatic quarantine must surface:
- triggering evidence/dependency;
- reason;
- affected Claim;
- recommended review action.

## Permanent belief change

Permanent changes require a durable Knowledge Change record conforming to `schemas/knowledge-change.schema.json`.

Allowed operations include:
- `expand`
- `challenge`
- `quarantine`
- `revise`
- `contract`
- `restore`
- `demote`
- `deprecate`
- `supersede`

### Demotion

Demotion lowers governance maturity when the original evidence or validation basis is no longer adequate.

Examples:
- Canonical -> Validated
- Validated -> Experimental

Demotion is explicit and reviewable. Automation may recommend it but must not silently rewrite historical maturity.

### Deprecation

Deprecation retains the Claim for historical/recovery purposes but prohibits default use for new work.

### Supersession

Supersession preserves the earlier Claim and points to a replacement with narrower, corrected, or more current semantics.

## Minimal-change principle

Belief revision should remove as little valid knowledge as necessary.

When evidence conflicts:
1. check scope and assumptions;
2. distinguish rebutting from undercutting defeaters;
3. invalidate only dependent Claims;
4. prefer narrowing/revising scope over global deletion when justified;
5. preserve provenance and the complete change history.

## Evidence independence

Raw evidence count is not promotion strength.

Evidence derived from a shared upstream rule, implementation, experiment, or decision belongs to the same lineage group unless an independent causal basis is demonstrated.

Promotion gates must reason over independent evidence groups rather than artifact count.

## Legacy aggregate records

Existing Pattern/Policy/Bug/Test/Case/Lesson records may still use their historical `status` field.

As they migrate to Claim/Evidence semantics:
- `status` remains a compatibility projection of maturity;
- effective authority comes from the epistemic graph;
- a quarantined Claim must not be presented as active guidance merely because its legacy aggregate record says `canonical` or `validated`.
