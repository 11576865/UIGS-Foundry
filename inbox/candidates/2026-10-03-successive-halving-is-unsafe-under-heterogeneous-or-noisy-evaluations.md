# Candidate: Successive Halving is unsafe under heterogeneous or noisy evaluations

Status: candidate
Date: 2026-10-03
Domains: evaluation, optimization, experimentation, media-processing
Evidence type: methodological analysis

## Summary

Successive Halving is only reliable when early low-budget evaluations are sufficiently predictive of later/full-budget performance.

It can prematurely eliminate strong candidates when:
- task instances are heterogeneous and candidates have crossing strengths;
- measurements are noisy or unstable;
- the first evaluation budget is too small;
- the objective is multi-dimensional or conditional rather than globally scalar.

## Failure modes

### Heterogeneous instances

If model A is better on one subset of instances and model B is better on another, evaluating only one sampled instance can reverse their apparent ordering.

A candidate should not be globally eliminated from evidence that only establishes local inferiority on one stratum.

### Stochastic evaluation

If repeated runs on the same candidate have nontrivial variance, a single early observation can eliminate the true best candidate.

### Crossing performance surfaces

In compression optimization, a configuration can be dominated at one bitrate or scene class but become optimal elsewhere. Elimination must therefore be conditional on region/context.

## Candidate rule

Use Successive Halving only after defining the evaluation distribution and robustness policy.

For heterogeneous/noisy tasks:

- evaluate candidates on the **same paired instances** when possible;
- stratify instances by meaningful regimes before sampling;
- require multiple observations before elimination unless deterministic dominance is proven;
- retain estimates of variance / confidence intervals;
- eliminate only when a candidate is dominated by a meaningful margin with sufficient evidence;
- preserve candidates that are locally optimal for any relevant region;
- distinguish global best-arm search from Pareto/frontier discovery;
- use adaptive allocation to spend more budget on uncertain or close comparisons rather than mechanically halving every round.

For compression decision engines:

- sample representative scene strata (motion, texture, noise, dark scenes, subtitles, etc.);
- compare all surviving encoding configurations on the same sample set;
- fit configuration-specific rate-distortion curves;
- eliminate a branch only when it is confidently dominated across the entire relevant size range, not because it lost at one sample or one bitrate.

## Relationship to existing Foundry knowledge

Related:
- `2026-10-03-target-size-mode-should-expose-a-content-aware-rate-distortion-frontier.md`
- `2026-10-03-continuous-decision-sliders-need-branch-aware-frontier-transitions.md`

## Provenance

- discussion of Successive Halving failure modes using heterogeneous translation segments and unstable repeated comparisons
- applied to compression calibration strategy for `11576865/Quick-Automatic-Hardsub-Encoder`

This is a Candidate only. It is not Canonical.
