# Candidate: Media format support is a compatibility relation, not a Cartesian product of individually supported formats

Status: candidate
Date: 2026-10-02
Domains: media-processing, compatibility-modeling, product-semantics, evidence-modeling

## Summary

A media tool may correctly claim support for several video, audio, subtitle and font formats while still being unable to execute every possible combination of those individually supported resources.

Therefore “supported formats” should not be modeled as independent allowlists whose Cartesian product is implicitly valid. The executable capability is a relation across the actual resources, target container, processing policy and playback target.

A representative relation is:

`Compatibility(video streams, audio streams, subtitle streams, font attachments, target container, processing policy, playback profile)`

## Candidate rule

For media-processing products that combine heterogeneous resources:

- identify the actual container / stream codecs before compatibility resolution; filename extensions are hints rather than authoritative media identity;
- model compatibility compositionally across resource relationships instead of treating per-format support lists as equivalent to supported combinations;
- distinguish at least:
  - container / mux legality;
  - codec Stream Copy policy;
  - required explicit transformations;
  - semantic relevance between resources (for example fonts and ASS/SSA);
  - target playback / renderer compatibility;
  - evidence confidence;
- surface a finite, explicit decision vocabulary such as:
  - `DIRECT_COPY`;
  - `COMPATIBILITY_WARNING`;
  - `CONVERSION_REQUIRED`;
  - `UNSUPPORTED`;
  - `UNVERIFIED`;
- unknown combinations should remain `UNVERIFIED` when a real executor can safely provide stronger evidence, rather than being guessed as supported or automatically rejected;
- never silently transcode or otherwise change user intent to “repair” an incompatible combination;
- if a transformation is built into the workflow, expose its exact scope (for example WebVTT → SubRip on one subtitle stream while video/audio remain Stream Copy);
- do not treat container-level mux success as proof of playback compatibility in an unspecified player or renderer;
- record rule-level compatibility and actual execution / audit evidence separately.

## Evidence

In `11576865/MKV-Fast-Muxer`, PR #55 introduces a compositional compatibility resolver after actual media probing and before the real FFmpeg mux.

Observed cases include:

- H.264 + AAC/FLAC + ASS + font can resolve as a direct-copy plan;
- WebVTT requires an explicit subtitle-only conversion to SubRip while video/audio remain Stream Copy;
- unknown video/audio codecs remain `UNVERIFIED` and are delegated to the actual FFmpeg mux rather than silently transcoded;
- a font attachment alongside only SRT / WebVTT / PGS / VobSub is not treated as a rendering dependency;
- target-player compatibility remains explicitly unverified unless a playback profile is evaluated separately.

The mux report records both compatibility-rule output and actual mux/audit evidence.

## Relationship to existing Candidate

This extends, rather than duplicates, `2026-10-02-generalized-media-workspace-legacy-output-assumptions.md`.

That Candidate concerns a single-purpose media product evolving into multiple operation modes and recommends a compatibility matrix when historical output assumptions become independent product dimensions.

This Candidate concerns a different abstraction boundary: even inside one operation and one fixed target container, individually supported heterogeneous resources do not imply arbitrary cross-product compatibility. It defines the compatibility relation, evidence states and separation of mux compatibility from playback compatibility.

It also complements `2026-10-02-filename-extension-vs-content-probe-media-ingestion-bug.md`: actual media identity is a prerequisite for compatibility resolution, but identity and compatibility are separate responsibilities.

## Scope

Applicable to muxers, transcoders, NLE/export pipelines, subtitle tooling, media ingest systems, asset packagers and other workflows that combine independently selectable media resources.

This is a Candidate only. It is not Canonical.
