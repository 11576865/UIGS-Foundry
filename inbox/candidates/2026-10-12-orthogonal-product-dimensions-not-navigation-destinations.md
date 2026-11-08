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
