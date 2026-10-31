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
