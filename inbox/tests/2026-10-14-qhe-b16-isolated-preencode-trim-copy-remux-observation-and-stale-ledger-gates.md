# Test — bounded pre-encode auxiliary trim-copy observation is NOT final-mux cost authority

Date: 2026-10-14
Product PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `de60914ad4177c4ecc786169eff94722c7224ec2`
Requirement: B16 partial; complete theoretical initial version B01–B25 / A01–A10 remains open.
Status: code and source-level isolated tests pass; hosted Windows PowerShell/FFmpeg execution Pending.

## Distinct reusable test boundary
Existing `inbox/tests/2026-10-14-qhe-b16-trimmed-copy-post-output-packet-cost-audit.md` concerns an **already completed** muxed output, while this Test concerns the **pre-encode** independent auxiliary-only remux and its source-evidence lifecycle. An isolated remux can select different packets/PTS behavior from a real video+audio+subtitle mixed mux. Therefore its observed packet bytes must NEVER silently replace authoritative full-source copied-stream budget, certify exact final bytes or claim delivery eligibility.

## Implementation/guard requirements
- `windows/trim-copy-preflight.ps1`: private bounded FFmpeg copy-remux of specified source-relative time range and selected audio/subtitle ordinals; an independent `windows/trim-packet-audit.ps1` FFprobe worker counts actual remuxed packet payloads per selected stream. Only Matroska/MP4 supported; unsupported copy/container combinations fail unavailable rather than guessed. Source size/FILETIME stat checked before/after. Receipt writes via atomic file move.
- `windows/trim-copy-preflight-bridge.ps1`: authenticated localhost POST launch and GET status, single-flight background work, source ownership, original full-source budget `measurementId`, clip and stream mapping bounds. Source changed -> invalidate and cancel. Re-measuring the same stat-stable file with a **new full-source measurement ID** revokes even a cached `ready` receipt. Worker method, exact interval/container/ordinals, nonnegative 64-bit packet totals and source stat must match before returning `ready`. No polling blocks Native job status.
- `src/trim-copy-preflight.js`: independently checks exact claimed source length and FILETIME ticks serialized as decimal **text** (never lossy JS floating-point number), interval, stream ordinals, output format, full-source packet ledger and observation-only restrictions. Returns observed bytes and whole-source reserved bytes separately; `canReplaceFullSourceBudget:false` and `canCertifyFinalMux:false` always.
- `src/media-planning.js::sizeBudget` remains unchanged: copied trim streams retain the conservative full-source packet count; FLAC re-encode costs remain unknown.
- FFmpeg is capped at 75s per private remux; separate audio and subtitle independent FFprobe scans are each bounded. The outer worker deadline was raised to 270s to cover sequential bounded scans; it remains asynchronous and source-owned.
- `scripts/check-trim-copy-preflight.ps1` constructs actual two-audio/soft-subtitle MKV, runs isolated remux and independently scans packet sizes on another FFmpeg remux, then demands rejection for duplicate stream ordinals. The existing `scripts/check-guided-budget-native.ps1` exercises Bridge start/poll and checks measurement identity.
- `.github/workflows/test-frontend.yml` includes the new Node test in both Draft-fast and full frontend gates; `.github/workflows/windows-local-smoke.yml` parses worker and Bridge and runs real FFmpeg oracle when enabled.

## Bounded observed evidence
Nine isolated actual-source JS receipt and wiring tests passed (including stale stat/FILETIME, spoofed replacement authority, negative/overflow bytes, wrong ordinals, duplicate helper guard and source-ledger-method gate). Source/CI static checks passed. These are **not** Windows PowerShell parser or runtime/FFmpeg/browser acceptance. On exact-head PR #105 the immediate workflow read showed frontend/UIGS queued and Windows local smoke skipped under Draft gating. Thus hosted PowerShell/FFmpeg long-form remains **Pending**, with no evidence of native completion.

## Pending questions and promotion constraints
- Need compare to the *real* mixed video/audio/subtitle trim task with seek semantics, timebase/PTS, reordered/VFR packets, attachments and an actual final mux before treating input cost as exact.
- FLAC full-encode cost, Android/Web source metering, bridge crash recovery, real high-density subtitles and long clips remain open.
- This is Test/Observation evidence only. Do not promote to Canonical from a single implementation, do not mark B16 complete, and do not reinterpret a preview as an exact byte ceiling.
