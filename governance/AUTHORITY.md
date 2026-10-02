# Authority and source-of-truth model

Status: **Canonical**

## Product repository authority

A product repository is authoritative for its source code, build graph, project-specific tests, runtime behavior, releases, device results, configuration, and migrations.

## Foundry authority

Foundry is authoritative for Canonical cross-project principles, schemas, promoted UI/interaction grammar, reusable reliability/operations policies, cross-project evidence semantics, and report contracts.

## Evidence precedence

When claims conflict, prefer evidence closer to the final execution path:

static declaration < inferred capability < runtime probe < real sample < real device/final output.

The strongest evidence remains scoped to what it actually tested.

## Reference implementation rule

Foundry may host small reference implementations and demos. Production code stays in the product repository and is referenced by provenance rather than copied wholesale.
