# Candidate: Split divergent media operations between shared ingress and shared egress

Status: candidate
Date: 2026-10-02
Domains: product-architecture, media-processing, interface-grammar

## Summary

When one media tool grows to support operations with materially different semantics, the UI and workflow should split where the operations diverge, while preserving a shared ingress and shared egress.

For a media workspace with:
- hard-subtitle encode;
- plain transcode;
- stream-copy trim;

the operations share enough early and late lifecycle to remain one product/workspace, but not enough middle workflow to remain one linear form.

## Candidate structure

Shared ingress:
- source selection;
- probe / media inventory;
- source identity and duration;
- common stream inventory;
- optional time-range intent;
- backend/runtime capability detection.

Operation-specific branches:
- hard-subtitle encode: ASS/fonts, subtitle preflight, renderer-authoritative preview, encode plan;
- transcode: codec/encoder, rate control, geometry, frame-rate, pixel format, audio strategy;
- stream-copy trim: keyframe-boundary semantics, stream preservation, no filters/no re-encode.

Shared egress:
- output container policy and compatibility validation;
- output naming/destination;
- execution lifecycle, progress, cancel;
- post-output probe and packet validation;
- save/export;
- history/report/evidence.

Not every field must be shared simply because it appears in more than one branch. Shared ownership should follow semantic identity, not visual reuse.

## Candidate rule

When operations have incompatible invariants, branch the workflow before those invariants are expressed. Rejoin only after operation-specific transformation semantics are complete.

Prefer:
`shared ingress -> explicit operation branch -> operation-specific task plan -> shared execution/verification/export`

over:
`one large form with conditional hiding`

if conditional hiding causes one mode's assumptions, terminology, or invalid states to leak into another.

## Evidence

Quick-Automatic-Hardsub-Encoder currently supports three operations in one shared compiler: `hardsub`, `transcode`, and `copy`.

Their middle semantics differ materially:
- hard-sub requires ASS/font preparation and a libass preview path;
- transcode exposes encoder/rate/filter/pixel-format controls;
- copy forbids audio transcode and video re-encode, and its trim start is keyframe-constrained.

They still share source probing, task lifecycle, output verification and save/export infrastructure.

Implementation evidence strengthened on 2026-10-03: PR #33 (`Refactor media workflow into fork-join branches with shared output policy`) was merged to `main` at `54854594a7232fd86317e21b85abca20bfa19b4c`. The merged implementation preserves a shared source/probe ingress, exposes the three operation-specific branches, and rejoins at output-container policy, execution, verification and save/export. Frontend tests including real FFmpeg integration and Playwright UI smoke, Windows local smoke, Android media-task compilation, and the Android/Web build-and-deploy workflow all completed successfully.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #33, merged main `54854594a7232fd86317e21b85abca20bfa19b4c`
- evidence level: merged cross-platform implementation + automated regression/FFmpeg/UI smoke evidence + design analysis
- status rationale: reusable architecture candidate with one implemented product case; not yet canonical

This is a Candidate only. It is not Canonical.
