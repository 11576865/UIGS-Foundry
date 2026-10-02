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
