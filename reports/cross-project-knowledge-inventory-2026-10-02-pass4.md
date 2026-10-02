# Cross-project Knowledge Inventory — Pass 4

Date: 2026-10-02

## Interface Grammar growth

Three additional UI patterns were extracted from real implementations and contract tests:

- **UIGS.WORKSPACE.SCOPE_TRANSPARENCY** — mutating tools expose WHO / WHERE / HOW MANY while the explanation remains derived rather than becoming another owner.
- **UIGS.WORKSPACE.TRANSIENT_COMMITTED_SURFACE_GEOMETRY** — drag/resize candidates, committed geometry, viewport projection and persistence are separated.
- **UIGS.INSPECTOR.PROGRESSIVE_CONTROL_DISCLOSURE** — primary actions and high-frequency controls remain above semantic advanced groups instead of becoming one flat parameter wall.

## Native execution hardening

Encoder's failure-prevention checklist was split into reusable mechanisms rather than copied whole:

- **REL.CAPABILITY_PROVEN_BY_OUTPUT** — capability names and success return codes do not prove final effect.
- **REL.DURABLE_STAGING_FOR_LONG_JOB** — formal long jobs use controlled persistent staging with preflight space checks and recoverable terminal states.
- **ARCH.NATIVE_RESOURCE_IDENTITY_PRESERVATION** — browser File objects, Android content URIs, native font pools and temporary protocol registrations retain explicit native identities.
- **OPS.RELEASE.NATIVE_BUILD_PROVENANCE** — native revision/build flags/license facts belong to release identity.
- **TEST.RENDERED_EFFECT_DIFFERENTIAL** — use a controlled visual difference to catch silent subtitle/effect failures.

## Harvest accounting

`harvest/coverage.json` now records what has already been extracted from each active repository and what remains. This is deliberately not a completeness percentage; remaining lists are evidence-backed work queues, not claims that undiscovered knowledge does not exist.
