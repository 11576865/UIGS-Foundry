# Test: independent rendered-pixel proof of final-MKV ASS with embedded font

Date: 2026-10-13 (Asia/Shanghai)
Status: **PASS — exact-head Chromium E2E and named JSON/PNG artifact verified; PR #118 merged**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/118
Baseline main: `22255a4130ecf04aaf8a0b494bd107ea1f868777`
Working branch: `feat/p3-final-mkv-libass-render-proof-20261013`

## New bounded delivery evidence

In a real Chromium browser, mux source MP4 + newly authored ASS with V4+ Style + TTF whose **SFNT internal family is uniquely renamed** to `UIGS P3 Embedded Proof`. Download the finished MKV. Use external MKVToolNix (`mkvmerge -J` and `mkvextract`) to prove the actual output contains the font attachment and that FileData matches the original uploaded TTF.

Independently demux the actual output's ASS through system FFmpeg with preserved timebase. Use the **same** system FFmpeg/libass `ass` filter and a controlled 320×180 synthetic frame at 1 second to render (a) staged source ASS with a private source font directory, and (b) demuxed finished-MKV ASS with an independently extracted font in a separate directory. Require **PNG byte-exact output** from these two same-filter paths. A tampered-ass text PNG and a blank no-subtitle PNG are mandatory negative controls.

Additionally render the final MKV **directly** via system FFmpeg `subtitles=finished.mkv:si=0`, require the libass `fontselect` log to select the fixture's unique internal PostScript family (rather than a system fallback), require visibly nonblank output and FFmpeg SSIM ≥0.995 compared with the source reference; require negative controls SSIM <0.97. Differing `ass` and `subtitles` ingestion pipelines can shift edge-antialiasing pixels even with identical contents, so direct-filter strict PNG-byte equality is NOT the oracle: the independently demuxed same-filter path retains byte-exact proof.

Output CI artifacts: `p3-final-ass-render-evidence.json`, `p3-libass-source.png`, `p3-libass-demuxed.png`, `p3-libass-final.png`, `p3-libass-altered.png`, `p3-libass-blank.png`. A failed proof must fail the formal Chromium E2E and leave artifacts if available. The product report's existing `assEventAudit`, `assStyleAudit`, and `fontPayloadAudit` are expected to continue to pass, but they must NOT be relabeled as runtime visual certification.

## Distinction / deduplication

- `inbox/tests/2026-10-13-mkv-finished-ass-event-roundtrip-pending-ci.md`: delivered Dialogue/time, not pixels.
- `inbox/tests/2026-10-13-mkv-finished-ass-style-semantic-readback.md`: delivered V4+ Style fields, not actual rasterization.
- `inbox/candidates/2026-10-02-shared-libass-not-identical-player-output.md`: general principle that shared libass does not guarantee equivalent player output. The current record implements a **specific Test**, not a new or revised Canonical rule.
- `inbox/candidates/2026-10-12-intended-reference-and-subtitle-render-order-for-media-qa.md`: transformed-reference and rendering order for hardsub QHE, related but different.
- `inbox/candidates/2026-10-12-subsecond-renderer-snapshot-timebase.md`: fractional-PTS research; this test only exercises one exact 1-second sample and makes no subsecond animation assertion.

## Explicit limits

One synthetic fixture, one sample time (1.0s), one font (distinct family), 320×180 fixed canvas and one Linux CI FFmpeg/libass host. Does not validate all source codecs, ASS animations, karaoke, coverage of large font collections, arbitrary user files, differing player APIs, hardware OS, Android or full MKV EBML relation preservation. No transfer of this CI-only test into user-facing project audit is claimed.

Initial status PENDING CI; only upgrade after exact-head full Node/build + Chromium run and the named verdict JSON confirms passage.


## Exact-head acceptance — completed 2026-10-13

Product PR [#118](https://github.com/11576865/MKV-Fast-Muxer/pull/118) tested exact branch head `f4ea6096fb4d32823f0ca9e793408a07c47892cc` against `main@22255a4130ecf04aaf8a0b494bd107ea1f868777`.

- [Node/build run 38392791180](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38392791180) **PASS**: 429 / 429 Node tests, production build.
- [Full actual Chromium E2E run 38392791187](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38392791187) **PASS**: all browser E2E scenarios, including new named P3 scenario.
- Downloaded and **inspected actual CI artifact** `p3-final-mkv-libass-render-proof`, artifact ID `11810567007`, not just the workflow status. Artifact contains `p3-final-ass-render-evidence.json` and five PNG files.
- Named verdict `ok=true`, `code=PASS_P3_NAMED_FIXTURE`; independently demuxed finished ASS rendered with an independently extracted byte-identical embedded font was **pixel-identical** to source ASS rendered through the same libass filter: SHA-256 both `b279d5e2cb38f302bdd8e7ca91ff5be802efd10aae212ca887541b17398a3570`.
- Direct FFmpeg `subtitles` render on actual final MKV selected the uniquely named embedded font and achieved **SSIM 0.998954** versus staged reference; deliberately altered ASS control **0.836122**, blank no-subtitle control **0.824797**. The independent actual font extraction SHA-256 was `5cdb07b15d8768855069274aa4a0351108be0956cac8eac34055282f45a4b1ac`.
- Note that different libass input filter paths (`ass` vs `subtitles`) yielded subtle antialiasing pixel differences in a local controlled reproduction despite identical source material. Therefore direct-MKV output passed a **declared bounded SSIM metric**, while the independently demuxed **same-filter** output has a separate **strict byte-exact pixel** assertion. Neither gate was disabled for CI.
- PR #118 squash merged to `main` commit `9a19ae02fe63a2113c28624a343cb91b8a1a2d30`.

### Unchanged limitations

This remains one synthetic 320×180 frame at t=1s, one renamed font, system Linux libass, controlled render background; it does not prove cross-player, subsecond animation, karaoke, all glyph families, arbitrary sources, actual user device, or complex EBML relation fidelity. Product runtime audit does not claim it performs this same visual validation on every user's actual file. No automatic change to Canonical governance.
