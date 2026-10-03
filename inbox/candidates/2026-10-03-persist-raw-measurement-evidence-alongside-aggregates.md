# Candidate: Persist raw measurement evidence alongside aggregate summaries

Status: Candidate

## Observation

Aggregate calibration metrics such as minimum SSIM, average SSIM, average bitrate, or average encode speed are useful for immediate decisions, but they discard the heterogeneity needed for later uncertainty estimation and adaptive sampling.

In Quick-Automatic-Hardsub-Encoder PR #47, quality calibration originally persisted only summary values for a CRF trial. The evidence store was extended to retain each sampled segment's position, duration, SSIM, bitrate, and elapsed time.

## Candidate rule

When a measurement is cheap enough to retain and may later support model fitting:

- persist the raw per-sample observations in addition to aggregate summaries;
- keep sample location/context so later analysis can distinguish heterogeneous regimes;
- derive averages, percentiles, confidence estimates, and risk metrics from raw evidence instead of treating one aggregate as the only ground truth;
- preserve provenance and scope so raw samples cannot be reused beyond their valid dependency set;
- avoid collecting detailed raw evidence that creates disproportionate privacy, storage, or operational cost.

## Why

A future model may need:
- variance and low-percentile quality;
- scene-specific failure detection;
- confidence bands;
- adaptive decisions about where another measurement would be most informative.

Those quantities generally cannot be reconstructed from a single mean/minimum after the raw observations have been discarded.

## Evidence

Single implementation observation from compression calibration work in PR #47. Candidate only; no Canonical change.
