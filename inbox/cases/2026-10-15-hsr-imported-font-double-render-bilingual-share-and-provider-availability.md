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


## PR #178: Termux fontconfig-utils provider corrected by physical device log (2026-10-15)

New physical Termux evidence at 15:27 contradicts the earlier package assumption retained in PR #174/#177: `pkg install -y fontconfig` reports `fontconfig is already the newest version (2.18.1)`, yet `command -v fc-match` yields no path, `fc-match -V` says `The program fc-match is not installed. Install it by executing: pkg install fontconfig-utils`, and Python `shutil.which("fc-match")` returns `None`.

This is a **confirmed dependency-provider mismatch** in this Android/Termux environment, not an assumption that an already-running process merely had a stale PATH. Installing core `fontconfig` cannot remedy a missing `fontconfig-utils` executable on the observed package split.

[HSR PR #178](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/178), head `47fe1dbee6d7e2fa806c7e17b2aba7f76d4f8166`, changes both Termux launchers to `pkg install -y fontconfig-utils` if `fc-match` is missing, verifies executable availability before the server starts, updates real-preview and preflight errors/docs, and replaces the previously wrong launcher contract test. Strict project-font and libass verification is preserved.

Dedup: this is a corrective *extension* of the existing HSR imported-font/Termux case family, **not** a new speculative global Fontconfig rule; package ownership may differ on other distributions. Product code PR #178 is submitted, initial exact-head CI **in progress/queued**, user installing the corrected package and repeating true ASS render **Pending**. No canonical change. The prior case's recommendation to install only `fontconfig` must be treated as invalid for this observed Termux environment.


## PR #179: real-font success reveals geometry-vs-libass authoring divergence (2026-10-15)

At 15:30–15:32, after correcting Termux's `fontconfig-utils` executable dependency, four on-device screenshots for the same HSR Layout studio show a now-successful actual `FFmpeg/libass` frame beside a browser geometry SVG preview whose font weight, vertical occupation, line breaking and visible outline differ substantially. This is a higher-severity authoring correctness case: semantic segmentation and subtitle positioning cannot be approved against an unfaithful renderer.

Direct source findings on `main`:
- Layout preview is rendered as SVG using browser shaping and an artificial `font-weight=600` while the ASS writer's actual style uses `Bold=0`. Its line positions and bounding boxes are mathematically estimated, with PIL metrics optional and heuristic character widths when unavailable. Even if `solve_subtitle_layout` is shared, **the rasterizers are not semantically identical**.
- Project Layout initial/default UI shows geometry; `queueLiveRealPreview()` previously only ran when manually armed or certain appearance changes armed it, so day-to-day segmentation might follow geometry rather than actual libass.
- `subtitle_layout/breaker.py` offered split points immediately after apostrophes, allowing English contractions/possessives to break across lines (e.g. `That's` -> `That'` / `s`).

[HSR PR #179](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/179) initial head `273b7ba086462b1106fe2c3da9de23d0c9283a3f`:
- Makes an automatically refreshed, input/sample-identity-checked genuine libass still frame the authoritative current-cue Layout authoring surface; honors manual temporary geometry inspection but resumes true render after next edit.
- Keeps the geometry SVG explicitly marked as unverified auxiliary diagnostics, removes its misleading bold weight and no longer reports an estimated-safe geometry state as actual layout approval.
- Prevents English apostrophe splitting in candidate breaks, with regression tests for contractions and explicit ASS writer-vs-solver planned breaks.
- Distinguishes single-cue real render success from **full archive raster coverage**; records pending full-corpus ink bbox, text reflow and timing validation in [HSR Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176).

Epistemic boundary: This is **implementation submitted, exact-head CI Pending**. Field evidence supports successful **one-device real libass frame**, not whole-corpus consistency, final MKV rendering parity across players, or equivalence of SVG and libass. Do not promote a single case to Canonical. Reuse/extend the current HSR case family; avoid creating a parallel overlapping record.


## PR #179 CI regression: stale geometry copy oracle (2026-10-15)

Initial PR #179 CI on head `273b7ba086462b1106fe2c3da9de23d0c9283a3f` failed in two workflows: [Python/Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38700482295) and [Chromium UI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38700482290). Both failures came from **one** assertion in `tests/test_hsr_touch_workbench.py::test_geometry_appearance_is_feedback_not_evidence`, requiring the removed literal copy `SVG 近似反馈，不能验证 libass 字形`. The changed UI communicates the stronger equivalent contract: an auxiliary geometry view is not actual ASS evidence and cannot approve authored line breaks. This is **stale test oracle drift**, not proof of a font render failure. The libass artifact job and Termux-lite surface passed independently.

Same-branch successor commit `7d489e4eebac171639f9b579917b046f363048fd` updates the test to check the intended evidence boundary (`geometry:['辅助几何图（非排版成品）'`, `未经真实验证`, and `不要依据此图定稿；等待自动真实渲染`), rather than the superseded informational wording. [Exact-head Python/Termux workflow](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38701135124) **success**. [Exact-head Chromium/libass workflow](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38701135195) was **in progress** at this writing; it must be independently checked before green claims.

Dedup against existing [MKV-Fast-Muxer E2E assertion drift](../bugs/2026-10-11-mkv-e2e-version-assertion-drift.md): shared failure class is an outdated independent test oracle after production semantic changes, but this case specifically concerns **visual evidence truthfulness** rather than application version metadata. Preserve substantive non-authoritative preview checks; do not simply remove the failing test or automatically promote one occurrence to Canonical.


## PR #180: #179 merged but real preview remained gated by geometry (2026-10-15)

A follow-up "still does not work" prompted inspection of merged HSR `main` `a5be46ce72e10e632d306873a5fedf2370af83e7`. The source contains a distinct, reproducible **workflow-dependency bug**: in `updateLayoutPreview()`, `queueLiveRealPreview()` was inside the success branch *after* `await Promise.allSettled(ensureHostFontLoaded(...))` and a potentially failing or cancelled `/api/subtitle-layout/preview` request. This meant the purported authoring authority (FFmpeg/libass) could be skipped or indefinitely delayed because the explicitly non-authoritative SVG geometry service did not complete. In addition, the queue allowed `document.body.dataset.workspaceTask==='layout'` only even though Layout and Effects share the same visual canvas.

[HSR PR #180](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/180), initial head `5a4fca3ee1f920ce67c9e3aa9861c33dee6134a4`, changes the true-render scheduler to run independently before awaiting optional geometry/font work, on parameter changes and on intra-canvas task transitions, with the existing 850ms coalescing/decode identity safety. It extends the queue to both `layout` and `effects` while keeping it inactive outside the shared canvas. A new Node VM regression executes the actual extracted production scheduling function rather than relying solely on copied UI strings. Exact-head Python workflow `38705018363` **success**; Chromium+libass workflow `38705018377` **in progress** at the time of intake.

Grounding boundary: this is an independently verified source-level *scheduler bug*, not yet evidence that the user's latest unspecified symptom was precisely this branch. Fixing automatic true-render scheduling does **not** mean SVG pixel parity, actual exported MKV frame acceptance or whole-archive sampled ink coverage. The phone's running service must also actually load the merged version. Do not promote to Canonical; append to the ongoing HSR case rather than duplicating cases.


## PR #180 follow-up: fail-closed real glyph ownership and correct Termux font metrics (2026-10-15)

Follow-up user report confirms the original geometry-vs-real-ASS layout disparity remains unresolved. Exact main `a5be46ce72e10e632d306873a5fedf2370af83e7` inspection identified **two independently concrete defects beyond asynchronous scheduling**:

1. `setPreviewEvidence()` shows approximate SVG glyphs not only for manually requested auxiliary geometry, but also while the authoritative libass result is pending, stale or failed. The editor thus still displays **two incompatible candidate layouts as if either might be used to author segmentation**. The new patch keeps the browser layer hidden in all normal/pending/failed/expired states and only exposes it after deliberate `showGeometryPreview()`. First successfully decoded FFmpeg/libass frame is the normal glyph display; no phantom SVG is promoted to actual evidence.
2. `subtitle_layout/measure.py` falls back silently to hard-coded per-character width ratios whenever Pillow is absent. Neither prior `requirements-termux.txt` nor Termux launcher installed `python-pillow`. On Termux this can generate line width plans unrelated to the imported TTF. The two launcher scripts now install/verify native `python-pillow` before launch, improving font-specific metric measurement without claiming Pillow and libass shape identically.

PR #180 initial head `5a4fca3` Chromium **failed** at live video E2E with timeout on `/api/subtitle-layout/render-preview-video` (job `116322174749`, run `38705018377`) even though unit tests and libass artifact passed. Source inspection identified that automatic still rendering calls `clearVideoPreview()` while a user-initiated dynamic FFmpeg video request is underway, and can therefore abort that video transport. On updated head `a8199bfdfebf4dc7c43ac7d1fbde8d8cac1e3227`, video starts by canceling the pending still timer and disarming automatic stills, and the real still queue avoids running while `videoPreviewController` holds the presentation pipeline. Added Node VM tests for explicit SVG ownership and video priority, plus Termux launcher dependency tests.

Evidence state: source patch **submitted, new Python and Chromium CI pending** (`38708781424` and `38708781446`). No claim of final exported ASS pixel parity, verified per-cue glyph ink bounds, actual device installation of Pillow, or acceptance of whole archive. This entry refines the existing HSR Case; no independent Candidate promotion nor Canonical change.


## PR #180 accepted and merged after fail-closed preview ownership (2026-10-15)

Final [PR #180](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/180) head `1620c17c8601a9e1452df6b513fd03138b752c1e` is **merged into HSR main** by commit `576b7ab596c678ce5115d54a12c35ee7789e80f0`. Exact-head [Python 3.11/3.12/3.13 and Termux-lite CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38709266638) and [Chromium UI + libass artifact CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38709266696) both **passed** before merging. The repaired tests assert *only explicit auxiliary geometry* may display SVG glyphs, rather than requiring the deleted misleading error message. The video preview race was checked in the actual browser/FFmpeg path, which had previously timed out.

Engineering scope: true FFmpeg/libass frame becomes the sole *default* authoring glyph view, including pending/stale/failure fail-closed states. The real scheduler is independent of the approximate geometry service. Termux bootstrap now installs `python-pillow` for font-file-specific advance measurement and `fontconfig-utils` for `fc-match`; neither Pillow nor geometry estimates certify libass glyph ink. An actual user Termux restart/update and real imported-font side-by-side validation are **Pending**; whole-corpus exported-frame evidence remains [Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176). CI proof is not user-device acceptance. No Canonical promotion.


## PR #181: imported font proof raced with automatic preview; SVG glyph duplication retired (2026-10-15)

Field screenshots 17:19–17:20 after main PR #180 demonstrated two unresolved observable problems: manual auxiliary geometry rendered a distinct font and line footprint from the real FFmpeg/libass frame despite matching inspector values, and importing `HYRunYuan-55W.ttf` reported "字体未应用：实际渲染未采用项目字体；未保存此字体选择" while another status said the project font was loaded. The user stated first import looked inert and the second import failed.

Source inspection of `app/static/index.html::importCurrentProjectFont()` proved a separate **transactional race**: it synchronously set the chosen family **and dispatched an input event**, which invalidated current render and scheduled automatic preview, before it awaited another explicit `renderLibassPreview()`. The geometry debounce/automatic FFmpeg path could cancel the manual proof. The import code then looked at global DOM `previewEvidence` rather than the returned result of its specific invocation, so a cancelled proof was reported as though libass rejected the uploaded font. A server-side font asset can persist before the separate project-preference save, so "font file loaded" and "font preference not saved" are not equivalent states.

[HSR PR #181](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/181), head `e76ee854d74930c17459e36773bd5dad21ec8c6b`, **merged** to main in `0f7932f38ce2ea63a2016bf22e4828cc701fde93`:
- Introduced serialized font-import validation: prevent concurrent auto redraw; do not dispatch the ordinary input handler before completion; accept the imported preference only on a successful, decoded and identity-matched actual ASS frame, then a successful settings save; retain concrete libass errors and rollback the draft selection on failure.
- Eliminated the misleading second font renderer from *manual auxiliary geometry*. It now displays safe-area/central-gap guides and estimated per-line boxes, not the SVG approximation of text glyphs. The real libass preview alone provides readable subtitle characters.
- Added executable Node VM tests that run the production font import handler for initial success, double tap during an in-flight validation, identical retry, and rejected true proof without preference commit. Retained strict font file/face/glyph checks.

**Exact head CI passed**: [Python + Termux-lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38713640082) and [Chromium UI + actual libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38713640121). Physical Android repeated-import acceptance, post-restart field screenshot and saved/actual-exported ASS corpus equivalence remain **pending**. This repair stops a false failure and a non-authoritative competing visualization; it does NOT demonstrate pixel parity between independent renderers or solve the distinct whole-corpus glyph-ink validation task under [HSR Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176).

Deduplication: extension of the existing 2026-10-15 HSR imported-font Case; no automatic Canonical update.


## PR #182: keep authoritative libass A/B review while preserving diagnostic overlay (2026-10-15)

User identified a fundamental unresolved correctness/interaction problem: the layout solver uses Pillow character advances with a hardcoded `font_size * 1.25` line height, and earlier SVG typography was visibly larger than actual FFmpeg/libass ink. Removing that misleading preview did **not** correct the writer's approximate line-breaking/region-fit model. It also eliminated quick before/after inspection because changing any inspector setting revoked and hid the previous successful rendered frame.

[HSR PR #182](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/182) exact head `1b00f3cb594dbf80a26a8d0fd447beebd032bde1` is **CI green / open, not merged** at intake:
- [Python/Termux workflow](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38719029049): success.
- [Chromium UI / libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38719028985): success.
- A GitHub merge tool action was blocked by host safety checks; no merge or main update occurred. Preserve **Pending: human/authorized merge** rather than claiming release.

Scope delivered on PR branch:
1. Keep the last decoded genuine FFmpeg/libass frame visible but **explicitly stale** while current-style render is queued; the old frame never proves new settings.
2. Decode new PNG in a staging `Image` before identity-safe publication, keeping at most two successful same-cue Blob URLs so before/after switching is immediate and requires no extra FFmpeg. Discard comparison on cue/text/timestamp change or later replacement. A Node VM regression executes the production preview state machine for request races, the guide toggle, frame comparison and release.
3. Draw the existing solver's safe-area/gap/bbox diagnostic guides as a transparent SVG **overlay** over actual libass pixels, never a separate glyph preview. The bbox visibility checkbox is obeyed; labels explicitly identify the text bbox as estimated rather than true ink.
4. Audit status of prior PR #180–#181 repair: those prevented false import proof and competing SVG captions, but never calibrated the solver's text width to real ink.

Remaining correctness debt explicitly assigned to [HSR Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176): define actual glyph/outline/shadow visible ink boundaries keyed by imported font SHA, precise ASS bytes and preview timestamp; compare ink against safe zones and bilingual overlap; then calibrate or rerender/reject export layout choices using actual evidence, without imposing a guessed global size multiplier. Current interactive overlay is **not** a real glyph measurement. Real Android device, exact exported ASS/video and full-corpus pass remain Pending. No Canonical promotion.

Reusable distinction: retaining a correctly identified *stale genuine image* is useful for authoring A/B comparison and not equivalent to presenting an approximate replacement renderer as fresh current evidence. A live diagnostic overlay can share the same rendered image without becoming another content authority. Source/UI regression alone is not proof of font metrics parity.


## Cross-project soft-mux/hardsub comparison for HSR measurement (2026-10-15)

User challenged the unclosed HSR measurement disparity: why is it not solvable when "软封硬压" projects seem to render ASS correctly? Source cross-check established a useful **non-equivalence of problem classes**:

- [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer) accepts already authored ASS and font assets, previews via FFmpeg/libass, and has *bounded CI proof* extracting ASS/fonts independently from its output MKV and rerendering them in controlled libass. Source/delivered libass frames are byte-identical for the controlled `ass` path, and a different `subtitles` path meets an SSIM threshold. It is **not** an automatic line-break/font-size layout optimizer. Its planning report expressly forbids duplicating a full ASS editor.
- [Quick-Automatic-Hardsub-Encoder](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder) uses real source video frame + actual ASS/fonts + FFmpeg/libass to create preview, parses actual fontselect logs, then burns subtitle with a real subtitle filter; it also supplies source-backed rendered reference and decoded final output-frame comparison. It avoids a browser glyph simulator; it does **not** certify arbitrary per-cue safe-area-solving accuracy.
- [HSR](https://github.com/11576865/HSR-Voice-Archive-Builder) uniquely solves `break_line` and `solve_subtitle_layout` using `measure_text_width` (Pillow or fallback width ratios) and `measure_line_height=font_size*1.25`; these synthetic metrics inform the generated ASS positions/line counts, whereas the final font ink is emitted by libass. Hiding SVG or comparing two true PNG frames cannot resolve the **solver input-metric mismatch**.

Reusable engineering direction: keep fast heuristic/semantic candidate generation but make libass raster/bitmap coverage the **acceptance oracle for layout**, not just for appearance. For a prospective candidate, render controlled text-only current-face layers on transparent/known backgrounds (or use native libass ASS_Image extents), measure per-line source/target ink + outline/shadow separately, compare true occupied area against configurable safe zones and central gap, and feed violations or underutilization back to bounded line-wrap/font-size candidate search. Attach evidence to exact cue text, face/content hash, override tags, output geometry, and timestamp. Distinguish visual glyph-ink bounds from advance/line-wrap metrics; screenshot overlay guides remain non-authoritative, and a static factor is not a reliable font metric correction. Cache measurements per stable immutable font/cue/style identity; avoid FFmpeg subprocess per slider event. Verify final authored/exported ASS by rerendering representative/all requested events with the actual export renderer and font dependencies. Any unverified case is Pending, not "safe".

This is a **proposed engineering resolution, not an implementation or CI-verified HSR fix**. Dedup with existing HSR Case and Issue #176; no Candidate-to-Canonical promotion.


## PR #183: render-in-the-loop ink fit merged, 2026-10-15

[HSR PR #183](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/183), exact head `ee2c1aab89c8c3a28c89a9fc526a28e1b78a165b`, **merged** as main `70eda529538a0d9c82c35d674581a3bcb884402e`. This converts the preceding proposed solution into **bounded implemented evidence**, but not whole-corpus device certification.

Change summary:
- Added `subtitle_layout/libass_ink.py`: each candidate's original and Chinese subtitle layer is drawn by actual system FFmpeg/libass at ASS 1920×1080, intended font family/size/anchor, outline/shadow/blur/multi-outline, to controlled RGB24 background; checks actual visible pixel-ink bboxes, safe margins and true bilingual central separation. Uses optional Pillow accelerator or a pure-stdlib raw RGB24 scanner (works in Termux-lite), with bounded probe-result cache keyed by content/style/font file identity metadata.
- The `solve_subtitle_layout` scaling sequence 100→95→90→85% is now accepted/rejected by **real ink**, rather than by Pillow rectangles, when oracle enabled. `render_ass` uses observed per-cue, per-language real ink/Pillow width ratios to propose revised line breaks; proposal must independently pass libass and cannot increase source/target line count. This is *not* a hard-coded HYRunYuan font multiplier.
- Fixed `collision.py` omission of the resolved font file path in its legacy horizontal check.
- Real pixel acceptance is enabled explicitly in `app/ass_preview.py` for genuine preview and `app/subtitles.py` for project ASS export. Other standalone pure-Python callers stay deterministic and do not silently start native FFmpeg. Exact-head project font-upload browser evidence exercises the real preview route.
- Verification: [Python 3.11/3.12/3.13 + Termux-lite + independent real-libass-ink job](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38724191545) **success**; [Chromium UI + libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38724191554) **success**. The real ink job constructs genuine 1920×1080 RGB24 data and an independently emitted verified ASS.
- Real no-renderer state **fails closed** for the explicitly enabled project path; old text editing tests use mock oracle only for irrelevant persistence assertions. A separate job proves the actual oracle.

Safety/acceptance scope:
- **Pending physical Android imported HYRunYuan-55W.ttf acceptance** and repeat-edit performance, as no screenshot from device after this main commit yet.
- Actual still-frame layout ink boundaries are measured. Full continuous ASS animation, card/HUD and player-specific output raster equivalence, exact all-event temporal sample coverage, and a full final MKV extracted-font audit are **not** established by this PR. Font face selection remains verified on the separate existing full-preview route; the oracle's font directory metadata-key cache is not a full SHA-bytes provenance contract. Track remaining work in [HSR Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176).
- This is an extension of the same HSR case family, not an independent universal typographic law. Do not change UIGS Canonical based on a single product's CI fixture.

Cross-project transferable observation: distinguish *raster-proven fit* from *estimated shaping/semantic line-break candidates*, use the real renderer only as bounded acceptance oracle and a measured candidate-specific correction, and keep ordinary UI tuning responsive through cached visual states. Integration and deployment must not conflate CI pass and actual user font proof.


## PR #184: grouped rendering-preview entry and nonblocking diagnosis (2026-10-15)

User-facing issue: after main #183, top-level **辅助边界** remained outside **画布与诊断**, which separately exposed safe-zone/center-gap/estimated bbox toggles. There was no clearly named **pre-export subtitle preview entry**; the genuine frame trigger was ambiguously named “实际 ASS 渲染”. The prior #182 visual A/B and overlay PR was open on an older base, so none of its capabilities was deployed.

Resolution [HSR PR #184](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/184) was **merged to main** at `bb4a4cadcbd0f64e9803644ea3da1c18723041d9` (exact tested head `3fc56d50c3bb6cdc79123697347d72f67420508c`):
- Clearly labels the main action **预览当前字幕（不导出）**: it calls actual FFmpeg/libass for current unsaved inspector settings, independently of final ASS export.
- Moves the former ungrouped “辅助边界” action into a **default-expanded 画布与诊断 · 渲染前布局预估** area as **渲染前预估（仅边界）**, adjacent to safe area, central gap and estimated text bbox controls. The preview estimates use guide rectangles only, never browser glyphs or fabricated font size parity.
- Carries #182's real FFmpeg decoded-frame ownership, explicitly stale old frame display while new frame is pending, bounded previous-vs-current true-frame comparison, and SVG guide overlay on the true image. Closed #182 as superseded/unmerged after #184 merge.
- Adds a diagnostic-only redraw entry, consuming a synchronous flag at entry of the unchanged `async function updateLayoutPreview()`, so guide toggles and rapid estimate do not trigger fresh FFmpeg or invalidate in-flight actual rendering. Preserving the production function signature was necessary: initial CI showed concrete regressions in test fixture source extraction when the signature changed. Restore/verify original signature, not weakening existing editor tests.
- Shows geometry-only preview as neutral unverified (not green “passed”), repairs estimated-bbox checkbox behavior.

Validation: exact-head [Python 3.11–3.13 + Termux-lite + real libass ink CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38727029280) **success**; [Chromium UI + libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38727029439) **success**; merged main was independently confirmed. User's physical Android browser screenshot and actual repeated fast-preview performance remain **Pending**, not silently promoted to acceptance.

Transferable case insight: an authoring UI should distinguish *candidate-estimate view*, *true renderer preview of unsaved edits*, *A/B of two true renderer outputs*, and *saved/exported artifact*, place each control under the subsystem owning it, and never let non-authoritative diagnostic-only toggles reenter the expensive authoritative pipeline. Real-render comparisons do not eliminate all full-corpus runtime/animated ink acceptance debt under HSR Issue #176. This updates an existing Case after dedup; no Canonical change.


## Follow-up: real ASS preview must be opt-in; import validation and expired overflow diagnostics (2026-10-15)

**Status:** Source-verified observation / field revalidation pending; does not promote Canonical.

- Android user evidence showed parameter edits repeatedly starting FFmpeg/libass real-frame rendering despite an explicit pre-render quick-preview control. In `app/static/index.html`, the Layout state had armed `liveRealPreviewArmed` during project load and `updateLayoutPreview()`; its 850ms timer then invoked `renderLibassPreview()` automatically. The direct `main` correction `3aadf1f3d2567b79a2e28059c276f9d5bced1b1b` makes Layout use browser quick preview by default and guards its automatic real-render scheduler, while retaining the manually invoked real ASS button and the existing Effects scheduler. V8 production-function mock checks for Layout exclusion, Effects scheduling and stale-frame deduplication passed. Full browser/device validation is not claimed.
- User's imported `HYRunYuan-55W.ttf` reached the font-load/ASS-validation boundary; error `ASS rendering blocked: 1 subtitle entries failed layout` is thrown by `subtitle_layout/ass_writer.py` when the actual preview's one representative entry fails a placement constraint. This does **not** by itself prove a corrupt font or libass font-face mismatch; the font importer currently rolls back applying the family if mandatory real preview fails.
- The diagnostic hint from `app/ass_preview.py` names `overflow.json` under `tempfile.TemporaryDirectory`. If `write_ass()` raises before the response is returned, the context manager deletes the directory, leaving a diagnostic path that users cannot subsequently inspect. This is a **source-grounded diagnostic-lifetime defect**, not yet a separately patched feature or device-confirmed reproducer. A future user-authorized fix should preserve actionable overflow details in the error response or at a durable diagnostic location without weakening font-face validation.
- Subtitle artifact receipt state (`unverified`) does not imply automatic export on a style change. Layout's repair action is a manual ASS/SRT refresh; saved subtitle display-time changes may legitimately update SRT timestamps. These operations should remain distinguished from style autosave and real-render preview.

**Deduplication:** Extends this same HSR imported-font/preview Case and the earlier `2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md` Case. No new Canonical rule.


## Follow-up: audio-clock ownership, bounded shrink, isolated font proof, ASS-only autosave (2026-10-15)

**Status:** implementation in HSR `main`; source and bounded JS probes completed, hosted CI and target-device validation **Pending**. Remains a Case, not Canonical.

- **Unauthorized editable timing was a domain-ownership defect.** `subtitle_timing_overrides.json` enabled arbitrary +/-5s display-time changes without changing audio. The corrected effective output window comes only from archive audio start/display end (including audio-derived gaps). The legacy JSON remains on disk for provenance but is ignored by UI and both SRT/ASS export. New timing mutations are rejected by the model; Layout/Effects no longer expose editable cue-time controls, while the Effects timeline remains available as read-only navigation.
- **ASS and SRT have distinct invalidation causes.** Source text/audio changes continue to update SRT, while saved ASS style changes schedule a debounced ASS-only regeneration. The `ass_only` refresh path reads existing manifest/corrections without rewriting SRT, manifest or CSV. Manual recovery is labeled ASS-only, no longer advertises SRT regeneration from the styling workbench. Strict long-file refresh and raw source edits remain separate flows.
- **Auto-shrink must exhaust its declared safe range.** The previous solver tried only 100/95/90/85 percent. The new bounded search continues in 5-percent steps to 25 percent; successful estimated downscaling and exhaustion are reported in the stage status. The lower bound is a readability constraint, not a guarantee that arbitrarily long text will fit.
- **Font identity validation must not depend on a stress-test subtitle's length.** Import now requests a short representative FFmpeg/libass font-match proof using the selected project font. A long subtitle failing layout does not cause valid font import to be rejected. The real still preview remains explicit user choice and does not automatically run on parameter changes in either Layout or Effects. Overflow reasons from the temporary report are included in error messages before temp cleanup.
- **Evidence boundaries:** source-level checks of endpoints/DOM and isolated V8 runs of font-import transaction and ASS-only debouncing passed. Physical Termux with the user's exact HYRunYuan-55W.ttf, large corpus runtime, host Python tests, Chromium UI and independent ASS/SRT byte verification remain **Pending**; do not claim those passed.

**Deduplication:** Extends this existing font/preview HSR Case and the earlier async-preview Case. No Canonical promotion.


## Follow-up: layout-plan fidelity after explicit libass verification (2026-10-15)

**Level:** continuation of existing HSR Case; not Canonical. **Status:** mainline source implementation + isolated V8 geometry/identity checks; exact-head Python/Chromium and target Termux device acceptance **Pending**.

- Failure mechanism: `preview_subtitle_layout()` and `render_ass()` share the initial solver, but actual ASS performs an additional raster-backed ink-validation/reflow stage. The browser then remeasured every solved text line using SVG's font metrics, so both line widths and potentially the number of lines or scale could differ from the actual image.
- Mainline repair: fast SVG now uses server-supplied per-line `measured_width`, `font_size` and `line_height` (`textLength` and shared linebox alignment) without browser-owned reflow. If browser loading of a selected font fails, UI flags fallback explicitly instead of presenting it as a comparable preview.
- On explicit still-frame render only, `render_ass()` optionally captures the final *validated* line geometry (after raster-driven shrink/reflow) already computed during the ordinary ASS write. Both FastAPI and Termux Lite return a bounded Base64 JSON provenance header alongside the normal PNG (no extra render). The Layout browser stores it under the exact project/payload identity; switching to fast view with the same identity reuses final lines/scale. Editing parameters invalidates the plan. Effects UI and the optional actual-render trigger are preserved.
- Limit: before first explicit real render, browser fast preview remains an estimate; even after plan reuse, SVG glyph outlines, fonts and ASS-native effects are not pixel-perfect libass replicas. Do not claim global pixel equivalence. Header provenance is optional and capped to avoid oversized HTTP headers.
- Local V8 execution verified that the SVG line widths/linebox positions match the backend contract and that a verified plan is applied to matching identities but rejected for stale identities. Added repository regression contracts for ink-validated scale capture, HTTP metadata and identity guard. Full host/runtime tests remain unverified.

**Deduplication:** Extends existing HSR font/preview Case and `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`; no new Candidate or Canonical edit required.
