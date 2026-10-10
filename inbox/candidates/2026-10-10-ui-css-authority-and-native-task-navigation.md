# Candidate: Isolate CSS authority and preserve native task navigation in a mature workbench

Date: 2026-10-10  
Status: **Candidate — real-browser verified on one project; do not promote to Canonical**  
Domains: CSS cascade ownership, incremental UI refactoring, keyboard accessibility, responsive navigation, CI evidence

## Observation / triggering conditions

In `11576865/MKV-Fast-Muxer`, Draft PR #69 gradually unified content-first MKV import, source stream index, single-object inspector and output actions. The entire `src/style.css` had grown to 6,238 lines. The latest ~369 lines declared compact stream navigation, master/detail placement, three-zone desktop grid, primary export button styling and mobile task links; these were appended **after** earlier competing desktop/tablet rules. Their effectiveness depended on CSS source order rather than explicit ownership. A previous round of screenshot/e2e work showed that merely piling new controls into the old form-per-track layout makes the interface bigger and harder to scan.

## Reusable candidate

A large legacy stylesheet need not be rewritten wholesale to create a clear ownership boundary:
- Isolate a **cohesive feature authority** (here: MKV workbench surfaces and responsive navigation) into its own CSS module.
- Load that module explicitly **after** legacy globals, so order is part of the entrypoint contract, not merely the happenstance last few hundred lines of one file.
- Preserve existing DOM IDs and domain ownership; relocate only style declarations unless the UI function requires a real host change.
- Add source-level checks that the intended CSS authority is loaded exactly in order, plus *real Chromium viewport checks* and actual application operations. Source matches alone do not establish computed layout equivalence.
- Native hash anchors remain preferable to manually intercepted clicks for jumping among source, edit, output and batch regions; enhance them with `aria-current="location"` only to reflect the current section. This state should be derived from actual viewport geometry, updated on scroll/resize/hashchange, and be cleaned up if the controller is unmounted.
- `scroll-margin-top` and sticky navigation can make a fragment's heading appear **below** a simple top-boundary comparison. Recognize a near-top active hash target while it is visible; let actual viewport ownership take precedence once the user scrolls away. Do not lock the entire active-state model to a stale URL fragment.
- After re-rendering a keyboard-selected object list, restore keyboard focus using stable object identity rather than array position. Navigating among task sections must not remount the underlying editor or erase its state.

## Implementation evidence

Project: https://github.com/11576865/MKV-Fast-Muxer/pull/69  
Head: `ec4ec2ed103a3db4d83fe3aa17f5b8c20e4070ca` (**open Draft / not merged**)  
Chromium CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38027820697  
Pages build: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38027820648  

Changed:
- Split out `src/workbench.css` (~369 extracted lines) from `src/style.css` (6,238 → ~5,868 lines), imported after the original stylesheet by `src/main.js`.
- Added `src/workbench-navigation.js` with `aria-current="location"` active state, scroll/resize/hash lifecycle and requestAnimationFrame coalescing, without intercepting native anchor navigation or focus.
- Updated UI architecture source assertions and added `tests/workbench-navigation.test.mjs`, including scrolling, breakpoint visibility, fragment scroll margin and eventual manual-scroll precedence.
- Full GitHub Actions report **177/177 Node tests**, zero failures, full Chromium E2E MKV scenarios PASS, GitHub Pages deploy/build success. Screenshots uploaded as artifact `mkv-ui-container-tree-viewports` ID `11660956495` using generated non-user fixture media.

## Limits and deduplication

These tests demonstrate the isolated CSS module and enhanced navigation have not regressed the CI-covered MKV workflows. They **do not** prove all computed styles are unique, that the 5,868-line global CSS contains no further contradictory rules, or that human/assistive technology users have completed usability tests. This is one project/case, hence Candidate only.

Foundry searches for CSS authority, cascade override isolation and sticky aria-current navigation did not locate a specific duplicate. Existing `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` concerns import identity and task-role-owned editing, while `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md` concerns semantic context after responsive layout changes. This candidate specifically addresses **explicit stylesheet authority and native URL/viewport-driven section current state**.

Next validations: computed-style snapshot/diff before and after CSS extraction at tablet/coarse pointer and at extreme desktop widths; touch and keyboard smoke tests for the sticky task bar; progressive removal of superseded base selectors by source ownership rather than regex deletion. Never automatically modify Canonical from this single observation.


## Final documented-head CI confirmation

The documentation-only successor head `e1e5f1a2e1d613e363eb673efa94c6ed0de79855` was also validated: [Chromium workflow #38033905034](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38033905034) **success**, **177/177 Node tests passed**, zero failures and all Browser E2E scenarios passed. [Pages workflow #38033905073](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38033905073) **success**. Synthetic UI screenshot artifact `11663048742` uploaded. The PR remains Draft/open and not merged; no Canonical promotion.


## Phase 9 — move base intake/tree styling into its actual authority (2026-10-11)

Project branch: `11576865/MKV-Fast-Muxer`, Draft PR #69, pending final CI head `22ee88477c4d8ff64cefe6d21624414d310b2fb4`.

Follow-up code audit found Phase 6 still left **279 lines** of content-first import and source-container tree declarations at the end of `src/style.css`, although modern stream index/inspector/output rules lived in `src/workbench.css`. This meant the same feature retained two separate style ownership locations despite explicit CSS load order. Phase 9 moved all source intake/tree styles to `workbench.css`, keeping the same selectors and original relative cascade order. `style.css` fell to ~5,587 lines, and the workbench file now owns its source inventory, stream tree, selected-object inspector, batch intake, responsive zone layout, and native navigation. An authority regression asserts none of four key marker blocks migrate back into legacy CSS. The prior `tests/desktop-layout.test.mjs` also contained outdated positive assertions for icon-only main actions and the old side-by-side preview/editor; tests now assert the current three-zone and visibly labeled output contracts instead.

The new real Chromium responsive scenario exercises **1600 → 390 → 1600 px** after an actual source MKV scan, verifies the selected stream identity, edited title and single live inspector survive without DOM remount, and checks native mobile navigation. The first attempt at this test timed out because the default `appendPreserveAll` mode had correctly disabled track metadata edits. The test now explicitly opts into selective edits before filling the title; it does **not** loosen this product safety gate. [Chromium run #38075840710](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38075840710) then completed **success with 186/186 Node tests and all Browser E2E scenarios passing**, including the new viewport retention flow. Artifact #11678254862 contains fixture-based screenshots. The later test-contract cleanup and documentation head `22ee88477c4d8ff64cefe6d21624414d310b2fb4` is **pending latest-head CI** at this record update and must not inherit the earlier result without verification.

Generalizable Candidate: stylesheet modularization is incomplete if only the last layer of overrides moves but the feature's base selectors remain in another file; audit **feature-specific ownership, source order, actual browser behavior, and stale tests** together. A test that selects a disabled editor under an intentional safe default should first reproduce and respect the task-mode precondition, rather than removing the guard. No Canonical promotion from one project.
