# Test — completed Native FFprobe packet receipt belongs to exact staged file and job, not merely matching payload bytes

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `7c0ddf0c53283220bcaf875cc1b0d55fdde6fab3`
Status: code pushed; precise-head Windows B16 runtime, Test frontend and UIGS coverage running at first check; real 182s fixture **Pending**.
Requirement: B16 partial, full initial version B01–B25/A01–A10 still open.

## Dedup

Existing `inbox/tests/2026-10-14-qhe-b16-completed-mixed-mux-flac-copy-packet-parity-draft-windows-accepted.md` proves one synthetic Windows case can compare pre-encode auxiliary packet bytes against an already completed mixed-media job; it checks source/ledger/track identity, but its Native completed packet JSON did not carry a separate **staged artifact identity**. This Test closes that narrower output-owner / cache invalidation boundary and adds a real asynchronous >180s worker probe. No Canonical promotion.

## New failure mode and test

A packet totals array with `scope:completed-artifact` and an application-level `verified:true` flag is not enough to distinguish a current output from another job's or a previously cached output's measurements. A short-video synchronous FFprobe result was cached without rechecking the staged file stat on later status polls. If the file was edited after auditing, an old packet report could be shown as still current.

Contract:
- Native synchronous and asynchronous post-output receipts include `artifactBytes` (actual staged file length), decimal **text** `artifactWriteTicks` (lossless Windows LastWriteTimeUtc.Ticks) and `artifactJobId` (Native job ID).
- Synchronous short-output FFprobe snapshots output stat before and after the packet scans; later status calls recheck the cached artifact and set evidence/state to `null/unavailable` on drift. Long worker checks receipt/output snapshot identity and rechecks finished-cache stat.
- The browser's `reconcileAuxiliaryMuxObservation` must require `completed.jobId===artifactJobId`, `completed.outputBytes===artifactBytes`, a valid decimal string tick, the complete compiler-defined audio and subtitle stream inventory, and the declared FLAC/copy preflight method before returning a *single completed-job* comparison.
- The resulting packet comparison still has `canReplaceFormalBudget:false`, `canCertifyFutureMux:false`. A current artifact fingerprint does not authorize future FLAC strict-size estimates; the FFprobe payload sum is also not whole-container bytes.

## Evidence and field acceptance

- `windows/native-bridge.ps1` and `src/auxiliary-mux-reconciliation.js` modified; synthetic negative JS tests reject job/byte/tick mismatch, extra/missing/reordered output tracks, fake packet source methods and unexpected subtitles.
- `scripts/check-flac-native-http-lifecycle.ps1`: real 3-second Native HTTP FLAC mixed-media encode, independently compare completed audio packets and finished staged file length/tick/Native job ID; mutate staged output and require the old packet receipt be revoked.
- `scripts/check-b16-long-async-output-identity.ps1`: real 182-second low-resolution, 1fps video with 8 kHz FLAC audio, whole Native encoding then independent **asynchronous** completed FFprobe scan; compare actual packet bytes, file stat and job, mutate output and require stale receipt invalidation. This tests real elapsed source duration but is not a meaningful performance benchmark for complex video.
- `.github/workflows/windows-b16-runtime.yml` runs both under Draft and includes PowerShell v5.1 syntax + JS tests. At immediate exact-head run lookup, `Windows B16 runtime acceptance`, `Test frontend` and `UIGS Evidence Coverage` were **in progress**. Do NOT mark PASS until observed.
- Additional unsupported cases remain: complex VFR/PTS copy seek, >512MiB long-file worker branch, restart resilience, cryptographic output identity, browser GUI, actual mixed mux FLAC strict-budget reuse, Android/Web and complete B16 acceptance.

## Promotion

A single passing negative source case or staged artifact check is Test evidence only. It does not update Canonical and does not prove that independently encoded FLAC audio predicts a future mixed mux.
