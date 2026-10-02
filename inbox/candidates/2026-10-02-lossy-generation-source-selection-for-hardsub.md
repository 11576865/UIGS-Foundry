# Candidate: Lossy-generation source selection for hard-sub transcoding

Date: 2026-10-02
Status: Candidate
Scope: video transcoding / hard-sub pipelines / source selection / quality verification

## Observation

When hard subtitles require full video re-encoding, using a previously lossy-transcoded derivative as the input introduces an additional lossy generation compared with rendering from the highest-quality available source.

Conceptually:

highest-quality source
→ subtitle render
→ final encode

has one fewer lossy generation than:

highest-quality source
→ intermediate lossy transcode
→ subtitle render
→ final encode

The second path cannot recover information discarded by the intermediate transcode, and the final encoder may spend bits reproducing artifacts introduced by that earlier encode.

## Candidate principle

For final hard-sub production, prefer the highest-quality available source and postpone the delivery encode until after subtitle rendering.

If an intermediate is operationally necessary, classify it explicitly:
- lossless / mezzanine intermediate: suitable for later hard-sub encoding;
- visually transparent high-quality lossy intermediate: acceptable only after verification for the target use;
- delivery-grade lossy derivative: should not be treated as a canonical source.

File size alone is not a sufficient proxy for quality. Source codec, duration, resolution, frame rate, bit depth, chroma subsampling, encoder settings, scaling, colorspace/HDR transforms and prior filtering all matter.

## Verification pattern

To compare two hard-sub pipelines fairly, create one common subtitle-bearing reference by decoding the highest-quality source, rendering subtitles through the intended renderer, and preserving that result losslessly or as decoded reference frames. Encode both candidate paths with the same final settings and compare each output against that same subtitle-bearing reference.

Use representative scene classes, not one average clip:
- motion / particles;
- dark gradients;
- fine texture / foliage;
- film grain;
- sharp line art / UI;
- subtitle-heavy frames.

Metrics such as VMAF/SSIM/PSNR can support the comparison, but visual inspection remains necessary. If the final delivery encode is itself very aggressive, its distortion can dominate and narrow the observable difference between source paths.

## Why reusable

This applies to hard-sub encoders, archive builders, remaster pipelines and any workflow where a derived lossy file may accidentally become the source of a later lossy encode.

Do not promote from this single discussion to Canonical without additional project evidence.
