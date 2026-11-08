# Candidate: Compact desktop workbench UIs must preserve semantic action and editor discoverability

Status: **Candidate / awaiting browser visual CI**  
Date: 2026-10-10  
Domains: UI information architecture, task-driven controls, responsive adaptation, media workbench UX

## Observation and evidence boundary

Project: `11576865/MKV-Fast-Muxer`  
Baseline: `main@d5669c6d9bb6ebdd6843ee8c7f651902c80c4d08`  
UI-first Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/67  
Draft head at intake: `81d7c479450fa609129b5dc2c0809f5108fe0326`.

A source review of `index.html`, `src/style.css`, `src/object-editor.js`, responsive layout tests, and Browser E2E showed that a previous desktop compaction layer hid the preview title and the five-category object editor focus navigation while using an **icon-only 48px button** as the primary mux action. The complete DOM editor and keyboard-capable filter continued to exist, and the mobile UI exposed navigation more explicitly; the desktop presentation made these operations less discoverable. The code-grounded observation is not yet evidence of a measured user error rate or screenshot-based failure.

The user explicitly prioritized improving existing MKV functionality by **redesigning UI first** and deferred all MP4 *output* work. The first targeted proposal retains the existing 01 source → 02 preview/edit → 03 MKV output workflow, restores desktop preview heading and object navigation, and provides visible primary mux, cancel and save labels. It does not touch FFmpeg, result contents, preview renderer or output container selection.

## Candidate learning

In a visually dense professional workbench, reducing text can accidentally remove **the only visible action name or navigation affordance** even if accessibility labels and keyboard events still exist. For primary, consequential task actions:
- Do not depend solely on icon interpretation, hover tooltip, or aria-label for semantic recognition.
- The core task action should be visible and named at the execution point, including relevant task constraints (here MKV-only and video/audio Stream Copy).
- Contextual object navigation should remain discoverable at the viewports where object controls are most complex; hiding it for cosmetic density may remove useful focus despite all original panels remaining in the DOM.
- Favor showing/hiding existing editable controls rather than remounting them to avoid losing unsaved metadata.
- Preserve smaller-viewport projection contracts; desktop improvements should not inadvertently expand five-category navigation into a two-mode phone editor.
- Verify actions **both semantically and geometrically** across representative viewports; source-order regex matches alone cannot establish visual correctness.

## Implementation and tests

Draft PR #67 includes HTML and responsive CSS, retained existing control IDs, new `tests/mkv-ui-hierarchy.test.mjs`, updated old icon-only desktop assertions, and a Browser E2E scenario for 1440px desktop and 390px phone with object focus and overflow assertions. A source-derived V8 harness executed **10/10** UI source checks; E2E parsed. **Actual npm CI / Chromium E2E / screenshot and human visual acceptance pending** at this intake point. The PR is intentionally Draft and must not be promoted to merged or production-validated based on static tests.

## Deduplication and scope

Foundry search terms `icon-only primary action workbench`, `context navigation hidden desktop`, `progressive disclosure editing objects`, `task primary action discoverable`, and `responsive layout UI evidence` found no duplicate record of this specific primary-action discoverability regression. Related records:
- `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md` concerns test navigation after presentation transitions, not hidden desktop action affordances.
- `inbox/candidates/2026-10-03-responsive-geometry-assertion-viewport-reflow-observation.md` addresses E2E reflow races and synchronization, not task-entry labeling.

This Candidate should not be promoted to Canonical from one source review and a pending Draft PR.


## Product-direction correction — initial UI PR rejected/superseded

The user objected that restoring labels and desktop object-filter navigation preserved the **four category-specific upload boxes**, despite the project's shift toward content identification. This is a substantive **information-architecture mismatch**, not merely an affordance issue. PR #67 was **closed without merge**: https://github.com/11576865/MKV-Fast-Muxer/pull/67. Follow-up specification: https://github.com/11576865/MKV-Fast-Muxer/issues/68.

The previous Candidate's claims about the icon-only action remain source-grounded, but its proposed first UI change **did not adequately address the requested transformation**. Its 10/10 source-derived checks establish only narrow markup/behavior invariants and are not evidence of correct future UI architecture. Do not cite PR #67 as an accepted UI redesign or merged change.

The corrective direction is a content-first asset inventory and explicit primary-source/track role assignment after classification. Four categories can remain *views for editing*, not top-level gates for importing. The current `main.js` also contains a single-job prerequisite `if (!video || !subtitleTracks.length) return;`, so merely unifying the file picker cannot make arbitrary valid container-only remux scenarios executable. Address task schema and execution readiness before interface cosmetics.

**Status: superseded implementation proposal; retained as a narrow Observation/Candidate, not Canonical.**

## 2026-10-11 object-oriented selection follow-up

