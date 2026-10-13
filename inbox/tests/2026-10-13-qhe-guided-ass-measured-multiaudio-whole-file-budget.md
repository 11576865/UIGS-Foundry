# Test: QHE Guided ASS measured dual-audio whole-file budget and dependent UI refresh

Date: 2026-10-13
Status: PASS on first hosted Linux FFmpeg integration; latest UI-invalidation continuation exact-head CI Pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder, draft PR #105
Evidence type: Short CI-generated real-media FFmpeg execution plus separate production DOM event fixture

## Real media scenario
QHE `src/guided-whole-file-budget.integration.test.mjs`, added at `5a48fba2e69fc8c3bed57677c615494d42667dd8` and registered in frontend CI at `463c91c2e2b687b3ab05bcd6fdf697388b63f8ad`, actually generates a short Matroska source with x264 video, two independent AAC audio tracks, a soft SRT subtitle and a file attachment. It independently measures both AAC track packet-byte totals using ffprobe.

It checks that Guided ASS full-container admission without measured copy cost is `unknown`, rejects a one-track-incomplete ledger, and that complete evidence gives exactly the same video bitrate, fixed payload and reserve bytes as `compileTask`. The production task is executed by real FFmpeg with a burn-in ASS filter. It then checks one video/two copied audio/no soft subtitles/no attachments, copied audio packet payload byte totals, full decode, visible difference relative to a plain output, and actual whole-container bytes. A strict delivery report rejects a limit one byte below the actual output and admits a limit exactly equal to it. This is a deliberate controlled gate check, **not a guarantee that the encoder naturally meets arbitrary target size**.

The frontend run `38422475740` completed its real `FFMPEG_INTEGRATION=1` suite step with success and later returned overall SUCCESS. This is short synthetic Linux FFmpeg source/output, not Windows Native bridge, hardware deployment, real-user film, MKV external-player or long-form acceptance.

## Cross-view dependent UI budget change
QHE `0a4f08ab58a50af65f9435fb892fd5d6364e137e` wires audio strategy, selected track, range, bitrate, channels, sample-rate, audioPlan and config restore to Guided projection refresh. Source-text regression `src/guided-budget-ui-wiring.test.mjs` and real Chromium production-workspace DOM fixture `scripts/check-whole-budget-ui.cjs` (continuation through `ee9ab6619b089f1c40c5868d1edea2d4562a6647`) assert those notification triggers and no encode side effects. Latest exact-head browser run pending at initial record; its result must be appended when confirmed.

## Provenance / dedup
Distinct from `inbox/tests/2026-10-13-qhe-full-formal-v4-hevc-flac-output-and-independent-ssim.md`, which independently tests the Windows Native HEVC + FLAC formal bitrate task and real full duration SSIM. Distinct from `inbox/bugs/2026-10-13-qhe-guided-size-frontier-not-refreshed-after-measured-cost.md`, which owns the cross-view invalidation defect. This Test captures actual two-AAC Guided ASS container budget arithmetic and the validation gates, not a new architecture rule.

Open: Windows Native loaded-source measured packet provenance, trim-precise copy payload, FLAC re-encode estimation, Android/Web cost measurement, source-referenced SSIM for the burned ASS output, physical workstation/long movie/media-player acceptance. No Canonical promotion, PR merge, release or full initial-version claim.

## Later exact-code frontend check

The QHE source commit `ee9ab6619b089f1c40c5868d1edea2d4562a6647` has a completed **SUCCESS** frontend workflow `38423311878`: its suite includes the real Linux FFmpeg Guided ASS copied two-AAC budget regression and the production Chromium budget audio-mutability/config-restore/no-encode DOM check. Seven of nine total platform workflows had succeeded as of the latest check; Android emulator and Windows required VVC acceptance were still running. Do not upgrade this Test to physical-device or whole-product acceptance.
