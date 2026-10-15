# Case: HSR Studio — double-painted subtitles, project-font fallback, hardcoded bilingual allocation and false affordances

Date: 2026-10-15
Source: User's three Android browser screenshots, font-selection and true ASS render report, plus HSR repository code.
Product work: [HSR-Voice-Archive-Builder PR #169](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/169)
Level: **Case**, not Canonical.
Status: **implementation in PR; exact-head Chromium/FFmpeg validation and physical device/user acceptance pending**.

## User-visible failure evidence
- In Layout, importing HYQiHei caused the fast geometry preview to show overlapping/ghosted text from old and new fonts, while the real FFmpeg/libass frame appeared to use a system fallback.
- The user could not find a UI control for the source/translated vertical-area allocation; source inspection confirmed `primary_region_height = available_height * 0.60` was hardcoded in the solver and geometry preview.
- The imported font was listed in the interface, yet the redundant "view imported" button and "import and save" action allowed a selection to be confused with a new upload.
- Layout still exposed Standard/Plain/Karaoke presets, an appearance panel without reliable fast-preview correspondence, and a timing section hidden by an earlier Layout-mode CSS rule.
- Effects exposed a local WhisperX word-alignment button despite the user-side Termux runtime reporting unavailable `whisperx`/`torch` dependencies. This is an unavailable runtime capability, not evidence that a usable forced aligner exists.

## Concrete causal findings
1. `renderPreviewCanvasSvg` rendered the text glyphs in SVG and then called `renderCanvasSubtitleOverlay` to paint the same glyphs again with different font metrics. Duplicate renderers are the direct mechanism for visual doubled glyphs.
2. Imported font files were stored under the project `subtitle_fonts` directory, but ASS/geometry measurement used `resolve_font_path` from system font locations. The `fontsdir` FFmpeg option *loads* local font files, but does not itself guarantee Fontconfig will prefer the project copy over a same-named installed font.
3. libass's `fontselect` log can identify the selected PostScript face without revealing the underlying font file; checking its output for a SHA-named upload file path is therefore incorrect. Scope Fontconfig to the project with a temporary configuration, run `fc-match` in the same environment to verify the resolved path, and surface fallback as an explicit failure.
4. A new region control needs a complete data path: UI -> both FastAPI and Termux Lite settings endpoints -> persisted ProjectConfig -> shared SubtitleRenderConfig -> geometry and ASS solver -> true FFmpeg still/video. Merely showing a 60/40 slider would not fulfill the request.
5. A disabled or hidden local word-alignment feature must say what prerequisite is missing and provide a valid alternate workflow; fabricating per-word timing is not an acceptable fallback.

## Work tracked in PR #169
- One authoritative geometry glyph layer, eliminating simultaneous SVG+Canvas text painting.
- Project-font-aware geometric measurements and real-FFmpeg font selection checks; application and persistence of an already imported font no longer require another file upload.
- New persisted adjustable source/Chinese vertical share, default 60/40, range 20–80; used by both geometry and ASS.
- Preset and redundant imported-font viewing removed from the active UI; timing made accessible from Layout.
- Fast geometry preview explicitly described as not simulating glyph effects such as `\blur`, outline and shadow; verification belongs to real libass.
- Word-level generation hidden when the processing host lacks WhisperX/PyTorch, while validation of imported JSON remains available.

## Reusable boundaries
- Never paint same content with multiple preview renderers unless intentional composite layers are independently controlled and tested.
- A successful file upload, a matched family name, and successful FFmpeg completion are three different propositions; proof of the actual selected project font must examine the font provider's resolved file.
- Satisfying a configured preset does not make an irrelevant or misleading control useful.
- Explicitly distinguish capability unavailable due to runtime dependencies from a working product feature.

## Verification and disposition
Foundry searches on `fontconfig subtitle imported font fallback`, `double-render SVG Canvas subtitles`, `HSR studio timing 60 40 ratio`, and `Word alignment Termux WhisperX unavailable` found neighboring HSR observations/cases but not this combined causal case. Keep as one issue-specific Case rather than promote a general normative rule based on a single product report.
Exact-head CI, physical Termux rendering with the reported HYQiHei file, and user visual acceptance remain **Pending**. No Canonical change.


## Exact-head verification and mainline disposition (2026-10-15)

- PR #169 exact head `178b99867a07e13aa918116094a7178b08a02133`: [Python 3.11/3.12/3.13 + Termux checks](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38648609153) **success**, [Chromium interactions + actual libass media check](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38648609168) **success**.
- PR #169 merged into `main` at `de69be2b1465469e74f477ff0dc344accbc56e6e`; main branch independently fetched and confirmed V4 source, 60/40 ratio solver and project-font-config render path.
- A first CI run was red because the old browser harness tried to click a deliberately hidden preset; a subsequent run exposed a test ordering mistake (editing Typography while Appearance was open). Tests were updated to follow visible user interaction. The final run also explicitly checks that Layout's expanded timeline can be operated, not only Effects'.
- **Scope limitation**: This verifies the implementation and representative imported-font/libass behavior on CI, not the user's specific HYQiHei binary or Android hardware. Full arbitrary glyph coverage is not established by `fc-match` for a font family alone. Unsupported Termux WhisperX/PyTorch means true local word-level forced alignment is **not implemented on that device**; only reliable disabling and JSON import are delivered. These two validations remain **Pending**, not Canonical claims.


## PR #170 follow-up: renderer exclusivity, font face evidence and UI truthfulness (2026-10-15)

The user showed continuing V4 failures after PR #169: imported Chinese fonts in geometric vs real FFmpeg render appeared visually superimposed, explicit font files sometimes rendered via fallback, 60/40 share and Layout timeline remained undiscoverable, dead style presets were visible, and real-render appearance controls appeared inert. This is a **follow-up to this same case, not a new Canonical rule**.

[HSR PR #170](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/170) was merged into main at `2a4c3b2e62b67a2698833e43801d6c0697955a61`. Its exact head `05a8921d848b0a900895c8025521c6e4346c7cae` passed [Python multi-version + Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38680338007) and [Chromium + FFmpeg/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38680338032).

Verified repair scope:
- Browser geometry SVG/Canvas now switch off while actual FFmpeg frame/video is visible; the two renderers cannot independently paint conflicting glyphs on the same frame. Explicit geometry choice restores geometry.
- Uploaded-font proof now requires the same isolated Fontconfig environment to resolve to the uploaded file (`fc-match`), and libass `fontselect` must report the intended face. Crucially, **fontselect may contain a resolved font file path OR only a PostScript face name**, dependent on libass build. Requiring a SHA-named file in all logs caused false negatives; checking only requested family name caused false positives. Unit tests cover path success, face-only success, path fallback, and face fallback. This is a bounded match, not complete glyph coverage.
- An imported-font action no longer reports successful real use merely after file upload, CSS FontFace load or settings persistence; it triggers true libass preview and treats failure as error. User's exact HYQiHei binary / Android Fontconfig remains **device Pending**.
- Bilingual 60/40 range is promoted in Position/Safe Area and visible on coarse touch beside its numeric stepper; Layout no longer hides timeline through legacy CSS; unused preset group and redundant list of already-imported font files are absent from active interface.
- Real ASS still render can refresh after explicitly armed visual changes (650ms after commit, not on each pointer move); background glass/entry/fade settings have disabled dependent inputs until feature enabled. This repairs misleading “adjusted but nothing changes” affordance without pretending fast geometry supports glyph effects.

Remaining **Pending**: exact user-provided font binary selection and full CJK glyph coverage on Termux; actual end-user visual acceptance of Layout/Effects; word-level forced alignment on Termux without WhisperX/PyTorch. The current product has a validated JSON import path, but **no native on-device alternate aligner**; never fabricate timings by equal division or imply local generation works. No automatic Canonical edit. De-dup performed using existing case and neighboring candidate searches.
