# Test: QHE WU-02 source-bound embedded ASS/font import into actual Windows Native hardsub

Date: 2026-10-14
Status: PASS — exact-head Windows hosted, bounded synthetic MKV acceptance; real user field pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder PR #105
Initial test submission: ea02ec78c83762dd60795cf1b82a37bc703501d1
Final tested implementation: 1148bcda33bc74f66275eaad73d125e29930b8fb
Successful workflow: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38554433547
Initial verifier failure: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38554057407
Requirements: B05/B06/B07/B24; A01–A03 of owner-approved complete initial-version report.

## New product capability under test

The Windows Native input shelf presents explicit selection of an ASS subtitle stream discovered inside the selected MKV. The localhost Bridge extracts exactly the selected ASS stream and the source's recognized TTF/OTF/TTC/OTC attachments with generated safe filenames, returns source-bound bytes to the existing source/ASS/font workbench, and stages the font files for libass preview and encode. Original video selection and source file-stamp changes invalidate or reject stale staged resources. Existing Guided/Manual source analysis and shared task compiler are reused; no new encoder or automatic subtitle selection.

## Falsifiable hosted acceptance

- Generate real 5 s rich MKV containing FFV1, two audio tracks (FLAC + AAC), embedded ASS, and a self-generated, valid TrueType attachment.
- Through actual Windows localhost HTTP Bridge, reject nonexistent subtitle ordinal and mismatched source identity; import the correct ASS and font bytes and compare the font hash with the original attachment.
- Use shared schema-v4 compiler to make a real x264/libass task, with original FLAC copy and second AAC re-encode, then await Native job completion.
- Probe output stream codecs and full decode; require no residual soft ASS stream or font attachment in final burned MKV, copied FLAC packet SHA-256 identity, changed AAC packet hashes, and actual burned ASS image divergence versus an identical encode with subtitle events removed.
- Modify source after staging; forbid preview from reusing imported source-bound fonts.

## Distinctions and constraints

Exact-head Windows hosted synthetic acceptance is PASS. Whole A01/A02/A03, user-facing browser action, real user MKV variations, font/glyph diagnosis and physical Windows/other platform evidence remain separate and Pending. This focused Test is not a separate root product goal and does not supersede A01–A03. No Canonical promotion.

Dedup: Existing QHE rich-MKV and audio-plan tests prove stream preservation without directly importing an embedded ASS/font from the selected source; prior MKV-Fast-Muxer ASS/font tests concern a distinct product and container editing. This test covers the previously absent source-owned Windows import-to-burn operation.

## Actual host result

The 2026-10-14 Windows runner completed every fixture step successfully. Real FFmpeg 9.0.2 from Chocolatey processed a 5.021-second MKV. Windows localhost Native Bridge extracted a user-selected ASS and a valid generated TTF; the shared schema-v4 output was H.264 with FLAC copy and AAC reencode. Independent verifier reported `sourceFlacPackets:235`, `outputFlacPackets:235`, font SHA-256 `d086d10bf01dea2e44fb14bf8b152b911b280a93bbd411da2965341ff3f67a90`, `outputBytes:251257`, and `burnedEventPixelDifference:true`. The source mutation rejection was also confirmed.

The earlier workflow failure was limited to constructing an **independent no-events verification filter** from an unescaped `D:\...` absolute filename; it followed a successful actual Native encoding and stream checks. The counterexample verifier now uses relative paths in a private cwd. Final CI is PASS, but scope remains Windows hosted 5-second fixture, not all B07/A01 in real-world conditions. Do not promote to Canonical.
