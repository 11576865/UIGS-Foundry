# Candidate: Measurement evidence identity must be separated from decision and budget projections

Status: Candidate
Date: 2026-10-10
Domain: compression calibration, evidence lifecycle, local invalidation
Source: 11576865/Quick-Automatic-Hardsub-Encoder main `2eeaab388851008a72c653aaf9f0f14560262b76`
Evidence level: code inspection; no runtime reproduction or correction in this intake

## Observation

In `src/transcode-calibration-panel.js`, `calibrationKey(raw, media)` includes `targetControl.value`, `profileControl.value`, `raw.audio`, `raw.audioBitrate`, `raw.audioTrack` and `raw.audioRange`; `invalidate()` clears `points`, `frontier`, and `sourceKey`. The target input has `input` and `change` listeners triggering this invalidation.

The actual per-sample native video measurement `hooks.calibrationSample({ codec, encoder, preset, multipass, quality, start, duration })` does not include target SSIM or audio selection. Editing a target threshold changes the search/acceptance decision, but not the SSIM/bitrate previously measured for unchanged encoded clips. Editing audio budget changes the total-size projection, not the video-only measured CQ/CRF curve, subject to any execution-contract dependency not yet shown.

The current single key therefore conflates *measurement dependency*, *search run identity*, and *budget/decision projection identity*. Strict stale-task fencing is necessary, but discarding valid costly observations is stronger than required by that safety invariant.

## Candidate rule

Separate at least:
1. `measurementKey`: actual source, reference, encoder and sample-execution dependencies;
2. `searchRunKey`: thresholds, strategy, sample position set, run generation and cancellation;
3. `budgetProjectionKey`: output duration, audio policy, reserve and target-size interpretation.

A threshold change should invalidate pass/fail, optimum/search continuation and current task publication as appropriate, without necessarily deleting validated observations; audio budget changes should recompute the derived size projection while retaining compatible video measurements. A sample-position profile change may legitimately require new measurements, but independent unchanged sample observations should retain provenance.

## Verification required

- In a deterministic UI regression, calibrate two or more CQ settings and change only target SSIM: old raw measurements should remain available; target status and search should update or request additional testing.
- Change only audio strategy and recalculate budget/size while preserving valid video samples.
- Change true encoder/source/filters and reject incompatible reuse.
- Cancel an in-flight run after threshold changes without publishing obsolete decisions.
- Measure avoided native sample cost.

## Relationship / deduplication

Not a duplicate of `2026-10-03-persisted-derived-evidence-must-carry-all-input-dependencies.md` (that candidate handles unsafe under-keying of measured dependencies). This observation is the complementary risk of *over-keying* on decision-only inputs. Related existing `2026-10-03-calibration-must-optimize-information-gain-per-unit-time.md` and `2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md` already cover cost and scope; no duplicate created for those.

No Canonical promotion, source modification or device acceptance is claimed.

## Implementation follow-up (PR #73; CI pending)

QHE commit `a98d291ad53e12e9dad557595214bead555d17b7` introduces `measurementKey` (video/sample identity including profile) separately from `calibrationKey` (in-flight search identity including SSIM target and audio). After a completed calibration, target or audio-budget edits re-evaluate point pass/fail and budget projections using retained measurement points; source/encoder/profile changes still clear evidence. During an in-flight calibration, changes conservatively abort the run instead of reusing partially confirmed observations. Browser lifecycle regression has assertions for no new sample calls after these completed changes.

Source PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/73. **Status: implemented in open PR, latest-head CI pending; not merged or device-verified.** The candidate rule remains provisional and was not automatically promoted to Canonical.


## QHE whole-file decision projection — PR #105, 2026-10-13

The current Manual multi-candidate path now projects the same video-only CQ evidence into a complete-file budget axis using the authoritative per-stream ledger: fixed copied audio/subtitle/attachments, encoded audio by each stream's duration, and ceil-rounded percentage container reserve. Unknown copied payload and FLAC re-encode cost remain errors; they are not substituted with zero. Default comparison coordinate is whole-file target; explicit video-only coordinate remains diagnostic. Switching coordinates retains CQ samples and revokes VBR/adoption status. Native budget snapshot and current settings must still match during VBR and adoption.

The proposed `whole-file-frontier.js` projection derives the exact integer video bitrate from the same byte ledger as `compileTask`; out-of-domain or infeasible targets do not extrapolate or silently switch to a midpoint. Explicit confirmed adoption atomically writes target size, MB unit, reserve, size mode and the original delivery policy. Compiler/rate divergence rolls back. Video-only diagnostic mode cannot silently clear a strict ceiling. This preserves the distinction between video measurements, derived budget coordinates, verified short-sample VBR and actual output-byte gates.

Local: 242 tests pass/9 conditional skips; seven real FFmpeg regressions and build pass. Four projection tests observed missing-module RED then GREEN; two size-adoption tests observed incorrect mode/mismatch acceptance RED then GREEN. Added browser scenarios for nonzero copied payload/attachment, missing-cost rejection, coordinate switch without new samples and strict-size adoption. Hosted browser/native outcomes Pending. This does not close Guided/single-branch budget integration, exact trimmed payloads, FLAC/cross-platform measurement or full-report initial-version acceptance. Existing Candidate only, no Canonical promotion.
