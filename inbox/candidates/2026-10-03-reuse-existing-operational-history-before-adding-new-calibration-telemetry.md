# Candidate: Reuse existing operational history before adding new calibration telemetry

Status: candidate
Date: 2026-10-03
Domains: engineering-workflow, telemetry, optimization, media-processing
Evidence type: implementation review

## Summary

Before designing a new adaptive calibration or prediction subsystem, inventory telemetry and historical records that the product already collects during successful real operations.

Existing records may already provide useful priors for runtime, bitrate behavior, hardware conditions, output size, and configuration-specific performance.

## Candidate rule

- inspect existing operational-history stores before introducing a parallel calibration database;
- treat successful full jobs as higher-value evidence than synthetic microbenchmarks for runtime prediction;
- identify which desired model dimensions are already recorded and which are missing;
- extend the existing schema when practical instead of creating disconnected histories;
- preserve platform parity: if one backend records history and another returns an empty placeholder, model availability must reflect that difference explicitly;
- distinguish data useful for speed/cost prediction from data useful for perceptual quality prediction.

## Evidence

In Quick-Automatic-Hardsub-Encoder Android Native:

- `NativeBenchmarkStore` persists up to 200 successful encode records;
- records include codec, mode, preset, CRF/target bitrate, source codec/pixel format/bitrate, resolution, fps, duration, audio-track count, subtitle/font counts, sample encode speed, calibration sample bitrate, encode duration, average speed, output bytes/output video bitrate, thermal state, power-save state, and validation mode;
- frontend prediction already uses recent matching records and median speed for ETA;
- Windows Native currently exposes `getLocalBenchmarkHistory()` as an empty record set.

Current history therefore already supplies runtime/throughput priors, but it does not directly provide a complete perceptual rate-distortion history such as full-output VMAF/SSIM observations.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation review after discussing time-budgeted compression calibration

This is a Candidate only. It is not Canonical.
