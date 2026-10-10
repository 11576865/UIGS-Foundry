# Bug: Low-resolution scene-risk probes can erase the signal being evaluated

Status: implementation fixed; broader field validation pending  
Lifecycle: validation-pending  
Date: 2026-10-10  
Domain: media-processing, adaptive-testing, signal-processing, engineering-evidence  
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/82  
Related Test: `inbox/tests/2026-10-10-ffmpeg-scene-risk-observations-and-paired-strata-regression.md`

## Fault

A cheap, fixed-size video preflight used `fps=2,scale=160:90:flags=bilinear,signalstats` to detect temporal changes, contrast, dark scenes, and scene cuts before choosing expensive compression-calibration windows.

**Failure:** downsampling attenuated high-frequency temporal grain before `signalstats` ran. That reduced the very source signal the preflight was supposed to use for deciding which difficult windows merit expensive matched encoding tests.

## Reproducible evidence

Using FFmpeg 7.1.5 locally and GitHub Windows CI, a single four-second FFV1 synthetic source had two paired windows: testsrc2 moving scene followed by seeded temporal noise. At the original 160×90 preflight size, mean `YDIF` was approximately 6.36 for motion and 6.79 for grain, giving weak noise discrimination.

Yet real `libx264 -preset medium` measured against each lossless reference showed:

| Scene | CRF 28 SSIM | Behavior at target 0.970 |
| --- | ---: | --- |
| Moving video | ~0.986 | Pass |
| Seeded temporal grain | ~0.929 | Fail |

The grain window at CRF 22 measured ~0.982 SSIM and passed. Real FFprobe packet sums for grain were more than five times motion at CRF 28. Therefore adding a difficult matched window changed the recommended admissible **CRF**, not just a simulated score.

## Repair

The source-risk probe now scales with an **even-dimension, aspect-preserving maximum 320px longest edge**. On the fixture, `YDIF` rose to ~22.6 for grain vs ~6.73 for motion; the actual production risk function now ranks grain above motion in the tested case. The analysis keeps the same `fps=2` and per-probe process deadline. Version `paired-scene-strata-v2` prevents old sampling-plan evidence from mixing with the new metric.

PR #82 passed Frontend, Windows, Windows Runtime and UIGS Evidence Coverage and was squash-merged as `2ba584183dcabad0183dda62527c1a6027ce2d77`.

## Generalizable caution

A surrogate diagnostic measured *after lossy preprocessing* must be tested against the downstream engineering decision, not merely for the presence of valid numeric fields. Increased resolution is a trade-off; it improves detection on this fixture but may increase preprocessing cost, and does not establish correctness on all grain scales.

**Non-claims:** This is not a validated motion/grain classifier, a proof of cross-codec optimality, a probabilistic expected-value-of-information method, or real NVENC/HDR/VFR/long-video acceptance. Do not promote Canonical from this single observed failure and synthetic fixture.
