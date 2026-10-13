# Observation: reserve whole-source copied payload for trimmed budgets

Date: 2026-10-13
Status: Observation / local implementation and actual FFmpeg evidence; hosted Pending
Source: 11576865/Quick-Automatic-Hardsub-Encoder PR #105, continuation after 4549acf.

## Dedup
Read inbox/tests/2026-10-13-qhe-heterogeneous-audio-plan-and-source-owned-ui.md before capture. Its per-track/source-owned budget family records the prior unknown-copy restriction; this narrow observation adds conservative allocation rather than claiming exact range measurement. No Canonical change.

## Mechanism and limits
When copied audio or subtitle range is trimmed, retain its entire source-scoped measured packet-byte cost in fixedPayloadBytes. Do not extrapolate packet costs proportional to duration. copiedTrimReserveBytes records the reserved subset and is disclosed in ledger and checked-plan UI; do not add it twice. Missing/invalid measurement or exhausted video budget still fails. Imported configuration cannot supply source evidence. Final actual-container byte ceiling remains authoritative.

A long source may exhaust a short clip budget under this conservative allocation. Exact interval measurement, FLAC re-encoding, physical-device/player support and subtitle boundary/perceptual fidelity remain separate unverified work. This is not a universal container-size guarantee.

## Evidence
Two pure/model regressions failed before implementation; real FFmpeg trim task also refused. After implementation: local Node 218 pass/7 conditional skips; five real FFmpeg regressions passed; Vite build passed. Actual trimmed FLAC copy and SRT packet bytes compared with full-source reserves, independent full decode and strict-byte checks. Browser fixture asserts reserve disclosure and removal on clearing trim; local Chromium absent, hosted browser/Windows execution Pending. No independent cross-project corroboration or Canonical promotion.
