# Candidate: External input adapters must separate source identity from execution staging

Status: candidate
Date: 2026-10-03
Domains: media-processing, workflow, reliability, product-semantics
Evidence type: implementation design plus compatibility boundary

## Summary

When an unsupported source is made executable through an external import/decoder adapter, the product must preserve two different identities:

- the **original source identity** selected by the user;
- the **execution input identity** produced by the adapter for downstream processing.

Treating the staging file as though it were the original source creates misleading size planning, Stream Copy semantics, metadata, recovery behavior and user-facing provenance.

## Evidence

Quick-Automatic-Hardsub-Encoder PR #44 adds an optional Windows Bink 2 adapter.

The original source is a `.bk2` / Bink 2 file. Current FFmpeg can identify Bink 2 but cannot directly decode its video stream, so an installed RAD Video Tools converter can produce a temporary AVI that FFmpeg can validate and consume.

The resulting workflow is:

```text
original .bk2
  -> external RAD decode
  -> temporary AVI execution staging
  -> FFmpeg transcode / hard-sub
```

If the AVI were silently promoted to “the source”:

- target-size planning could use a much larger decoded/intermediate AVI instead of the user's original file size;
- “Stream Copy” could falsely imply copying the original Bink stream even though decoding already occurred;
- UI could report AVI as the user's source format;
- refresh/recovery could lose the association between the original file and its adapter staging;
- staging cleanup could become indistinguishable from source deletion.

PR #44 therefore retains the original Bink source separately, records adapter provenance, uses the staging AVI only as the execution path, anchors source-size planning to the original file, and rejects Stream Copy once external decoding has been applied.

## Candidate rule

For workflows with external or internal input adapters:

- preserve original source identity independently from generated execution staging;
- record which adapter produced the execution input and whether the adapter has already transformed semantics;
- source-facing UI and reports should continue to identify the user's original source;
- executor-facing paths may use staging, but should not overwrite source provenance;
- size/quality heuristics must explicitly choose whether they are anchored to original source or staging rather than inheriting staging values accidentally;
- operations whose meaning depends on untouched source bytes or streams, such as Stream Copy, lossless passthrough, hash comparison or source-relative patching, must be disabled or renamed after a transforming adapter;
- replacing the source invalidates and cleans adapter staging;
- refresh/recovery must restore both the source identity and any still-valid adapter/job identity;
- staging validation proves only that the downstream executor can consume the adapted representation; it does not prove preservation of source-specific semantics such as alpha, auxiliary tracks or proprietary metadata.

## Relationship to existing Foundry knowledge

Related but distinct:

- `2026-10-02-media-format-support-is-a-compatibility-relation.md` separates probe, decode and compatibility evidence.
- `REL.DURABLE_STAGING_FOR_LONG_JOB` addresses long-job staging durability.
- `REL.VERIFY_THEN_PUBLISH` addresses validated output publication.

This Candidate concerns provenance and operation semantics specifically when **input** is transformed before the main executor sees it.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #44 `Add optional Windows Bink 2 import adapter`
- evidence level: code-level adapter integration; real RAD + real BK2 E2E remains device/external-tool validation

This is a Candidate only. It is not Canonical.
