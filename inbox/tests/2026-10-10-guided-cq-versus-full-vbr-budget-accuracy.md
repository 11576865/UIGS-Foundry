# Test: CQ short-sample frontier does not guarantee full VBR size or SSIM

Status: Test; synthetic Windows FFmpeg CI passed, field validation pending  
Date: 2026-10-10  
Domains: media-processing, guided-output-budget, rate-control, measurement-provenance, CI  
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/84  
QHE merged main SHA: `eb0cbdfbdc9fcc7d067e57d077ab0675a5f3c14f`  
Related existing Candidate: `inbox/candidates/2026-10-03-target-size-mode-should-expose-a-content-aware-rate-distortion-frontier.md`  
Engineering backlog: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/85

## Failure mode and why the test is distinct

A target-size UI can display credible **CQ/CRF-measured** short-sample R-D quality predictions, while the formal encode uses **bitrate-based single-pass VBR**. Even with the same source, pixel dimensions, rendering pipeline, codec and preset, the *control mode* and observation population are not equivalent. A target bitrate multiplied by source duration is a **planned video payload** estimate, not a hard upper bound for container bytes.

Unlike existing Foundry QHE scene-risk tests (which verify which scenes are measured and which branch wins), this Test verifies **end-to-end output byte and quality error at the formal encode boundary**.

## Reproducible fixture and execution

Windows GitHub runner with FFmpeg/libx264, `scripts/check-guided-full-budget-ffmpeg.mjs`:
- One six-second 640×360@12fps **lossless FFV1** source. First 3s testsrc2 motion; next 3s seeded temporal noise. Two ASS Dialogue cues. Render ASS to an authoritative lossless reference, ensuring quality is compared against the same subtitle-bearing pictures.
- Encode two matched 2s time windows with **CRF 18, 22, 26, 30**, `libx264 preset=medium`; record measured SSIM, FFprobe packet video bitrate and real encode durations; build the repository's production `fitRateDistortionModel` and `createSizeQualityFrontier`. Evaluation at **2 Mbps** is inside measured evidence. The **CQ-fitted mean SSIM** at that bitrate was approximately **0.956865**, with a sample-derived range **0.916004–0.997725**.
- Complete the **entire 6s** source with the same subtitle filter, selected video codec and preset using (a) **single-pass `-b:v 2000000`** and separately (b) **two-pass `-b:v 2000000`**. Inspect real MKV bytes, video packet bytes, FFprobe dimensions and full duration, full-output FFmpeg SSIM against the original-size ASS-rendered reference, and wall-clock times.
- Planned **video** payload is `2000000 * 6 / 8 = 1,500,000` bytes, excluding normal container/audio overhead (test has no audio).

## Observed Windows CI result

| Quantity | One-pass VBR | Two-pass VBR |
| --- | ---: | ---: |
| Actual MKV bytes | 4,216,001 | 1,780,843 |
| Video packet bytes | 4,214,790 | 1,779,647 |
| Relative error vs planned video bytes | +181.07% | +18.72% |
| Full-video SSIM | 0.976881 | 0.957878 |
| Observed process-stage wall time | 1.1516 s | 1.2441 s |

Both encode outputs exceeded the **1,500,000 planned video bytes** yet satisfied this **controlled fixture's** minimum full SSIM of 0.95. The small absolute wall-time difference is **not** a universal two-pass cost multiplier; first-pass speed and OS scheduling differ. Consequently the CI test now records the actual times but does not assume strict monotonic ordering of two-pass and one-pass wall time on a tiny fixture.

The existing **single** target-size/quality UI curve and selected-plan summary were updated in PR #84 to explicitly distinguish *CQ sample prediction* from *formal VBR output quality*, and to warn of potential significant size overshoot. **Production behavior remains single-pass**; no silent two-pass switch was introduced.

QHE latest-head Frontend, Windows and UIGS Evidence Coverage checks passed before squash-merge `eb0cbdfbdc9fcc7d067e57d077ab0675a5f3c14f`.

## Limits and follow-up

The source is intentionally synthetic and grain-heavy, not representative user content. Its two-pass result is **closer to the requested size**, not proof of precise byte-ceiling compliance. This regression does not exercise the actual Windows Native user export/reopen shell, HDR/VFR, physical NVENC hardware, several-hour footage or multi-track audio. Those remain FIELD-PENDING in #77. Production strict-limit semantics and accurate two-pass mode are separate engineering work in #85, not claims of PR #84. Never treat a modelled short-sample size/quality point as a verified complete output.

**Do not modify or promote Canonical based on this single software synthetic case.**
