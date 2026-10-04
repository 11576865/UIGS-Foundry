# Candidate: Media import capability stages must not collapse

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-05
Project evidence: `11576865/ASS-Workbench-Android` PR #124

## Observation

External media import exposes several capability questions that are easy to collapse into a single word such as “supported”.

In practice, the following are distinct evidence layers:

1. **Source parseability** — a demuxer/extractor can enumerate the source Track and metadata.
2. **Decoder availability** — a decoder exists for the source codec on the current device/runtime.
3. **Stream-copy compatibility** — the encoded payload, framing and codec configuration can be mapped into the destination container without decode/re-encode.
4. **Execution readiness** — the application has actually implemented the required adapter/writer path and verifies the produced output.

Evidence at one layer does not automatically prove the next.

For example, Android `MediaExtractor` may parse a Track and `MediaCodec` may decode it, while the application still lacks a proven Matroska CodecPrivate/framing mapping. Likewise, a codec-level mapping may be known while the product has not yet implemented the demux -> writer execution path.

## Candidate rule

For media/container import capability:

1. **Represent the stages separately.** Do not compress parseability, decoder availability, stream-copy compatibility and execution readiness into one boolean `supported`.
2. **Do not infer stream-copy from decoder availability.** Decoding evidence proves a decode path only; it does not prove payload framing or destination-container metadata compatibility.
3. **Do not infer execution from theoretical compatibility.** A valid codec/container mapping is not an executable product capability until the adapter and writer path exist.
4. **Keep observation state separate from mutation state.** Compatibility inspection must not create or enable write mutations merely because a Track is theoretically compatible.
5. **Require explicit codec-configuration evidence when the destination mapping depends on it.** Missing `csd-*`, CodecPrivate or equivalent configuration should remain UNKNOWN unless the adapter can reconstruct and verify it.
6. **Treat unproven container mappings as UNKNOWN, not “probably supported”.** Codec existence in both source and destination formats is insufficient when framing/headers have not been proven.
7. **Use TRANSCODE_REQUIRED only when stream-copy is not supported by the current mapping but a decode path is actually observed.** This classification must not imply that a transcoder is implemented.
8. **Never silently transcode.** Decode/re-encode must be an explicit workflow boundary because it changes payload identity, quality, performance cost and verification requirements.
9. **Expose execution readiness directly in UI/preflight.** Users should be able to distinguish “compatible in principle” from “available now”.
10. **Promote to executable only after real output verification.** The adapter must produce a destination artifact that is re-opened and checked before capability is treated as implemented.

## Implementation evidence

PR #124 implements the first read-only media import compatibility probe:

- Android `MediaExtractor` enumerates external media Tracks.
- Track evidence includes MIME, dimensions/channels/sample rate, observed `csd-*`, language and decoder availability.
- A pure planner classifies Tracks as:
  - `STREAM_COPY_COMPATIBLE`
  - `TRANSCODE_REQUIRED`
  - `UNSUPPORTED`
  - `UNKNOWN`
- Initial codec-level Matroska candidates include AVC, HEVC, VP8, VP9, AAC, MP3, FLAC, AC-3 and E-AC-3.
- Opus, Vorbis and AV1 remain UNKNOWN because required Matroska header/CodecPrivate/framing mappings have not been proven in this project.
- Every generic-media result has `executionImplemented=false`.
- UI exposes compatibility evidence but provides no Add action.
- A regression proves that even a `STREAM_COPY_COMPATIBLE` assessment creates zero `ContainerMutation` entries and leaves `ContainerEditPlan.executable == false`.

## Relation to existing reliability guidance

This candidate is consistent with the broader project rule that capability must be proven by real output rather than API names or return codes, but it adds a media-import-specific evidence hierarchy and an explicit observation-vs-mutation boundary.

## Evidence boundary

This is implementation-backed by one Android media compatibility probe. Actual external demux + stream-copy execution has not yet been implemented for generic media sources, and transcode execution is intentionally out of scope.

Do not promote to Canonical from this evidence alone.
