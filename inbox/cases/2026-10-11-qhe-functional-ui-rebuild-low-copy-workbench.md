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
