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
