# UIGS Epistemic Model

Status: **Canonical**
Adopted: 2026-10-07
Scope: cross-project reusable knowledge, evidence, governance, retrieval authority, and belief change.

## Purpose

UIGS is not a document archive whose knowledge only accumulates upward.

It is a non-monotonic, evidence-governed engineering knowledge system. New evidence may add knowledge, narrow it, challenge it, remove its authority, or replace it.

The basic epistemic unit is a **Claim**. Pattern, Policy, Bug, Case, Test, Lesson, Report, and UI Grammar records are views or packages that may contain or refer to one or more Claims.

## Prior-art basis

UIGS deliberately maps its semantics to established work rather than inventing an independent epistemology:

- **Truth Maintenance Systems (TMS)** — maintain reasons/justifications for beliefs and revise beliefs when discoveries contradict assumptions. Primary reference: Jon Doyle, *A Truth Maintenance System*, Artificial Intelligence 12(3), 1979.
- **Assumption-Based Truth Maintenance Systems (ATMS)** — represent conclusions under assumption sets and support multiple contexts without treating every disagreement as a global contradiction. Primary reference: Johan de Kleer, *An Assumption-Based TMS*, Artificial Intelligence 28(2), 1986.
- **AGM belief revision** — distinguishes expansion, contraction, and revision of a belief state.
- **Non-monotonic / defeasible reasoning** — conclusions may be retracted when later information supplies rebutting or undercutting defeaters.
- **Case-Based Reasoning (CBR)** — Retrieve -> Reuse -> Revise -> Retain provides the learning loop for reusable engineering cases.
- **W3C PROV** — provenance semantics for entities, activities, agents, derivation, and attribution.
- **Knowledge-management systems** — governance must include establishment, maintenance, review, and continual improvement rather than capture alone.
- **Active learning** — evidence acquisition should prefer unresolved, high-impact, discriminating questions rather than indiscriminate harvesting.

These theories guide semantics. UIGS does not claim to be a complete formal implementation of any one of them.

## The four-layer model

### 1. Source artifacts

Authoritative external facts remain in their owning systems:

- product source code;
- tests;
- commits and pull requests;
- workflow runs;
- releases;
- runtime probes;
- device/final-output evidence;
- standards and external references.

Foundry records provenance and interpretation; it does not become a duplicate source repository.

### 2. Evidence

An Evidence record states what was observed, where it came from, when it was observed, what environment it applies to, and how it relates to one or more Claims.

Evidence may:
- support a Claim;
- contradict a Claim;
- test a Claim but remain inconclusive;
- narrow the scope of a Claim.

Evidence has lineage. Multiple artifacts derived from the same originating decision or rule are not automatically independent evidence.

### 3. Claims

A Claim is a proposition that can be supported, contradicted, scoped, challenged, superseded, or withdrawn from active authority.

Claims carry:
- statement;
- kind;
- maturity;
- authority;
- epistemic state;
- assumptions;
- scope;
- evidence references;
- dependencies on other claims;
- supersession relationships;
- support policy;
- review metadata.

### 4. Knowledge views

Pattern, Policy, Bug, Case, Test, Lesson, Report, UI Grammar, and other higher-level records organize Claims for humans and agents.

A view does not become more authoritative than the Claims and evidence it depends on.

## Three orthogonal state dimensions

### Maturity

Maturity records how far a Claim has passed through governance:

`observed -> candidate -> experimental -> validated -> canonical`

Maturity is historical/governance information. It is not a declaration of eternal truth.

### Authority

Authority controls whether an agent may currently use the Claim as guidance:

- `active` — may be used according to maturity and scope.
- `quarantined` — do not use as default guidance pending review.
- `deprecated` — do not use for new work except historical analysis/migration.
- `superseded` — a more authoritative Claim replaces it.

A Canonical Claim may be quarantined without erasing the fact that it was previously promoted to Canonical.

### Epistemic state

Epistemic state summarizes the current evidence relation:

- `unknown` — insufficient current evidence.
- `supported` — current support exists and no active contradiction is known.
- `mixed` — current support and contradiction both exist.
- `challenged` — a defeater or dependency problem requires review.
- `contradicted` — strong current evidence directly opposes the Claim.
- `stale` — previously relevant evidence is no longer sufficiently current for its declared scope.

These dimensions MUST NOT be collapsed into one status field.

## Assumptions and context

Claims may be valid only under stated assumptions.

