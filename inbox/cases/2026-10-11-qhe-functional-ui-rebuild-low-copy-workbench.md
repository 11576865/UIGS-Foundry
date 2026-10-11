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
