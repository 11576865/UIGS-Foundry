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


## Follow-up observation — a container source need not contain video (2026-11-02)

Softmux PR #223 (https://github.com/11576865/MKV-Fast-Muxer/pull/223) applies the legacy-assumption refinement to source eligibility rather than the output-container axis. The prior single-workbench remux path required a video stream although its Matroska mapper and audit could represent audio-only output. The feature separates observed primary-media eligibility from the narrower video-only batch/preview contract; optional video mapping does not authorize an empty output.

Reusable observation: when removing a historical mandatory object, change the ingest/runtime gate, composition projection, compatibility decision and output oracle together. Require actual retained/output media, rather than mistaking a recognized container header for an executable stream set. Keep narrower consumers' contracts explicit instead of changing a shared video predicate globally. Specific intentional refusal causes must take precedence over incidental successful probe text in recent logs.

Local evidence on the submitted 0.1045 implementation: five actual Chromium zero-video outputs cover AAC/FLAC MKA retained/edited/external-only replacement, AAC M4A and Opus WebM. Independent packet payload/count checks, retained Matroska PTS/private data, ASS/font extraction and source/output SHA checks passed. Empty-audio and actual subtitle-only MKS sources refuse and external-audio selection recovers. Existing three-output video history regression passed;832 Node tests/build passed. Exact-head hosted CI pending. Named short fixtures do not establish general playback, long-media/device or complete EBML preservation.

This is an observation attached to the existing Candidate after de-duplication. It does not change Canonical.
