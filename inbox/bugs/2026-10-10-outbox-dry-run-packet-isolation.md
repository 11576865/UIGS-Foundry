# Bug: Outbox dry-run writes Pending and single-packet failure blocks siblings

Date: 2026-10-10
Status: Bug
Lifecycle: repair-evidenced
Scope: UIGS-Foundry / durable intake / collector safety

## Confirmed source behavior

At Foundry main `afb6dd51c88e6152934c4a2e1da70a5d8551f2ad`, `collect(..., dry_run=True)` still
called `apply_packet()` which directly wrote Pending files before the
dry-run check. The source-level exception handler surrounded a complete
packet loop, so one malformed record aborted subsequent records from that
repository. Known Receipt keys were skipped without checking Pending
storage integrity.

## Submitted correction

- Dry-run only mutates the in-memory Receipt simulation.
- A malformed packet produces a path-scoped error and does not block siblings.
- A missing/mismatched persisted Pending payload is not accepted as collected.
- Identical interrupted Pending snapshots can be safely adopted on replay;
  conflicting snapshots cannot be overwritten.
- JSON snapshots are replaced atomically; regression tests cover the boundaries.

## Evidence and promotion limits

Code review against the indicated main SHA establishes the initial behavior.
Test execution and external CI for the repair are distinct; no device or
cross-project validation is inferred. This record is a Bug, not Canonical.
