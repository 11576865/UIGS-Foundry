# Test: independent rendered-pixel proof of final-MKV ASS with embedded font

Date: 2026-10-13 (Asia/Shanghai)
Status: **PENDING exact-head Chromium E2E + named artifact**
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
