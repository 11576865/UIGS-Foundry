# Candidate: Orthogonal product dimensions should not become competing navigation destinations

Date: 2026-10-12
Status: Candidate / user design-review insight plus cross-project architectural hypothesis; not an implemented or validated UI
Primary product: `11576865/MKV-Fast-Muxer`
Related domains: ASS authoring, professional media workspaces, object-centered interfaces
Related prior records:
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`
- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md`
- `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md`
- `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`

## New distinction from design discussion

Four plausible product directions were initially classified as peer modules:

A: ASS/font subtitle delivery;
B: Matroska container composition;
C: output correctness and compatibility verification;
D: source-container inspection/extraction.

The user noted that they are compatible but conceptually different in *every* respect. Analysis yields a narrower, falsifiable candidate:

- B is **domain object and edit authority** (one composed Matroska document).
- D is **observation capability** (source/inventory/provenance).
- C is **cross-cutting evidence and assurance**, applied before and after edits.
- A is **task-specific workflow/recipe** assembled from B/D/C; not a separate backing document or exclusive top-level app section.

Rendering these dimensions as four exclusive pages or independent mutable models forces unnecessary context switches and duplicate source/track representations. A UI should instead bind an active resource identity to relevant inspection, modification, and verification commands, while recipes provide guided entry without spawning a second state authority.

## Suggested representation contract

- One authoritative container composition; one selected semantic resource; one modification log.
- Persistent composed-object navigation on desktop-size layouts, secondary source provenance, contextual inspector, and continuous compact verification status.
- Select item -> context actions and information without navigating A/B/C/D as destinations.
- Allow focused mobile/narrow-screen re-projections without serially stacking every workspace pane into an indefinitely scrolling document.
- Treat viewport presentation (desktop/tablet/narrow) and execution capability (browser/Wasm/native) as independent axes. A narrow viewport must not be mistaken for missing codec support or vice versa.
- For very narrow viewports, preserve core inspection and task access; complex editing may use an explicit focused inspector. Zoom is not a substitute for providing a readable and keyboard/touch-accessible fallback.
- Avoid describing all this as proven UX quality without actual 1440/1280/1024/768/390 widths, zoom, focus and screen-reader acceptance. W3C WCAG Understanding SC 1.4.10 allows focused two-dimensional interfaces such as data tables and toolbars to retain necessary spatial relationships while reflowing surrounding content. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

## Source observations and evidence boundaries

- Product `src/output-composition.js` at main `7781a4f410a9c6edb9a1f3d056091e6ace333cc4` is already a display projection over legacy tracked state, not a general container authority.
- Existing Foundry composition-first Candidate documented three duplicated visible representations, long phone vertical stacks and non-accepted four-tab navigation.
- User's current review explicitly rejects long scrolling, excessive prose, vague iconography/colour, oversized actions, and degraded narrow-screen stacking.
- Matroska official format spec distinguishes tracks/attachments/chapters/tags and font attachments, so these must not be flattened into a single undifferentiated file list. https://www.rfc-editor.org/rfc/rfc9559

This records a proposed *cross-project classification and layout principle*, not visual validation, Canonical status, or a completed product direction. The user has not approved any implementation from this discussion.


## Cross-project extension: source container, stream operations, and output composition (2026-10-12)

In a new user question comparing Quick-Automatic-Hardsub-Encoder and MKV-Fast-Muxer, an existing MKV's embedded video/audio/subtitle/font attachments were correctly recognized as possible **inputs** to hardsub, transcode and stream-copy workflows. This raises a second orthogonality issue beyond navigation: `input container/asset inventory`, `selected source roles`, `per-stream transform`, `resulting stream set`, `target container`, and `physical save destination` are distinct modeling axes.

