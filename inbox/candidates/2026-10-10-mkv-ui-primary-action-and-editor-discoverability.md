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
