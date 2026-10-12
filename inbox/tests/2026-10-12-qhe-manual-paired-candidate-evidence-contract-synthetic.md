# Test: QHE Manual Transcode paired candidate evidence compatibility (synthetic)

Date: 2026-10-12
Status: TEST / passing automated *synthetic model-level* regression, **no real codec comparison acceptance**
Related Candidate: `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`
QHE draft PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
QHE head: `8b5c437809aae3c22524f261c4c9811467737105` (branches from main `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`)

## Test source and reproducibility
- New test `src/manual-transcode-comparison.test.mjs`, registered as `node --test src/manual-transcode-comparison.test.mjs` in `.github/workflows/test-frontend.yml`.
- Exact-head Test frontend: run `38263407888`, completed **success**; includes all listed Node regression checks, unrelated frontend unit/FFmpeg integration/build/browser checks. UIGS Evidence Coverage run `38263407783`: **success**.
- Synthetic three-window 60-second trimmed SDR source; windows start 30, 58, 88 seconds, each two seconds. H.264/x264 and HEVC/x265 example CQ observations feed the *existing* QHE R–D model; all example SSIM values and encoder identities are artificial, not measured by FFmpeg.

## Asserted test behaviors
- Compatible declared source, native runtime, decoded reference, source video stream, processing/filter identity, sample plan, dimensions and paired windows yield exactly one bounded multi-branch model.
- Alternative branches retain explicit identities, no comparison outside shared measured budget interval, and resulting recommendation does not authorize VBR execution.
- Mismatched source/runtime/reference/filter identity or reference metric, wrong source timeline and sample plan, unpaired starts/missing windows/incorrect sample duration fail closed.
- Null, Boolean, NaN/Infinity and otherwise invalid SSIM do not become fabricated numeric evidence; per-window minima, mean SSIM and mean bitrate must agree with summarized R–D points.
- Duplicate branch IDs, differing output resolution, too few distinct rates, no overlapping measured size interval, invalid/unknown copied-audio budget or mismatched output duration fail closed.

## Evidence boundaries
This confirms deterministic JS validation, not that the caller-provided source/runtime/reference tokens are truthful, nor that multiple physical encoders have been sampled under equal actual conditions. No GPU, hardware codec, Android, WASM, HDR, VFR, real film, 7-hour source, formal VBR native adoption or downstream user UI workflow was exercised. The draft is unmerged. Do not promote to Canonical. Follow-up requires native runtime protocol binding, real paired samples and final output independent verification.
