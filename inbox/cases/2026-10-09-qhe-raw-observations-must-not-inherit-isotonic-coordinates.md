# Case: Raw observation markers must retain measured coordinates

Status: case
Date: 2026-10-09
Domains: data-visualization, media-processing, evidence-semantics
Evidence type: implementation review and automated regression

## Context and deduplication

Extends existing Candidates `2026-10-03-target-size-mode-should-expose-a-content-aware-rate-distortion-frontier`, `2026-10-03-persist-raw-measurement-evidence-alongside-aggregates`, and `2026-10-03-continuous-decision-sliders-need-branch-aware-frontier-transitions`. This is concrete regression evidence, not another generalized rule or a Canonical promotion.

## Failure and correction

QHE used isotonic-adjusted qualities for markers presented as measured evidence. When measured quality decreases as bitrate increases, isotonic regression pools values: markers at those fitted values erase the original discrepancy.

The correction retains observedQuality / observedLowerQuality / observedUpperQuality separately from fitted quality. The frontier exposes observed coordinates for markers, fittedQuality separately, and fitted values for interpolation. The plot domain includes both observation and fit ranges. Legends distinguish raw observations, isotonic fit, interpolated range, and scene range; scene range is not a statistical confidence interval.

## Verification and provenance

- Repository: 11576865/Quick-Automatic-Hardsub-Encoder
- PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/71
- Commit: c9d5b304552af67a4799ac2b2e10375d1cc708ce
- Regression: src/size-frontier-ui.test.mjs — observation markers retain raw quality when isotonic fitting changes it.
- Rendering checks: src/curve-chart-svg.test.mjs and scripts/check-curve-design.cjs.
- Follow-up local verification: FFMPEG_INTEGRATION=1 node --test src/*.test.mjs — 109 passed, zero skipped; npm run build and git diff --check passed.
- Local browser smoke could not launch because the current scratch environment lacks the matching Chromium binary. Standard CI rendering verification is separate and pending at intake time.

## Limits

Short sample SSIM and sample-bitrate-derived whole-duration budgets do not prove full-output visual quality or actual final size. This case does not claim device acceptance, HDR correctness, or Canonical status.