The user rejected successive copy reduction and work-area framing as insufficient in MKV-Fast-Muxer PR #74. A domain/model inspection found the underlying selection mismatch: imported subtitle/audio/font objects were visible in the unified asset inventory, but the user still had to independently locate the corresponding `object-editor` category and individual metadata field. A source-container track already had `data-tree-select` linking to a single shared inspector; imported adjunct resources did not have an equivalent direct bridge.

This bounded revision adds one explicit **编辑** control per supported external asset row, maps its file identity to the original `newSubtitleState` or `externalAudioState` row via stable file-key equality, and focuses the existing matching title field; a font row opens `fontMode`. On phone the same click reveals the existing edit work area. It does not clone forms, change ffmpeg.wasm/stream-copy logic, or drop unknown/unsupported diagnoses. A focused item loses its highlight on removal. The selected source inspector additionally receives explicit border-box, max-width and min-width constraints after a real Chromium geometry failure.

**Verification boundary:** previously observed run 38134061521 had 203/203 Node tests passing, but real Chromium failed on central inspector geometry. Subsequent changes are submitted in the same PR #74 with added browser-selection and Node source contracts. These remain **pending exact-head Chromium E2E and updated screenshots** and do not establish accepted design quality or promote this Candidate to Canonical. The reusable hypothesis is that list selection should resolve to the _same identified object's existing editor_ rather than merely open a separate category screen. Validate data identity, focus movement, responsive projection and post-mux results together.


## 2026-10-11 stream-selection single-owner follow-up

The next concrete MKV PR #74 regression arose from an overlapping **two-editor projection** of one source stream: a selected track populated the single `assetInspectorHost`, yet the legacy `.source-track-card` could also display the complete `#trackList` and `#attachmentList` when the `source` editor category was active. Both wrote the same `trackState`, so this was a duplicate *view* of one editor, not a duplicate domain-state owner; it still harmed spatial clarity and direct manipulation.

Bounded correction: selecting a source stream sets the existing category to `source`, retains the container-level `scanTracksBtn` and `appendPreserveAll` safety controls, hides its redundant full track/attachment rows in ordinary unified mode, and keeps the explicitly invoked advanced source editor accessible. The selected `assetInspectorHost` remains the single normal track attribute editor, with state shared through the existing source model. Add source-contract plus browser assertions that the second full table is hidden after stream selection but advanced mode remains available.

**Evidence boundary:** previous exact-head PR #74 CI had 204/204 Node passing; browser halted on an unsupported `Locator.isFocused()` test helper rather than establishing the actual focus behavior. Three calls now use supported `locator.evaluate(el => el === document.activeElement)`, without relaxing assertions. The selected-inspector projection and actual FFmpeg/evidence paths remain **pending new exact-head Chromium and screenshot review**. Avoid extrapolating to a canonical rule without multiple observed products.


## 2026-11-04 design-stage observation: contextual action clipped by bounded inspector

Evidence: [Softmux single-surface Figma design, cross-source interaction state](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=10-2); source design review was static Figma only, not production code. During the same-turn design review, the first rendering of the selected A.mkv ASS resource appended a “加入拟输出” button at the bottom of the object inspector. The action was partially outside the visible inspector above the persistent output footer, despite existing as an editable layer. A corrected design removed redundant source-attribute controls from this *source selection* state, exposed the exact selected A.mkv subtitle member in the read-only source browser, and brought the primary contextual action back into the visible inspector.

**Refinement to existing Candidate:** Primary task affordances can be geometrically invisible *inside contextual inspectors* as well as in global toolbars. “An action exists in the panel” and “the action is visible or reachable without unexpected scrolling” are separate claims. Evaluate bounded panel height, persistent footer overlap, scroll/keyboard reachability and touch target size on portrait/landscape viewports; avoid solving overflow by duplicating an editable state. Source members shown for selection are not second authoritative copies of a target track.

**Evidence limit:** One prototype composition failure and its correction. No real-browser runtime, user testing, saved-file behavior or cross-device geometry is established. This augments the existing discoverability Candidate; do not promote to Canonical.


## 2026-11-07 V3.5 real Chromium counterpart: OPEN does not imply an in-viewport control

This is the real browser counterpart to the **2026-11-04 static Figma clipping observation above**, not a separate Canonical principle.

