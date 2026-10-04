# Candidate: Conflict-heavy stale feature branches should be replayed as semantic deltas onto current main

Date: 2026-10-04
Status: Candidate
Scope: branch integration / long-lived PRs / conflict recovery

## Observation

A long-lived feature PR for a Windows Bink 2 input adapter became non-mergeable after main accumulated substantial unrelated work in the same files: compression history, timeline waveform/keyframe handling, output verification, and Bridge diagnostics.

Resolving this by copying the stale branch versions of conflicted files would have silently regressed newer main behavior.

## Candidate principle

When a stale feature branch overlaps heavily with a substantially evolved main branch, prefer:

1. create a fresh branch from the current main;
2. identify the feature's semantic delta, not merely its old file snapshots;
3. replay non-conflicting hunks mechanically where context still matches;
4. manually integrate conflicting hunks against the current architecture;
5. assert that both the feature contracts and newer main contracts remain present;
6. open a replacement PR and mark the stale PR as superseded.

The unit of preservation is behavior/contract, not historical file content.

## Why this matters

Textual conflict resolution can produce a syntactically valid branch that deletes or weakens newer capabilities. A semantic replay makes the default direction explicit: current main is authoritative; the older branch contributes only the intended feature delta.

## Evidence boundary

This is derived from one concrete cross-cutting rebase/integration case. It should remain Candidate rather than Canonical until repeated across additional repositories or features.


## Additional independent evidence — ASS Workbench MKV stack

ASS Workbench Android independently reached the same integration boundary after its Matroska work accumulated through inventory, generic attachments, mutation preflight, CRUD, extraction, and metadata editing while `main` advanced through unrelated semantic-search hardening.

The consolidation did not merge the stale stack wholesale. It rebuilt the latest complete MKV surface from current `main`, reused exact historical blobs only for the 18 MKV/container-owned paths, verified the replay was one commit ahead / zero behind, and submitted replacement PR #103 while closing intermediate replay PR #101 and stale stacked PR #102.

This adds a second project/feature family to the Candidate and sharpens the rule:

- exact blob reuse is appropriate only after path ownership and newer-main overlap are checked;
- when an evolved main and stale feature both changed a file, semantic reconciliation is required;
- once a later stacked feature strictly supersedes an intermediate replay, keep one authoritative replacement PR rather than preserving parallel integration branches.

This remains Candidate evidence; it is not automatically Canonical.
