# Candidate: Output verification should compare against the expected pre-lossy state, not necessarily the raw source

Date: 2026-10-04
Status: Candidate
Scope: media verification / intentional transforms / subtitle burn-in

## Observation

For operations that intentionally change the image, raw-source-vs-output comparison mixes expected changes with unintended degradation.

Hard-sub encoding is a clear example: the subtitle itself is an intentional visual difference. Comparing the untouched source frame against the hard-sub output would make the verification surface dominated by the expected subtitle render rather than by encoding/output deviations.

## Candidate principle

Choose the comparison reference from the semantic contract of the operation:

- pure transcode without intentional transforms: raw source frame can be a useful reference;
- transcode with crop/scale/filters: disclose or normalize the intentional transforms;
- hard-sub output: construct an expected pre-encode reference by applying the authoritative visual transform chain and subtitle renderer to the source, then compare that reference against the decoded verified output.

The reference should stop immediately before the lossy stage being evaluated when the goal is to inspect generation loss.

## Timing requirement

The expected reference and output evidence should be paired by authoritative timeline time. When a separately sought source frame is rendered with timed subtitles, reset its local PTS and rebase it to the absolute source timestamp before subtitle rendering, then reset PTS afterward.

Frame-rate conversion can still select an adjacent sampled frame; the UI should disclose this ambiguity instead of presenting every difference as codec loss.

## Limits

This is a Candidate derived from one implementation and should not be promoted to Canonical without broader validation across additional transform/render pipelines.
