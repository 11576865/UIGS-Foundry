# Test: Paired risk-scene measurement can reverse a real measured codec frontier

Status: Test / CI-validated synthetic software fixture; real media and hardware field acceptance pending  
Date: 2026-10-10  
Domain: adaptive-calibration, video-encoding, cross-codec evaluation, rate-distortion, test-design  
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/83  
Merged: `0f8b8c20e248e43aa09f67fa4cbdfa35aba6e7b4`  
Related existing test: `inbox/tests/2026-10-10-ffmpeg-scene-risk-observations-and-paired-strata-regression.md`  
Related Candidate: `inbox/candidates/2026-10-03-calibration-must-optimize-information-gain-per-unit-time.md`

## Distinct test objective

The existing QHE scene-risk test verifies that FFmpeg low-cost decoded signals differentiate scene regimes and influence time-stratified selection. This **separate test** verifies that a *real measured rate-distortion frontier*, using two different encoders, can change its **recommended codec** after adding the *same new scene to every tested CRF point across both branches*.

This is not a simulation of SSIM scores and is not the single-codec CRF-threshold reversal tested by QHE PR #82.

## Fixture and method

- One four-second **lossless FFV1** synthetic source at 320×180, 15 fps. First two seconds: moving testsrc2. Next two seconds: gray synthetic temporal grain via seeded FFmpeg `noise=alls=45:allf=t+u:all_seed=42`.
- Same original-size lossless references for all measured encoders. Two actual software encoders: `libx264` and `libx265` with `preset=medium`; CRF grid 18, 24, 30, 36 for **each codec and every sampled window**. CRF numbers are codec-internal controls, not assumed equivalent between codecs.
- Real FFmpeg SSIM for each encoded/reference pair. Real video-packet bytes via FFprobe. Wall time for each encoded sample and entire additional measurement stage.
- Feed observed bytes and quality to QHE production `fitRateDistortionModel`, then `createMultiBranchFrontier`. Compare a **single fixed projected source-size budget of 80,000 bytes**, only inside both codec models' shared measured bitrate region.
- Use the production `planPairedRefinement` to require a complete matched additional batch (all eight codec/CRF configurations). Feed the actual new-window results through `appendMatchedSceneObservation` and refit whole curves, retaining `paired-scene-strata-v2` measurement provenance and the same 80KB target. Test fails for unmatched positions, unsupported target, no all-CRF coverage, or absent crossover.

## Windows CI observations

- Initial motion-only measured frontier selected **H.264**, with conservative quality approximately 0.993743 versus H.265 0.992850 at the fixed target.
- After pairing the difficult noise window, the measured frontier selected **H.265**, with conservative SSIM **0.455891**, versus H.264 **0.436746**. Advantage of the newly selected codec: **0.019145 SSIM** at the *same projected size budget*.
- Observed initial sample encoder time: **1.320s**. Additional matched-scene encoder time: **3.604s**. Added stage wall time including SSIM and packet measurements: **4.925s**. The batch covered eight new codec/CRF measurements.
- Latest-head Windows and UIGS Evidence Coverage succeeded. QHE PR #83 squash-merged into main as `0f8b8c20e248e43aa09f67fa4cbdfa35aba6e7b4`.

## Interpretation / non-claims

The measured same-budget codec **decision reversal is real for the specified synthetic software case**. It does **not** show that calibration pays off economically in general: the stage cost is visible, but a universal expected value-of-information or probabilistic regret estimate has **not** been established. The minimum SSIM of both candidates in the stress case is very low, so the result is *not* evidence of acceptable perceptual quality.

The 80KB target comes from a rate-distortion model derived from short samples. This CI test does **not** run and verify a complete output exactly matching 80KB. It is not real-film/game footage, diverse ASS/font input, NVENC/GPU, HDR/VFR, multi-hour video, or a representative scene distribution.

This Test can inform additional field Cases and candidate-level research, but **must not promote Canonical norms** from a single controlled software synthetic observation. QHE issues #76 and #77 remain open/pending for their respective acceptance boundaries.
