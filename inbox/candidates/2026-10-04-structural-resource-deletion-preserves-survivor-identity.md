# Candidate: Structural resource deletion must remove data-plane payload and metadata-plane references while preserving survivor identity

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #106

## Observation

Deleting a track from a container is not equivalent to hiding its inventory row or deleting its TrackEntry metadata. A correct structural deletion crosses multiple representations of the same resource:

- TrackEntry / structural metadata;
- media blocks carried by the removed TrackNumber;
- Tags or other metadata references targeting the removed TrackUID;
- the identity and ordering of every surviving track.

The first Track mutation implementation in ASS Workbench exposed a reusable distinction between a metadata-only edit and a structural resource deletion.

## Candidate rule

For container/resource editors:

1. Treat **metadata update** and **structural deletion** as different mutation classes.
2. Metadata-only edits should preserve stable identity and payload when the format permits it.
3. Structural deletion must remove both:
   - the resource's structural declaration / inventory entry; and
   - the data-plane payload associated with that resource.
4. Metadata-plane references whose target identity was deleted must be removed or explicitly reconciled; do not leave known orphan references.
5. Surviving resources must keep their stable identities and relative order unless renumber/reorder is itself an explicit user mutation.
6. Post-output verification should prove:
   - deleted identity absent;
   - deleted payload absent;
   - deleted-target references absent;
   - survivor identity/order/codec unchanged;
   - requested metadata changes applied only to their intended targets.
7. A writer that internally prefers dense numbering must not silently renumber survivors unless that behavior is part of the explicit mutation contract.

## Implementation evidence

PR #106 implements this for Matroska tracks:

- Track targets prefer `TrackUID`, falling back to explicit `TrackNumber`;
- metadata edits preserve TrackNumber / TrackUID / codec / payload;
- track removal drops matching blocks and TrackEntry without renumbering survivors;
- Tags targeting removed TrackUIDs are filtered;
- removing all tracks is rejected;
- output is rescanned and compared against the planned mutation set.

The regression fixture intentionally leaves a non-contiguous surviving TrackNumber after deletion so accidental dense renumbering is observable.

## Evidence boundary

This is implementation-backed in one Matroska editor. Other container formats may use different identity/reference mechanisms, and some formats may require renumbering or index regeneration.

Do not promote to Canonical from this evidence alone.
