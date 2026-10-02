# Candidate: Green CI requires cross-boundary invariant coverage, not only per-layer tests

Status: candidate
Date: 2026-10-03
Domains: reliability, testing, cross-platform-contracts, operations

## Summary

A repository can have broad green CI while still missing regressions created at the seams between individually tested layers.

The failure mode appears when:
- one layer produces a versioned task or capability;
- another layer advertises support for that version/capability;
- a downstream parser/executor accepts a different set;
- CI exercises each layer separately or with stale fixtures.

Likewise, UI smoke can prove that a control exists and a mocked task compiles while never exercising the real backend path, large-source lifecycle, or alternate workflow presentation that owns the same setting.

## Observed case

Quick-Automatic-Hardsub-Encoder after media task schema v3 / fork-join integration showed three green-CI blind spots:

1. Windows advertised `taskSchemaVersion=3`, while `windows/media-task.ps1` accepted only v1/v2. Existing Windows smoke fixtures used v1/v2 and therefore remained green.
2. Audio strategy existed in the manual task workspace and task compiler, but guided hard-sub still hard-coded `-c:a copy`; UI smoke did not execute the guided audio choice through the real encode backend.
3. Browser probe and execution each staged the same selected large source. Unit/integration tests used small or mocked media and did not exercise the probe -> execute lifecycle with source reuse, so the user-visible “reading source” stall was not detected.

## Candidate rule

For features that cross UI, task compiler, capability advertisement, parser, executor and output verification, maintain an explicit invariant matrix.

Each critical invariant should identify:
- producer;
- advertised capability;
- consumer/parser;
- executor;
- verification/output evidence;
- current-version test fixture;
- at least one end-to-end path crossing the real boundary.

A green test for each component separately is insufficient if no test crosses the boundary where the contract is transferred.

When a schema/capability version changes, CI should fail unless the current producer version is exercised against every claimed consumer.

When a shared setting has multiple presentations (for example guided vs manual), each presentation that claims the capability needs at least one behavioral test that reaches task compilation or execution.

Large-file/runtime lifecycle risks should have dedicated lifecycle tests; tiny synthetic fixtures are not evidence that repeated staging or memory behavior is acceptable.

## Relationship to existing UIGS knowledge

This complements the existing requirement/evidence traceability candidate. That record separates implementation state from evidence coverage per requirement.

The additional rule here concerns **cross-boundary evidence topology**: evidence must cross the same interface boundary that can fail in production, rather than remaining partitioned by layer.

It also aligns with the Canonical governance rule that CI success is not equivalent to device validation.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- incident date: 2026-10-03
- related repairs: `8645d596`, `e575a5db`, `b4a6acae`, `5087c061`, `4f763585`
- evidence level: three concrete regression classes + repaired automated tests
- status rationale: reusable testing architecture candidate; not Canonical

This is a Candidate only.
