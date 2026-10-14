# Test — isolated pre-encode FFmpeg auxiliary remux is observable cost, not authoritative mixed-task budget

Date: 2026-10-14
Project: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact HEAD: `c5aae53490c23df4b8c38bf609f7a3a6b81aed0f`
Status: code submitted; exact-head Node and actual Windows Native/FFmpeg acceptance Pending
Requirement: B16 partial, not complete theoretical V1

## Distinct engineering insight

Prior B16 `inbox/tests/2026-10-14-qhe-b16-trimmed-copy-post-output-packet-cost-audit.md` covers **post-output** packet observation. This test is distinct: it validates a separate **pre-encode** isolated remux measuring selected copied audio/soft-subtitle packets before spending video encoding cost.

A preview created with `ffmpeg -ss start -t duration -i original -map 0:a:n -map 0:s:m -c copy -f container` is useful observed evidence but still lacks the original task's video+other streams and interleaving. Output packet selection and timestamp rebasing can vary with final mixed remux, codec, container and seek boundaries. Therefore **do not replace the complete full-source conservative packet reserve with the isolated observation**, even when the same source and requested trim timestamps are used.

## Executable test boundary
1. A bounded Windows PowerShell worker independently remuxes selected auxiliary tracks and runs a separate FFprobe packet-byte worker on its private output; retains no intermediate full-media file after receipt; source file length and precise FILETIME ticks checked before/after.
2. Authenticated Native Bridge POST/GET endpoints launch **one active isolated preflight per selected source** in a background worker without blocking normal job-status calls. Must require the existing Windows source-budget measurement ID; reselecting a file cancels stale work. A worker receipt must match requested stream ordinals, start/end, muxer and source stat.
3. JavaScript receipt verification requires an exact source stat **with FILETIME ticks represented as strings** (JavaScript Number cannot exactly represent modern Windows FILETIME 100-nanosecond ticks), independent full-source packet ledger and nonnegative safe packet bytes. Forged stream ordinals, changed interval, changed stat, null/negative values, or claimed permission to update the conservative budget reject.
4. Result always indicates `scope:'isolated-trim-copy-observation'`, `observationOnly:true`, `canReplaceFullSourceBudget:false`; it is not a strict target byte-certificate, post-output proof or completion acceptance.
5. Windows real FFmpeg test uses two audio streams plus an ASS soft-subtitle in MKV, compares the preview to an independently invoked FFmpeg/FFprobe mux packet oracle, checks duplicate ordinal rejection, and exercises the Native localhost asynchronous endpoint against the current source measurement. These tests have been authored and wired but not yet executed on hosted Windows.

## Bounded evidence
- `windows/trim-copy-preflight.ps1`
- `windows/trim-copy-preflight-bridge.ps1` plus Native `POST/GET /api/trim-copy-preflight`
- `src/trim-copy-preflight.js`, `src/trim-copy-preflight.test.mjs`
- `scripts/check-trim-copy-preflight.ps1`, extended `scripts/check-guided-budget-native.ps1`
- `.github/workflows/windows-local-smoke.yml` and `.github/workflows/test-frontend.yml`
- Eight isolated source-equivalent JavaScript validation tests PASS; 13 static code/source/API/CI checks PASS. Exactly one workflow status read showed `Test frontend` in progress, Windows local smoke skipped due Draft; **no actual Windows runtime PASS** claimed.

## Open and no Canonical promotion
Exact **final mixed-task** copied packet selection, source trim PTS/VFR, subtitle event boundary handling, shared audio/subtitle/video input policy, possible different MP4/MKV copying, FLAC re-encode exact cost, Android/Web source metering, real long-form/physical acceptance remain unsolved. Windows file stat is noncryptographic source identity, not robust content tamper detection. The work is a Test/Observation candidate, **not** permission to change canonical policy or declare B16/theoretical initial version complete.

De-dup performed via Foundry search for `QHE B16 preencode isolated audio subtitle remux packet cost`, `trim copy packet preflight source scoped observation no budget replacement`, `FFmpeg isolated mux cannot certify final mixed stream copied bytes`, and `full-source budget conservative trim copy candidate`; existing post-output B16 Test is related but covers a different evidence stage.
