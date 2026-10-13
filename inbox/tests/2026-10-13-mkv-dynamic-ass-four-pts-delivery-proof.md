# Test: real finished-MKV dynamic ASS at four fractional PTS

Date: 2026-10-13 (Asia/Shanghai)
Status: **PENDING exact-head CI and named temporal artifact**
Product: `11576865/MKV-Fast-Muxer`
Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/119
Initial PR head: `50b3baf7b255d10a9a8f12ccffab983906870e54`
Main baseline: `9a19ae02fe63a2113c28624a343cb91b8a1a2d30`

## Distinct real-delivery acceptance

Real Chromium generates an MKV with newly authored ASS containing three separate events/effects `\\move`, `\\t`, and `\\kf`, plus a dedicated TTF whose internal family `UIGS P3 Embedded Proof` is absent from system fontconfig.

Independent MKVToolNix must extract the actual delivered font byte-identically to the uploaded input. System FFmpeg must demux the real finished MKV's ASS using `-copyts`. Four fractional times **0.20, 0.65, 1.10, 1.55 seconds** must be rendered with explicit high precision `settb=AVTB,setpts=PTS+time/TB`, not a 1-fps integer-seek approximation. Both source and demuxed output are rendered using the same libass `ass` filter with independent isolated input/output font folders; their PNG SHA-256 digests must match at every time. All four reference frames must be pairwise distinct.

Direct final-MKV `subtitles` filter is a separate oracle requiring libass to select the unique embedded family, SSIM ≥0.995 against source at all four samples, and blank-frame SSIM <0.97 at each time.

A crucial separate check requires **three effect-specific negative controls** at 0.65 sec. Changing only the `\\move` into a static position, removing `\\t`, and altering karaoke `\\kf` timing must EACH independently change the reference render. This protects against claiming all three effects are exercised just because some frames changed for another reason.

Workflow artifact `p3-dynamic-mkv-ass-temporal-evidence` must contain JSON verdict and PNG matrix. The official complete Chromium run must fail when named oracle fails; green CI alone is not sufficient without inspecting the verdict.

## Deduplication

- `inbox/tests/2026-10-13-mkv-final-ass-libass-render-pixel-proof.md` is a previous real **single** frame 1.0-second final delivery check; current entry extends coverage to fractional dynamic timeline and per-effect mutation.
- `inbox/candidates/2026-10-12-subsecond-renderer-snapshot-timebase.md` already records the *general* high-resolution frame timebase rule in HSR. This entry is product-specific **Test evidence**, not a duplicated Candidate or new Canonical rule.
- `inbox/candidates/2026-10-04-visual-verification-needs-shared-viewport-and-temporal-evidence.md` is a proposed visual interaction method; this implementation instead validates persisted final MKV.
- `inbox/candidates/2026-10-02-shared-libass-not-identical-player-output.md` prohibits claiming other-player equivalence from one libass renderer.

## Unverified boundaries

Only 4 discrete frames from one 2s synthetic MKV, one unique TTF and system Linux FFmpeg/libass. No proof for animation continuity between sampled times, all karaoke variants, chained transforms, font resolution across real user projects, native Android players or universal Matroska semantics. The product itself does not perform a general runtime visual verification on arbitrary files. No Canonical promotion permitted from this single implementation.
