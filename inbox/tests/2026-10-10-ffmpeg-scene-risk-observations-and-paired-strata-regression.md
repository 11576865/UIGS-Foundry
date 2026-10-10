# Test: Scene-risk selection must use decoded evidence and paired temporal strata

Status: test (integration CI pending)
Date: 2026-10-10
Domains: media-processing, calibration, test-design, evidence-provenance, adaptive-decision
Related Candidate: inbox/candidates/2026-10-03-calibration-must-optimize-information-gain-per-unit-time.md
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/80

## Purpose

Guard against a false sense of scene-aware quality optimization: selecting "risky" scenes from made-up or misparsed metadata is not evidence that a native decoder distinguishes risk regimes. Unit-test-only synthetic quality values are insufficient to establish real FFmpeg filter operation.

## Fixture and procedure

Generate one reproducible 12-second H.264 file containing three four-second regimes in known temporal order:

1. dark/static black frames;
2. moving testsrc2 content;
3. temporally varying noise/grain over gray.

Probe six predetermined short temporal windows (two seconds each) with real FFmpeg decoding and the production low-cost filter chain:
`fps=2,scale=160:90:flags=bilinear,format=yuv420p,signalstats,scdet=threshold=10,metadata=print:file=risk.stats`.

Use per-probe isolated working directories so metadata files cannot be mistaken for evidence from previous requests. Parse numeric `lavfi.signalstats.YAVG`, `YDIF`, `YLOW`, `YHIGH`, and optional `lavfi.scd.score` without interpreting blanks or boolean values as numbers.

Send these real decoded scene signals into the shared pure scene selection function.

## Expected outcomes

- Entirely static black frames have near-zero temporal difference.
- Motion and dynamically noisy sections generate nonzero frame-difference evidence.
- Black frames have appreciably lower mean luma than moving test patterns.
- The planner selects stable, deterministic paired windows across three temporal strata and includes a motion-class window.
- When no probe evidence is provided, the planner reports `riskAware=false`, not a fabricated confidence score.
- The smoke uses timeout-limited FFmpeg commands and temporary fixtures, with cleanup.

## Boundary conditions

A probe starting shortly before the 4-second scene cut can overlap the motion regime. A "static" assertion must therefore select only a window wholly within the known static interval; otherwise the test would incorrectly treat a boundary-crossing mixed window as a pure static fixture.

This test validates decoded signal plumbing and risk-informed window planning on synthetic content. It does **not** validate real GPU, ASS rendering correctness on complex typesetting, long videos, compression recommendation optimality, full-quality SSIM, probabilistic confidence bounds or heterogeneous real-media acceptance.

## Evidence status

The equivalent local FFmpeg fixture and Node assertion were executed successfully on 2026-10-10. The repository version was submitted in QHE PR #80 with a Windows Actions check; CI result and merge are pending at intake.

No Canonical promotion.


## CI completion and mainline status (2026-10-10)

QHE PR #80 passed the Windows CI job, including the exact named step `Decode real dark, motion and temporal-noise risk fixtures`, as well as existing Windows acceptance steps; UIGS Evidence Coverage passed. PR #80 was squash-merged into `main` as `bec45f9795a4ca6a1470f79abee34ff36ee1fb27`.

This confirms execution of the synthetic decoded-content smoke on the GitHub Windows runner, not on the user's actual GPU, full-length media or complex ASS production corpus. The test remains a regression fixture, not evidence that scene-risk features are perceptually calibrated.

Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/80

No Canonical promotion.
