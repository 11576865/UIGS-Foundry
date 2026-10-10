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


## QHE paired-scene reinforcement, PR #79 (2026-10-10)
The QHE Compression Decision Engine now proposes a one-step ambiguous-frontier refinement that explicitly **tests all active branches at the same added scene** and discards the *entire* batch if any branch cannot produce valid evidence. It keeps historical source/metric/sample-window fingerprints and refuses incomparable stale points. The rank leader is *not* declared robust if any lower-ranked challenger retains an observed upper quality bound that overlaps the leader's lower quality. A deterministic three-branch counterexample protects this rule. The experimental design supports conditional retention rather than eliminating candidates from one easy scene.

Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/79. Status at intake: PR open, latest-head CI pending; no real heterogeneous-scene field acceptance, no confidence intervals and no Canonical change.


### CI/merge qualification — PR #79
This paired-case example is now implemented in QHE main as `fc3e479d342ebc2bda25a49222bbbe9435c810e3` (PR #79) with Frontend, Windows and UIGS Evidence Coverage checks passing. Revision before merge addressed within-curve sample-population inconsistency by insisting that **all CRF points of every compared branch** measure the same additional window before a whole-curve refit is published. Unaffordable or incomplete evidence retains the prior curve. Synthetic ranking reversals are proven in pure regression; field content validation is pending (#76/#77). Candidate only; no Canonical change.
