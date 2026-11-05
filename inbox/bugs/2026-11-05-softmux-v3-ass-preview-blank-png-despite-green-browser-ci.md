# Bug · Softmux V3 ASS preview can appear blank although the PNG/CI claims success

**Status:** OPEN — reproduced from exact CI artifact; root cause NOT YET CONFIRMED.  
**Intake:** 2026-11-05, Softmux [Draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239).  
**Evidence baseline:** product implementation `b8ef01b372cf2299cbc56f30e6b1b10ee457ac2f`; V3 Pilot [#41966549198](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549198), SUCCESS. Visual evidence [artifact 13387079096](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41966549198/artifacts/13387079096).

## Direct observations

The real source ASS case generated `ui-v3-ass-source/v3-native-ass-preview-820.png`, `-620.png`, and a browser JSON receipt `passed:true`. On the 820px screenshot the image visibly presents black without the expected glyph. Sampling the actual visible image rectangle (~390×218) yields **0 pixels above 150 in any RGB channel**, despite a loaded `blob:` PNG and status naming FFmpeg/libass. The artifact's `proof.ass` includes a WHITE dialogue at 0.10–1.40 s (`V3 ASS Native Preview`), and the UI preview time is 0.75 s. Running a separate **native** FFmpeg/libass compositing check on the same supplied ASS on a black 640×360 frame at 0.75 s yields ~2560 bright text pixels. This proves the fixture has drawable content; it does not prove native and browser-WASM font configurations are equivalent.

The original V3 E2E `tests/e2e/v3-source-ass-preview.e2e.mjs` checked `img.complete`, `naturalWidth > 0`, screenshot position and native extraction, **not actual subtitle glyphs**. Thus its green status is compatible with a visibly empty preview. The sampled source had **zero embedded font attachments**, so unavailable browser-WASM fonts is plausible but **unconfirmed**; time shifting, filter behavior, and runtime/font-provider configuration must also be investigated. This does not show that all ASS previews fail or that all fonts are unavailable.

## Product-branch correction / test status

- Visual audit filed on PR #239: `docs/ui-v3/V3_EXACT_HEAD_VISUAL_REVIEW_2026-11-05.md`, commit `ccde933d987aa1626285e05a246c8688f628b093`.
- New controlled browser test at `351dc3d892caee502e664f2637928f7bf06b2f80` captures `previewImage` into a same-origin canvas, records `previewContentPixels` in the existing evidence JSON and requires >=100 bright pixels for this **specific white-on-black active ASS fixture**, after the original extraction/authorization safety checks. It does **not** assert that arbitrary user subtitles must be bright or provide universal raster similarity.
- **New exact-head CI PENDING** at intake. An expected red result must not be relabeled as existing Green; determine font selection and actual frame pixels, then fix the product preview or correctly refuse unsupported render/fallback without inventing visual completion.

## Reuse / disposition

Extend the existing visual-evidence body of knowledge but register this **concrete screenshot-backed product bug** separately for tracking. A generated image file, valid dimensions, and exit-code success are not evidence of correct raster content. For deterministic fixtures, acceptance requires a content-sensitive oracle tied to known text/color/time (or a reliable independent renderer), with font identity, locale and runtime distinctions recorded. No Canonical change and no automatic default V3 merge.


## Exact-head red result — confirmed 2026-11-05

On product commit `351dc3d892caee502e664f2637928f7bf06b2f80`, [V3 pilot #41973336353](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41973336353) completed **FAILURE** at the actual Chrome `v3-source-ass-preview.e2e.mjs` pixel assertion, while its previously exercised real single-source Stream Copy extraction, exact-File identity and authorization checks continued through the test. Downloaded [artifact 13390508216](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41973336353/artifacts/13390508216) contains `ui-v3-ass-source/evidence.json` with the measured **source preview PNG 640×360, brightPixels=0**, `passed:false`, the precise content-pixel assertion, and an intact standalone `real-source-extraction.ass` verified by hash. This rules out an earlier screenshot-only dark-theme optical illusion: the actual browser-generated image content is blank for this specific white-text fixture.

Status updated: **REPRODUCED / OPEN / exact-head V3 CI RED**. Root cause still unresolved. This does not invalidate prior successful native mux and S12 results on their own scoped heads; do not merge Draft PR #239 until the font/render/time issue and controlled content test are resolved. No Canonical change.

## 2026-11-05 verified fix: WASM font provider, overwritten explicit fonts, fontselect grammar

**Disposition:** FIX VERIFIED IN SCOPED REAL CHROMIUM V3 PILOT (not whole UI acceptance). Product [Draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239), exact HEAD `e753c91c658d7cb4d41d6f9d58432d69918cbe31`, [V3 Pilot #41977713226](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41977713226) **SUCCESS**, uploaded screenshot/receipt artifact [13391943973](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41977713226/artifacts/13391943973). S12 and Pages completed SUCCESS at the same SHA when inspected; full Browser E2E remained in progress at the last intake query, so never ascribe full-suite PASS to the latest head until checked.

**Root-cause chain, based on actual failing evidence (not conjecture):**

1. `351dc3d8` controlled visual oracle: active white ASS cue on black actual 640×360 frame had `brightPixels=0` despite successful `blob:` PNG and FFmpeg code 0. [#41973336353](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41973336353) RED. The later diagnostic artifact recorded actual FFmpeg.wasm libass `can't find selected font provider` and **0 source attachments**, proving the isolated renderer had no font provider; Chromium host fonts do not automatically populate the WASM virtual FS.
2. Product preview for source-embedded ASS replaced `let fontFiles=selectedFonts()` wholesale with `fontFiles=await readEmbeddedPreviewFonts(...)`. An explicit external `DejaVuSans.ttf` (759,720 B) was present in the native input, yet the source branch logged **0 external fonts**. [#41976990625](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41976990625) tested the merged selection and recorded both `0` source fonts and `1` explicit font, with actual `Loading font file ...font-0.ttf` and `fontselect: (DejaVu Sans, 400, 0) -> DejaVuSans, 0, DejaVuSans`.
3. A provisional fail-closed guard incorrectly parsed only `fontselect: ... -> (` while this genuine libass build emits an unparenthesized resolved family. It therefore falsely rejected a selected face. Corrected guarded parsing accepts real non-null targets, not any FFmpeg process exit. Test also anchored `^预览帧：` so `无法生成预览帧：` cannot be misclassified as success.

**Verified result:** In exact-head artifact `ui-v3-ass-source/evidence.json`, `noFontProviderRefusal=true` for the first no-font pass; the second pass reports `explicitFontInput: DejaVuSans.ttf`, `previewContentPixels={width:640,height:360,brightPixels:2391}`, `passed=true` with `fontselect` to DejaVuSans. The actual `v3-native-ass-preview-820.png` contains white glyphs; the native standalone ASS extraction and source File identity checks also pass. Product keeps original source font attachments first, supplementary explicitly selected fonts second, bounded to 32 fonts / 8 MiB each / 32 MiB total in the embedded-source preview branch, and displays provenance separately. No extra renderer, no writer admission, no implicit target, no shipped system font file.

**Scope:** The pixel oracle is valid only for this controlled white-text/black-background active cue, NOT arbitrary subtitle colors, animations, CJK coverage, all fonts, or real hardware. This entry is an evidence-based fix observation; no Canonical edit. Whole 11-screen Figma + physical device/accessible controls acceptance remains pending; PR #239 remains Draft and default UI unchanged.
