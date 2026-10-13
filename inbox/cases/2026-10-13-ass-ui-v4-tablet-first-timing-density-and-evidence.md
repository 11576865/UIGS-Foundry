# Case: Tablet-first ASS editor UI allocation, timing-oriented effect editors and compact capability access

Date: 2026-10-13
Status: Case / implemented in offline HTML prototype and locally browser-tested; not production Android acceptance
Product: ASS-Workbench-Android (UI Study 04)
Artifact (conversation-local): /mnt/data/ASS_Workbench_UI_Prototype_v4.html
Package: /mnt/data/ASS_Workbench_UI_Prototype_v4.zip
Related prior: inbox/cases/2026-10-13-ass-offline-ui-v3-draft-undo-and-mobile-interaction-evidence.md
Related Foundry Bug: inbox/bugs/2026-10-13-ass-offline-ui-v2-draft-loss-and-undo-contract.md

## User-observed trigger
The owner approved improvement of v3's tablet-wide composition but criticized narrow layouts, motion/animation authoring, missing directly-visible existing functionality, and excessive area allocation. The correct target is predominantly a tablet used as an Android professional editing device, **not a phone-first dashboard enlarged**. These are owner design judgements, not independent usability metrics.

## Initial evidence and reproducible issues
Actual Chromium screenshots of v3/v4 pre-fix at 800×1280 showed FIXED main preview stretched vertically to nearly the full remaining editor height. The Raw ASS inspector was hidden at that intermediate breakpoint; 390×820 timing screenshot clipped the summary/fields; compact Font/QC rendered a resource list over a large otherwise empty lower region and hid provenance; Karaoke occupied space with nine equally-large cards despite unequal durations. v3 batch review with one selected Event left a large blank results table area. These observations cannot be substituted with a mock image, and are not claims about the Kotlin APK.

## Changes made in self-contained v4 HTML
1. 800px portrait tablet FIXED main editor: bounded video reference, immediately visible Raw ASS inspector in the same main column, event table alongside, bounded timeline under inspector; task titles single-line with scrollable navigation. 1280px landscape keeps parallel native-task organization.
2. Animation/Karaoke: proportional nine-segment timing lane derived from explicit demo centisecond durations totaling the 330cs sample Event, current segment selected/start/duration surfaced, 1cs nudge and direct numeric controls, \\k / \\kf / \\ko / \\kt mode selection, token sequence preview; Fade-in/Fade-out and \\t animation have distinct duration bars, visible boundaries and synchronized temporal scrub; scrub updates illustrative alpha and scale CSS effects.
3. Compact phone effects: one active video preview at a time with original/result toggle, parameter panel remains reachable below the time track; eliminated side-by-side 195px videos and large equal-sized syllable tile grid. Demo motion and audio are **not** mpv/libass evidence.
4. Compact timing: initial time/PTS/frame action strip no longer clipped; user may switch explicitly into supporting video; narrower lane headers release width to waveforms/event blocks.
5. Compact Font/QC: paired resource list and currently selected evidence, font row selection updates provenance, different tool modes (requirements/QC/compatibility/diagnostics) have distinct contextual detail instead of showing stale ExampleSans metadata.
6. Batch: kept true selection-based target counts and safe preview/commit guard from v3, but bounded the results list and allocated otherwise-empty space to before/after sample Raw ASS token strings.
7. Route audit fixed `PROJECT` catalog selection to actually reveal the project delivery drawer; `FRAMES` explicitly conveys distinct frame-time context. Workbench tool directory still includes 18 exact persisted names; SPATIAL_EXPERIMENTAL is a separate Host selectable via global workspaces.
8. Routed event action semantics fixed prefix collisions: `syllable-plus` must not be interpreted as a numeric `syllable-N` selection; resource-detail must not be classified as resource type. Effect example parameters are stored per selected Event inside prototype state, not committed to true ASS.

## Test evidence and boundary
- Local Playwright/Chromium using 360×780, 390×820, 800×1280, 1280×800 and 1440×850 viewports.
- **74/74 passing** browser checks: six tasks at five viewport sizes and overflow checks, actual tablet Raw ASS visibility / video bound, mobile time actions, one active effect preview, selected karaoke segment and numeric edits, animation scrub/parameter changes, mobile provenance, exact 18-tool catalog including PROJECT and FRAMES, event draft switching, apply/Undo/Redo, separate experimental Host, and long-press suppression.
- Actual headless browser screenshots generated for six wide tasks, Fade mode, 800px portrait, and compact phone modes.
- NOT verified: native Android Compose or production build, system keyboard/IME, actual mpv/libass output, true event token parsing or graph editing, MKV save or font matcher, animation rendering compatibility, TalkBack, tablet OEM hardware, and task-time usability. CSS animation is illustrative and never evidence of \\t real renderer semantics.
- Browser tests cover named traces only, not every route/order/gesture combination or 74 independent production requirements.

## Reusable conclusion
**Layout allocation should follow task object and input mode**, not a uniform dashboard skeleton or naïve breakpoints. A tablet-wide multi-pane arrangement can require a different *intermediate portrait composition*, not just the same three panes narrowed. For timing-controlled content, directly visualize real temporal ratios, boundaries, current sample and edit origin; do not use equally weighted decorative cards when underlying units differ. On phones, reveal one primary media reference and nearby, bounded controls; make secondary evidence reachable by toggling or small secondary panes. Demonstrate content truth and editing state in the UI, not long explanations.

## Dedupe and governance
Searched Foundry for 'tablet portrait video bounding Raw ASS inspector', 'Karaoke timeline proportional syllables compact viewport', 'ASS prototype responsive mobile timing font QC', and 'conditional resource evidence mobile inspect'. Prior v3 Case and mobile responsive Test did not cover the new concrete allocation/animation implementation and measured v4 regression.
No Canonical change. No production ASS repository modification.
