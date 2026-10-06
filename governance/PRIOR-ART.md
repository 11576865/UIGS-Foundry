# Prior-Art Map for UIGS

Status: **Canonical design reference**
Adopted: 2026-10-07

UIGS must not invent foundational epistemic mechanisms without first mapping them to established theory, standards, or engineering practice.

This document is a design map, not a claim that UIGS fully implements every referenced formalism.

## Truth maintenance

### Jon Doyle — Truth Maintenance System (TMS)

Problem addressed:
- record reasons for beliefs;
- revise beliefs when discoveries contradict assumptions;
- preserve explanation structure;
- dependency-directed belief change.

UIGS mapping:
- Claim;
- Evidence;
- `depends_on`;
- challenge propagation;
- effective authority;
- explanation of why a Claim is active or quarantined.

Reference:
- Jon Doyle, "A Truth Maintenance System", *Artificial Intelligence*, 12(3), 1979.
- DOI: 10.1016/0004-3702(79)90008-0

## Assumption-based truth maintenance

### Johan de Kleer — ATMS

Problem addressed:
- conclusions under assumption sets;
- multiple contexts;
- inconsistent information without collapsing the whole system;
- avoiding unnecessary global retraction.

UIGS mapping:
- explicit Claim assumptions;
- scope/environment/version constraints;
- context-sensitive contradiction;
- no global invalidation when only one assumption set fails.

Reference:
- Johan de Kleer, "An Assumption-Based TMS", *Artificial Intelligence*, 28(2), 1986.
- DOI: 10.1016/0004-3702(86)90080-9

## Belief revision

### AGM framework

Problem addressed:
- expansion;
- contraction;
- revision;
- minimal change to an existing belief state.

UIGS mapping:
- Knowledge Change ledger;
- `expand`, `contract`, `revise`;
- demotion/deprecation/supersession as governance operations around belief change;
- minimal-change principle.

Reference:
- Alchourrón, Gärdenfors, Makinson (1985), AGM belief revision.
- Stanford Encyclopedia of Philosophy: Logic of Belief Revision.

## Non-monotonic and defeasible reasoning

Problem addressed:
- conclusions may cease to be warranted after new information arrives;
- rebutting and undercutting defeaters;
- adding knowledge may reduce the set of justified conclusions.

UIGS mapping:
- Canonical does not mean irreversible truth;
- contradiction may automatically remove effective authority;
- rebutting vs undercutting evidence;
- challenge/quarantine state.

Reference:
- Stanford Encyclopedia of Philosophy: Non-monotonic Logic; Formal Representations of Belief.

## Case-Based Reasoning

Classic learning cycle:
- Retrieve;
- Reuse;
- Revise;
- Retain.

UIGS mapping:
- retrieval/search;
- cross-project reuse;
- validation and belief revision;
- intake/harvest retention.

Design warning:
A system with strong Retrieve/Reuse/Retain but weak Revise is not a complete learning loop.

## Provenance

### W3C PROV

Core ideas:
- Entity;
- Activity;
- Agent;
- derivation;
- attribution;
- lineage.

UIGS mapping:
- Evidence source;
- PROV-inspired provenance fields;
- `was_derived_from`;
- attribution;
- independence lineage.

Reference:
- W3C PROV-DM / PROV-O, 2013.

## Knowledge-management governance

### ISO 30401

Relevant management-system ideas:
- establish;
- implement;
- maintain;
- review;
- improve.

UIGS mapping:
- governance lifecycle;
- review debt;
- knowledge health;
- deprecation/supersession;
- continuous improvement.

Reference:
- ISO 30401:2018 Knowledge management systems — Requirements.
- The standard is under revision as of 2026; UIGS must not freeze implementation assumptions to one edition.

## Active learning

Problem addressed:
- choose observations/queries that are most informative under limited acquisition cost;
- distinguish reducible epistemic uncertainty from irreducible uncertainty where relevant.

UIGS mapping:
- validation missions;
- prioritize high-impact Claims with uncertainty, stale support, conflicting evidence, or missing platform coverage;
- do not harvest indiscriminately.

## Software configuration and build-system semantics

Relevant ideas:
- source of truth;
- derived artifacts;
- dependency graphs;
- invalidation;
- deterministic regeneration;
- immutable history.

UIGS mapping:
- product repositories remain authoritative for execution;
- generated reports/indexes are derived;
- changed/stale evidence invalidates only dependent knowledge;
- Git history preserves revisions.

## SRE / incident learning

Relevant ideas:
- incidents are evidence;
- remediation is distinct from prevention;
- regression recurrence measures control failure;
- postmortems should lead to executable safeguards.

UIGS mapping:
- Bug lifecycle;
- prevention registry;
- recurrence count;
- challenge of Claims that asserted prevention effectiveness.

## Distributed systems / event sourcing

Relevant ideas:
- durable state;
- idempotent processing;
- explicit event history;
- asynchronous boundaries;
- replay/recovery.

UIGS mapping:
- product outbox packets;
- durable task state;
- Knowledge Change ledger;
- external validation Pending;
- agents as disposable workers.

## Prior-art-first rule

Before adding a new foundational concept to UIGS:

1. state the problem precisely;
2. identify mature disciplines that already study it;
3. record the closest formal/engineering concepts;
4. distinguish what can be adopted directly from what must be adapted;
5. document why the adaptation is necessary;
6. preserve interoperability where a standard vocabulary exists;
7. add a new UIGS-specific abstraction only when prior art does not adequately represent the requirement.

"Not invented here" is not evidence of originality.
