# Case: HSR Subtitle Studio V3 rebuilt after CI-green V2 failed user experience

Date: 2026-10-15
Product: `11576865/HSR-Voice-Archive-Builder`
Delivery PR: [#167](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/167)
Exact verified head: `3111e4fcb0d1dd83d0aaad129391a33a6c159d9c`
Classification: **Case** (project-specific UI redesign and acceptance); no Canonical modification
State at Intake: CI-green implementation; main merge/device and user visual acceptance not yet observed

## Explicit user rejection

After merged [PR #166](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/166) passed Python, Chromium and real libass/FFmpeg validation, the user still judged both the Layout and Effects workbenches unsatisfactory and explicitly requested a **complete redesign**. The fact of this rejection is a user report, not an inference from screenshots. Green source/geometry tests did not establish user acceptance of the interaction and information hierarchy.

## V3 implementation, distinct from decorative refinements

Main source `app/static/index.html` formerly held one `.layout-preview-region` containing stage, output evidence, timeline and selected cue while a very long `.preview-inspector` owned render, save, settings and media inputs. Legacy embedded style plus `hsr-ui-convergence.css` repeatedly overrode grid, sticky and breakpoint rules. Changing the background and collapsing a section was not enough to create a real authoring task model.

V3 explicitly restructures the DOM while keeping every authoritative input ID and backend API:

1. **Stage-owned actions**: geometry, true FFmpeg/libass still render, moving ASS preview, style save and explicit ASS export move into a `.studio-v3-command-bar` with the 16:9 video stage. Their operation and evidence status stay nearby.
2. **Single subtitle editing deck**: the existing continuous timeline, real pointer-driven boundary adjustment, selected cue read-only source/translation, explicit timing save/revert and Review link remain in `.studio-v3-editors`. It does not clone Review's final-text editor or original audio.
3. **Task-scoped Inspector**: Layout typography/position/readability and Effects motion/Karaoke/HUD inputs remain the same controls in a separate independently scrollable `.studio-v3-inspector`; no extra competing navigation for Layout/Effects.
4. **Mobile task switching**: three explicit tasks Timeline / Selected Cue / Parameters share the same stage and underlying state. Switching uses a semantic `role=tablist`, `aria-selected`, `aria-controls`, roving `tabIndex`, pointer and arrow-key interactions. Tablet/desktop keep bounded concurrent stage+editing/Inspector regions.
5. **CSS authority**: obsolete breakpoint/grid/sticky Studio geometry removed from `hsr-ui-convergence.css`; `app/static/studio-v3.css` introduced as the dedicated V3 geometry authority, loaded after shared legacy CSS. Existing wider inline CSS remains in the historical page and should be reduced only with parity tests, not blind bulk deletion.
6. User-supplied red-clouds WebP is still a diagnostic preview asset, never silently a final MKV background.

## Verification at exact PR head

- [Python multi-version + Termux Lite CI 38637680675](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38637680675): **success**.
- [Chromium responsive/workspace interactions + real browser preview and FFmpeg/libass evidence 38637680694](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38637680694): **success**.
- Source contract `tests/test_studio_v3_architecture.py` covers single owner per control, stable rendering/timing hooks, CSS authority and mobile tab keyboard semantics.
- `tests/browser_visual_evidence.py` now exercises actual mobile task switching as well as selected-cue accessibility, desktop timeline drag, source-only Review editing, QA rail, keyboard/touch, and bounded portrait/tablet/desktop geometry.
- Test fixtures deliberately exercise operations through visible panels and a real FFmpeg video endpoint; CI does **not** imply user preference acceptance, actual Android device screenshots or device-side MKV-resume confirmation.

## Portable lesson (case-supported, not Canonical)

A user can reject an interaction hierarchy after code, test and pixel-proof greenlights. When the request is “thoroughly rebuild”, changing color, copy or CSS spacing cannot substitute for **task and control ownership**, spatial grouping, and visible interaction routes. Preserve unique authoritative controls through DOM moves, separate preview-operation ownership from setting ownership, and test **pointer hit targets**, responsive pane switching and saved state—not just text-source snapshots. Match regression tests to the intended new tasks without erasing the functionality they previously protected.

Deduplication: Foundry searched `studio stage inspector layout`, `mobile panel workbench task`, `HSR subtitle studio redesign`, `CSS single authority studio`. Reviewed neighboring HSR [PR #153 focused viewport case] and ongoing subtitle requirement-to-mainline Observation. This new Case uniquely records *explicit rejection of a CI-green prior implementation* and V3 DOM reconstruction with exact-head acceptance, so it does not duplicate the older diagnosis.

**Canonical promotion: none.** Device/user visual acceptance: Pending. 


## Verified mainline integration (2026-10-15)

The product PR #167 was verified as **merged=true** and **closed**, and the product `main` commit is `a1d833679d299a729f3519c3e02f92c25bb8fda0`. Mainline source fetch confirmed `app/static/studio-v3.css`, `app/static/index.html` with `studio-v3-workbench`, and `tests/test_studio_v3_architecture.py`. Exact pre-merge PR-head Python/Termux and Chromium/FFmpeg workflows remained `success`. A separate branch-hygiene workflow was still in progress at verification. This confirms code landed in `main`, **not** that actual Android/Termux field usability or user aesthetic acceptance has been achieved. No Canonical promotion.


## Field screenshots rejected merged Studio V3; flat V4 correction (2026-10-15)

After Studio V3 PR #167 passed CI and merged to product main, the user presented **two actual Microsoft Edge/Android screenshots** (Effects and Layout, both 2026-10-15 ~05:13–05:14) and explicitly rejected its visual and interaction quality. Observed failure: a giant redundant “字幕特效工作台 / 字幕排版工作台” page title; stage was below command rows, a reference-background selector, repeated status/evidence/export banners; the 16:9 red-cloud preview was **reduced to a narrow sliver** within a fixed-height nested-scroll grid, while timeline and Inspector each required further internal scrolling. The user further rejected the unrequested reference-background choice (the user-supplied red cloud picture was meant to be the sole reference), a second editable sample-text area in the Effects/Studio Inspector (final subtitle text belongs exclusively to Proofreading), and project imported fonts that still appeared unusable. The complaint and screenshots are **direct user field evidence**; images are not republished into the repository or Foundry, only the product-derived symptoms are recorded.

The existing V3 CI success was real but insufficient: acceptance criteria had asserted `height:clamp(...)` and independent internal `overflow-y:auto`, actively protecting the **same interaction the user found unacceptable**. This is a genuine acceptance-model failure, not solved by claiming more CSS polish.

Product V4: [PR #168](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/168), merged product main commit `4f1ce784fa1ce11a5356630ef9fddc9aa55e3025`, exact PR test head `e278cfeac6b7e0123fe0e4a508f188c6e7dfae71`. V4 introduces `app/static/studio-v4.css` replacing the loaded V3 geometry authority with **normal document scrolling and no fixed-height nested panes**; canvas first, full 16:9; primary render/save immediately below canvas; status/export proof compressed into succinct non-blocking rows; timeline and cue editing available through a closed-by-default explicit disclosure; giant redundant headings are visually hidden while retaining accessible names. Browser sample text edit details are hidden and inert, preserving the internal preview fixtures without reintroducing a user-facing subtitle editor. `previewBackgroundMode` becomes inert hidden `reference` input and the browser always displays bundled red-clouds: no switcher for gradient/black/grid/local decorative background. This diagnostic image is still distinct from real project/Final MKV backgrounds or user-selected footage.

**Font-specific corrective chain:** `loadFontBrowser` had originally only listed host fonts, despite uploaded project fonts living under `subtitle_fonts/`. V4 merges `GET /api/subtitle-layout/project-fonts` into the chooser, prioritizes imported font families and marks them, checks that `FontFace` genuinely loaded instead of reporting a false import success, and calls `saveSubtitleLayoutSettings()` after choosing the imported font so refreshing the project does not silently restore the old font selection. It reports failure if either browser activation or persistence fails; existing FFmpeg/libass `fontsdir` + imported TTF smoke test stays active. **A specific real user's imported font and device-side family mapping have not been verified**; do not claim that this precise font has been fixed by source-only tests.

**Exact-head verification:** [Python 3.11/3.12/3.13 + Termux Lite, run 38641932555](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38641932555) **success**, and [real Chromium-responsive interactions + FFmpeg/libass media artifact run 38641933057](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38641933057) **success**. Chromium screenshot acceptance now rejects nested scroll regions, rejects background picker/second visible editor, asserts 16:9 stage size and stage-before-actions, and still executes actual optional timeline editing and playback. Source verified in merged main. Physical device visual and actual imported user font acceptance remain **Pending**; user aesthetic acceptance is not inferred from CI.

**Reusable engineering learning:** production screenshots can falsify a CI-green interface model; the test oracle itself must be inspected. A test that insists on bounded nested scrolling can encode a bad design as success. Treat one field screenshot as a strong **specific failure observation**, adjust concrete tests for the actual needed task, and never extrapolate one report into Canonical product norms automatically. Deduplicated against this same V3 Case, so appended the observed correction rather than creating overlapping Candidate. Canonical untouched.
