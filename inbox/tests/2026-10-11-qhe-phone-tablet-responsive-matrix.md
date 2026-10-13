# Test: QHE focused workbench responsive viewport matrix

Date: 2026-10-11
Status: **Automated Chromium verification passed / physical-device Pending**
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/94
Merged source head: `5714004a3323b92a697effd0f9dc3a808acf91c3`
Main merge: `840aaef17891cccbfd2cb252c5e5dfd96d8f4ed5`
Evidence: Frontend + Playwright `38130794916` **success**; UIGS Evidence Coverage `38130794896` **success**; Windows smoke not rerun for this UI-only change.

## UI regression addressed

Focused QHE workbench PR #93 introduced `body.ui-tablet .task-overview-rail { display:none }`, hiding task context at every tablet width despite the earlier source design reserving a summary rail for 920px and wider tablets. The earlier `display:block` rule for `.workspace-layout` looked suspicious but did not prove a regression: an existing `display:grid !important` rule remained authoritative. PR #94 removed that contradictory inert declaration and restored the original wide-tablet task summary without remounting existing DOM/Bridge state.

## Browser acceptance matrix

The new `scripts/check-media-ui.cjs` responsive smoke uses a separate Chromium page and checks **actual computed layout** at 320, 390, 640, 768, 919, 920, 1024, 1180 and 1280px:
- Phone through 640px; tablet above 640px through 1180px; desktop beyond 1180px.
- No document-level horizontal overflow at any checkpoint.
- Tablet CSS Grid remains active and runtime entry precedes the main work area.
- Compact tablet (below 920px) does not allocate an overview side rail; 920–1180px tablet displays task overview alongside the main panel.
- At 320px, all three guided mode tabs are visible and each meets the test's 44px height minimum.

Evidence archive: Frontend workflow `38130794916` artifact `media-workspace-screenshots` (artifact id `11698393258`), including real `media-workspace-guided-phone-320.png` and `media-workspace-tablet-1024.png`. Both captures were reviewed: no apparent horizontal clipping or competing side column at 320px, and task overview present beside source controls at 1024px. Existing production capture sources now list `src/focused-workbench.css`, the new appearance owner.

## Regression-test lessons and limits

Initial red CI was a **test selector mistake**, using nonexistent `#workflowMain` instead of the real `.workflow-main`. After correction, the second red CI at 768px read stale `phone` class immediately after Playwright `setViewportSize`. The acceptance script now waits for `document.documentElement.dataset.uiShell` to reflect the requested breakpoint before comparing computed layouts. The final head is green; these earlier failures are not reported as product defects.

The Matrix tests deterministic Chrome rendering, not real mobile OS window insets, actual Android accessibility, physical Windows GPU/long-form processing, or user-task completion time. No Canonical promotion.


## 2026-10-13 recurrence: VVC fixture (Observation, hosted revalidation Pending)

QHE PR #105 frontend run 38340600806 failed the mobile VVC overflow assertion immediately after desktop-to-phone viewport resize. Unlike the existing responsive matrix, this new fixture omitted the uiShell transition wait. Repair waits for uiShell=phone and two animation frames, retaining the original overflow assertion and adding offending-element geometry to failures. This establishes a missing synchronization precondition, not proof that every observed overflow was a false positive: hosted revalidation is Pending. Local regression observed RED then GREEN; 206 Node tests passed, 7 conditional skips; build passed. Same project/upstream lineage as prior evidence, not independent corroboration. No Canonical promotion.

Separate Windows run 38340600773 reported a supposedly deleted oversized manual artifact, but the fixture searched quick-hardsub-job-* while Start-MediaTaskJob owns quick-media-job-*. Correct the namespace, retain file-existence and blocked-export checks; hosted actual staging verification Pending. Scope is test observation provenance, not evidence of a product deletion defect.
