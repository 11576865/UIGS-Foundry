# Candidate: Target-size mode should expose a content-aware rate-distortion frontier

Status: candidate
Date: 2026-10-03
Domains: media-processing, planning, interaction-design, explainability
Evidence type: implementation review plus design synthesis

## Summary

A target-size control should not behave as a blind numeric input that merely converts bytes into bitrate.

For lossy media encoding, users are deciding along a rate-distortion frontier: additional bytes buy diminishing perceptual quality, and very small budgets can cross from efficient compression into rapid quality collapse.

A useful target-size mode should make that frontier visible and content-aware.

## Evidence

Quick-Automatic-Hardsub-Encoder currently has two useful but disconnected mechanisms:

- `sizeBudget()` performs deterministic arithmetic from requested target size, duration, reserve and audio bitrate to a video bitrate budget;
- the sample workflow encodes nearby candidate settings and extrapolates sample size to full duration.

The first proves mathematical budget feasibility but says nothing about perceptual quality.
The second provides empirical evidence but does not yet fit a quality-versus-size model.

Combining them can turn target-size mode from an arbitrary number field into a decision surface.

## Candidate rule

A target-size workflow should distinguish at least three layers:

1. **Budget floor**
   - compute fixed or separately budgeted components such as audio, container overhead, attachments and reserve;
   - show where no positive video budget remains.

2. **Codec/configuration-specific rate-distortion evidence**
   - choose representative source samples;
   - encode them at multiple logarithmically spaced rate points;
   - measure a reference quality proxy such as VMAF/SSIM plus robust low-percentile quality;
   - fit a monotonic quality-versus-rate curve;
   - treat the result as an estimate, not a guarantee.

3. **Decision frontier**
   - map bitrate to full-output size;
   - show the marginal quality gain per additional byte;
   - identify the knee / diminishing-return region;
   - show the selected target on the curve;
   - verify the final full encode against both size and quality evidence.

For adaptive workflows, each representation (resolution, frame rate, codec, encoder preset) has its own rate-distortion curve. The useful global curve is the upper envelope of those curves rather than one fixed-resolution line.

## Interaction implications

The user should be able to see:

- mathematically impossible region;
- severe quality-collapse region;
- efficient compression region;
- estimated knee / recommended range;
- diminishing-return region;
- current target;
- what resolution/frame-rate/codec plan is predicted to dominate at that target.

The UI must distinguish:
- deterministic arithmetic;
- sampled/estimated quality;
- verified final output.

Do not label an empirically estimated perceptual floor as a universal “theoretical minimum”.

## Mathematical framing

For fixed duration `T`, aggregate audio rate `R_a`, estimated overhead `O`, and video rate `R_v`:

`S ≈ O + T(R_a + R_v)/8`

This gives a deterministic budget transform.

Perceptual quality is content- and encoder-dependent:

`Q = Q_c(R_v)`

for configuration `c`.

When multiple configurations are allowed, the useful frontier is:

`Q*(S) = max_c Q_c(S)`

The knee can be estimated from curvature or from the point where marginal quality gain per extra byte falls below a chosen threshold.

## Relationship to existing Foundry knowledge

Related:
- `2026-10-03-impossible-target-budgets-must-explain-the-constraining-component.md`

That Candidate concerns infeasible arithmetic budgets. This Candidate concerns empirical perceptual guidance once the budget is mathematically feasible.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- reviewed areas: `src/media-planning.js`, `src/media-task.js`, `src/media-workspace.js`
- design discussion: replacing arbitrary target-size guessing with a visible, content-aware compression efficiency curve

This is a Candidate only. It is not Canonical.
