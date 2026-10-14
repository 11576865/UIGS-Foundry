# Candidate: Copy-cut keyframe hints must be source-bound and not equated with verified presentation time

Date: 2026-10-14
Status: Candidate / evidence pending exact-head Chromium and model CI
Origin: QHE R19 §06, R24 §09, B08/B09/A04; PR #105 WU-04

## Distinct reusable issue

An interface can have a valid-looking timeline from an earlier media source or another video stream, or correctly locate a nearby keyframe yet still be wrong about the actual first decoded/presented output frame. An arbitrary request IN cannot be proven frame-exact by finding a prior keyframe alone, particularly in VFR/B-frame material and with non-zero audio priming/offsets.

## Proposed boundary

- Make any pre-output predicted cut IN depend on stable source identity, selected video stream ordinal, analysis coverage/truncation and requested IN. On drift, degrade to UNKNOWN, not false continuity.
- Differentiate `unknown`, `keyframe-near-request (predicted)` and `likely-preceding-keyframe (predicted)` from independently probed **actual output PTS/DTS and packet spans**.
- Keep fast packet copy and potentially frame-accurate reencoded trimming separate, user-selected workflows; do not silently reencode and then label it lossless.
- A UI conversion to reencoded trim must be explicit, preserve requested IN/OUT, disclose fidelity cost, and require rechecking the chosen encoder and audio plan.

## Implementation-level evidence and limits

QHE draft WU-04 commit `9f812dd5226bb4da171c522916b30ec0313a387a` introduced `src/copy-cut-feasibility.js`, source/stream-bound timing in `src/media-workspace.js`, and a user-confirmed cut-mode switch. Independent model tests and a Playwright browser acceptance were submitted. An initial Playwright failure came from comparing normalized visible time text instead of semantic seconds; the verification script was fixed at `61047914b588ffbeea94c34e299d0cfe7c1d867c`. Exact-head final browser acceptance remains to be read.

This is a proposal informed by one engineering implementation and already grounded in QHE's theoretical report. It is **not** a Canonical rule, and does not assert actual VFR/B-frame packet integrity or output time-offset correctness.

Dedup rationale: existing QHE source-bound copy budget/evidence Candidates concern payload-cost provenance, not predictive keyframe UI versus decoded presentation semantics; existing QHE trim-copy Full Source Observation concerns cost reservation rather than cut fidelity and user-visible strategy choice.
