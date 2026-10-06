# Authority and source-of-truth model

Status: **Canonical**

## Product repository authority

A product repository is authoritative for its source code, build graph, project-specific tests, runtime behavior, releases, device results, configuration, and migrations.

## Foundry authority

Foundry is authoritative for:
- Canonical cross-project governance decisions;
- schemas and evidence semantics;
- promoted reusable knowledge;
- Claim/Evidence lineage and belief-change history;
- report contracts;
- computed effective authority for Foundry knowledge.

Foundry authority is conditional on scope, evidence, and current epistemic state. `Canonical` is a governance maturity, not an assertion of timeless truth.

## Evidence precedence

When claims conflict, prefer evidence closer to the final execution path:

static declaration < inferred capability < runtime probe < real sample < real device/final output.

The strongest evidence remains scoped to what it actually tested.

Evidence precedence does not erase provenance, assumptions, time/version context, or independence requirements.

## Effective-authority rule

Agents and retrieval systems must distinguish:
- stored maturity;
- declared authority;
- computed effective authority.

If the epistemic graph computes a Claim as quarantined because of contradiction, stale support, or a broken dependency, it MUST NOT be used as default guidance until review resolves the challenge.

## Provenance and lineage

Evidence ancestry is part of authority evaluation.

Multiple downstream artifacts derived from one upstream UIGS rule, decision, experiment, or implementation do not automatically count as independent confirmation.

W3C PROV concepts guide the Foundry provenance vocabulary:
- Entity;
- Activity;
- Agent;
- derivation;
- attribution.

Foundry may use a simpler JSON representation while preserving these semantics.

## Reference implementation rule

Foundry may host small reference implementations and demos. Production code stays in the product repository and is referenced by provenance rather than copied wholesale.
