# Bug — Derived SubRip inserted before async subtitle content identity became authoritative

Date: 2026-11-03
Status: **Bug observed and patch submitted; exact corrected browser E2E pending**
Project: `11576865/MKV-Fast-Muxer`
Product PR: [#232](https://github.com/11576865/MKV-Fast-Muxer/pull/232)
Related existing product mechanism: `src/main.js` `setAdapterFiles` → `subInput.change` → `inspectSelectedSubtitles` → `syncNewTrackState` and `newSubtitleState`.
Related existing Foundry history: `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` and `inbox/observations/2026-10-23-softmux-composition-duplicate-metadata-live-row-selection.md`; their concerns are overlapping resource authority, but not this **specific actual pending-state repro**.

## Real observed failure

Product PR #232 implements a new user-visible operation: import real A.mkv with internal SubRip track and B.mkv without subtitles, select B target; inspect A's actual subtitle stream; execute browser `-map 0:<index> -c copy -f srt` to construct a bounded operation-local File and feed it to existing ordinary subtitle workbench without downloading/reimporting.

Initial head `40c9c0bbfd37032a131d1e9475c6247b5202468c` in [Browser CI 41669244396](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41669244396) showed **source SRT was successfully extracted** but then the app displayed `来源字幕处理未完成：字幕未能进入原有字幕封装路径。`; the actual Chromium E2E timed out waiting for output member at `tests/e2e/cross-source-subrip-scenario.mjs:76`. The prior real A AttachedFile → B test passed. No corrupt output was published.

**Root cause evidenced by code:** `applyImportedAssetRoles` invokes `setAdapterFiles(subInput,...)` which dispatches `change`; `inspectSelectedSubtitles` initially sets `subtitleInspectState.status='pending'` and `syncNewTrackState` legitimately projects no ready subtitle rows. The new operation synchronously looked for its File in `newSubtitleState` and treated *pending* as *missing*, removing the candidate before identity scanning could complete. Distinguish a transition state from an authoritative absent-state.

## Patch, acceptance and generalizable test

Head `64e06c06ff5943319b722b4b9a22d021db9f4690`: await the existing canonical `subtitleInspectPromise` after `applyImportedAssetRoles()`, recheck live source File/source choice and cancellation, then find the exact File reference in `newSubtitleState`. Earlier intermediary patch `fa297906a0f192ff3a41bdf6441af691f344ec85` also rendered authoritative source title/language into editor before the next `updateUI` snapshot could overwrite it with filename-inferred fields.

The actual real-browser test must confirm derived SRT appears, source language/title are retained, real B output contains exact A SubRip packets/PTS/DTS, A/B files are unchanged, and source A removal prunes the dependent member. Failure must not permit partial output. Exact new Browser run [41670341944](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41670341944) **pending** as of this record.

This is not a justification to bypass content sniffing, assume a file extension is authoritative, or automatically grant a new writer. Correct general pattern: **attach a real File → await its actual async content identity and currentness → commit role-specific metadata through the existing domain state**; preserve error vs pending distinction. New Candidate/Bug intake only; no Canonical modification.

## Exact-head verification accepted — 2026-11-03

Corrected product head `64e06c06ff5943319b722b4b9a22d021db9f4690` passed **full** [Chromium E2E run 41670341944](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41670341944) including new A.mkv SubRip → B.mkv real browser output with source and output MKV artifacts, independent native ffprobe packet hash and PTS/DTS/track metadata checks, original source file SHA, duplicate prevention and A source removal revocation. Node tests/build, S12 scoped, and Pages build also passed. Product [PR #232](https://github.com/11576865/MKV-Fast-Muxer/pull/232) squash merged to `main@5ce85fc8d1657797809d25b51c8b51512f762406`. **Observed bug is fixed within its bounded scope**; do not extrapolate to ASS/source font closure or all delayed async identities. Retain as Bug for future regression and workflow evidence, not Canonical rule.
