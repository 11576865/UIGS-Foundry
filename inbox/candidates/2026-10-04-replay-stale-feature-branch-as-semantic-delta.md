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


## Additional implementation evidence — ASS-Workbench-Android PR #129

On 2026-10-05, the ASS-Workbench-Android container/media import stack provided a stronger reconciliation case.

The stale feature line had diverged substantially from current `main`: the old integration branch carried roughly 159 commits not on main while missing roughly 126 newer main commits. The branch still contained an older generalized Track-addition model, while current main had independently strengthened the same subsystem with:

- source TrackUID pinning;
- fresh destination TrackNumber / TrackUID allocation with removed-identity reservation;
- BCP 47 and accessibility/semantic track metadata;
- track-targeted Tag retargeting;
- newer output Inventory verification;
- unrelated later workspace/UI changes.

A textual or wholesale merge would therefore have risked replacing newer invariants with an older implementation.

PR #129 was reconciled using current main as the authoritative baseline:

1. Current-main state, bridge, native TrackImport planner, ViewModel workflow, preflight, and UI files were taken as the structural baseline.
2. Only the intended semantic delta was replayed:
   - standalone ASS import;
   - SRT → deterministic ASS normalization;
   - read-only generic-media compatibility assessment;
   - executable MP3 compressed-packet stream-copy;
   - source-drift evidence and post-write packet/semantic verification.
3. The older parallel `PendingContainerTrackAdditionUi / TrackAdditionInput` model was dropped instead of merged.
4. New source adapters were expressed as extensions of current-main `ContainerTrackImportCandidateUi / PendingContainerTrackImportUi / TrackImportInput / TrackImport`.
5. Current-main TrackUID, BCP 47, accessibility metadata, Tag retargeting and fresh-identity rules remained authoritative.
6. Unrelated old-stack differences were eliminated rather than conflict-resolved file by file.

After reconciliation, the compare against current main became `behind=0` and the visible file delta contracted to the small set of files that actually implement the semantic feature. The PR returned to a mergeable state and Android CI, emulator regression, and native/fontconfig validation were triggered.

This strengthens the Candidate rule:

> When both main and the stale branch evolved the same subsystem, replay **behavioral intent and evidence contracts**, not the stale implementation shape.

A useful completion signal is not merely “merge conflicts resolved”, but:

- current main is an ancestor / the branch is no longer behind;
- unrelated file differences disappear;
- newer-main invariants remain represented in the reconciled code;
- only the semantic feature delta remains reviewable;
- the reconciled branch re-enters the normal CI boundary.

This is additional implementation evidence only. Do not promote to Canonical from this case alone.


## Final validation of the PR #129 reconciliation

The reconciliation described above subsequently reached a full external validation boundary.

Final PR #129 state before review:

- current-main compare: ahead 5, behind 0;
- mergeable: true;
- Draft converted to Ready for review;
- Android CI #1022: success;
- Android Emulator Regression #647: success;
- Fontconfig renderer native probe #915: success.

The final reviewable delta remained constrained to the container/media import implementation and tests rather than reintroducing unrelated historical branch changes.

This strengthens the Candidate with a complete execution sequence:

`diverged stale branch -> semantic replay on authoritative main -> unrelated-diff elimination -> current-main invariant preservation -> green CI across unit/native/emulator lanes -> ready-for-review boundary`.

This remains Candidate evidence, not Canonical policy.
