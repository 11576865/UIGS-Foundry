# Case — Softmux external candidates: UI capture and completed-output identity

Date: 2026-11-01
Status: Case / local real-browser and native-output evidence; full CI pending; not Canonical.
Product: 11576865/MKV-Fast-Muxer
Product delivery: https://github.com/11576865/MKV-Fast-Muxer/pull/207
Exact product head: 6dbbb06a881481d8aa959a6d1264c57e36a6c95b

## Dedupe and scope

Searched Foundry for membership/preview/candidate and stale/checkbox/capture. Related family: inbox/candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md (interaction hypothesis), and historical editor-source identity defects. This record adds implementation/reproduction evidence, not a new interaction Canonical or a claim that all proposed scenarios are complete.

## Findings

1. A resource-list include transaction can be undone by a subsequent global UI refresh if that refresh captures an older checkbox in the existing metadata editor as new user input. Project the newly committed membership into the editor BEFORE live-field capture. Use the same existing semantic owner; do not add a second authority.
2. Display-plan equality does not establish output provenance: excluding A and including B can retain identical title/language/format/dispositions while using a different exact File. Bind completed-output currency and final execution handoff to included File/sidecar/font references and authored fields, independently of preview focus. A historical artifact can remain saveable without becoming evidence for the new draft.
3. Generated save/report content can make a centered child taller than a bounded action dock, putting its first controls above the scroll origin. Actual repeated-output ordinary clicks exposed this; top alignment retained reachable overflow. A screenshot or first-run button test alone missed the failure.

## Evidence actually obtained

Initial 747 Node tests; final 757/757 Node and build pass. A real Chromium 153.0.8010.0 test of the built application imported MP4+two ASS+TTF+FLAC, excluded one ASS and FLAC, rendered the excluded ASS without including it, downloaded a real MKV and independently probed with FFprobe 6.1.1 (one subtitle, source-only audio). Reinclude yielded a second downloaded MKV with two subtitles and preserved authored title. Swapping identically authored candidate memberships made historical output evidence stale. 1440/1024/768 viewport ordinary clicks passed after the dock fix. Physical-tablet, full exact-head CI and 1.0 release are NOT proven.

Tests: tests/e2e/candidate-membership-scenario.mjs; tests/live-external-asset-authority.test.mjs; tests/portable-external-project-recovery.test.mjs; tests/portable-workspace-atomic-recovery.test.mjs; tests/container-workbench-evidence.test.mjs.

Product remains implementation authority. Single case, no automatic Canonical change.


## Follow-up: attachment-only route and mixed-mode currency (2026-11-01)

Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/208; implementation head d29d17c1eddba333d99f9ffa7a799c9179d3b14b. Previous PR #207 exact-head browser/S12/build passed and was merged at b8f4c957ee49e3ece5bd2506cdd8a030f6ecc0c9.

The next bounded unit integrates PNG/PDF into the existing normal import/Start/artifact-save workflow with the existing bounded new-container writer, including single attachments. Two independently reviewed defects extend this case's authority-boundary lesson: (1) a generic-only visible inventory did not imply actual legacy media File inputs were empty, so routing must consult both; (2) newly included generic attachments changed output intent while the unsupported media display plan lacked a generic writer entry, requiring generic membership in historical media-output currency too. Both now have direct browser negative regressions. Resource identity and route readiness are runtime facts, not inferred from one UI projection.

Local evidence: 764 Node tests/build; actual built Chromium single/two-attachment MKVs with complete payload SHA readback; real media candidate scenario with native FFprobe regression; 1440/1024/768 clickable dock and readable artifact links. Rehosting original result controls revealed inherited 38px icon-link sizing; geometry assertions prevent vertical text/overflow. New full browser CI requires native mkvmerge/mkvextract against actual downloads; this independent native proof remains Pending (not installed locally). Physical-device proof remains absent. No Canonical promotion.


## Follow-up: exact imported File source drafts across navigation (2026-11-01)

Product https://github.com/11576865/MKV-Fast-Muxer/pull/209, implementation a0f1e14bd0e298b1d4d92bd1d071f02af5753bca. PR #208's complete browser/MKVToolNix/S12/build proof passed and merged at e9f9066966cc55fc9c3f30f7f60f5454b3ed2d11.

A source-only session shelf now retains the existing validated source-domain session and executor projection under an exact File WeakMap key, revalidates before storage/retrieval and re-reads Matroska identity before reintegrating the source subset with the current external domain. It never persists File permissions, outputs or undo/approval receipts. A repeated change event retaining the same File initially erased the active draft because caching skipped unchanged source while reset still ran; independent review and a RED→GREEN real-browser test caught the mismatch. Treat event occurrence, changed File identity and intended state reset as separate facts.

Actual browser evidence: A/B distinct authored audio titles and attachment names survived switching and separate native-FFprobe-checked outputs; source SHA stayed unchanged. Importing B retained A; opening/switching did not generate outputs; removal/reimport did not inherit old draft; 1440/1024/768 source-drawer operations passed. 767 Node tests/build and existing focused media/attachment regressions passed locally. Complete exact-head CI and physical devices remain Pending. This is source-side session state, not a complete independent external recipe per target. No Canonical promotion.

## Release-attestation boundary (2026-11-01)

The same exact-identity rule applies to release evidence: a recorded Git HEAD does not prove the loaded working-tree receipts are that revision. Strict validation now rejects staged/unstaged tracked changes in both candidate and evidence checkout. Historical CI artifact IDs/digests/expiry are indexed separately from formal 1.0 PASS: a green old head cannot prove a later candidate. A read-only gate must not be described as a deployment dependency; ordinary developer deployment explicitly rejects formal major versions until a validated publication path exists. Product implementation/regressions remain authoritative in `scripts/audit-softmux-1.0-release.mjs` and `tests/release-1.0-gate.test.mjs`. Bounded Case extension only; not Canonical promotion.

## Item-level coverage reconciliation (2026-11-01)

Review of 44 legacy and 57 historical Softmux requirements exposed three false equivalences to reject: (1) recognizing/pairing graphic subtitles does not prove actual muxed PGS/VobSub output; (2) independently rendering a generated MKV from external ASS/fonts does not locate a normal-workbench path to preview ASS/fonts already inside an imported MKV; (3) rejecting writer-ineligible sources does not prove read-only inspection remains available independently. Batch jobs filtered to require subtitles likewise cannot establish pure-container batch support. Product coverageReview entries retain these distinct gaps and do not promote formal PASS. Documentation discovery is useful for selecting the next executable proof, not a replacement for it. Case only; no Canonical promotion.

## Bitmap timed-output regression (2026-11-01)

The next executable proof used authored valid PGS/SUP and DVD VobSub IDX/SUB streams with a non-zero cue start and an explicit clear/stop. The actual workbench reported successful audit and kept the subtitle bytes, but native packet PTS checking failed. Timeline preservation had been scoped to timed text; extending the existing copyts/avoid_negative_ts protection to graphic subtitles made the same real-browser test pass. A valid independent oracle must tolerate PGS SUP segment-to-Matroska display-set repacketization while preserving concatenated bytes and PTS; comparing per-packet hash lists directly would reject legitimate repacketization. Native decoded geometry/whole-frame hashes at before/during/after samples and media packet hashes supplement codec/title checks. These authored fixtures prove a bounded regression, not every graphic subtitle implementation. Product code, tests and CI artifacts remain authoritative; no Canonical promotion.
