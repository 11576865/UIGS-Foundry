# Test: QHE B16 trimmed copy per-stream actual packet cost vs conservative whole-source ceiling

Date: 2026-10-14
Status: Implemented in draft QHE PR #105; hosted exact-head CI Pending
Evidence type: pure ledger report test, real Linux FFmpeg MKV integration, Windows Native local Bridge runtime regression
Primary source HEAD: `8027be06c5238f5f2e5eeebe3c3fafac7fadffb9`
Project: 11576865/Quick-Automatic-Hardsub-Encoder

## Test purpose and trust boundary

The existing QHE size compiler `src/media-planning.js::sizeBudget` deliberately counts the complete full-source copied packet bytes as a **conservative preflight upper bound** when audio/subtitle streams are trimmed. It must not scale full-source bytes by duration: input seeking, codec priming, packet boundaries, soft-subtitle overlap and remux selection make proportional forecasts unsafe.

This new B16 slice measures **what the completed, validated artifact actually contains** and compares it to that upper bound, without treating a post-encode observation as a previously certified prediction or reducing the strict target-size allocation.

## Implementation and checks

- QHE `src/trim-copy-audit.js`: fail-closed post-output audit maps source audio track ordinals, possibly mixed encoded/copied `audioPlan` output ordinals, and selected copied subtitles to separately measured completed-artifact packet totals. Requires full-source budget measurement and `scope:'completed-artifact'`; rejects partial, missing or incompatible evidence. Reports actual packet bytes, source upper bound and their difference; explicitly `canReplacePreflightBudget:false`.
- `src/media-planning.js::outputReport` now includes the optional `trimCopyAudit` for a suitable completed output. Existing `sizePlan.copiedTrimReserveBytes` is unchanged.
- `windows/native-bridge.ps1`: for small completed structured tasks with trimmed copied payloads, independently scans and caches actual staged-output audio and subtitle packet sizes using FFprobe's bounded source packet scanner, returning `outputPacketEvidence` from both initial and repeated terminal status. Audit failure is nonfatal, never a reason to waive strict whole-container output verification. Automatic synchronous auditing is bounded to at most 180 seconds of expected video and 512 MiB of staged output; long-form metering needs separate asynchronous work.
- `src/main.js` transports output evidence to `outputReport`; `src/media-workspace.js` shows the measured trim cost alongside the original full-source budget upper bound, and the exported JSON task report retains details.
- `src/trim-copy-audit.test.mjs`: audio/subtitle ordinal selection, mixed per-track encoding actions, missing/incorrect scope, unmeasured costs, actual payload exceeding source cost, no preflight promotion, and Native status wiring.
- `src/whole-file-budget.integration.test.mjs`: real Linux FFmpeg MKV with FLAC-copy audio, SRT and attachment; trimmed source and completed output packet scans independently check the audit while preserving unchanged formal reservation and exact strict output-size gate.
- `scripts/check-guided-budget-native.ps1`: actual Windows Bridge/FFmpeg shorter 2-track PCM MKV, trimmed formal size task and FFprobe independent output cost comparison; negative and positive byte gates from the existing test remain. Repeated terminal status must preserve the measured output snapshot.

## Provenance and limits

This Test is distinct from prior `inbox/tests/2026-10-13-qhe-windows-guided-ass-source-bound-copy-audio-budget.md` (untrimmed measured copy at execution) and `inbox/tests/2026-10-14-qhe-guided-native-completed-budget-recovery.md` (restored whole-file byte receipt). It is **post-output trim cost observability**, not an exact pre-encode trimmed byte predictor.

Not verified or intentionally deferred: byte-exact preflight forecasts for arbitrary trim, long-form asynchronous packet scanning, FLAC *re-encoding* cost prediction, Android/Web auxiliary packet sources, arbitrary MKV stream combinations and physical workstation acceptance. No Canonical promotion or initial-version acceptance claim.

CI was queued at this recording, so this evidence must stay **Pending** until the hosted frontend/Windows steps actually pass.

## Hosted observations (2026-10-14)

- QHE frontend run `38439057934` on `7d3b784e8394c8dcf2608d408be2bf971321690b`: the `node --test` block containing `src/trim-copy-audit.test.mjs` completed **SUCCESS**, and the `FFMPEG_INTEGRATION=1` block containing real `whole-file-budget.integration.test.mjs` also completed **SUCCESS**. The complete frontend run was still finalizing browser steps when recorded; distinguish test-step from full-run status.
- Windows local smoke `38439434090` on `451be2146de01f7ae9f78f98df911b5d3d385d58` completed **SUCCESS**, including the production `Exercise real guided Windows Native two-pass and strict byte ceiling` step. That step now runs a real structured trimmed two-track size task, independently measures its final packets against the cached Native status and source upper bound, and checks a repeated terminal read.
- Later QHE commit `8027be06c5238f5f2e5eeebe3c3fafac7fadffb9` bounds the synchronous audit to short outputs; `fb07c74b6174d309fa06243805855044b76e7677` permits audit reporting only for verified positive output bytes. Their exact-head CI is still pending at this checkpoint, so do not claim it has passed based on earlier commits.

**Acceptance classification:** B16 short-output observed copied trim cost = measured/automated tests passing for the above actual code stages, with later HEAD regression pending. B16 pre-encode exact trim cost / FLAC encode rate prediction / long-form Android and Web = still Pending.