Source inspection:
- QHE `src/media-task.js` v4 supports selecting video ordinals, video `hardsub/transcode/copy`, independent audio `copy/aac/libopus/none`, independently scoped `trim/full` for video/audio/subtitles, opt-in copy of embedded subtitles and attachments, metadata/chapters toggles, and a separate output-container resolver. It does **not** prove a completed UX to pick an embedded ASS track and use embedded font attachments as the **burn-in filter inputs**; the current hardsub filter explicitly uses staged `__ASS__` and `__FONTS__`, while `src/main.js` provides distinct ASS and font inputs.
- QHE `src/media-container.js` currently resolves MP4/MKV, checks the selected stream/codec policies and refuses certain attachments/subtitle/Opus-to-MP4 combinations. QHE native workers stage and verify before user-selected publication; save location is not encoded by MKV itself.
- MKV-Fast-Muxer `src/mux-command.js` uses `-c copy` for its primary container-assembly workflow, retaining/inserting stream resources without burning subtitles or re-encoding audio/video. It can take QHE output as an input for further soft-subtitle/font/track composition, but that optional two-stage workflow is not proof of automatic app integration. Current soft-mux writer is still video-rooted despite broader no-video document projections.

Tentative reusable recommendation: a cross-project media suite should expose the **same source media as a structured inventory** without equating `MKV input` to `MKV output`, `attachment present` to `font consumed by renderer`, `subtitle track mapped` to `subtitle burned into pixels`, or `output compatible` to `destination saved / player compatible`. Tasks should express stream-level operations; a container composer can own final track/attachment/metadata arrangement without requiring redundant encoding. Avoid an artificial product split that forces the user through a separate mux app for an otherwise straightforward verified native encode.

This extension is a Candidate-level model/integration observation, not an approved QHE feature expansion or implementation, and not a Canonical promotion. Evidence: QHE `src/media-task.js`, `src/media-container.js`, `src/main.js`, `docs/manual-media-workspace.md`; MKV-Fast-Muxer `src/mux-command.js` and `README.md`; user question dated 2026-10-12.


## 2026-11-08 controlled counterexample: eight batch stages became competing navigation rather than usable workspace

The earlier distinction (domain object / observation / assurance / task recipe are not interchangeable top-level destinations) now has one **real screenshot-backed, user-rejected design counterexample** in [Softmux Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), exact HEAD `7bf4bbc50b65c4661fda7f7f2435aad4b4bfa371`. The eight always-visible native Batch "stages" were added under 11 existing top-level task routes. Their implementation only sets `data-sfv35-batch-focus`, clicks an original Source/Recipe disclosure, and scrolls/focuses native controls; it does **not** replace the large underlying long-page visual structure with 8 coherent workspace contexts. The three new summary bars repeat underlying `#batchReviewSummary`, queue status and run console state. This **did not duplicate domain data ownership**, but still duplicated *presentation and navigation*.

Visual comparison of real 1440×900 Chromium `ui-v35-navigation/03-batch-imported.png` (before) versus `ui-v35-batch-deep-workflow/02-ambiguous-pair-blocked-1440.png` (after) places the task content at approximately y=256 before and y=370 after (loss of ~114 px above fold). At 620×900 the 11 global links + 8 large phase cards + 3 summary strips reduce first-screen access to native task content; the screenshot shows the actual queue in the lower portion. At 820px portrait the eight-stage sticky shell competes visually with the native job inspector and queue. The user explicitly challenged the result with “倒退了吧”.

**Crucial asymmetry:** The same exact HEAD's [V3 Pilot #42398683308](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683308), [independent blank-MKV #42398683363](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683363), and [full Browser E2E #42398683260](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683260) were green. Real two-video/two-subtitle ambiguity, explicitly chosen B, per-job subtitle tags, JSON v2 export, independently verified MKV and provenance hashes passed. These facts establish **operational continuity**, *not* that the extra presentation hierarchy improves task efficiency or information density. The implemented scroll/pointer/header regressions had been fixed; usability still regressed at the information architecture level. The user's criticism therefore must not be dismissed by functional CI.

**Candidate refinement (not Canonical):**
- A *native single domain owner* is necessary but insufficient for a coherent UI. **Avoid redundant navigation hierarchies and status echoes** even when all layers point to the same native controls.
- For a professional workspace, prefer a stable object-centered matrix/inspector and contextual task commands over permanent dashboard-like stage cards. If a stage switch does not reclaim actual visual space, it is often only an expensive shortcut.
- Test *effective task surface*: first actionable task/control vertical position, above-fold editor/queue occupancy, number of simultaneous competing navigation choices, redundancy of status announcements, and mobile tablet adaptive pane size. Compare actual before/after same-viewport, same-workload user tasks; screenshots are supporting evidence, not an aggregate success metric.
- Separate **design acceptance** from **code/unit/E2E acceptance**. A green runner with a valid artifact may coexist with an unapproved UI regression.
- Preserve the successful batch editor logic and objective E2E while blocking visual promotion of the 8-card/3-summary shell. Current PR #269 remains Draft with explicit [UI acceptance block review](https://github.com/11576865/MKV-Fast-Muxer/pull/269#issuecomment-6717486884). No source revert was authorized, and no default-release change has been made.

