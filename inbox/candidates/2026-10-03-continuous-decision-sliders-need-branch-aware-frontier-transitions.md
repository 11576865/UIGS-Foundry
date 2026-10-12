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



## 2026-10-12 implementation boundary: aggregated envelope is not multi-line shifting or automatic handoff

The owner asked whether QHE's “efficiency curve” has completed “multi-curve translation/shift” in the context of keeping independent pure-video-transcode and stream-copy-cut workflows.

Grounded repo state checked: QHE `main` `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`; PR #73 merged (single foreground visualization), #74 merged (same-resolution codec envelope), #75 merged (common-reference resolution envelope).

- **Guided ASS target-size:** `src/main.js` exposes "生成当前编码器曲线", "比较可用编码器", "比较当前编码器分辨率". `createMultiBranchFrontier()` compares multiple independently measured models in their common, valid byte-budget range and provides branch ID, alternatives, 0.003 SSIM incumbent hysteresis, and an explicit "采用推荐配置" action. `src/size-frontier-ui.js` and `src/curve-chart-svg.js` render **one** aggregate fitted line/band with all evidence points; per-branch dashed or "ghost" curves, visually translating multiple plotted curves as the slider moves, and automatically committing a new codec/resolution during drag are **not** implemented. The cursor moves in output-budget coordinates; the execution plan is only changed after explicit acceptance.
- `currentSizeFrontier()` prioritizes `resolutionChoices.length>=2` and otherwise uses codec branches: it does **not** form a general Cartesian-product frontier over all codec × output-resolution × preset choices.
- **Manual pure transcode:** `src/transcode-calibration-panel.js` constructs only a same-current-encoder/preset/time-range measured curve and requires same-parameter VBR short-sample verification before adopting a budgeted bitrate. It does not incorporate guided multibranch upper-envelope visualization.
- **Stream Copy cutting:** does not use a rate-distortion curve because the selected video packets are copied, not codec-reoptimized. Its correct evidence includes actual keyframe in-point, PTS/sync, packet preservation, and output integrity.

This is **not a report of a bug**. "Multi-curve shifting" is ambiguous: moving cursor along a single upper envelope, moving multiple translucent/ghost branch curves graphically, horizontal re-projection after audio or container budget changes, and seamless automatic branch handoff are four different behaviors. When discussing status, name each explicitly and avoid equating the existing aggregate envelope with a multi-curve animated visualization or fully automated plan switch.

Candidate next review: preserve one dominant decision frontier while optionally exposing branch-labeled ghost lines or crossing ranges, separately version fixed-bitrate/audio-budget projection from source encoding evidence; plan transitions remain explicit by default until the owner authorizes true automatic handoff and runtime acceptance supports it. No QHE code, Canonical, or product settings were changed in this intake.


## Engineering proposal / PR #103 (2026-10-12): evidence-bounded candidate context paths

After the user instructed continued QHE engineering, submitted **draft, unmerged** PR [QHE #103](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/103) from baseline `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38` (head at submission `5012eb9d3d11d75cb9e4e86b338c456d886f26aa`).

Implementation:
- `src/compression-decision.js`: `createMultiBranchFrontier().sampleBranchCurves(count)` returns each independently fitted candidate restricted to the intersection of already measured target-byte domains; refuses incomplete points instead of extrapolating.
- `src/size-frontier-ui.js`: plot model builds `comparisonPaths`, includes losing candidate samples in the common y-axis domain to avoid clipping, while preserving one upper envelope and one cursor.
- `src/curve-chart-svg.js` and `src/style.css`: render subtle dashed candidate lines with escaped SVG title identities **beneath one solid primary decision curve**. This is one chart, not many independent competing charts.
- `src/main.js`: user-facing legend distinguishes candidate fits vs upper envelope; documentation states manual transcode remains a separate single-branch calibration and Stream Copy cutting has no rate-distortion curve.
- Added Node test assertions in `src/compression-decision.test.mjs` for common domain, model plot validity, one primary line, fallback for single branch and HTML/SVG escaping.

Scope limitations: **not** a generic codec × resolution Cartesian-product optimization, multi-line animated translation, manual-transcode envelope merger or automatic codec/preset handoff. The PR intentionally leaves actual encoder execution, clip cutting, output semantics, and task schema v4 unchanged. The per-branch lines are model fits, not separately validated final files.

Initial GitHub workflows at PR creation: `UIGS Evidence Coverage` success; `Test frontend` and `Windows local smoke` in progress. Exact-head CI and actual measured-branch browser screenshots remain pending. Do not merge or promote to Canonical before external validation; future CI status must be checked separately.

This modifies an existing Candidate to avoid duplicated observations, not a new authoritative specification.
