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