Examples:
- platform;
- framework/runtime version;
- architecture style;
- execution environment;
- ownership model;
- persistence model;
- hardware constraints;
- user workflow constraints.

Contradictions across different assumption sets are not necessarily contradictions in the same context.

This is an ATMS-inspired design rule: context is explicit instead of being hidden in prose.

## Evidence lineage and independence

Evidence independence is a first-class concept.

If Rule X caused projects A, B, and C to adopt the same implementation, then harvesting A, B, and C does not create three independent confirmations of X.

Evidence records therefore carry an `independence_key` (or equivalent lineage identity). Support counting is performed over independent lineage groups, not raw artifact count.

Derived evidence MUST preserve its ancestry.

## Defeaters

UIGS recognizes two important classes of defeater:

- **rebutting defeater** — evidence supports the negation or failure of the Claim itself;
- **undercutting defeater** — evidence attacks the reliability, applicability, assumption, or provenance of the reason supporting the Claim.

Both can trigger challenge and authority quarantine.

## Dependency invalidation

If Claim B depends on Claim A, loss of authority or support for A MUST propagate to B as review debt.

The propagation rule is conservative:

- direct contradiction of A does not automatically rewrite B;
- it does make B `challenged` when B materially depends on A;
- high-authority B may be effectively quarantined until the dependency is reviewed.

This implements the Charter principle: invalidate only what depends on changed state.

## Belief-change operations

UIGS records belief change using operations aligned with established terminology:

- `expand` — add a new Claim/evidence without removing existing authority;
- `challenge` — register a defeater or unresolved contradiction;
- `quarantine` — remove effective default authority while preserving history;
- `revise` — change statement/scope/assumptions to accommodate evidence;
- `contract` — withdraw a Claim or part of its scope from the active belief set;
- `restore` — return a quarantined Claim to active authority after review;
- `promote` — raise governance maturity after an explicit promotion review;
- `demote` — lower governance maturity by explicit decision;
- `deprecate` — retain history but prohibit new default use;
- `supersede` — replace with another Claim.

Every non-trivial authority/maturity change requires a durable Change record with reason and evidence.

## Automatic vs governed change

Automation MAY:
- detect contradictions;
- detect stale evidence;
- detect broken dependencies;
- compute independent support groups;
- mark a Claim as effectively challenged;
- **automatically quarantine effective authority** when a configured safety rule is triggered;
- create a review item.

Automation MUST NOT silently:
- promote to Canonical;
- permanently demote historical maturity;
- deprecate a Claim;
- rewrite Claim meaning;
- invent supporting evidence.

Permanent revision/demotion/deprecation/supersession requires an explicit governance decision recorded in a Change record.

## Effective authority

Consumers MUST prefer computed **effective authority** over the stored declared authority.

Example:

```
declared maturity: canonical
declared authority: active
current contradiction: yes
computed effective authority: quarantined
```

The historical record remains Canonical, but agents must not use it as default guidance until review resolves the contradiction.

## Retrieval rule

Knowledge retrieval must rank/filter in this order:

1. scope and assumptions match;
2. effective authority permits use;
3. epistemic state;
4. maturity;
5. evidence directness/freshness;
6. relevance.

A semantically relevant but quarantined Claim must not outrank an active, scoped Claim merely because it once reached Canonical.

## Learning loop

UIGS learning is externalized and auditable:

```
Observe
-> Evidence
-> Claim
-> Retrieve / Reuse
-> Execute
-> Observe outcome
-> Revise / Challenge
-> Retain
```

This is not model-weight training.

A system that only executes `Observe -> Retain` is an archive, not a learning system.

## Active-learning direction

UIGS SHOULD generate validation missions when high-impact Claims have:
- insufficient independent evidence;
- stale evidence;
- unresolved contradictions;
- platform coverage gaps;
- assumptions that have never been tested;
- repeated prevention recurrences.

The system should prefer evidence that can discriminate between competing explanations.

## Compatibility

Existing Pattern/Policy/Bug/Case/Test/Lesson records remain valid aggregate knowledge artifacts.

Migration is incremental:
- existing records do not need to be rewritten immediately;
- new high-impact or promoted knowledge should attach explicit Claim/Evidence records;
- Canonical or Validated knowledge should migrate first;
- retrieval and reports should increasingly consume the Claim/Evidence graph as coverage grows.

Legacy aggregate records are not automatically granted claim-level certainty.
