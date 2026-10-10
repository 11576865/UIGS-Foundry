# Candidate: Diagnostic curves must not be represented as an optimized decision frontier

Status: Candidate
Date: 2026-10-10
Domain: product semantics, optimization UX, engineering evidence

## Context
A review of Quick-Automatic-Hardsub-Encoder after PRs #67–#72 found that its Windows Native manual-transcode workflow now produces real measured quality-search traces and a single-configuration rate-distortion curve. The broader user goal was a time-budgeted Compression Decision Engine that could compare competing codec/resolution branches and produce a justified recommendation at a selected target size.

These are different evidence and decision contracts:
- diagnostic exploration: what was measured for the selected configuration and sampled scenes;
- single-branch estimation: an interpolation within observed bitrate bounds;
- cross-branch decision frontier: the best supported candidate across relevant alternative configurations, with uncertainty and cost explicitly accounted for.

## Candidate rule
Do not promote a diagnostic curve or single-branch fitted line to the semantics of a globally optimal decision frontier.

A decision-facing surface should declare:
1. candidate space actually explored;
2. evidence modality (measured CQ/CRF output, inferred target-size, true final-encode verification);
3. uncovered candidate families and sample regimes;
4. sampling/calibration time already paid and remaining budget;
5. whether the selected configuration is a recommendation, a provisional local winner, or merely a user-inspected alternative;
6. rate-control-mode changes between measurement and execution, which invalidate any implication that the same quality is guaranteed.

## Evidence
- Quick-Automatic-Hardsub-Encoder PR #67: measured exploration and efficiency curves for current Windows Native encoder/preset, explicit caveat that selecting target bitrate differs from CQ measurement.
- PR #68: quick/balanced/thorough fixed sampling profiles; long-video safeguards but no value-of-information stopping rule.
- PR #69: UI differentiates measured points, fitted curves, observed dispersion, and local knee.
- PRs #70–#72: stale-evidence and chart-validity corrections.

## Verification boundary
The review is based on current-main code and PR metadata, not a field test on the user's actual machine. This is a Candidate, not a Canonical rule.

## Scope and user-intent review (2026-10-10)

The user explicitly challenged the introduction of two separately exposed “exploration” and “efficiency” charts in Quick-Automatic-Hardsub-Encoder: they had requested a target-size/quality decision curve and eventual cross-resolution/codec comparisons, not necessarily two manual-transcode diagnostic charts. Available historical discussion supports the original draggable target-size/quality decision surface and cross-branch optimization intent; it does **not** establish an explicit request for the two separately named diagnostic surfaces. Absence of a located authorization record should be reported as an evidence gap, not proof that none ever existed.

Reusable scope-review observation:
- Distinguish a user-requested *decision abstraction* from an engineering-chosen *diagnostic presentation*. The fact that search traces and single-branch measurements exist does not authorize elevating each internal representation into a prominent user workflow.
- For each new primary UI surface, retain a concrete chain: source user task or explicit approval -> decision/operation enabled -> necessary user interaction -> implementation and validation evidence. Technical usefulness, CI success, and merged PR status do not themselves establish demand.
- Investigate less intrusive realizations first: preserve accurate measured evidence and optional diagnostics, but favor concise actionable recommendations and progressive disclosure when detailed search traces are not needed for the primary task.
- Evaluate opportunity cost against unresolved higher-priority user constraints: bounded calibration time, representative sampling, and cross-configuration upper-envelope decision-making.
- Do not infer that the user's objection requests code deletion or reversal of all rate-distortion modeling. Scope disposition remains a product decision, not a completed change.

Evidence: user feedback during a 2026-10-10 project-status reassessment; recorded original October 3 user intent; QHE main `2eeaab388851008a72c653aaf9f0f14560262b76`, particularly `src/transcode-calibration-panel.js` and PRs #67–#72. This extension remains **Candidate** and does not alter any Canonical rule.

## Explicit single-curve direction and implementation (2026-10-10)

The user explicitly requested that the exploration curve be merged or removed because the compression workflow should present only one curve. The chosen implementation removes the standalone exploration plots in **both** the manual transcode panel and the guided hard-sub quality panel, while retaining actual CQ/CRF sampling, measurement provenance, and progress/target status. Manual transcode retains one interactive target-size/SSIM frontier; individually tested CQ/CRF settings and adoption controls are available in a collapsed details section under the graph.

- QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/73
- Branch: `fix/single-measured-compression-curve`
- Commit: `7b4f635d97e45422717a27d5c3c975f70ad95319`
- State at submission: PR open; CI pending; not merged; no hardware/device acceptance.
- Reusable boundary: a diagnostic search trace may remain operationally essential without occupying a primary user-facing visualization. Preserve the underlying observations and parameter-selection affordances when collapsing the diagnostic surface.
- This is one product-specific disposition and does not automatically prescribe a single curve for every application.

This is an update to the existing Candidate, not a new duplicate or Canonical promotion.

## Follow-up implementation: single curve plus evidence integrity (2026-10-10)

The user requested continued implementation. QHE PR #73 now has a second commit `a98d291ad53e12e9dad557595214bead555d17b7`: the existing single-curve design remains while completed sample measurements are reusable across decision-only threshold/audio-budget changes. Live sampling still rejects changed run identities; source/encoder/sample-profile changes remain incompatible. Pure tests, browser lifecycle regression, and documentation were extended. PR remains open; latest-head CI pending.

This concretizes the distinction between a primary decision surface and internal diagnostics; it does **not** establish a global upper envelope or measured VBR equivalence. No Canonical promotion.

## Single-curve baseline merged; next decision module pending (2026-10-10)
QHE PR #73 is **merged** into main after Frontend, Windows and UIGS evidence CI passed. Merge SHA: `7b6cddfe766a9a0f70fd67442bf14170cd9438e8`. Its single-curve interaction and strict raw calibration evidence are now the mainline baseline, not merely a proposed PR.

The next multi-codec envelope and VBR validation implementation is tracked separately at https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/74 and was **unmerged, CI/device acceptance pending** at this checkpoint. No Canonical promotion.
