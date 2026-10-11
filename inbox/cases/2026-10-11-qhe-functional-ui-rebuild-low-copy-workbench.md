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


## PR #96 acceptance closure: font scale and file-picker focus

The preceding PR #96 **Pending** case is superseded by verified evidence for the exact source head `39529fd498e7836af82ac8ccd253bacd6736adf8`. GitHub Frontend + Playwright run `38132443862` and UIGS Evidence Coverage run `38132443859` both finished with **success**. PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/96 merged to QHE main as `bbc2576ebf4ffef2bf70c806ba17a86e48615b83`; subsequent QHE checkpoint `626afcc81e94d3559bbe96cf035a1c57053fa525` records that acceptance.

Frontend screenshot evidence artifact: `media-workspace-screenshots`, ID `11699272986`, contains `media-workspace-studio-intake-320.png`, `media-workspace-studio-phone-150pct-text.png` and `media-workspace-studio-produce-320.png`. The snapshots were extracted and reviewed: one live backend status remains visible on phone, visible focus border was present on the source picker after focusing its visually hidden file input, and long metadata wraps instead of causing horizontal document overflow under a 320px viewport with 24px root font (representing 150% of the 16px default). Actual browser tests measured the focus outline, computed type sizes and responsive geometry.

**Boundary:** CSS root font enlargement is not identical to physical Android system font-size settings. Real Android screen-reader behavior, on-device safe-area and touch ergonomics have **not** been tested. Windows smoke was not rerun for this CSS/test-only PR; previous PR #95 Windows smoke remains valid only for its own exact head. QHE physical GPU/HDR/VFR/long-form #77 is still FIELD-PENDING. This remains one Case-level observation without any Canonical promotion.


## Professional-workbench references and Studio v3 structural redraw

Date: 2026-10-11
Status: **Candidate implementation / source committed / latest-head CI and screenshot acceptance Pending**
Product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/97
Source head at intake: `a8874900600d6af4107cde459a94089b7b5a8a58`
Design basis: official Apple Compressor guide on viewer/batch/inspector distinctions; official HandBrake workflow and setting sections; Linear's 2026 design refresh emphasizing that secondary navigation must not compete with the task.

**Concrete critique:** QHE's preceding #93/#95/#96 iterations repeatedly reduced text and equalized card decoration but left a long vertical queue of asset/input, preview, strategy, output plan, audio and execute blocks in its desktop main column, with the video viewer much less prominent than it ought to be. This did not satisfy the user's explicit request for design quality on par with mature applications. The mistake is one of **information architecture and area allocation**, not merely colors.

