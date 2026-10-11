# Case / Pending: QHE functional UI rebuilt as a focused low-copy media workbench

Date: 2026-10-11
Status: **Case / implementation submitted / latest-head CI and visual acceptance Pending**
Product: `11576865/Quick-Automatic-Hardsub-Encoder`
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/93
Current head at intake: `9da52f359e296381f031ccdbd336e8fe760cb526`
Baseline main: `4a2d473cd3575fb21f67fb2f744bab8df0607055`

## User intent and initial observation

The user explicitly rejected a polished rendered screenshot as the requested deliverable and asked to **redesign the actual functional application UI**, with notably less explanatory prose. The QHE source markup had separate explanatory text around input, preflight, preview, guided/manual choice, encode planning, platform cards, runtime, and manual Stream Plan. Some copy was defined by the initial HTML while other lengthy explanations were overwritten on startup or when switching operation by `renderRuntimeIdentity()`, `syncModeChrome()` and `updateMode()`. Merely editing the HTML or drawing a mock screenshot cannot solve both paths.

The UI already carries a dense task progression with actual IDs for file pickers, libass preview, guided plan, manual media task, encode progress, cancellation and Native Bridge. Destructive reimplementation that remounts controls or fabricates progress is out of scope.

## Bounded product-side implementation

QHE PR #93 modifies the **real source**, not an image:

- `src/main.js`: shorten static source/preview/plan/control headings and runtime descriptions while preserving essential element identifiers and action points; retain explicit hardware capability detection and Windows Bridge recovery notice.
- `src/media-workspace.js`: shorten dynamic operation descriptions that would otherwise reintroduce verbose prose on mode switches; preserve copy/keyframe cautions, codec choice semantics, timeline controls and command/verification UI. Move duplicate input/branch/output architecture explanations into a native closed-by-default `<details class="media-workflow-notes">`, leaving every control mounted.
- `src/focused-workbench.css`: a new standalone appearance layer (not mixed with old utility CSS), emphasizing a desktop main canvas and narrow status/runtime rail, larger preview, compact source and task cards, subdued background/borders, and phone-specific density without replacing stage ownership or reducing primary touch targets.
- `src/focused-workbench.test.mjs`: source-contract regression for task and native-bound IDs, responsive grid and progressive-disclosure markup.
- `.uigs/tasks/qhe-focused-ui-2026-10-11.json`: durable continuation record with pending validation and blockers.

No FFmpeg, native state ownership, HDR protection, job export, cancellation or field evidence is changed. The old Windows WinForms launcher remains a documented diagnostic entry and is not called an orphan.

## Reusable distinction and competing concerns

1. Functional UI redesign must be delivered in the application's **rendered source/controls**, not substituted by an aesthetically appealing static image.
2. Reducing on-screen explanation requires auditing **runtime text mutations**, not only initial templates. Native safety warnings and consequential action labels must remain available.
3. Rebalancing hierarchy should retain one state owner for existing task components; presentation changes should not create fake job state or remount independent copies.
4. Progressive disclosure is appropriate for infrequent architecture/tutorial prose, **not** for blocking errors, keyframe-risk notices, consent, codec capability evidence or encode/cancel/verification controls.
5. A source-contract test establishes only structural continuity; screenshots and actual browser/device interaction are distinct validation layers.

This case is related to existing candidates:
- `inbox/candidates/2026-10-04-workflow-centric-ui-acceptance-preserves-simultaneous-context.md`
- `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md`
- `inbox/candidates/2026-10-03-presentation-density-state-continuity-by-stable-component-identity.md`

## Validation boundary

At the single immediate status read, PR #93 latest-head runs were queued:
- Frontend CI `38120661887`
- Windows local smoke `38120661872`
- UIGS Evidence Coverage `38120661898`

**Pending external CI**, not green, not merged. No latest-head screenshot review, Android device, physical Windows hardware, GPU or long-film acceptance is claimed. A passing CI later would not itself prove that the redesigned information hierarchy satisfies the user's visual preference.

Case-level evidence only; **do not promote a single project redesign to Canonical**.


## Final UI CI, visual evidence and merge acceptance — 2026-10-11

The earlier Pending-only report is superseded by a **merged, source-backed QHE UI implementation**:

- QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/93
- Final PR head: `3f2d51c2a7610be1aee2239919fb83757143096d`
- Main merge commit: `68a4ebe387f925d0c736dea9875edcca2733ac21`
- Final GitHub Actions evidence (all **success**): Frontend + Playwright run `38129084062`, Windows local smoke `38129084064`, UIGS Evidence Coverage `38129084169`.
- The last CI captured actual Chromium browser screenshots as artifact `media-workspace-screenshots`, id `11699001128` under Frontend run `38129084062`. Generated screenshots include guided/manual desktop at 1280 px, guided/manual mobile at 390 px, Windows Native simulated desktop, Copy and timeline snapshots. These are browser layout evidence, **not physical device/GPU validation**.

