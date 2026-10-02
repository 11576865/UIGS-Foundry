# Candidate: Content identity may belong to a composite multi-file resource

Status: **Candidate / reusable ingestion pattern**
Date: 2026-10-02
Project evidence: `11576865/MKV-Fast-Muxer`, PR #56

## Observation

Not every importable media asset has a one-file identity.

VobSub is a concrete example: the logical subtitle track is composed of an IDX text index plus a SUB binary MPEG program stream. Treating each filename extension as an independent “format” is insufficient because:

- the IDX and SUB files are only meaningful together for this workflow;
- either file can be renamed, while the actual content signatures remain recognizable;
- validation must distinguish a valid composite pair from an orphan sidecar;
- downstream mux planning should operate on one logical subtitle track with two physical files.

## Candidate rule

When content inspection reveals that an asset is structurally multi-file:

- represent physical file identity separately from logical resource identity;
- detect each component from actual content when practical;
- pair components using an explicit relation (for example normalized basename, manifest reference, declared linkage, or embedded identifier);
- treat missing required components as a first-class invalid/incomplete state;
- expose the logical resource to downstream planning rather than leaking component filenames as if they were independent assets;
- preserve mismatch diagnostics for each physical component without letting filename extensions override the detected resource type.

A content-authoritative ingestion layer therefore needs to answer both:

```text
What is this file?
```

and:

```text
Which logical resource does this file belong to?
```

## Evidence

PR #56 introduces content-derived subtitle identification for ASS, SSA, SRT, WebVTT, PGS and VobSub. For VobSub, IDX content and SUB program-stream content are identified separately, then paired into one subtitle track by normalized basename. Orphan sidecars remain explicit invalid/incomplete inputs.

## Scope

Applicable to subtitle sidecars, image + metadata pairs, manifests plus segments, cue/bin media, split archives, model checkpoint shards, and other workflows where one user-visible asset spans multiple files.

Do not promote to Canonical from this single project implementation without broader validation.
