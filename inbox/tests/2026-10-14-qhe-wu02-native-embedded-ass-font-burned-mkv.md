# Test: QHE WU-02 source-bound embedded ASS/font import into actual Windows Native hardsub

Date: 2026-10-14
Status: PENDING — real Windows hosted exact-head workflow in progress; no PASS claim
Project: 11576865/Quick-Automatic-Hardsub-Encoder PR #105
Submitted QHE head: ea02ec78c83762dd60795cf1b82a37bc703501d1
Workflow: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38554057407
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

Submitted and running is not PASS; WU-02 full completion also requires user-facing browser interaction, real user MKV variations, font/glyph diagnosis and physical Windows/other platform evidence as applicable. This focused Test is not a separate root product goal and does not supersede A01–A03. No Canonical promotion.

Dedup: Existing QHE rich-MKV and audio-plan tests prove stream preservation without directly importing an embedded ASS/font from the selected source; prior MKV-Fast-Muxer ASS/font tests concern a distinct product and container editing. This test covers the previously absent source-owned Windows import-to-burn operation.