### Visual defects found and corrected in real rendered pages

1. **Split CSS grid track gap:** Initial Chromium screenshot of the first PR #93 version placed `taskOverviewRail` near the top right but the runtime/platform cards much further down, leaving a large empty right gutter. Root cause: two independent right-hand grid rows next to the main column spanning both; intrinsic main height influenced grid row sizing. Replaced with one `.support-rail` wrapping the existing components, without remounting their JavaScript-owned contents. Latest browser smoke checks actual computed desktop two-column grid, rail width, adjacent vertical gap and right-edge alignment. Actual screenshot review confirmed no long gap.
2. **Premature expanded audio controls:** Previously, bitrate/channels/sample-rate occupied the screen before the guided encode plan. Moved the shared output mount **after** guided plan and **before** execute; kept audio strategy and output container visible, moved optional audio tuning into an expandable `media-output-audio-details`, and preserved all form bindings. Latest Playwright checks control visibility and disclosure.
3. **Mobile target mode clipped:** A 390 px Chromium screenshot displayed only the first and second of three guided target tabs, hiding target-size offscreen in a horizontal tab row. Replaced with a three-column phone grid preserving all three named actions, removing secondary descriptions in that specific narrow tab row only. Latest Playwright evaluates each tab's actual bounds and rejects any hidden/clipped third option; screenshot review confirmed all three visible.
4. **Long copy recreated dynamically:** Shortened initial static labels and runtime/mode-switch JavaScript updates. Kept succinct semantics for recommended-parameter fallback, native capability probing and the fact that a source timeline is not before/after image-quality verification. Existing source tests were updated to assert semantic requirements rather than old paragraphs.

### Acceptance boundary

**Accepted:** committed, merged and green automated source/FFmpeg/Windows smoke/browser visual checks; actual Chromium screenshot reviewed for 1280 px desktop layout and 390 px guided phone target tabs. **Not accepted/not claimed:** physical Windows GPU/NVENC long-form, real Android device screenshots, arbitrary viewport visual sign-off, HDR/VFR field test, perceptual usability testing, or completion of QHE issue #77.

This supports a Case-level lesson, not single-observation promotion to Canonical: avoid independent CSS grid rows for related support cards beside a tall main column, do not let screen compaction hide the only target-mode affordance, and reserve explicit primary actions while progressively disclosing advanced nonrequired parameters.

No Canonical change.


## Post-merge responsive follow-up — PR #94

QHE real UI refinement continued after #93 merged. [PR #94](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/94) fixed the wide-tablet task-overview visibility contract and added a nine-viewport Playwright acceptance matrix. Final UI branch head `5714004a3323b92a697effd0f9dc3a808acf91c3`; successful Frontend `38130794916` and UIGS `38130794896`; merged into main at `840aaef17891cccbfd2cb252c5e5dfd96d8f4ed5`. Current QHE bookkeeping commit `8afdb474478a248fbca4d5fc1224e982991f3f64` records #94 completion and remaining field limits.

Visual screenshots were generated and inspected for 320px phone and 1024px tablet. Browser tests covered 320, 390, 640, 768, 919, 920, 1024, 1180 and 1280px; 320px main modes remain on-screen and wide-tablet task status returns in its right column. Two initial red checks were test harness errors (nonexistent DOM ID, then viewport resize shell state read too early), corrected prior to passing the latest head. Full test detail: `inbox/tests/2026-10-11-qhe-phone-tablet-responsive-matrix.md`.

**Scope:** browser visual and responsive behavior only. Native Windows smoke was not rerun by the UI-only changes; physical Android or NVIDIA GPU/long-film field acceptance remains unverified. This refines an existing Case, without Canonical promotion.


## QHE Studio v2 full source redraw after repeated user rejection — 2026-10-11

**User intent:** after the original model-generated mockup was rejected, QHE #93's actual low-copy CSS workbench and #94's tablet acceptance did not end the task; the user explicitly asked once more to **redraw the running application UI**. This is not permission for another static image. Browser screenshots of the existing 1280px desktop and 320px phone showed (a) large Android/Windows tutorials before the first actionable task switch, (b) a vertically stacked mode choice occupying needless phone space, (c) repetitive boxed subregions and weak preview hierarchy, (d) guided audio/container controls surfaced in the phone **Prepare** stage before production could begin.

