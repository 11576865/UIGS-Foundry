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

## Follow-up implementation evidence — single-branch model v1

A stacked implementation PR for Quick-Automatic-Hardsub-Encoder now exercises the first Model layer on top of the evidence store:

- fit one codec/preset/resolution branch at a time;
- sort measured points by bitrate and fit in log-bitrate space;
- use weighted isotonic regression to enforce the expected non-decreasing quality-vs-bitrate shape without introducing spline overshoot;
- refuse extrapolation outside the measured bitrate domain;
- preserve lower/central/upper sample-derived evidence ranges separately from the fitted center line;
- estimate a local diminishing-return knee only when enough measured points exist;
- map video bitrate to whole-file target size using duration, audio bitrate and reserve, while preserving explicit impossible / below-evidence / within-evidence / above-evidence states.

This implementation reinforces the earlier Candidate: the decision curve should remain evidence-bounded and shape-constrained rather than presenting a decorative smooth curve as if it were measured truth.

The current implementation remains single-branch and SSIM-based. It does not yet justify Canonical promotion.


## QHE multi-codec upper-envelope checkpoint — PR #74 (2026-10-10)
QHE PR #74 introduces `createMultiBranchFrontier`: joins at least two codec-specific measured R–D models **only when their evidence scope is identical**, restricts the visual/decision size domain to the **intersection** of measured ranges, compares conservative lower-quality estimates at fixed budget, applies an incumbent hysteresis (0.003 SSIM), and requires **explicit user acceptance** of an encoder switch. The interface still presents one interactive target-size/quality curve; codec switching is not implicit.

**Limitations:** scope is current-source/current-runtime/identical-source-resolution and reference-rendering. Cross-resolution, cross-frame-rate and differently processed input references cannot be assumed quality-comparable with the present source-SSIM metric. The envelope is a measured-codec **prototype**, not the full multi-configuration optimum and not a final VBR guarantee.

Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/74. Status at checkpoint: PR open; acceptance pending; Candidate only.

## CQ/VBR evidence contract and output-error feedback — PR #74 (2026-10-10)
The user asked to implement the remainder. QHE PR #74 proposes gating adoption of a bitrate extrapolated from a CQ/CRF-measured size/quality curve on **independent, native, same-encoder/preset, same-timeline VBR short samples** with raw SSIM validation. CQ and VBR measurements must retain different measurement/decision provenance; an interpolated CQ SSIM is not an observation of VBR execution. A separate full-encode completion readout records planned target bytes, actual output bytes and percentage error. Packet/decode verification still does not establish perceptual quality on all full-length scenes.

Tests have been added for policy, UI verification, Windows sample arguments and actual software FFmpeg VBR samples. These are proposals in an open PR, not evidence of real GPU, HDR/VFR or long-video acceptance. This expands the existing target-size Candidate only; no Canonical promotion. Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/74.


## Cross-resolution common-reference implementation checkpoint (QHE PR #75)

QHE PR #74 is **merged** on main as `5d9fe3aa812c71dc32c43173b2184a69365329a1`, with Frontend, Windows, Windows Runtime, and UIGS evidence CI green. This establishes bounded calibration, same-resolution multi-codec shared-domain envelope, explicit handoff, VBR short-sample gate, and output-size prediction-error reporting.

The user explicitly requested the remaining cross-resolution stage. PR #75 (https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/75) proposes:
- A fixed `original-source-bicubic-upscale-ssim-v1` comparison contract: 720p/1080p/original output candidates rendered from the same source/subtitle input, candidate reduced resolution encoded with bicubic filtering, then upscaled to **one original-resolution subtitle-rendered reference** before scoring.
- Session-only per-resolution evidence (existing persistent CQ record identity lacks output dimensions). One compatible measured-budget upper envelope; explicit user acceptance of a recommendation changes both codec and formal output size; FFprobe verifies encoded output dimensions.
- Windows Native-only gating, FFmpeg filter smoke, CI tests and fail-closed insufficient-evidence handling.

A code-review error was found and corrected before merge: the reference candidate was initially scaled along with the candidate; the corrected path applies scaling **only** to candidate video while reference stays original resolution. Windows CI smoke needed a PowerShell 5.1 stderr-safe SSIM output fixture; that test is under revision. **PR #75 remains open until latest CI succeeds; no real GPU/crossover case/long-form acceptance.**

Additional remaining work: GitHub Issue #76 covers paired scene-complexity stratification/VOI stopping; Issue #77 is field acceptance on actual GPU/long-form source. These are not satisfied by merged CI. No Canonical promotion.