This supplements this existing Candidate rather than creating a duplicate; one product screenshot/user feedback pair is not grounds to modify Canonical.


## 2026-11-08 verified correction: context-sensitive projection recovers task area without new navigation

Following the prior screenshot-backed rejection of the eight permanent Batch phase cards, [Softmux Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269) actually **deleted** `src/v35-batch-workflow.js`, its injection, eight cards and three secondary status echoes. Exact-head commit `130f0e547e58b576fbfbb48b07f5f6af8c98f3c4` passed [V3 Chromium pilot #42450348433](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42450348433) and [independent blank-MKV #42450348497](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42450348497). The complete Browser E2E [#42450348463](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42450348463) was still running when this follow-up was recorded; release-wide signoff remains dependent on it and a user design review.

The correction reused native `#sf14Batch`, `#batchPlan`, `#batchJobInspector`, `#batchUnifiedInput`, `#batchRecipeV2ExportBtn`, `#batchRunConsole` and `#batchResults` exactly once. It surfaced a **previously real-but-CSS-hidden** `.sf14-batch-controls` pair via original events. In desktop 1440px, where the entire source inventory already appears, that pair stays hidden to prevent redundant navigation. At 820px / 620px, the same **two controls** move into the existing native Batch heading; a single `data-controls=sources|recipe` projects the original input or settings region. The default compact task view shows the real task matrix first, not the entire source inventory before the queue. No second File owner, recipe, metadata editor, execution queue, result or new authorizations were introduced.

The exact new 29-shot **real Chromium + independent media** evidence [artifact #13605611113](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42450348433/artifacts/13605611113) and `batch-deep-evidence.json` recorded:
- At 1440×900: native batch queue top **y=199.8**, versus previous visually rejected eight-stage version approximately **y=370**.
- At 620×900: native batch queue top **y=249.5**, versus visually rejected eight-stage version approximately **y=746**. This required fixing the *second underlying cause* (narrow single-column source inventory consuming the viewport) after removing the shell alone; first rollback screenshot still had queue at y≈746. At 820×1180, queue top **y=251.5**.
- At all tested widths, global header top y=0, eleven-category navigation top y=58, no duplicate batch phase shell, no copied status strips, no document scroll and source-only footer absent in batch view.
- At 820/620, pressing actual native "批量资源" displays the same original File intake; pressing "配方与输出设置" displays the original settings and hides sources; returning to task view restores matrix prominence.
- Original real-file ambiguity gate, explicit B assignment, original subtitle title/language field edits, JSON v2 export, one-of-two task selection, new MKV, independent FFprobe/FFmpeg SubRip and tags, SHA-256 output/report equality and original input hashes all **passed**. The receipt reported *1 generated, 1 audited, 0 rejected and 0 failed*. This is evidence of unchanged domain functionality, not a new batch runner.

**Why this refines this existing Candidate:** "less navigation" alone was not sufficient at 620px; the first simple rollback left the original long source inventory above the queue. The effective solution combines **selective removal of redundant navigation** with **conditional projection of the one real native source/recipe panel**, keeping the task object above the fold. Verify both real controls and content geometry. A visually hidden CSS control whose handlers still exist is a functional discoverability bug; actual computed `display:none` and pointer access must be tested rather than checking DOM presence alone. A first-screen coordinate is evidence for this known viewport/sample, not a universal design constant; task-specific outcomes, physical devices, font scaling and design approval remain pending. No Canonical change or automatic merge.


## 2026-11-08 follow-on: one native batch inspector across split tablet and focused compact navigation

The previous Softmux V3.5 rollback restored a matrix-first workspace and removed eight redundant navigation cards, but real 820×1180 Chromium screenshots still showed the **one original `#batchJobInspector` stacked below `#batchPlan`**. User work was not fully object-centered: selection and edit fields required long vertical travel. [Softmux Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), opt-in `?ui=v3&nav=full`, now adds width-conditioned master–detail *presentation*, preserving the exact native source File, job selection and owner:

- **780–1180px**: real matrix and original inspector are side-by-side; measured 820×1180 with 16 real paired jobs, `#batchPlan` width ≈315px and inspector ≈435px, aligned top y≈449px. Only the matrix has a bounded 600px job-list scroller; the owner inspector and all original subtitle language/title/flags controls remain live. Unselected list-item metadata preview is constrained to two visible lines for scan density, but its complete text stays in the DOM, and the selected/focused row plus native inspector retain full detail; the original checkbox label hit column remains 44px wide.
- **Below 780px**: keep the original vertical object editor; clicking **the existing task-row button** delegates to the native selection handler first, then only scrolls the **bounded native batch viewport** to the same inspector and focuses it as a region. This does not modify job metadata, grant File access, start a mux, create a new editor or scroll the global document/header. In the real 620×900 test, after selecting Job #14, inspector top moved from offscreen y≈915 to y≈166 and actual subtitle title input to y≈366, while global header and 11-task navigator stayed at y=0 and y=58. Edited title survived selection of Job #13 and re-selection of #14.
- **Execution checkbox is not task inspection**: selectors `input[data-batch-execute-index]` must never trigger compact detail navigation. A separate 16-job Chromium negative assertion explicitly toggles one of 16 execution checkboxes and requires the original per-session selection count to change without moving to the inspector; this extra assertion was committed after the first successful layout proof and its exact-head CI should be checked independently.
- Tests use one FFmpeg-created real short media stream copied into **16 independently named actual MP4 Files plus 16 independent SRT Files**. These are actual File identities and pairing/multi-job UI exercise, **not** evidence of sixteen independent encodes/muxed outputs. A separate preexisting [real batch output E2E](https://github.com/11576865/MKV-Fast-Muxer/pull/269) still verifies 2 real videos/2 subtitles, true tie requiring manual binding, title/language changes, JSON v2, one selected output, native new MKV, independent ffprobe/ffmpeg audit, SHA256 receipt and source immutability.
- [V3 Pilot #42455512949](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455512949) passed the 16-job geometry, draft-reentry, two-line preview and 44px hit-column tests on SHA `08f043afe9a361de3e602e1ac9742c2eb17955b3`; independently [blank-MKV #42455512968](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455512968) succeeded. Full Browser E2E and follow-on checkbox invariant were pending at this intake checkpoint, and **do not inherit these passes**.

**Reusable candidate refinement**: For professional multi-resource tools, a stable single native object inspector can be made *simultaneously visible* beside a moderately sized list and *directly reachable* on narrower screens without cloning editors or introducing another top-level navigation hierarchy. Test distinct actions: inspection row, execution checkbox, uncommitted metadata draft and scrolling. Real visual geometry must distinguish `batch-queue` panel top from `#batchPlan` nested scroller top: one initial E2E incorrectly compared the nested list y≈443 to the prior queue-card top y≈250, creating a false layout regression until separately measured. Position thresholds need object identity and consistent workload/viewport. Verify with real original File objects, field changes, focus and independent output evidence. No Canonical promotion; physical device, long media and complete 55-state Figma signoff remain outstanding.


**2026-11-08 final opt-in confirmation:** On SHA `f5478102f5ab4d89cccfc874f99395ce1a7f7dc4`, [V3 Pilot #42455734862](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455734862) **SUCCESS**, including the 16-real-File density proof plus the added *checkbox != inspector navigation* negative assertion, title draft persistence, two-line nonselected preview and 44px native checkbox label. [Independent blank MKV #42455734838](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455734838) **SUCCESS**. [Exact-head Chromium artifact #13607456964](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455734862/artifacts/13607456964) reports `passed:true`, 16 independently named real video File identities + 16 SRT, 6 actual desktop/tablet/compact screenshots and runtime geometry. In the 620 screenshot selected inspector top y≈166 and subtitle input y≈366; 820 list/inspector top y≈449. Full [Browser E2E #42455734836](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42455734836) was in progress at this checkpoint. No Canonical promotion, no release or Figma signoff.
