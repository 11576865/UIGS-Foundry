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


## QHE legacy PR #65 / #66 semantic replay — 2026-10-11

QHE had two open, stale contributions dating from 2026-10-06:

- [#65](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/65): browser Stream Plan v4 UI-to-execution E2E test, old head `a63c7b32921b13e7cb33fce01aef8defe7bbe547`, old Frontend CI **failed** at a later snap-to-keyframe assertion (`check-media-ui.cjs:345`); this failure is not a rejection of its multi-stream test intent. Its exact multi-video and independent audio/video time-policy assertions were transplanted into the current main source tree, and a semantic two-parent integration commit `c89492c2f62b84b7d1acd50981ed28d1d53588c8` was pushed to the original PR branch. **New CI pending**; not merged.
- [#66](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/66): standalone product-side `AGENTS.md` UIGS execution protocol. Current QHE main had no `AGENTS.md`; original protocol text alone was replayed on current main in two-parent commit `06653c8d1f897179bb12294f786a9073465898e8`. **Review/CI pending**; not merged.

Both reconciliations use the latest authoritative main tree as the base, retain old head ancestry for auditable provenance, and avoid overwriting unrelated later product changes. Pending validation is distinct from a finished cleanup; neither old PR should be closed or declared implemented until integrated CI and review are acceptable.

Separately, QHE [#90](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/90) passed four workflow checks and merged as `c1c7872016dbee4d0c199522a5ab7bfcf77d4665`; [#91](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/91) required replay atop that new main to preserve its UI progress recovery and #90 integrity work. #91 new head `7d3121958c1f693ce3c43227743bcf6b6b6be60f` remains **Pending integrated-head CI**; its prior `402a095e` workflow suite had passed.

This is Candidate-level supporting evidence, **not** Canonical promotion.


## QHE legacy cleanup acceptance update — 2026-10-11

- QHE [PR #91](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/91), semantic refresh-progress recovery head `7d3121958c1f693ce3c43227743bcf6b6b6be60f`, passed all three integrated Frontend, Windows local smoke and UIGS checks; **merged** into main at `8508545cc0c35408dbfb53a520e04c11001e2825`.
- QHE [PR #66](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/66) added only the standalone product-side `AGENTS.md`; after file-delta review it was **merged** into main at `5ea28881b5bb8d3aa16d0726c9d57d7867a11e21`. This is a repository protocol addition, not real-world media acceptance.
- QHE [PR #65](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/65) reconciled head `c89492c2f62b84b7d1acd50981ed28d1d53588c8` **failed** Playwright after the new test leaked `end=0:03` into an unrelated keyframe-snap test that needed to place IN at 8:00. `media-workspace.js` legitimately clamps the requested IN to the current OUT. This failure was not proof of a production keyframe defect. Branch repair now resets the form and mock-media fixture after its new multi-stream assertion, retaining the current main changes as a semantic merge. New #65 head `490221e3fba947e64ebd5bbf80207308172a4692`, based on main `5ea28881b5bb8d3aa16d0726c9d57d7867a11e21`; Frontend CI run `38117809648` **queued / Pending** when submitted. Do **not** claim this stale PR cleanup is complete or merge it before successful new CI.

This adds a reusable failure mode: a new browser E2E case can alter persistent UI state and make a later unrelated assertion fail despite correct production clamping. Restore scenario state before handing control back to a shared fixture. Candidate only, not Canonical.


## QHE final #65 cleanup / draft PR merge boundary

The legacy QHE [PR #65](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/65) ultimately reached a passed, source-verified Frontend/Playwright test head `f7d9ef96834e757b909cb037a94912aa77826591` (workflow `38118095158`). The last test-only generation ran original shared browser tests before the independent multi-video E2E, eliminating the persistent-form/workspace interference without modifying production. The PR was additionally **Draft** and could not be merged via REST (HTTP 405), so it was promoted to **Ready for review**, rechecked for head and mergeability and merged as `2260227d0c2b1d191833e38f59af9900fca22391`.

At merge verification, QHE main was `2260227d0c2b1d191833e38f59af9900fca22391` and the open PR list was empty. Earlier Pending entries are superseded by this evidence for PR #65. 48 repository branches remain, but branch name or PR closure alone is insufficient justification for deleting their refs. Functionally distinct open issues #76, #77 and #85 remain.

Reusable insights: semantic replay onto authoritative main must preserve proven behavior, shared Playwright fixtures should isolate scenario lifetimes, and a verified Draft PR still needs an explicit Ready transition before merge. **Candidate**, no Canonical promotion.


## QHE historical branch retention audit after PR closure

After QHE main became `2260227d0c2b1d191833e38f59af9900fca22391`, the REST open-PR list was empty; an earlier branch listing had shown 48 total refs, but a later branch comparison returned 404 for the just-merged `test/stream-plan-v4-ui-to-task` ref, consistent with a post-merge deletion (the complete current branch count was **not re-verified**).

Eight named refs were selected for a bounded ancestry spot-check. Seven returned `diverged` (both main-ahead and branch-only commits): `fix/strict-budget-export-reverification` (26 main ahead, 2 branch unique), `feat/stream-plan-v4` (94/9), `feat/windows-bink2-import-adapter` (155/30), `feat/windows-bink2-import-adapter-v3` (91/5), `test/android-stream-plan-v4-emulator-acceptance` (91/5), `feat/budgeted-paired-refinement` (33/9), and `uigs-outbox` (380/191). The eighth was not found after merge.

These counts **do not prove** unmerged feature content: semantic merges can incorporate behavior without making older branch commits ancestors of main. They do show that blanket branch deletion is unjustified. Repository branch deletion is not available through the presently exposed GitHub mutation actions. **Remaining branch-reference audit and any explicit deletion are Pending**, not claimed completed. Keep product branch retention separate from CI-green PR closure and preserve traceability of divergent unreviewed work. No Canonical promotion.
