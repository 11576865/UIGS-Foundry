# Bug: Filename-extension gating can override successful content probing

Status: **Bug / reusable media-ingestion failure**
Date: 2026-10-02
Project evidence: `11576865/MKV-Fast-Muxer` current main

## Failure

The single-file media workflow does not consistently treat actual media content as the authoritative identity.

For the primary video input:

- the HTML `videoInput` accepts arbitrary files;
- preview mounts the selected file and runs ffprobe / FFmpeg against its bytes, so a renamed MP4 can still be probed as an MP4-family container and its video codec can be discovered;
- but the final mux path first derives `videoExt = ext(video.name)` and rejects any extension outside `.mp4 / .mkv / .webm / .mov / .m4v` before the input probe is used as the source of truth;
- MKV-specific UI capabilities such as source-track scan, append-preserve-all and attachment preservation are also enabled strictly from the filename extension `.mkv`.

Therefore a valid MP4 renamed to `.mmmmmm` can be content-probeable in preview but is rejected by the normal mux workflow. A valid MKV renamed to another extension can lose MKV-specific controls even though its bytes remain Matroska.

External audio is different but still inconsistent: the selected file is written into the FFmpeg virtual filesystem using the filename-derived extension, then ffprobe inspects the actual stream and records `codec_name`. Thus content probing exists, but there is no explicit extension/content mismatch state or unified authoritative media identity.

## Reusable rule candidate

For media-ingestion systems:

1. Treat filename extension and MIME type as hints, not authoritative media identity.
2. Establish a probed media identity from the actual bytes/container before capability gating whenever probing is available.
3. Keep at least these concepts separate:
   - user filename / extension;
   - browser-provided MIME;
   - probed container format;
   - probed stream codecs;
   - application support policy.
4. If extension and content disagree, surface a mismatch warning rather than silently trusting one or rejecting the other.
5. Use the probed identity for downstream capability decisions such as track scanning, container-specific metadata preservation, stream-copy compatibility and mux planning.
6. Retain extension allowlists only as file-picker ergonomics or cheap prefilters, not as final truth.

## Regression cases

At minimum:

- MP4 bytes renamed from `.mp4` to `.mmmmmm`;
- MKV bytes renamed from `.mkv` to `.mp4` and to an unknown suffix;
- raw AAC renamed to `.flac`;
- FLAC renamed to `.aac`;
- valid media with no extension;
- non-media bytes renamed to a supported media extension.

Tests should assert both the probed identity and the product-level decision, not merely whether FFmpeg accepts the file.

## Scope

Applicable to muxers, transcoders, media editors, upload validators, asset pipelines and any software that can inspect actual file content.

Do not promote to Canonical from this single-project observation without broader validation.


## Implementation evidence — MKV-Fast-Muxer PR #53

PR #53 implements a first content-authoritative media identity layer for the single-file workflow:

- lightweight header sniffing distinguishes ISO BMFF / MP4-family and Matroska / WebM before capability gating;
- ffprobe remains the execution-time authority for actual container and stream codec identity;
- the old primary-video extension allowlist is no longer the final mux gate;
- a valid MP4 renamed to an unknown suffix is accepted after content identification and receives an explicit extension/content mismatch warning;
- Matroska content renamed to `.mp4` is treated as Matroska for source-track scan and attachment/preserve capabilities;
- external audio is staged under a neutral virtual filename, probed, and handled by its actual audio codec rather than its claimed extension;
- invalid or unsupported actual media remains rejectable even if its filename uses a supported suffix.

Regression coverage was added at helper, integration, and browser E2E levels. Browser scenario 34 directly exercises renamed MP4 and raw AAC content; a later extension of the same scenario exercises renamed Matroska capability exposure and source-track scanning.

During full-suite validation, the new asynchronous header preflight exposed a separate batch-orchestration readiness race. That failure is tracked independently as `2026-10-02-batch-execution-async-preflight-readiness-race.md`; the fix makes batch execution await media-identity preflight before triggering mux.

This remains Bug / candidate-level evidence and is not Canonical.


## Additional implementation evidence — MKV-Fast-Muxer PR #54

PR #54 extended the same rule from the single-file path into batch discovery and pairing. Batch selection now reads candidate file headers before deciding which files are videos, accepts supported MP4/MOV/M4V/Matroska/WebM content even when the suffix is unknown or misleading, excludes supported-looking filenames whose actual content is not recognized, and drives Matroska preserve-all behavior from detected content identity. Browser E2E verifies a renamed MP4 and a Matroska file renamed to `.mp4` in the same batch, including preservation of original Matroska attachments. PR #54 merged as `25fe3f0956ccb22837dc0d0693ca8e8f281a5df5` after unit, build, and browser E2E success.

This strengthens the Candidate with a second workflow surface in the same project, but does not promote it to Canonical.
