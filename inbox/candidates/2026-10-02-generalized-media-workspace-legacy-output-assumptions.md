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

Quick-Automatic-Hardsub-Encoder currently supports three task operations in the shared compiler: `hardsub`, `transcode`, and `copy`, while command preview, native bridge, browser engine, Android native output, save dialogs and output naming remain hard-wired to Matroska/`.mkv`.

The UI already calls the area “视频处理工作区” in navigation semantics and exposes “硬字幕压制 / 纯视频转码 / 无损快速剪切”, demonstrating that the product model has generalized beyond its historical hard-sub-only origin.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- evidence level: current repository implementation + product evolution observation
- status rationale: reusable architectural lesson, not yet cross-project canonical

This is a Candidate only. It is not Canonical.
