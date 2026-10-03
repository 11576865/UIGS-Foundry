# Candidate: Impossible target budgets must explain the constraining component

Status: candidate
Date: 2026-10-03
Domains: media-processing, planning, interaction-state, explainability
Evidence type: implementation review plus quantitative diagnosis

## Summary

When a user requests an output-size target that is mathematically infeasible under the currently selected non-video components, the product should not report only “cannot do it”.

It should decompose the budget and identify the component that already consumes or exceeds the target.

## Evidence

Quick-Automatic-Hardsub-Encoder target-size planning computes:

- target payload after reserve;
- aggregate encoded-audio bitrate across selected tracks;
- remaining video bitrate.

A target can therefore become impossible before video encoding is considered at all. For example, multiple 128 kbit/s audio tracks over a long duration can consume hundreds of megabytes, so a 30 MB whole-file target may be infeasible even with effectively zero video bitrate.

The current implementation rejects the task when the remaining video bitrate drops below 1000 bit/s, but the user-facing explanation does not yet expose the complete budget decomposition or the minimum target implied by audio + reserve.

## Candidate rule

For target-budget workflows:

- show the requested total budget;
- show reserved/overhead allowance;
- show fixed or separately budgeted components such as audio, attachments, subtitles or metadata;
- show the remaining budget for the variable component;
- when infeasible, name the first constraining component explicitly;
- calculate and show the minimum mathematically feasible target under current settings;
- offer the smallest relevant corrective actions, such as dropping audio tracks, lowering audio bitrate, disabling attachments, shortening duration or increasing the target;
- distinguish mathematical infeasibility from perceptual impracticality: a bitrate can be mathematically positive while still being useless for the requested resolution/frame rate/content.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- reviewed implementation: `src/media-planning.js` and `src/media-task.js`
- observation: a 30 MB target can be dominated by audio-track budget long before video quality is considered

This is a Candidate only. It is not Canonical.
