# Case: ASS UI v5 temporal graph, adjacent syllable boundary, geometry precision, compact task view

Date: 2026-10-13
Status: Case / offline interactive HTML prototype + Chromium evidence, **NOT** production Android UI evidence
Product: 11576865/ASS-Workbench-Android / prototype study 05
Related prior: inbox/cases/2026-10-13-ass-ui-v4-tablet-first-timing-density-and-evidence.md

## User-directed continuation
User requested continuing after the v4 tablet-first revisions. Prior feedback focused on small layouts, effects/animation authoring, omitted existing functionality and poor space allocation. The continuation retained FIXED as primary Host, experimental canvas as separate selector and 18 navigable catalog keys, then deepened temporal and geometry interactions instead of repeating generic panels.

## Delivered artifact
- Conversation-local: /mnt/data/ASS_Workbench_UI_Prototype_v5.html (offline, single HTML/CSS/JS)
- Packaged: /mnt/data/ASS_Workbench_UI_Prototype_v5.zip (index, 8 real Chromium captures, test logs, README)
- Six main task layouts remain separately composed.
- Native Android Kotlin/Compose repository is unchanged.

## Changed prototype behavior
1. Effect authoring: Fade Alpha and Transform Scale X numerical curves based on a shared temporal preview model. Fade, transform start/end boundary handles support pointer dragging; Scale X target and \\t acceleration (0.5, 1, 2) controls update the same model. Scrub position immediately synchronizes preview opacity/scale, graph cursor, and numeric sample. Graph also displays explicit illustrative \\fad and \\t token summary. Does not imply true libass animation parsing or playback.
2. Karaoke: eight boundaries separating nine syllables may be dragged to redistribute adjacent centisecond durations while preserving the pair and whole Event duration. Numeric 1cs adjustment from v4 remains; the sample durations total 330cs. This is a **relative timing visualization** and source-independent proto model.
3. Geometry: preview overlays safe area, horizontal/vertical guide and anchor, togglable via tool buttons; drag snapping to 10 ASS coordinate units; four ±1 precise nudges and sample X/Y centering update per-Event transient geometry draft, not the document or Undo until Apply.
4. Compact: tablet width can show track/curves adjacent; mobile mode selects one activity (“时间轨” vs “参数曲线”) without stacking two tall editors, and exposes a compact command strip on the precision studio. Studio fixed-height preview no longer leaves a large dead gap before the inspector.

## Actual testing
- Headless Chromium through Playwright; self-contained HTML loaded into page context.
- Five viewports (1440×850, 1280×800, 800×1280, 390×820, 360×780).
- Primary battery **105/105** passing checks: element and viewport presence, 8 draggable Karaoke boundaries/relative duration preservation, 4 draggable animation boundaries, Scale X/acceleration/scrub, visibility toggling and X/Y nudges, per-Event geometry draft, raw draft A→B→A, Apply/Undo/Redo, JS exceptions and horizontal overflow.
- Supplemental battery **35/35** passing checks at 1280×800 and 390×820: exact 18-tool directory, Host isolation and selection preservation, 7 specialized tool routes, cross-Event geometry and per-Event effects state, wide dual and compact single-editor presence.
- Additional touch-pointer check: >500ms help tooltip on Save, release+click does not save, separate short click does save (prototype).
- Original browser QA caught two real v5 regressions: a redundant closing div made the width of desktop Karaoke boundary rail zero and all handles overlapped, and a guide action was intercepted by the generic studio navigation prefix. Both corrected and browser checks rerun. Another observation: a curve whose time cursor did not update when the scrub slider moved; corrected by using the same temporal model and updating cursor/readout on input.
- Captured eight real browser screenshots and assembled a contact sheet. These are actual rendered HTML, not generated ideal images.

## Evidence boundaries
All data/sample scenery/waveform are illustrative. The model is not arbitrary ASS semantics: actual \\t nesting, reset scopes, font shaping, VSFilter differences, Karaoke production alignment, actual video decode and mpv/libass output are **not tested**. HTML does not write ASS, MKV or .asswb and does not represent Android Compose rendering, keyboard/IME/OEM stylus behavior, Task performance, TalkBack or real-device acceptance. Its Undo applies only to the prototype's supported fields. Do not use browser check counts as product requirement completion claims.

## Reusable engineering observation
Professional editing tools should maintain one source for **interactive time/state**, feeding the visual curve, exact numeric field, time cursor and preview rather than recomputing slightly different approximations. Adjacent-boundary editing should preserve conserved quantities (here: combined syllable duration). UI geometry must be verified at real widths because an HTML structural break may produce zero-width interactive rails while initial screenshots superficially appear plausible. Compact task routing should show one primary editable spatial object, not shrink and stack all desktop visuals.

## Dedupe and governance
Searches in Foundry: 'ASS UI v5 temporal graph parameter playback sync', 'Karaoke drag adjacent durations preserve total', 'visual timeline transient and commit shared model', 'tablet mobile curve track switching'. Existing v4 Case covers the earlier proportional timing and layout improvements but not this interactive v5 runtime evidence and concrete regressions. No Canonical promotion and no production repo source changes.
