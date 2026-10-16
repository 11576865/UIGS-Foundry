# Observation: HSR README default-MKV background diverges from executable fallback

Date: 2026-10-17
Status: Observation — source-verified documentation/runtime discrepancy, not Canonical
Product: 11576865/HSR-Voice-Archive-Builder
Inspected HSR main SHA: `dea5411312ed3e819864f1915f4f2008f938cba3`

## Observation

At the inspected SHA, the README still describes the default full-delivery MKV as having a black background (e.g. “默认生成连续 FLAC、SRT、ASS 与黑色背景的完整 MKV”, and “默认黑色背景，可以配置纯色、渐变或本地图像”). However, `app/archive_bundle_lifecycle.py::previous_bundle_settings()` returns `background_kind="image"`, `bundled_default=True`, and an image-mode spec for a project with no saved MKV receipt/preferences. `load_previous_bundle_image()` loads `static/assets/studio-red-clouds.webp` through `load_default_red_cloud_background()`. `app/pipeline.py::build_project_v02()` consumes those settings for first complete bundle publication. The UI likewise describes the red-cloud default, so the prose README and runtime/default-control surface are inconsistent.

This is a documentation accuracy issue, **not** evidence that the actual media renderer is broken. No new full-character archive was built in this review.

## Evidence

- README: https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/README.md
- Runtime preference and image loader: https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/archive_bundle_lifecycle.py
- Packaged asset: https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/archive_bundle_backgrounds.py
- Consumer in build pipeline: https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/pipeline.py

## Suggested limited remediation

Align the README's default-output description with the actual red-cloud packaged background (and distinguish explicit solid-black user choice). Include a regression assertion covering a first-build default and an existing saved background preference. Do not infer unrelated UI/renderer defects.

## Deduplication

Reviewed existing Foundry Candidate `inbox/candidates/2026-10-16-hsr-generation-intent-destination-and-preview-defaults.md`, which already establishes the **intended red-cloud default** and save-vs-generation semantics, plus related studio UI records. This Observation is narrower: the current README continues to contradict that implementation. It does not replace or promote the Candidate/Canonical specification.