[Softmux Draft PR #267](https://github.com/11576865/MKV-Fast-Muxer/pull/267) added ten opt-in task entries via native existing source/target/Bulk/inspector/editor/tool DOM. The first Chromium E2E passed source identity, target authorization and `<details>.open` checks, but **visual review of the actual captured 1440×900 subtitle/font screens** showed the native `#newSubtitleList`/font settings below the bounded inspector's visible region because a previously expanded `#sf14Recovery`, an unneeded empty preview drawer and a selected unrelated video card consumed the context. This is a specific **visibility failure despite reachability and DOM existence**.

A correction intentionally did **not** duplicate or recreate editor state:
- entering subtitle/font collapses unrelated recovery/empty preview, uses the same `#sf14OptionsDrawer`, same `[data-editor-filter]`, native `#newSubtitleList`/`#fontMode`, and temporarily projects away the unrelated video inspector context only for the selected specialist category;
- the E2E imports a **real standalone SRT**, explicitly authorizes an MKV target, asserts the live `data-new-sub-field="title"` exists and is actually within the inspector viewport, then checks the real font controls;
- subsequent real screenshots revealed `scrollIntoView()` could **scroll the entire page and clip the fixed workbench header**, even when the field became visible. Replaced with a `revealWithin(field, originalOwnerScrollPane)` helper that changes only the appropriate native pane's `scrollTop`; E2E now asserts the global header remains in viewport when navigating to project/subtitle/font.

**Verification:** exact [PR HEAD `56a26df3d234043a8a50c98174ab0b23f2b5f457`](https://github.com/11576865/MKV-Fast-Muxer/commit/56a26df3d234043a8a50c98174ab0b23f2b5f457) passed [V3 Pilot run #42372513201](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513201), including Node tests, Vite build and real Chromium ten-route/focus test; independent new-MKV [#42372513241](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513241) also passed. CJK screenshots and JSON evidence [artifact #13574686515](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513201/artifacts/13574686515) were manually inspected for subtitle and font fields with the top header fully visible. The 620px screenshot confirms all ten category labels displayed in two rows.

**Reusable acceptance refinement (Candidate only):** In a dense app, **route click / expanded disclosure / DOM element count** are different from **current-task visual accessibility**. Test the selected real control's viewport geometry *and* the surrounding stable shell/focus/scroll owner, using real task fixtures that populate fields rather than empty lists. Distinguish task view projection from second mutable editor ownership.

**Limits:** one product, one targeted native Chrome desktop/compact fixture, not design approval, physical tablet, arbitrary real media, 55-state parity or user discoverability study. Full Browser E2E is a separate release gate. No Canonical promotion.


## 2026-11-08 bounded follow-up: plural subtitle/source ambiguity must preserve exact File ownership and distinct accessible labels

[Softmux Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269) added an **opt-in V3.5 presentation-only** semantic enhancement for two actual unresolved subtitle-to-video ties and one selected Job with two original subtitle metadata editors. It decorates the ONE existing `#batchPlan` and `#batchJobInspector` from `src/v35-batch-review-detail.js`; it does not duplicate or replace the native selectors, File references, exact subtitle `data-batch-track-index` generation, `currentBatchTaskMetadata` map, JobPlan, output authorization, mux runner or audit.

In an actual 820×1180 Chromium fixture (two independent FFmpeg MP4 Files, four SRT Files), the native batch owner returned **two real Job rows plus two genuine tie selectors**; Start was blocked while 2 ambiguities existed, remained blocked after the first explicit session-only mapping, and unlocked only after both manual grants. The V3.5 layer adds per-conflict ordinals ('待确认 01 / 02'), grounded candidate count from the actual native `select` options, and a unique ordinal/file identity group label for each subtitle editor ('字幕轨 01 / 02'). It **never assumes a first candidate** and only observes immediate original render childList mutations to reapply labels when native HTML changes. Each native title/language/Default/Forced control obtains its own source-File-associated accessible name, rather than indistinguishable per-task field labels when 2+ tracks exist. The visual CSS groups actual editors and conflicts in the original matrix/inspector, without new navigation/drawers.

**Independent real-output evidence** from exact-head [V3 Pilot #42463670383](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42463670383) **SUCCESS**; independent [blank-MKV #42463670364](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42463670364) **SUCCESS**; [artifact #13610786950](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42463670383/artifacts/13610786950): eight real viewport images (820 conflict/review/multi-track editing, 620 compact second-track editing/output), original B-two-subtitles.mkv, its JSON report, and `multi-subtitle-review-evidence.json` with `passed:true`. The test edits distinct exact File-bound subtitle titles/languages, switches to the other Job and back, and confirms both preserved. It then selects **only B of two jobs**, executes actual BatchRunner to a new MKV, downloads bytes, and independently checks **two real SubRip streams** with expected title/language tags (`eng` and `zho`), both true cue texts (native FFmpeg extraction), output SHA-256 equals report, and all six original source File SHA-256 remain unchanged. Terminal: **1 generated, 1 audited, 0 awaiting review, 0 execution failures**. The browser UI fixture has two short source videos; it does **not** prove long heterogeneous media, ASS Group font closure, physical tablet touch, or general Matroska edit completeness. Full Browser E2E was still separately running at this checkpoint.

**Candidate refinement, not Canonical:** Counted routes/screenshot cards and one-file metadata forms are insufficient proof for *plural object* professional editing. Use at least two unresolved ambiguous resources simultaneously and two same-target native editors, assert the exact fail-closed state after each partial decision, focus and unique per-File field names, independently inspect resulting actual multi-track artifact and original File immutability. Preserve the native renderer as the single mutable owner; a one-way DOM projection can improve ordinal/context labeling, but observers must avoid recursive loops and must not change business-state inputs.
