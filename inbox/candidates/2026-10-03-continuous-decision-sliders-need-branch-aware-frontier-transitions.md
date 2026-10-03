# Candidate: Continuous decision sliders need branch-aware frontier transitions

Status: candidate
Date: 2026-10-03
Domains: interaction-design, media-processing, decision-support, visualization
Evidence type: design synthesis

## Summary

When a continuous slider represents an optimization frontier assembled from multiple competing configurations, the UI should not pretend that one smooth physical configuration underlies the entire line.

A user may drag continuously through one visible quality/size frontier while the optimizer silently hands off between branches such as 1080p AV1, 720p AV1, 1080p HEVC, or different frame-rate/preset choices.

The interaction should feel continuous, but the configuration identity changes underneath.

## Candidate rule

- model each configuration family as its own measured curve;
- construct the user-facing optimal frontier as the upper envelope of those curves;
- keep the size/quality slider continuous in decision space even when the selected configuration changes discretely;
- expose branch handoff points with subtle but inspectable labels rather than abrupt UI replacement;
- use hysteresis or a confidence margin around crossover points to prevent jitter when two branches are nearly equivalent;
- preserve the user's current decision coordinate (for example target size) when switching branches;
- animate or interpolate visual focus across a handoff, but do not interpolate invalid encoder parameters;
- show the currently dominant branch and optionally the nearby alternative with predicted quality delta;
- represent uncertainty bands around sampled curves so a statistically insignificant crossover does not trigger a false “best configuration” switch;
- if the frontier is genuinely discontinuous because of hard format constraints or invalid regions, render the gap explicitly rather than drawing a misleading continuous line.

## Interaction example

A continuous target-size slider may traverse:

```text
80–180 MB   -> 480p AV1
180–420 MB  -> 720p AV1
420–950 MB  -> 1080p AV1
>950 MB     -> 1080p HEVC/AV1 near-equivalent region
```

The thumb position remains continuous while the active execution plan changes at branch crossover points.

## Relationship to existing Foundry knowledge

Related:
- `2026-10-03-target-size-mode-should-expose-a-content-aware-rate-distortion-frontier.md`

That Candidate defines the measured rate-distortion frontier. This Candidate concerns the interaction and state semantics of traversing a frontier composed from multiple competing curves.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- design discussion: using a continuous slider on a compression decision frontier with seamless handoff between resolution/codec branches

This is a Candidate only. It is not Canonical.

## Follow-up refinement — exact crossover, hysteresis, and uncertainty are different things

A mathematically exact crossover between two continuous branches is a sharp boundary:
`Q_A(S*) = Q_B(S*)`.

Hysteresis should not be treated as proof that the boundary itself is fuzzy. It is a control/interaction policy layered on top of that boundary:

- moving upward in size may switch A -> B only at `S_up > S*`;
- moving downward may switch B -> A only at `S_down < S*`.

The interval `[S_down, S_up]` is therefore a stability band, not necessarily the full uncertainty interval.

For measured compression curves, a better default is to derive stickiness from evidence:
- remain on the current branch while the predicted quality advantage of the alternative is below a perceptual epsilon or while confidence bands overlap materially;
- switch only when the alternative's advantage is both large enough and sufficiently supported;
- report the region as “near-equivalent” rather than pretending the optimizer knows a unique winner.

This bounds the deliberate efficiency loss: the maximum regret inside the stability band can be measured as the quality delta from the instantaneous upper envelope.

## Follow-up refinement — curve continuity and branch kinks

If each candidate rate-distortion curve is continuous over a shared valid size domain, their finite upper envelope is also continuous. Branch handoffs therefore normally create a **kink** (a derivative/slope change), not a visible break.

True gaps/discontinuities arise only when:
- candidate domains do not overlap;
- a configuration becomes invalid below/above a hard constraint;
- discrete format/decoder requirements create an unreachable interval.

The visualization should preserve this distinction.

## Follow-up refinement — comparison space vs physical display

The core frontier should be measured in a canonical comparison/viewing space before any user display device is considered.

For mixed-resolution candidates:
- map every output to one fixed comparison resolution with one fixed resampler;
- compare against the same reference in that space;
- keep actual display-device assumptions out of the baseline optimizer.

A display-aware profile may be an optional later layer when the product is explicitly optimizing perceived quality for a phone, desktop monitor, or TV. It should not contaminate the default source-to-output quality model.

## Follow-up refinement — uncertainty rendering

For a continuous slider, the primary representation should remain:
- a continuous fitted curve;
- a translucent confidence/uncertainty band;
- discrete measured sample points visible as evidence;
- optional thin “ghost” curves for competing branches.

Block/cell visualizations are better suited to a secondary matrix or experiment table. They should not replace the continuous frontier when the user's primary interaction is continuous target-size selection.

## Follow-up implementation evidence — the curve itself can be the control

Quick-Automatic-Hardsub-Encoder's first single-branch target-size frontier now uses the plotted measured curve itself as a slider surface:

- horizontal pointer position maps continuously to the decision coordinate (whole-file target bytes);
- the thumb is rendered on the fitted curve rather than on a separate generic range track;
- pointer drag and keyboard slider semantics update the same target-size coordinate;
- the selected curve coordinate drives the execution bitrate budget directly, instead of being silently re-clamped by an unrelated legacy heuristic;
- the legacy source-relative multiplier remains available as an explicit fallback control rather than competing with the curve;
- when execution constraints impose a minimum video bitrate, the plotted evidence domain is clipped to the same executable domain;
- measured points remain visible as evidence, while the shaded band is currently labelled as sample dispersion rather than overstated as a statistical confidence interval.

This adds implementation support for two parts of the Candidate: preserve one continuous decision coordinate, and ensure the visualization does not claim regions that the execution layer cannot actually realize.

The implementation is still single-branch. It does not yet provide evidence for automatic branch handoff, hysteresis, or upper-envelope switching, so those parts remain Candidate-level design work.

