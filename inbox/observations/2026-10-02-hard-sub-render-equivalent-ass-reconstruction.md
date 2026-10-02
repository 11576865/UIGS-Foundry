# Observation: Hard-sub extraction should target render-equivalent ASS, not source-semantic recovery

Date: 2026-10-02
Status: Observation
Scope: subtitle extraction / ASS reconstruction / OCR / render verification

## Observation

When reconstructing subtitles from a video that already contains burned-in subtitles, the rasterized image preserves only visible output. It does not preserve the original subtitle source structure.

Recoverable with varying confidence:
- visible text;
- appearance/disappearance timing;
- line breaks;
- approximate position and alignment;
- visible font characteristics;
- font size relative to script/video resolution;
- text/outline/shadow colors;
- border/shadow thickness;
- observable fades, movement, karaoke progression or other visible effects.

Not directly recoverable from pixels alone:
- original ASS Style names;
- exact original font file or font-family identity when multiple fonts render similarly;
- original PlayRes values;
- whether a visible property came from shared Style versus event override;
- exact tag ordering or syntactic form;
- hidden/non-visible tags;
- original margins/coordinates if multiple ASS parameterizations yield the same raster output;
- original timing precision beyond what the encoded video frames/timestamps can demonstrate.

## Reusable principle

For hard-sub reverse extraction, define success as a render-equivalent or visually equivalent ASS under a declared renderer and video geometry, not as byte-level or semantic recovery of the original ASS.

Use confidence labels for reconstructed properties and validate by rendering the reconstructed ASS through the intended renderer (e.g. libass) and comparing frames against the source video.

SRT is appropriate when only text and timing matter. ASS is appropriate when position, styling, line layout and observable effects should be preserved or reconstructed.

Do not promote to Canonical from this single discussion.
