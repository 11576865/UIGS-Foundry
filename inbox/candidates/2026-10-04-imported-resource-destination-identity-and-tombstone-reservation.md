# Candidate: Imported resources receive destination identity; deleted identities remain reserved within the transaction

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #109

## Observation

When a resource is imported from another container, the source resource already has identifiers. Reusing those identifiers in the destination creates two independent collision classes:

- the source identifier may already belong to a destination resource;
- an identifier freed by a deletion in the same transaction may appear available even though reusing it aliases the identity of the just-deleted resource in audit, undo, verification, or downstream references.

The Track import implementation therefore treats source identity as provenance, not destination identity.

## Candidate rule

For cross-container / cross-document resource import:

1. **Source identity is provenance.** Keep enough source information to describe where the resource came from, but do not assume the source identifier is valid in the destination namespace.
2. **Destination identity is allocated by the destination.** Imported resources receive fresh destination identifiers under the destination's collision rules.
3. **Transaction tombstones remain reserved.** Identities of resources deleted earlier in the same mutation plan are not recycled by resources added in that same transaction.
4. **Survivors keep identity.** Addition must not renumber or retarget unrelated existing resources unless reindexing is itself an explicit mutation.
5. **Verification checks non-aliasing.** Post-output verification should prove imported identity is unique and does not equal any pre-transaction destination identity, including identities of resources removed by the transaction.
6. The user-visible plan may show source identity for provenance, while the actual destination identity can remain pending until materialization if allocation occurs at write time.

## Implementation evidence

PR #109 applies this to Matroska Track import:

- source TrackNumber / TrackUID identify the selected source Track only;
- destination TrackNumber / TrackUID are allocated fresh;
- allocation reserves all original destination TrackNumber / TrackUID values, including tracks deleted in the same write plan;
- survivors retain their original TrackNumber / TrackUID and order;
- output verification rejects imported identity reuse.

## Evidence boundary

This is implementation-backed in one container editor. Other domains may use UUIDs, database keys, graph node IDs, file handles, or composite identities rather than integer Track identifiers.

Do not promote to Canonical from this evidence alone.
