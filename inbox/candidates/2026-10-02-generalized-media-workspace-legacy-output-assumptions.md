# Candidate: Promote legacy fixed output assumptions when a single-purpose media tool becomes multi-operation

Status: candidate
Date: 2026-10-02
Domains: product-architecture, media-processing, interface-grammar

## Summary

When a media tool evolves from one fixed workflow into multiple operation modes, assumptions that were once valid implementation constants can become hidden product constraints.

Example evolution:
- original product: hard-subtitle encode;
- later product: hard-subtitle encode + plain transcode + stream-copy trim.

A fixed Matroska output was reasonable for the original workflow, but once the tool owns multiple media operations, output container becomes an independent product dimension rather than an implementation detail of the original mode.

## Candidate rule

When a single-purpose processing tool acquires multiple operation modes:

- audit names, task schemas, output assumptions, validation rules and save/export paths for original-mode coupling;
- promote any now-independent choice (for example output container) into explicit task semantics;
- keep operation, codec, encoder, audio strategy and container as distinct concepts;
- validate combinations with a compatibility matrix rather than silently transcoding or changing user intent;
- permit an `auto` mode that resolves to a safe container, but surface any transformation required by compatibility;
- update product copy so the enclosing workspace describes the generalized capability while individual modes retain specific names.

## Evidence

Quick-Automatic-Hardsub-Encoder supports three task operations in the shared compiler: `hardsub`, `transcode`, and `copy`. The historical fixed-Matroska assumption was subsequently removed in PR #33 and promoted into task schema v3 as an explicit output-container policy.

The merged implementation provides `Auto`, preserve-source-container, MKV and MP4 choices; resolves compatibility through a conservative matrix; carries the resolved format/extension/MIME through Web, Windows Native and Android Native; and rejects incompatible combinations rather than silently transcoding audio. Stream-copy trim in `Auto` prefers the source container when the combination is known compatible.

PR #33 was merged to `main` at `54854594a7232fd86317e21b85abca20bfa19b4c`. Frontend tests including real FFmpeg integration and Playwright UI smoke, Windows local smoke, Android media-task compilation, and the Android/Web build-and-deploy workflow completed successfully.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #33, merged main `54854594a7232fd86317e21b85abca20bfa19b4c`
- evidence level: merged cross-platform implementation + automated compatibility/regression evidence + product evolution observation
- status rationale: reusable architectural lesson with one implemented product case; not yet cross-project canonical

This is a Candidate only. It is not Canonical.