**Product implementation:** [QHE PR #95](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/95), final source head `bb167e748f857f4a18f4837218205869c1f7083c`, **merged to main** at `52963c91fc0c3ec3674c8ce55c316428b3eb5a1d`.
- New `src/studio-v2.css` defines a distinct visual hierarchy: typographic app toolbar, compact 3-way mode switch, flat/quiet source inputs, wide 16:9 real preview, secondary status rail, compact planning selectors, stronger action emphasis, and phone-specific layout.
- Source-side `src/media-workspace.js` shortens the **visible** modes to **硬压 / 转码 / 剪切**, retaining full names via real `aria-label` and the existing event handlers.
- After initial app markup creation, `src/main.js` moves **the original** `.mobile-runtime-help` node after `.workspace-layout` once; on 320px phones the video/ASS pickers are reachable before setup/install tutorials. This does not duplicate the DOM or create a new task owner.
- The first Studio screenshot showed `sharedMediaOutputMount` prematurely visible on a 320px hardsub Prepare view. The final PR gates this existing control to the production stage for phone hardsub only, preserving Transcode/Copy semantics. The previous blue/purple/green source picker visual competition was unified without hiding file types.
- `src/studio-v2.test.mjs` and `scripts/check-media-ui.cjs` source + actual Playwright browser tests enforce mode action reachability, phone task/tutorial ordering, production-stage audio reveal, all responsive viewport checks, and a new production UI screenshot artifact.

**Observed acceptance:** Final head's GitHub Actions runs all **success** — Frontend + Playwright `38131737590`, Windows local smoke `38131737587`, UIGS Evidence Coverage `38131737624`. GitHub Frontend screenshot artifact id `11698973822` contains 1280px desktop, 320px phone intake and 320px phone Produce among other Chromium captures; these images were opened and reviewed. On 320px the default prepared intake view became `1057` px high, down from `1547` px on the first Studio head (the difference is principally the now-gated audio section, not a generic performance metric). No real physical Android screenshots/gesture/accessibility acceptance or NVIDIA GPU/HDR/VFR long-film acceptance is claimed. QHE #77 remains FIELD-PENDING.

**Reusable knowledge, Case level only:** changing a real interface involves ownership-aware ordering, task-state conditional visibility, and validating computed browser output; stylesheet changes alone can leave irrelevant controls in the wrong stage. A mode selection can use short *visual* names without losing full accessible meaning. A repeated UI request after a passing previous PR is product feedback, not a signal to generate a prettier illustration. Prior QHE #93/#94 context is preserved and this is deduplicated into the existing Case; no Canonical specification is modified.


## Studio v2 phone readability and keyboard-focus follow-up — PR #96

**Status: Product change submitted / CI pending (not merged).** QHE PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/96, checkpoint head `39529fd498e7836af82ac8ccd253bacd6736adf8`, based on main `a4d108655956d0314951115a735cdfe5a15f36f3`.

A reviewed *real* Chromium screenshot at 320px of merged Studio v2 showed duplicate backend identity (header status pill plus lower runtime mode banner) and very small helper copy for file choices, source state and runtime details. The production file-input pattern uses a `1px` transparent-but-focusable native `input.file-input-control` associated with a visible sibling `label.file-picker-trigger`; without a focus proxy, keyboard focus could remain visually indistinguishable on the input picker. That focus risk is source-grounded; the latest browser check to verify the actual focus ring is **Pending**.

The bounded patch adds a phone-only text hierarchy with readable helper labels and runtime metadata, hides only the duplicate header pill (retaining the actual backend banner), and adds `.file-input-control:focus + .file-picker-trigger` to show a visible focus ring without changing the native file input or any picker events. It retains relevant file metadata, phone stage ownership, Native Bridge and encode controls.

Regression additions: browser-computed text sizes must be at least 12px for the selected critical phone metadata, backend identity must remain visible exactly once in the phone presentation, the label must show a visible focus ring after native input focus, and 320px intake must not overflow or clip mode buttons with root `font-size:24px` (a simulated 150% root text size; **not** physical Android OS font scaling). Also emit `media-workspace-studio-phone-150pct-text.png` screenshot. Frontend run `38132443862` was in_progress at the initial check; UIGS Evidence Coverage `38132443859` succeeded. **Do not claim browser/Android accessibility passed until the exact latest head passes.**

Cross-project observation, not Canonical: when a styled label replaces an invisible file input's visual affordance, keyboard focus must be mapped to the visible label, and design review must measure actual computed small text and font scaling rather than only screenshot color hierarchy. Existing QHE functional UI Case used to avoid duplicating a separate broad Candidate.
