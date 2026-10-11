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


## Second observed UI test interference and bounded isolation correction (2026-10-11)

The first attempted fix (`490221e3fba947e64ebd5bbf80207308172a4692`) restored `[name=end]`, `start`, selected videos and range policies after the Stream Plan v4 case. The keyframe alignment assertion consequently advanced, but **Frontend CI `38117809648` still failed**: Playwright `page.click('#taskInspect')` timed out because the button existed but was **not visible** (`scripts/check-media-ui.cjs:384`). This indicates the original added case had altered more of the shared browser/workspace UI lifecycle than resetting a few form values restored. The exact hidden-parent mechanism is **not proven** by that log; do not label a product visibility bug based solely on this test.

A more bounded test-only repair moves the entire new two-stream E2E to the **end** of the original Playwright smoke, after all pre-existing assertions. The original suite receives its original single-video mock setup, the original sample-run count expectation is restored to `4`, and only the last new E2E scenario adds the two-video mock metadata and exercises the UI-to-task boundary. New QHE PR #65 head: `f7d9ef96834e757b909cb037a94912aa77826591`. Frontend run `38118095158` was **in_progress** on the single allowed initial external status read; CI result **Pending External Validation**, not passed and not merged.

Reusable testing observation: adding an end-to-end scenario to a shared, stateful browser workflow can invalidate later assertions in ways that survive partial form-value reset. Prefer a truly fresh page/mount fixture or run independent add-on assertions after existing shared-session tests; preserve an explicit failure trace. Do not promote this single observation to Canonical. No real GPU/long-form hardware test was performed.
