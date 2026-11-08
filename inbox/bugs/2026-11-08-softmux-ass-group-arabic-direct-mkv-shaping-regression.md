# Bug: Group ASS subset may change direct-MKV Arabic shaping despite passing font-cmap and HarfBuzz checks

Date: 2026-11-08
Status: **Confirmed Bug / exact-output reproduction; conservative original-font fallback in Draft PR #269; fix not yet fully CI-accepted at first recording**
Project: `11576865/MKV-Fast-Muxer`; opt-in V3.5 `?ui=v3&nav=full`; [Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269).
Affected behavior: Frozen BatchRunner Group (`subsetEnabled=true`, `subsetScope=group`) with Arabic-script ASS content and a test-only unique family absent from the runner's installed fonts.

## What actually failed

Two actual MP4 inputs plus two ASS episode files were rendered in a browser batch with a test-only renamed DejaVu TrueType face `UIGS S03 TrueType Proof`. Independent extraction showed both finished MKVs carried a byte-identical reduced font, Unicode cmap union, unmodified ASS cue text, correct name, preserved GSUB/GPOS tables and passing basic native HarfBuzz clusters/positions. The native FFmpeg `ass=...` path using original font versus the extracted subset produced **identical pixels**. Nonetheless, independently rendering the **finished Matroska** through the native `subtitles=filename=finished.mkv:si=0` libass path changed the Arabic glyph geometry. [Exact-head V3 CI #42470001327](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42470001327) red with direct/reference SSIM **0.973473** where the test required 0.995.

A later independent same-entry-path control compared `subtitles=original.ass:fontsdir=original-font` against `subtitles=finished.mkv` and still found **different pixels**, so the problem is not explained away by mixing `ass` and `subtitles` filters. [V3 red #42489226672](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42489226672) preserved actual PNGs, genuine MKVs and independent receipts. Inspection of direct `fontselect` confirms the **intended isolated PostScript family** was selected, rather than an obvious system-family fallback. The reference-font and subset-font images differ in Arabic letter join/width even with the same renderer entry path. The production-derived attempt to expand the subset text with Unicode Arabic Presentation Forms did **not** fix it. Therefore this is a **scoped observed real-product output discrepancy**, not a cosmetic screenshot comparison.

No universal conclusion about every Arabic font, text, renderer or Matroska player is supported. Cause within the native libass/HarfBuzz/subset interplay is not fully isolated at the glyph-lookup level. Earlier HarfBuzz helper compared clusters, counts, advances, offsets and `.notdef` but did not compare all glyph names/IDs across two differently indexed subsets.

## Bounded correction under evaluation

In [Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), the Group preprocessor now calls `mustPreserveOriginalGroupFonts(text)` on the actual full batch visible-character union. For text containing Unicode Script=Arabic, it returns the **same original user-authorized font File objects** (deduplicated by actual byte SHA), not an unverified byte-reduced subset. `createFrozenBatchMuxContext` retains the explicitly requested Group policy but adds an immutable `reportPlan.fontPreparation` observation with `applied:false` and reason `arabic-direct-libass-shaping-unverified`. The batch terminal announces that the font originals were retained. No new File picker, owner, permission, subtitle mutation, second execution path, or fabricated output is added. Non-Arabic Group batches still use original HarfBuzz subsetting and must remain genuinely byte-reduced.

### Verification required

- A genuine two-output browser MKV E2E must assert both original font **byte hashes** survive as real Matroska attachments, both actual ASS cues are present, the unchanged source files remain immutable, native HarfBuzz shaping is unchanged, `ass`-to-`ass` and `subtitles`-to-`subtitles` renderings are each **pixel identical**, and audit reports contain requested Group versus actual byte-preserving `fontPreparation` decisions.
- A separate non-Arabic real Group test must still produce two **byte-identical reduced** font attachments and cover both episode repertoires.
- Full exact-HEAD V3 Pilot, blank MKV, full Browser E2E and other touched checks must run, with no inherited green from earlier commits.
- Ordinary users should not be told that Group optimization was applied when only an original-font preservation fallback was delivered.

**Reusable principle:** preserved name tables, cMap coverage, native HarfBuzz cluster/advance equality and `ass=fontdir` pixel equality are each insufficient as general proof of the delivered Matroska. Use the same renderer entry path for source/output comparisons; require actual downloaded MKV bytes and a deliberately isolated font family. A failed renderer test is evidence, not a threshold-tuning opportunity. If fallback is selected, make requested policy and actually applied transformation separate, immutable audit facts.

No Canonical promotion. This Bug shall not be marked resolved until the precise new implementation SHA passes its own real-output tests.