**New product-side implementation** (keeps the application's own identity and controls; no third-party copyrighted assets):
- The existing `media-mode-switcher` is reparented into one top-level `#studioModeDock` without copying the nav, breaking event ownership, or remounting Native state.
- On desktop `workflow-main` is recomposed into actual source controls on the left, large preview and planning in the central stage, with the already-existing current-task inspector on the right. The default blank stage is explicitly labeled as no media; it is **not a generated or fabricated video preview**, is excluded from phone/tablet and copy/transcode contexts, and yields to the real `subtitleCard` once visible.
- Actual source, preview, plan, audio/container, task cancellation, logs and source checks remain in their original functional DOM.
- A new presentation layer `src/studio-v3.css` draws the intended composition; baseline compatibility styles are retained for bounded migration rather than unreviewed deletion.
- A dedicated source invariant test `src/studio-v3.test.mjs` and Playwright real-browser geometry checks cover top-level mode ownership, actual source vs viewer vs inspector bounds at 1280px, and screenshot `media-workspace-studio-v3-desktop.png`. Existing 320–1280px viewport and 150%-root-font checks remain.
- UIGS visual capture source dependency registers the new stylesheet. A durable QHE task record states the pending validation and device/GPU blockers.

**Distinction:** this is the first explicitly reference-led structural workbench redesign in this QHE sequence, not another screenshot rendering or style palette. Validated acceptance cannot be claimed before latest-head frontend CI + actual Chromium screenshots; even a green browser test does not validate physical Android screen reader and touch experience or #77 Windows GPU/HDR/VFR long-film field use. No Canonical promotion on a single product iteration.

Cross-project reusable learning: professional-tool visual quality is strongly affected by spatial ownership and display priority. UI assessment should measure whether the working object (media viewer) is allocated a first-class region, whether inputs and inspector are stable navigational zones, and whether "same-level cards with less text" merely preserve the original cognitive overload. Preserve actual functional control ownership across layout movement.


## Studio v3 visual regression: copy and transcode editor reparenting

Date: 2026-10-11
Status: observed browser layout regression / product repair committed / external revalidation Pending.
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/97
Original passing-head screenshot evidence: Frontend run 38133524314, media-workspace-screenshots artifact 11699659325.
Repair head: e5964e9dda37cbbfa77197bba6e192eea694567b.

Visual defect: Actual 1280px Chromium screenshot media-workspace-copy.png showed an approximately 250px-wide copy timeline/codec editor inside the source shelf; nearly the entire central editing column was unused. This source-backed issue occurred because syncHardsubStrategyChrome() reparented the live non-hardsub mediaWorkspace after inputCard, which Studio v3 now places in the narrow left shelf. Transcode uses the same branch. The previous passing automated desktop check validated hard-sub preview source/stage/inspector geometry but did not switch to copy/transcode and assert their editor locations. Green tests therefore did not establish three-mode desktop composition acceptance.

Bounded correction: change the non-hardsub reparenting to put the original live section into hardsubManualMount (central production editor) as hardsub manual already does, with old fallback when the mount is absent. Keep task compiler, DOM events, form IDs and phone prepare-stage semantics. Add Playwright 1280px geometry checks for separate transcode and copy modes: editor visible, parent the central mount, editor to the right of source shelf, and editor >=400px wide. Capture screenshot for each. Add phone 320px reachability tests after the same move. Separately suppress the audio/container panel during the unprepared desktop hard-sub empty viewer state.

Evidence boundary: the source repair has been pushed; latest-head Frontend/Playwright, Windows smoke and UIGS checks and screenshots are Pending. Do not treat original head green CI as validating repair. The lesson is Case-level only: mode-dependent DOM reparenting and breakpoint layout changes require a mode x viewport test matrix, not only checking the default mode. No Canonical promotion.


### Repair validation: desktop copy/transcode central editor screenshots

The repair head e5964e9dda37cbbfa77197bba6e192eea694567b passed Frontend+Playwright run 38134035730 and UIGS Evidence Coverage run 38134035779. The newly captured Frontend artifact media-workspace-screenshots ID 11700645709 was extracted and inspected: media-workspace-studio-v3-copy-desktop.png (1280 x 1930) now shows the live Copy editor in the central pane, not the source shelf; media-workspace-studio-v3-transcode-desktop.png (1280 x 3338) likewise places the full Transcode editor centrally. The fixed DOM and actual browser geometry agree. The original copy screenshot was 1280 x 3272 and predominantly empty to the right of the narrow editor; the repair is a major spatial regression fix, not merely a style adjustment.

Latest Windows local smoke was still in_progress on the first post-repair status read (run 38134035725), so exact latest-head PR #97 merge acceptance stays Pending; no physical GPU/Android field acceptance is claimed. No Canonical promotion.


### Final PR #97 merge and exact-head validation closure

QHE Studio v3 repaired head `e5964e9dda37cbbfa77197bba6e192eea694567b` achieved **success on all three exact-head workflows**: Frontend+Playwright `38134035730`, Windows local smoke `38134035725`, UIGS Evidence Coverage `38134035779`. PR [#97](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/97) was successfully **merged** at `a502c7258dc07e81c1722e1ef3e93052e039992d`. Main task checkpoint commit `54cd4a92009425e0c3b099db117f4d4c23cd3b6a` reconciles earlier Pending labels.

Frontend screenshot artifact `11700645709` (media-workspace-screenshots) was reviewed for the corrected Copy and Transcode 1280px central editor placement, alongside hard-sub default source/viewer/inspector. Browser assertions confirm actual geometry and retention of the 320px mode reachability path. This settles PR #97 browser/CI acceptance only; do **not** claim that professional visual design quality has been universally established, or that physical Android accessibility, real NVIDIA GPU, HDR/VFR, long-video processing and QHE #77 field acceptance were completed.

UIGS lesson remains at **Case** level: mode-dependent DOM reparenting in an editor-style responsive layout needs cross-mode geometry evidence; a green default-mode CI can conceal high-impact non-default-mode layout collapse. No automatic Canonical modification.


## Studio v3 empty-source execution affordance — PR #98

Date: 2026-10-11. Status: **Product fix committed / external validation Pending**, not merged.
QHE: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/98
Source commit: `6eda22a36bcfedbb5a647296958c85c1aec337fe`
Previous stable main: `54cd4a92009425e0c3b099db117f4d4c23cd3b6a`

A real Studio v3 1280px Chromium screenshot for **Copy** (`media-workspace-studio-v3-copy-desktop.png`) showed a green enabled **开始视频流复制 / 剪辑** button next to the source shelf's **未选择视频** state. Inspection of the actual `src/media-workspace.js` confirmed `syncTaskActions()` only disabled this primary action during busy/saving; there was no source/probe readiness gate. The UI's visual promise therefore contradicted the task's prerequisites. The backend still validated at submit, but that did not justify an apparently runnable primary action.

Bounded product correction: use already-owned optional `videoIdentity()` and `mediaSnapshot()` hooks in `syncTaskActions()` to map three states: no video (disabled, **先选择视频**), selected but not probed (disabled, **先读取视频参数**), and ready (existing mode-specific Start label). Keep these optional to preserve isolated tool consumers, and preserve existing successful-output save/retry/cancel policy. Listen to the existing `quick-hardsub-media-info-changed` event to refresh the button; Windows-native file picker and selection recovery now dispatch this same event. Explicit disabled UI styling prevents the previous bright green action from appearing runnable.

Regression work: existing Chromium smoke asserts no-input Copy and Transcode Start is disabled; in an isolated task fixture it transitions no video → selected/unprobed → probed/ready via the real event and then continues through existing task completion, cancellation, save/export and retry behaviors. Source/CSS tests were added, while keeping the current phone/tablet layout matrix.

**Validation limits:** new PR #98 Frontend/Playwright, Windows local smoke and UIGS CI are Pending on exact current head, and no repaired screenshot has been reviewed. This is a source-backed bug and regression test, **not** acceptance of physical Android, screen reader or Windows NVIDIA GPU/HDR/VFR/long-film hardware. Add further acceptance evidence before changing this status. This stays in the existing QHE Case as a related observation; no Canonical promotion.


### PR #98 first red CI triage and bounded test repair

QHE PR #98 branch head after one repair: `8dd888a6ed55346d57fd698c40e9fc0a6d9e61e0`. The first source-readiness change's test suite initially returned red, and the causes were separated using actual GitHub job logs instead of treating all CI failures as the same product regression:

- Frontend workflow run `38134970979` reached the new Playwright readiness transition, then failed its **test-side string assertion**, expecting `开始硬字幕压制`. The actual long-standing manual hard-sub `runButtonLabel()` returns `使用当前参数开始硬压`. The bounded repair updates only this expectation, without removing readiness checks or modifying encode behavior.
- Windows smoke run `38134970959` stopped at its first FFmpeg-dependent step because Chocolatey failed fetching `ffmpeg` package 9.0.2 with **HTTP 504 Gateway Timeout**. Despite the installer step being marked success, `ffmpeg` was absent in the job environment. This is an external install prerequisite failure, not evidence of a codec regression, and is not silently waived.

Repair source and UIGS task checkpoint were committed to the same PR. **Latest-head CI Pending External Validation**. Separate planned lightweight multi-segment queue remains **not implemented** and must not be represented as a completed feature. Reusable Case-level test practice: distinguish assertions on exact user-facing copy from semantic readiness assertions; diagnose external binary installation before attributing failures to production code. No Canonical promotion.


## Queued Stream Copy: verified Native save failure requires save-only retry

Date: 2026-10-11 · **Merged + exact-head browser/Windows/UIGS CI passed** · QHE PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/100
Product source head: `7b26c4fd2242b6de234287fa771b00ef4ea22c6d`
Merge commit: `133e0e16ae30810866f4a5fbe98c27cac7343f70`
QHE durable task checkpoint: `e02b3d2445e752edaeff64f0973cd5286fa8dc93`

**Observed source-backed failure after #99:** The multi-clip queue correctly serializes real copy jobs and Native save acknowledgments, but a verified clip whose asynchronous Native export failed became a generic "failed" queue row. The queued "export remaining" path refused to override an unsaved verified artifact, leaving a dead end: neither save-only retry from the row nor safe discard was available. The first PR #100 Frontend browser regression also exposed that generic catch/status copy replaced the intended no-reencode recovery guidance. This was addressed in the final head rather than waiving the user-facing assertion.

**Bounded fix:** Retain the completed verified artifact and its original Native `jobId`; hold a per-queue `clipAwaitingSave` reference. Render `待重试保存` with the actionable `重试保存` row control. Route retries through the same existing `#taskSave` export hook. Only a relevant Native export-result event settles the pending row as saved; failed/cancelled saves preserve its artifact for another retry. Disallow deletion, clearing, source invalidation, mode changes, or normal form submissions that would overwrite it. No new encoder path or output concatenation.

**Evidence:** Frontend/Playwright exact-head run `38143257105` success; Windows local smoke `38143257110` success; UIGS Evidence Coverage `38143257131` success. Actual Chromium artifact `11703821648` shows the compact 390px two-clip queue without horizontal overflow. A scripted browser scenario covers another clip's failed Native save, an unrelated job event not satisfying the pending save, save-only retry, a matched success, and **no repeat encoding**. PR merged and no open QHE PRs at closure.

**Boundary:** Native event simulation is not a real Windows save-picker or Android SAF dialog. On-device failures, cancellations, duplicated/missing job identifiers, file-naming collisions and long-video output verification still warrant physical testing. Keep them FIELD-PENDING; do not promote this one product Case into Canonical.

Reusable pattern: a completed compute artifact and an unfinished export form separate lifecycle phases. An asynchronous export failure should preserve the artifact and offer an export-only retry, while guarding against destructive source/task changes until the artifact is saved or explicitly discarded under an approved workflow.
