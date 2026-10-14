# Candidate — ASS fixed workspace: aspect-first media layout and task-dependent density without anchor swaps

Date: 2026-10-14
Status: Candidate / DRAFT next-version layout proposal for user review; NOT approved, implemented, compiled or field-validated.
Product: 11576865/ASS-Workbench-Android
Context: user-provided pending-review 1534×960 ASS Workbench concept screenshot, subsequent explicit request to optimize UI layout and design the next version without drawing an image.

## Specific proposed delta

1. Retain stable Event navigator (left), media image/playback/timeline (center), context-aware Event inspector (right) in expanded landscape. Changing between 正文 / 排版 / 时间 / 效果 alters control density and region allocation rather than swapping the main media and editor columns. Remain within one Domain/Editor Session; no duplicate Native editor owner.
2. Render the video without a redundant visible “预览” header, multi-layer ornamental pane or fixed-height black placeholder. Determine displayed pixel bounds from current source aspect and constrained available rectangle. Proposed allocation: determine region widths and minimal active time/editor heights, then display media at `videoHeight = min(centerWidth / displayAspect, remainingVerticalBudget)` (with corresponding videoWidth); video hosting space hugs the actual letterboxed-content bounds instead of claiming all leftover height via `weight(1f)`. Remaining vertical budget is reallocated to the active timeline/editor rather than left as unnecessary inner black space. Do NOT stretch/crop media to fake occupation; genuine letterbox due to video-to-window ratio is distinct.
3. One time dock/component instance remains mounted, with task-inferred default densities and manually overridden heights: compact in 正文/排版, expanded in 时间, keyframe/transform-aligned in 效果. Task changes keep media PTS, current event, timeline viewport/zoom/snap, draft, selection and history.
4. Per-field effective source/value belongs beside the corresponding inspector control, while a persistent write-scope receipt adjacent to Apply shows read object, actual write layer, object count and draft conflict. Separate document Save from Event Apply. Editing shared Style is its own explicit operation; mere provenance inspection cannot change write scope.
5. Window adaptation uses usable bounds (WindowMetrics/Insets/IME, video aspect, tools' minimum hit targets) not device-name heuristics. Collapse into 2 columns/sheet or 1 focused column only when min viable dimensions cannot be met. Protect saved user layout from IME-induced transient clamps and restore on rotation.
6. Avoid duplicating global mode icons when task tabs and tools menu already exist. Keep explicit discoverable paths to all previous professional tools and the optional SPATIAL Host, without creating extra business state or silently migrating saved tool IDs.

## Distinct contribution vs existing Foundry work

- `inbox/observations/2026-10-14-ass-preview-aspect-panel-chrome-attribution.md` established visual-vs-code attribution and identified `weight(1f)` risk, but did not specify task-dependent space allocation for a stable three-anchor Fixed host.
- `inbox/observations/2026-10-13-ass-real-android-ui-video-comparison-and-spatial-anchors.md` grounded stable anchors from comparison footage.
- `inbox/candidates/2026-10-03-presentation-density-state-continuity-by-stable-component-identity.md` established preserving a single timeline instance under density changes.
- `inbox/candidates/2026-10-14-ass-per-field-provenance-and-write-intent-receipt.md` covers fine-grained source/write scope, not the full layout.
This entry is the **composition and allocator hypothesis** integrating them, not an invented new fundamental interaction law.

## Falsifiable layout tests required before promotion
- Actual Android Compose measured image bounds, panel bounds and reclaimable idle area for 16:9, 4:3, 9:16 and portrait/landscape window sizes. Never classify true aspect-ratio bars as needless blank.
- Switching tasks and IME show/hide retains Focus, Selection, media PTS, uncommitted Raw/parameter draft, timeline viewport, source binding, Undo and user proportions; no accidental text commit.
- Inspector still exposes all professional tools/Raw and Apply is visible/accessible with enlarged fonts, TalkBack and target hit areas.
- User-resized pane sizes survive ordinary task changes; task-based density defaults do not override explicit user choices.
- Source-preflight/attach-vs-replace semantics are a separate prior reported issue; do not paper over them with navigation rework.

Decision boundary: design proposal for review. No production UI code modifications. No tests or screenshots implied. Do not alter Canonical.
