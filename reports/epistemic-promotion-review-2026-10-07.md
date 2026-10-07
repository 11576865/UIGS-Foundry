# Experimental Promotion Review — 2026-10-07

Status: **Governed review complete**

Scope: the 12 Experimental records identified as promotion candidates before Claim-level mapping.

## Result

- Reviewed: 12
- Promoted to Validated: 7
- Retained Experimental: 5

Promotion is deliberately stricter than implementation existence. A Claim was promoted only when the evidence was sufficient for its current narrow scope and included executable/runtime or production-path validation. Records retained at Experimental now have support policies that drive explicit Validation Missions.

## Decisions

- `ARCH.DECLARED_DISCOVERED_RECONCILIATION` — **promote** — Production reconciliation implementation plus automated tests validate the narrow single-project Claim.
- `ARCH.RUNTIME.EXCLUSIVE_RESOURCE_OWNERSHIP` — **promote** — Production supervisor behavior plus automated ownership/conflict tests validate the narrow single-project Claim.
- `OPS.PROJECT.OWNERSHIP_AWARE_LIFECYCLE` — **promote** — Production implementation, clone contracts, destructive-operation guards, and active-job safety tests validate the scoped lifecycle policy.
- `OPS.UIGS.PRODUCTION_REALIZATION_PROVENANCE` — **retain_experimental** — Three production implementations demonstrate adoption, but the provenance/currentness contract still lacks independent runtime/final-output validation.
- `OPS.UIGS.SOURCE_OWNED_UI_INVENTORY` — **retain_experimental** — Five repositories demonstrate inventory adoption, but static inventory presence alone does not validate collection/currentness semantics.
- `REL.CHECKPOINT.ROUTE_AND_INPUT_IDENTITY` — **promote** — Production checkpoint implementation plus automated invalidation/reuse tests validate the scoped Claim.
- `REL.CI.HEAD_COVERAGE_AWARE_REPORTING` — **promote** — Two independent path-filtered production CI configurations plus Foundry reporting implementation validate the scoped reporting invariant.
- `TEST.UIGS.ANDROID.DETERMINISTIC_COMPOSITOR_CAPTURE` — **promote** — Implemented instrumentation harness plus successful production capture and observed failure evidence validate the test pattern within its declared boundary.
- `UIGS.COMPOSITION.PREVIEW_INSPECTOR_SPLIT` — **retain_experimental** — One product has implementation and UI contract tests; independent realization or discriminating UX/visual validation is still missing.
- `UIGS.INSPECTOR.PROGRESSIVE_CONTROL_DISCLOSURE` — **retain_experimental** — Executable evidence is concentrated in one product; the second-project evidence is currently supporting audit material.
- `UIGS.NAVIGATION.CAPABILITY_CATALOG` — **promote** — Implemented refactor plus regression contract validate the narrowly scoped catalog identity/navigation Claim.
- `UIGS.WORKSPACE.EXPLICIT_TOOL_BINDING` — **retain_experimental** — The recorded implementation still has an open remainder and only one implementation lineage.

## Boundary

This review does not promote the five retained Claims, does not widen any Claim scope, and does not treat multiple files from one implementation lineage as independent confirmations.
