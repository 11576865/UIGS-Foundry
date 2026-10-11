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
