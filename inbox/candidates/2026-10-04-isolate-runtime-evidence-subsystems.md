# Candidate: Isolate runtime evidence from nonessential subsystem liveness

Status: candidate
Date: 2026-10-04
Domains: testing, visual-evidence, renderer-validation, CI

## Summary

A runtime-backed visual test should exercise the production path that supports the claim, while avoiding unrelated subsystems whose liveness is not part of that claim.

If a renderer-backed subtitle test only needs real renderer/compositor behavior, requiring a hosted emulator to decode H.264 introduces an unnecessary failure mode. Decoder stalls can prevent evidence collection even when the renderer, subtitle engine, overlay, and compositor are functioning correctly.

## Candidate rule

1. Define the exact claim each runtime evidence artifact is intended to support.
2. Keep the production components necessary for that claim in the path.
3. Replace unrelated inputs with deterministic fixtures when those inputs only provide substrate and are not themselves under test.
4. Record the resulting evidence limitation explicitly; isolating a renderer from decoder liveness must not be described as decoder coverage.
5. Maintain separate DEVICE or subsystem-specific evidence for capabilities intentionally removed from the isolated fixture.
6. When integrating feature-specific visual captures, inherit the isolated fixture instead of reintroducing the nonessential dependency.

## Evidence

ASS Workbench Android PR #94 replaced an embedded H.264 video fixture in `UigsRendererVisualCaptureInstrumentedTest` with a generated PNG still. The test continues through the production `VideoPreview` → libmpv/libass → Android compositor path and real interaction overlay, but no longer depends on hosted-emulator H.264 decoder liveness.

When PR #93 (spatial reflection fade) was synchronized after #94, its renderer-backed spatial-fade capture was explicitly adapted to the same PNG fixture rather than restoring the old video dependency.

This preserves renderer-backed evidence strength for subtitle rendering while narrowing the claim: video decoder/device behavior remains separate evidence.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PRs: #94, #93
- evidence level: concrete CI liveness failure mode + implemented isolation strategy + successful pre-merge validation on the isolation fix
- deduplication: searched UIGS-Foundry for renderer/decoder dependency isolation and runtime evidence liveness; no direct duplicate found
- status rationale: reusable testing/evidence principle; not promoted to Canonical from a single project observation

This is a Candidate only. It is not Canonical.
