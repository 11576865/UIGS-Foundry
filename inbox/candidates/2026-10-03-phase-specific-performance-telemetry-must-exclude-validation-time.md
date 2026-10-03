# Candidate: Phase-specific performance telemetry must exclude downstream validation time

Status: Candidate

## Observation

When a task has distinct execution and validation phases, wall-clock duration captured only after validation can silently contaminate performance telemetry for the execution phase.

In Quick-Automatic-Hardsub-Encoder PR #47, Windows full-encode history was reviewed for ETA use. The proposed `averageSpeed` timer started before FFmpeg encoding but could be read only after output validation, causing validation work and status-poll delay to be counted as encoding time.

## Candidate rule

When telemetry is later used for phase-specific prediction:

- timestamp phase start and phase completion separately;
- compute encode/transcode throughput from the execution interval only;
- store validation duration separately when useful;
- do not relabel end-to-end task wall time as encoder throughput;
- for multi-pass work, define explicitly whether the metric represents one pass, all encoding passes, or total task time.

Conservative-looking telemetry can still be semantically wrong if the measured interval does not match the quantity being predicted.

## Evidence

Single project observation from PR #47 high-risk review. Candidate only; no Canonical change.


## Follow-up implementation evidence

PR #47 was changed so Windows Native accumulates each FFmpeg process interval from `Process.StartTime` to `Process.ExitTime`. Two-pass jobs sum the two encode-process intervals, while downstream FFprobe/packet-scan validation no longer contributes to `encodeSeconds` or `averageSpeed`.

This reinforces the distinction between phase throughput and end-to-end wall time.
