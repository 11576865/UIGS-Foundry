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

## Follow-up refinement — priors have different transferability

Historical observations should not be pooled as if every field transfers equally across future jobs.

A practical split is:

- **hardware/runtime priors** (encode speed, thermal behavior, startup overhead): relatively transferable across different source videos when codec/preset/resolution/fps and device conditions are similar;
- **rate-control priors** (planned bitrate -> actual bitrate/output-size deviation): moderately transferable when encoder mode and source class are similar;
- **perceptual quality priors** (SSIM/VMAF vs bitrate/CRF): strongly source-content dependent and should not be treated as exact evidence for unrelated videos.

Therefore:
- reuse runtime history broadly;
- reuse rate-control history conditionally;
- use perceptual-quality history only as a weak prior unless current-source features or direct samples support transfer;
- persist current-source calibration samples separately so repeated decisions on the same source can reuse them at high confidence.

This distinction prevents a history-rich product from becoming confidently wrong by over-transferring quality observations across unrelated content.

