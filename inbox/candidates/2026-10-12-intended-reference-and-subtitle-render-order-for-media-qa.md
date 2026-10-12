# Candidate: Evaluate media output against the intended transformed reference, with subtitle render-order and color provenance

Date: 2026-10-12
Status: Candidate / extension hypothesis; **not verified defect or Canonical decision**
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
Related existing record: `inbox/candidates/2026-10-02-lossy-generation-source-selection-for-hardsub.md` (common subtitle-bearing reference and avoiding extra lossy generations).

## Distinct extension
For media jobs deliberately changing content (ASS burn-in, crop, resize, deinterlace, tone mapping, denoise), comparing the final encode directly against untransformed source conflates **intended transform** with **additional compression distortion**. Conversely, judging only average SSIM/VMAF against a rendered reference can conceal incorrect subtitle positions, missing glyphs, wrong color interpretation and temporal mismatches.

QHE `src/media-task.js` currently orders crop -> deinterlace -> scale -> rotation -> denoise/deband/sharpen -> ASS -> even-dimension pad. `src/media-verification.js::hardsubReferenceFilter` already reconstructs a reference filter and warns about spatial transforms; research must **reuse** this rather than assert no reference handling exists. FFmpeg `ass` filter documents `original_size` used to scale fonts when source display geometry differs; therefore crop/resize/ASS sequencing and intended subtitle coordinate policy deserve fixture-backed tests. No specific wrong rendered output is proven.

## Proposed dual-oracle contract
1. A **content-intent oracle**: expected visible subtitle presence/glyph/shaping/layout/safe area, frame/time correspondence, chosen colorspace/HDR transform, aspect and effective filter order.
2. A **codec-distortion oracle**: compare actual decode to the correctly rendered and geometrically aligned pre-lossy transformed reference, with scene stratification and temporal alignment. Report compression metrics separately from content-intent failures.
3. A **delivery oracle**: output stream structure, metadata signaling and target display/player rendering; structural output or FFprobe success must not claim universal visual parity.

Test representations: rescale before vs after subtitle for changes in display aspect ratio; ASS PlayRes and original_size; crop/rotate; 10-bit/HDR SDR input; subtitle-heavy frames; font alias fallback; mixed VFR clips. HDR re-encode remains currently blocked in QHE; do not interpret this as an observed HDR transcoding bug.

## Dedup / boundaries
Foundry search for 'transformation-aware reference metric' and 'subtitle burn original_size crop scale order' found no exact Candidate. This **extends** rather than reproduces existing lossy-generation source-selection Candidate; the extension explicitly separates semantic correctness from numerical compression quality and asks for filter-order/color test matrix.

Sources: QHE `src/media-task.js`, `src/media-verification.js`; FFmpeg official filters `https://ffmpeg.org/ffmpeg-filters.html` and `https://ffmpeg.org/doxygen/trunk/vf__subtitles_8c_source.html`. No product decision, no implementation, no Canonical change.