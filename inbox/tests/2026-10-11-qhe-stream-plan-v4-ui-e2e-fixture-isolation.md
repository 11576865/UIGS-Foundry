# Test / Pending: Stream Plan v4 UI-to-task E2E fixture isolation

Date: 2026-10-11
Product: `11576865/Quick-Automatic-Hardsub-Encoder`
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/65
Current head: `490221e3fba947e64ebd5bbf80207308172a4692`
Status: **Pending Frontend CI** (run `38117809648` queued at submission).

## Trigger and diagnosis

The new Browser Playwright case exercises two selected video streams `0,1`, video range `1s..3s`, full-duration copied audio, expected output video tracks `2` and independent stream mapping. It runs inside the **same** `scripts/check-media-ui.cjs` browser session as pre-existing waveform and keyframe timeline checks.

Two red CI attempts (historical PR head and reconciled head `c89492c2`) failed later on `Snap-to-keyframe did not align IN to the actual keyframe`. Source inspection shows the E2E case left `[name=end]` at `0:03`; the later test requested `IN=8:20`, previewed the prior keyframe `8:00`, and clicked `taskKeyframeSnapStart`. The production `setBoundary('start', value)` correctly enforces `IN <= OUT` and therefore clamps to the stale three-second OUT instead of permitting an eight-minute start. No production snapping defect is established.

## Repair and regression boundary

After asserting the captured actual execution task, restore the previous single-stream scenario:
- Clear OUT to unbounded; reset IN to 0.
- Restore selected video streams to 0 and both audio/video range policies to their default trimmed state.
- Drop the temporary two-video metadata from the shared mock media.
- Assert that OUT is blank and selected video stream is 0 before handing control to pre-existing timeline tests.

Latest source-verified repair head: `490221e3fba947e64ebd5bbf80207308172a4692`. **This is not reported passed until its own latest-head CI succeeds.** All physical NVIDIA, HDR/VFR, long-form and Android device claims remain separate from the browser fixture.

## Candidate relation

Deduplicated against `inbox/candidates/2026-10-04-replay-stale-feature-branch-as-semantic-delta.md`. Test-layer evidence only. Do not auto-promote Canonical.
