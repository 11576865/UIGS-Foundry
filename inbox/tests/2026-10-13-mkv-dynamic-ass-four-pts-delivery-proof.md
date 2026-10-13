# Test: real finished-MKV dynamic ASS at four fractional PTS

Date: 2026-10-13 (Asia/Shanghai)
Status: **PASS — exact-head 434/434 Node, build and complete Chromium E2E, named image/JSON artifact; PR #119 merged**
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


## Verified exact-head delivery and regression — 2026-10-13

- PR [#119](https://github.com/11576865/MKV-Fast-Muxer/pull/119), tested head `474fdb997af42e6d9500cfcf953ddddea3ad5ccd`, main baseline `9a19ae02fe63a2113c28624a343cb91b8a1a2d30`.
- [Node + production build 38398134597](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38398134597): **PASS 434 / 434 tests, Vite build**.
- [Full Chromium E2E 38398134701](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38398134701): **PASS all scenarios**, including new real browser four-timepoint rendered-ASS sample and P0/P1 source-structure refusal.
- Independently downloaded and inspected *the exact-head workflow artifact* `p3-dynamic-mkv-ass-temporal-evidence` (artifact ID `11813232279`): 17 files (16 PNG images + one JSON), `ok=true`, `code=PASS_P3_DYNAMIC_NAMED_FIXTURE`, four source/demuxed-finished ASS PNG SHA-256 pairs pixel-exact and pairwise distinct, all unique font selections confirmed. At 0.20 / 0.65 / 1.10 / 1.55 s the direct-final-MKV SSIMs were **0.998322 / 0.998733 / 0.997728 / 0.998158**; blank negatives **0.898715 / 0.889948 / 0.870812 / 0.862270**. The `move / transform / karaoke` mutation controls each yielded a different PNG versus original frame. Delivered TTF was independently extracted byte-equal, SHA-256 `28f6c676f6104031212f862201cb5554c527a66e4056e75d52cba1db618cf6aa`.
- Initial exact-head run [38396463275](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38396463275) **failed twice** *after* the P3 dynamic scenario had already passed. The unrelated P0 test awaited the scan-completed **status label** and immediately synthetically clicked the Mux button before scanning's `finally` reset `isBusy()`; its click was legitimately ignored and it timed out awaiting a runtime refusal status. The revised E2E waits for the observable idle control `#cancelBtn.disabled === true` first, then still asserts the same safety refusal. No production safety gate or P0 assertion was weakened, and exact-head E2E is green.
- PR #119 merged via squash into `main` at `383274ad586719b202d7412a8e812b8d9398781c`.

**Limits unchanged:** one controlled 2-second browser-generated MKV, one unique TTF, four discrete fractional times, one Linux system libass. Does not establish continuous animation, all karaoke variants, all ASS builds/players/devices or generalized user runtime rendering. No Canonical promotion.
