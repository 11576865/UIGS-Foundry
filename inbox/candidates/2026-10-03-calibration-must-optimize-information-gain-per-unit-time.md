# Candidate: Calibration must optimize information gain per unit time

Status: candidate
Date: 2026-10-03
Domains: media-processing, optimization, evaluation, interaction-design
Evidence type: design synthesis

## Summary

A compression decision engine cannot optimize only the final encode. The calibration process itself has a cost-quality curve: more measurement time reduces uncertainty, but with diminishing returns.

For short or easy jobs, exhaustive calibration can cost more than the encode it is meant to improve.

## Candidate rule

Calibration should be treated as a budgeted, anytime optimization problem.

- define a calibration time budget relative to expected encode cost and job duration;
- use cheap deterministic/source-analysis signals before expensive trial encodes;
- use multi-fidelity evaluation: short clips, reduced candidate sets, coarse bitrate spacing, and progressively higher-fidelity probes only where uncertainty matters;
- measure decision uncertainty and estimated regret, not merely score variance;
- stop when expected value of additional information is lower than its time/resource cost;
- preserve a usable recommendation at every intermediate stage so calibration can be interrupted;
- reuse hardware-, codec-, source-class-, and prior-job evidence as priors, while clearly distinguishing reused priors from current-source measurements;
- allocate more calibration only to decisions that can realistically change the selected frontier;
- for very short jobs, prefer a conservative prior/default over long calibration.

## Mathematical framing

Let:
- `B` be calibration time/budget,
- `U(B)` be remaining decision uncertainty,
- `R(B)` be expected decision regret from selecting a suboptimal encoding configuration,
- `C(B)` be calibration cost.

A stopping rule should approximate:

`marginal expected reduction in R(B) <= marginal cost of more calibration`

rather than using a fixed number of probes.

## Interaction implications

Expose calibration as progressive confidence, not a blocking precondition:

```text
Instant estimate -> quick calibration -> refined frontier -> high-confidence calibration
```

For each stage show:
- elapsed calibration time;
- current confidence / uncertainty;
- whether additional testing is likely to change the recommendation;
- estimated additional time for the next refinement step.

## Relationship to existing Foundry knowledge

Related:
- `2026-10-03-target-size-mode-should-expose-a-content-aware-rate-distortion-frontier.md`
- `2026-10-03-successive-halving-is-unsafe-under-heterogeneous-or-noisy-evaluations.md`

This Candidate focuses on calibration cost and stopping policy.

## Provenance

- design discussion for `11576865/Quick-Automatic-Hardsub-Encoder`
- observed constraint: calibration itself has a diminishing-return curve and must not dominate short encode jobs

This is a Candidate only. It is not Canonical.

## QHE implementation checkpoint — PR #74 (2026-10-10)
The user explicitly directed completing the outstanding Compression Decision Engine implementation. QHE PR #74, branch `feat/compression-decision-next-stage`, implements a **cost-aware** CQ/CRF search using per-trial observed encodeSeconds; when a projected next sample exceeds a bounded soft budget, search stops and reports partial/insufficient evidence instead of extrapolating. A Windows Native FFmpeg short-sample **encoder-process timeout** was also added. Neither rule is yet a whole-process wall clock bound: reference preparation, SSIM, startup and scheduling overhead can still overrun. The strategy does **not yet measure expected regret/value of information** or select representative scene positions by visual complexity; it is a partial implementation of the Candidate, not demonstrated optimal stopping.

Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/74. CI/real hardware acceptance were pending at this checkpoint; no Canonical change.


## Source-risk paired sampling implementation evidence — QHE #78 (2026-10-10)
QHE PR #78 is merged on `main` as `eb84018d2c33344c6c69a965ec48f2c118c99bb3` after Frontend, Windows, Windows Runtime and UIGS Evidence Coverage checks all passed. The Windows Native implementation performs **bounded low-resolution decoded FFmpeg risk preflight** (signalstats luma/frame differences, scene-change scores, contrast), combining measured signals with ASS subtitle event overlap to choose paired windows across timeline strata. All competing codec and output-resolution measurements reuse the exact same window fingerprint. Missing/unsupported probes **fall back** to time-stratified windows and do not masquerade as measured risk. The preflight budget bounds FFmpeg process time only, not the entire pipeline. The new samples remain **session-only** because legacy evidence cache lacks sampling-plan identity.

This is an implemented **partial advance** of the existing Candidate, not completion of value-of-information optimization: a pure observed-band decision ambiguity function exists, but there is no integrated, budgeted, regret-aware policy for requesting extra matched samples. Actual challenging-scene comparison changes and field GPU/long-video acceptance are pending under QHE Issues #76 and #77. Reference: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/78. Candidate remains non-Canonical.


## QHE PR #79: budgeted matched-scene incremental refinement (2026-10-10)
Issue #76 follow-up: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/79 implements an actual runtime scheduling step after initial codec/resolution frontier discovery. A deterministic policy identifies unmeasured high-risk windows, checks **all** candidate observed-quality upper ranges for plausible reversal of the incumbent recommendation at the currently selected file-size target, estimates the aggregate cost of one *paired all-branch batch* from measured native sample times, and refuses it when the wall-clock allowance is insufficient. Every branch measures the same extra position on its own already-tested CRF/preset. The model updates are staged privately and only published atomically after all branches pass strict SSIM/timestamp/sample-plan-fingerprint checks and a valid common measured-size domain exists. Incomplete or stale batches preserve the prior shared frontier. One synthetic deterministic test shows A winning before the risk scene and B winning after paired difficult-scene samples.

**Scope/limits:** this is an ambiguity- and cost-guided **one-step heuristic**, not Bayesian expected-regret minimization, a statistical confidence interval, an unlimited anytime refinement loop or proof that all real high-risk scenes were found. CI status for latest PR #79 head is pending at intake; do not record it as mainline acceptance until merged. Real GPU/long-form acceptance remains tracked separately under #77. Candidate only; no Canonical promotion.
