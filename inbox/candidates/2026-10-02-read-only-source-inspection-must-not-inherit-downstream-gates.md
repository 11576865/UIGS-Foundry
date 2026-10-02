# Candidate: Read-only source inspection must not inherit downstream workflow gates

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, workflow, diagnostics
Evidence type: direct user workflow failure plus code-level root cause

## Summary

A read-only inspection capability for already-selected source material must not be disabled merely because later workflow inputs are missing.

If a system can inspect source metadata independently, that information should remain available before authoring, validation, preview, or execution prerequisites are complete.

## Evidence

In Quick-Automatic-Hardsub-Encoder, the visible “分析素材” action was gated by:

`state.video && state.ass`

even though source-video probing is technically independent from ASS parsing. On Windows / Android Native, FFprobe / Native probe already ran after video selection, but the resulting codec, resolution, frame rate, duration, bitrate, pixel format, color and audio metadata were not surfaced in the source area.

The user therefore could select a source video yet still see the analysis action disabled and could not inspect the source parameters needed to make later encoding decisions.

## Candidate rule

- Separate source inspection from downstream transformation prerequisites.
- Read-only metadata/probe actions should require only the source and the minimum runtime needed to inspect it.
- Missing subtitles, fonts, output targets, publish destinations, validation acknowledgements, or other downstream dependencies must not block source inspection unless they are technically required for that inspection.
- If a native/runtime probe is already performed automatically, publish its result into the user-facing source context instead of hiding it only in internal state or logs.
- Preserve valid source metadata when unrelated downstream inputs change; invalidate it when the source identity changes.
- Use distinct user-facing states for:
  - source selected;
  - source probe pending;
  - source metadata available;
  - downstream/preflight inputs incomplete.

## Scope

Applies to media workbenches, importers, editors, build/deploy interfaces, data pipelines, and other staged workflows where users need to understand an input before configuring later stages.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- source: direct user report and repository inspection, 2026-10-02
- code root cause: source analysis button required both video and ASS although video FFprobe did not require ASS
- implementation follow-up: PR #32 `Expose source video parameters without requiring ASS`

This is a Candidate only. It is not Canonical.
