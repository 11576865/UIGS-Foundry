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
