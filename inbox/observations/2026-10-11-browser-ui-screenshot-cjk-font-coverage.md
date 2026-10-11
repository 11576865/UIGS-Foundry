# Observation: screenshot CI must prove script-specific glyph coverage

Date: 2026-10-11
Status: **Verified corrected on PR #73; merged to main**
Source: [MKV-Fast-Muxer PR #73](https://github.com/11576865/MKV-Fast-Muxer/pull/73)
Observed successful head: `94bcea940023c49970bfb767ca89a1f06d5f1ce3`
Observed E2E: [run 38120405869](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38120405869), [artifact 11695471162](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38120405869/artifacts/11695471162).

## Observation

All actual Chromium media E2E scenarios and 199/199 Node tests were
successful; six desktop/phone/batch visual screenshots were captured and
uploaded. Direct inspection of `mkv-container-tree-desktop-viewport-1440.png`,
`mkv-container-tree-phone-viewport-390.png` and batch shots revealed that
almost every **Han character rendered as a square/tofu missing-glyph symbol**.
ASCII/Latin text rendered correctly. CI installed `fonts-dejavu-core`,
which did not establish adequate Simplified Chinese coverage.

This makes the screenshot artifact **unfit for visual acceptance** even
though the output file exists and interaction E2E is green. It is evidence
of the runner's missing script font, **not** by itself evidence that
the product is broken on users' systems with functioning CJK fonts.

## Bounded repair

PR #73 subsequently added conditional `fonts-noto-cjk` provisioning
and a `fontconfig` check using `fc-list :lang=zh-cn family`.
The runner fails explicitly if no Chinese-capable system fonts are
available before launching E2E screenshot capture. A source-level
regression ensures the font preflight remains part of the workflow.

At registration, regenerated screenshots and complete latest-head CI
were **Pending**. Do not treat the original green artifact as visually
valid and do not assume glyph coverage in production clients from a
runner-only package.

## Reusable lesson

Visual acceptance evidence needs environment parity for **fonts,
locale, DPI, and asset availability**, not merely file existence and a
passing automation run. For multilingual products, explicitly validate
font coverage for the languages used by the actual UI, capture
populated states, then inspect the pixels before granting a visual gate.
This single observed defect is an Observation, not an automatic
Canonical change.


## Verified correction and closure (2026-10-11)

The final PR-head [Chromium run 38128807086](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38128807086)
and [Pages run 38128807027](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38128807027)
both **succeeded** at `f4ae5c1b7d896eebe21a5c4dd830acb7f59cf2e2`.
The first CJK-fixed complete Chromium run,
[38128420956](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38128420956),
supplied six legible screenshots, verified by direct inspection.
The final run generated [artifact 11698626440](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38128807086/artifacts/11698626440),
whose 390px batch view was directly inspected: Chinese copy was readable
and the sticky navigation was fully opaque above scrolling content.
No horizontal clipping was apparent in reviewed 1440px and 390px shots.

[PR #73 was merged](https://github.com/11576865/MKV-Fast-Muxer/pull/73)
to `main` with merge commit `60d41336ed7d6df5a422001289824510ea823d9e`.
Post-merge main-branch CI was starting at the time of this update.
The Observation concerns correctness of multilingual screenshot evidence,
not a product defect in every browser configuration. No Canonical change.
