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
