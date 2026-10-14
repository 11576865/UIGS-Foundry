# Candidate: Reuse staged large media across probe and execution in browser pipelines

Status: candidate
Date: 2026-10-03
Domains: media-processing, browser-runtime, performance, workflow-state
Project evidence: `11576865/Quick-Automatic-Hardsub-Encoder`

## Observation

The browser workflow probes a selected source before execution. The same File object was then mounted again into a new WASM/WORKERFS input mount when the user started transcode or stream-copy trim.

For large media this duplicated preparation work and left the UI in the generic “reading source/checking settings” state long enough to appear stalled. The path also loaded the bundled subtitle fallback font even when no ASS subtitle was involved.

## Repair

The engine now:
- recognizes the same selected source by object identity or stable file identity (name, size, lastModified);
- reuses the existing mounted source path instead of creating a new input mount;
- skips subtitle fallback-font setup for media-only transcode/copy paths.

A regression test mounts the same ~433 MB logical source twice and requires only one source mount and zero fallback-font loads.

## Candidate rule

If an earlier probe/preflight phase already materialized or mounted a large immutable source, later phases should reuse that source identity rather than silently re-stage it.

Re-stage only when source identity changes or when the downstream operation needs additional operation-specific assets.

This reduces duplicate I/O/memory pressure and keeps “preparing” latency proportional to new work rather than file size already paid for.

## Evidence

Repair commits on `main`:
- `e575a5dbc1fb5fface91fc64dd0d0d9af6896107` — source staging reuse and media-only font bypass.
- `2cdca7f508b2ccba433d003bf85406bb1ddc4eab` — regression test.
- Frontend unit, real FFmpeg integration, build, and UI smoke passed after repair.

This is a Candidate only. It is not Canonical.

## 2026-10-15 counterexample — same metadata does not mean same mounted media

Status: **Candidate correction / product fix submitted / exact-head CI Pending**.

The original 2026-10-03 code used `previousVideo === videoFile || (name, size, lastModified all equal)`. The second branch permits two distinct browser `File` objects with identical metadata but different byte content to reuse the first object's WASM mount. This undercuts the earlier text's assumption that the metadata triple represents a stable *content* identity. It is not a content attestation.

QHE PR #105 existing branch `feat/qhe-five-round-delivery-20261013`:
- Regression test commit [7a141e7](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/commit/7a141e79eb5d02653f2995d21cfce7303b14c5cc): two distinct same-metadata objects must each be mounted, while the original same-object reuse test remains.
- Product fix [195df5d](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/commit/195df5d277f03db5efc57eae337cfbcb420cc5dc): limit mounted-source reuse to the exact same `File` object identity, avoiding accidental content substitution. Does not add an expensive full-file content hash, new cache authority, or another staging system.
- The project's existing `.uigs/invariants.json` (`MEDIA.BROWSER.SOURCE_STAGING_REUSE`) expressly covers the **same immutable File**, not arbitrary same-stat files.
- Source inspection verifies the old branch is absent at this commit; exact-head GitHub CI was queued/in progress at intake. Neither full Web FFmpeg runtime nor physical-browser long-film acceptance is claimed.

**Narrowed rule:** Reuse an already mounted immutable browser source only with an identity binding that proves it is the same underlying bytes. In this implementation, identical `File` object identity is acceptable; a name/size/mtime tuple is not. Different `File` objects may be restaged, even if that costs extra I/O, unless stronger source-byte identity is independently established.

This amends the earlier Candidate family instead of creating a duplicate. Related existing candidate: `2026-10-03-persisted-derived-evidence-must-carry-all-input-dependencies.md`. No Canonical promotion from this single QHE observation.
