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


## PR #171 follow-up: accordion semantics and glyph-level fallback honesty (2026-10-15)

User continued reporting that the imported font rendered with a different face, that the 60/40 share remained effectively undiscoverable, that imported fonts were listed redundantly, and that word-time generation was unavailable in Termux. Inspecting latest product `main` *after* PRs #169 and #170 revealed a second, distinct, user-facing cause:

1. Three Layout `<details>` panels ("文字与字体", "位置与安全区", "外观与可读性") shared `name="hsr-style-parameter-groups"` and `open`, creating a browser-native **exclusive** accordion. The Studio-mode switch also forcibly opened *only the first* group. A wired, persistently saved slider was therefore not visible until the user discovered a buried panel. PR #171 removes the accordion `name` on these and Effects panels and opens Typography + Position together by default; Readability stays optional. This is a concrete DOM semantics/design regression, not a missing mathematical 60/40 feature.
2. The font picker previously called `ensureHostFontLoaded` but applied the chosen family even when it returned the unmodified family name, signalling browser fallback. PR #171 leaves the current choice alone when the FontFace load fails and reports a failure.
3. A valid Fontconfig resolution via `fc-match` doesn't guarantee every selected font contains each character. PR #171 now rejects real libass logs reporting `Glyph 0x... not found` for codepoints present in the current text. The first regression test exposed an erroneously double-escaped regex (`\\s` in a raw Python string); corrected to `\s` before exact-head green CI. It does **not** prove full coverage of an unavailable user-specific HYQiHei binary on Android; that remains device Pending.
4. The nonauthoritative second Canvas subtitle layer is explicitly hidden and cleared. The duplicate imported-font list is removed from visible UI while the main font browser still includes imported families.
5. WhisperX/PyTorch absence in Termux is made explicit through a **visible disabled** real-generation action plus machine-specific explanation; a hidden control is neither a working implementation nor transparent capability communication. Actual on-device forced alignment remains unsupported; validated external JSON import stays available.

