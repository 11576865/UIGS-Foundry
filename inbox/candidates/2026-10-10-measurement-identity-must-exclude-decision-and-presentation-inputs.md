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


## Single-encoder full-budget adoption checkpoint — QHE PR #105

The single-encoder panel now reuses `wholeFileLedger` and `projectWholeFileFrontier` instead of a separate audio-rate-only formula. It counts full-duration encoded audio even with trimmed video, blocks unknown copied payload, retains compatible CQ samples on budget edits and fences VBR against exact target/settings/source/cost snapshot. New `commitVerifiedSizeBudget` retains the current encoder (including AV1) and atomically writes size controls/policy; it recompiles exact bitrate/ceiling and rolls back divergent or stale selections. This is a coordinate/decision integration, not new universal quality evidence.

Previous multi-candidate implementation `73c9470` now has 9/9 hosted workflows successful. This new single-encoder continuation has 245 local tests pass, nine skips, build pass; hosted browser and platform results Pending. Updated former source-text assertions to check shared ledger/adoption wiring and added a behavioral full-audio/trimmed-video ledger test; no audio duration requirement was removed. Browser lifecycle checks cover current full budget adoption and cost-snapshot mutation without form events. Guided ASS decision integration, cost coverage and full initial-version acceptance remain open. No Canonical promotion.

## QHE Guided ASS formal budget-convergence checkpoint — 2026-10-13

QHE PR #105 `fce0edaba227421e172a77f0f47845da06356a8a` adds `assessGuidedWholeFileBudget` to the source-owned Guided ASS planner. Its `currentGuidedBudgetAssessment` and `buildEncodePlan` now consume measured copied packet bytes or planned encoded-audio bytes, whole-file fixed cost, and the same ceil-rounded reserve and integer video bitrate as `compileTask`. Unmeasured or incomplete copied audio returns an unknown state and **does not produce a formal target-size plan**; the exploratory curve may still be displayed as explicitly estimated. Regression cases cover encoder-independent full-container bitrate equality (AAC, Opus, mute, measured copy), two copied audio tracks, exact minimum budget byte boundary and fail-closed missing evidence. `d517d44cd6b24e160e6c75d05460c3e748b18917` updates an obsolete source-text UI assertion to the new shared-budget invariant; exact-head frontend test/build workflow `38417854286` **PASS**. The user's requirement is the full supplied theoretical-report initial-version scope, not this bounded slice.

**Evidence boundary:** no new CQ/SSIM or full-output byte verification is implied by budget arithmetic; Native/Android and actual user-source whole-product field acceptance remain separate. This is additional evidence in the existing Candidate about keeping measurement/projection/decision identities separate, not a new Canonical rule. Pending: real loaded-media audio cost provenance across Guided/Manual and formal VBR validation; trimmed/FLAC/cross-platform cost gaps remain.