Evidence: [HSR PR #171](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/171), exact head `4b31dd98b333a2018bde7984d822f865984b2431`, [Python 3.11/3.12/3.13 and Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38683051058) **success**, [Chromium UI and actual libass media](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38683051057) **success**; merged into `main` at `49e7f18e13ca51ad4fa263311de5bf45007ab280`. Subsequent real HYQiHei device playback, font-specific CJK coverage and automatic Android word timing are still **Pending**. No Canonical edit.

Intake de-dup searched `accordion name attribute hidden controls`, `font picker silent fallback`, `termux WhisperX user-visible capability`, and `HSR 60/40 hidden typography`; found this existing Case as the correct referent and appended instead of creating a duplicate Bug/Case.


## PR #172: same-family asset replacement and browser FontFace cache invalidation (2026-10-15)

After prior PRs #169-171 passed CI and merged, the user requested continued work on font fallback, double glyph previews, appearance controls and unavailable word alignment. A new, independent provenance defect was found: `import_project_font` stores assets by content hash; importing different bytes with **the same internal SFNT family** left both old and new files in the same project's `subtitle_fonts`. `project_font_for_family` enumerated sorted filenames rather than an authoritative latest family selection, while libass `fontsdir`/Fontconfig was free to choose either file. Additionally, the web `hostFontFaces.delete(family)` only removed Map bookkeeping, not the old `FontFace` already registered in `document.fonts`; asynchronous pending loads could resurrect it, and a different project sharing the same family name could reuse its bytes.

[HSR PR #172](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/172) proposed a bounded cross-layer fix: after the new validated asset is durably written, safely retire previous matching-family files (not unrelated families), invalidate the registered browser FontFace and any pending generation, and drop cached font faces on project switch. Tests cover different hashes sharing one SFNT name and a **real FFmpeg/libass render after same-family reimport** (CI permitting). The original SVG/Canvas duplicate-render guard remains checked. Previously inert appearance effects now schedule a debounced true FFmpeg preview upon committed outline/shadow/Blur/card changes, rather than implying SVG geometry reproduces real glyph effects.

On Termux missing WhisperX/PyTorch, the action is now hidden (the capability status explicitly explains why) rather than advertised as a disabled generator. This is a product affordance revision; it **does not deliver on-device word forced alignment**, and validated external JSON import remains the honest supported route.

**Evidence boundary:** Source-level old-vs-new family alias issue is supported by inspected logic; real reported HYQiHei bytes are not available. PR #172 exact-head UI/libass CI and physical Android glyph checks remain **Pending** at this intake stage. No automatic Canonical promotion. Dedup: this is a follow-up under the existing HSR user-report Case, not a new one.


### PR #172 exact-head acceptance and mainline status

PR #172 exact head `7b354cffd7d16f5e2f09a7cfd283e053fcabba2e` passed [Python 3.11/3.12/3.13 + Termux Lite workflow 38685697807](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38685697807) and [Chromium + actual FFmpeg/libass workflow 38685697813](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38685697813). Initial red checks exposed a partial Node test harness referencing an absent font helper and a literal-escaped PNG signature in a new test; both were repaired without relaxing the actual font rendering or timeline checks. The implementation was **squash merged into product main** at `dac71b0f9cc11a8ced19a7e7cf7f113a90b6d80e`.

Specific verified improvements: same-family reimport leaves a single file eligible for Fontconfig/libass, browser FontFace registration of previous bytes is removed and pending asynchronous loads cannot override a newer import, project switch invalidates the font cache, and committed appearance edits trigger a debounced true libass frame. On-device HYQiHei/HYRunYuan appearance/glyph coverage and native Android word alignment **remain Pending**, not claimed resolved. No Canonical modification.


## PR #173 browser evidence provenance regression (2026-10-15)

Product PR [#173](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/173) had an exact-head Chromium failure at commit `95595d720d20ca6392dbd45389dd2b8aebc235f8`. The real Chromium video **had decoded successfully** (`readyState=4`, playback source `blob:`, no media error), and `data-preview-evidence` correctly reported `video-image` because the sole reference backdrop is the bundled red-clouds WebP. `tests/browser_visual_evidence.py` line 368 still required the obsolete `video` evidence value used for plain-color footage. The 20-second wait timed out even though video was playable. Later in the same test, the expected `video-image` provenance had already been asserted, proving an internal fixture expectation inconsistency.

Repair commit [`ab92a074`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/ab92a0741fef808737c7a31218197bd739de2ddf) corrects the **first** evidence assertion to `video-image`, preserving `readyState>=2`, visible decoded playback, and downstream active-video interactions. It does **not** accept an absent/undecoded video or suppress the test. Exact-head [Chromium+libass run 38692052061](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38692052061) and [Python/Termux run 38692052088](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38692052088) completed **successfully**.

Reusable case detail: when renderer source classes evolve from generic `video` to `video-image` or `video-footage`, browser acceptance must assert both actual decode/playability **and provenance identity** consistently throughout the same test. A state mismatch can falsely surface as a time-out; include media diagnostics to distinguish playback failure from stale evidence expectations. This is appended to the existing HSR case rather than creating a duplicate or modifying Canonical. Physical Android/HYQiHei/Karaoke user acceptance remains Pending; passing CI here is not evidence of those device-specific outcomes.


## PR #177: missing style feedback during real renderer failure and touch repeat (2026-10-15)

New field screenshots at 15:07–15:08 show an unresolved Termux dependency error ("no fc-match") despite main already containing the launcher bootstrap from PR #174. This is **user-device evidence of missing executable discovery in the *running* HSR process**, not proof that FFmpeg/libass is broken on every Termux installation; updating GitHub or refreshing the browser does not provision packages into an existing Termux environment. A UI project-font success badge remains unearned until the executable is installed and the libass path re-tested.

Distinct direct source findings on main `6a507d57c36beb9a4761453e724faf0798ee12f7`:
- Browser SVG geometry text stroke was hardcoded to `Math.max(2, font_size * 0.08)`; shadows, Blur, backdrop and multi-outline were absent from the visible geometry layer. A real FFmpeg failure therefore made changing Appearance appear inert.
- Coarse-touch numeric steppers handled `click` only; no hold-repeat/cancellation/keyboard semantics were implemented.
- Mobile slider caps 8 / 8 / 2.5 were below the backend preview clamps 12 / 12 / 5, and out-of-range numeric input was silently clamped, without stating this was an implementation constraint rather than an ASS format limit.

[HSR PR #177](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/177) re-lands a coherent repair onto main (initial SHA `e0097771226569a78539881757d169c5796554ed`):
- Preserve strict fc-match and libass actual-file/face/glyph proof; add executable Termux prefix lookup and explicit install + process-restart diagnostic. Preflight reports missing fontconfig but does not silently install from an HTTP request.
- Add responsive SVG **approximate** appearance feedback (outline, shadow, Blur, card, multi-outline) while explicitly **refusing** to elevate it to actual ASS visual evidence. True FFmpeg/libass rendering remains the only result authority.
- Add delayed pointer repeat and cancellation; keep single click/keyboard step; align UI caps to backend and expose input errors rather than silently forcing numeric bounds.
- Add source regressions. At creation, both exact-head Python/Termux and Chromium/libass GitHub runs were `in_progress`; **CI Pending**, **user Android/Termux Pending**.

Reusable scope-bound observation: when the authoritative renderer is unavailable, a fallback preview must continue to communicate user intent *without impersonating final rendering*; input/renderer bounds and press-and-hold behavior must be explicit and tested. No claim of validated 100% pixel parity, end-user acceptance or root-cause elimination without device `fc-match` evidence. Same ongoing HSR Case family; no new Canonical claim.
