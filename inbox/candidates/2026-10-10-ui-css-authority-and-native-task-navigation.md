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


### Phase 9 final-head verification

Draft PR #69 head `22ee88477c4d8ff64cefe6d21624414d310b2fb4` was verified by [Chromium workflow #38076120462](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38076120462), **completed success, 186/186 Node tests, zero failures, all Browser E2E scenarios PASS** (including viewport-edit retention, original-track ordering/dispositions and batch MKV workflows). [Pages build #38076120503](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38076120503) succeeded on the same head. Screenshot artifact #11679315134 was generated from synthetic media, with no claim of a new independent human visual review.

CSS now has a more complete authority boundary (`src/style.css` about 5,587 lines; `src/workbench.css` about 735 lines). Three outdated source assertions were rewritten to protect the current source/editor/output hierarchy and visible action labels, rather than protect an obsolete adjacent preview/editor or icon-only mux button. All 11 directly exercised source-derived desktop/workbench assertions also passed. The safe-default `appendPreserveAll` behavior remains enforced. PR is still Draft, `main` has not been merged, and no Canonical update is supported by this single project observation.


### 2026-10-11 follow-up: when anchor scrolling becomes insufficient on phones

[MKV-Fast-Muxer PR #74](https://github.com/11576865/MKV-Fast-Muxer/pull/74) exposed a distinct boundary of the earlier native-scroll proposal. After removing an explanatory billboard, real 390px/1440px fixture screenshots showed that the phone still vertically stacked the entire source/container tree, current-track editor, secondary settings, preview and MKV output. Although task anchors worked, the controls themselves were separated by many screens. This is a **layout ownership problem**, not a text or scrolling polish problem.

A new bounded PR #74 work unit keeps all original DOM inputs, state owners and hash links, but uses `data-mobile-view` to project only the selected **source/edit/output/batch** area at widths up to 600px. Selecting a source tree row switches to the original inspector; batch selection opens the existing native disclosure. At desktop widths all three separate regions remain visible and nav continues its original anchor/scroll semantics. The active inspector is followed by contextual subtitle preview, before optional supporting configuration. This preserves source identity and editor state as a single owner rather than copying an edited form into the file rail.

**Important:** earlier PR #74 screenshots validated removal of the billboard and above-fold import but not the *new* mobile task projection. The latest functional change and its unit/Chromium assertions are **pending exact-head CI and new CJK visual review**; premature semantic promotion would be unsupported. This may refine the Candidate: native scroll navigation is not sufficient when the actual task areas are too tall; a single-area responsive projection can retain native hash semantics and state identity, but needs keyboard/focus and resize-transition tests, and a single live inspector. No Canonical change.


## 2026-11-08 follow-up: native batch task contexts and fail-closed visual readouts (CI pending)

The existing Softmux 1.0 batch engine already owns `#batchPlan`, `#batchJobInspector`, `#batchFontSubsetEnabled`, `#batchRecipeV2ExportBtn`, `#batchRunConsole`, `#batchResults` and bounded `#batchInspectBtn`. Yet these real functions occupy distant areas of one long batch page. The user objected to **UI coverage and functional depth** after seeing a gallery of 70 images; redisplaying the same screenshots was not evidence of coherent operability.

The follow-on [Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), based on pending #267/#268, adds *eight always-visible, opt-in batch task contexts*—resources, pairing/ambiguity, per-job subtitle fields, font policy, recipe/directory, run control, completed artifact, and independent container inspect. They are **view/focus navigation only**, bound to existing original IDs, data ownership, actual FFmpeg/Wasm batch runner, and native File grants. Derived readouts count existing DOM job/tie/output rows; they do not create an alternative mutable pairing plan or completed output state. The real long-form Chromium test asserts ambiguity → explicit selection → native per-job metadata edit → frozen actual MKV execution → independent ffprobe/report SHA and original source identity. It captures up to 24+ screenshots, correctly labelled as *8 task contexts × 3 viewports*, not 24 new product capabilities. **Full CI of this draft was still pending at intake time; it is not validated by historical green runs.**

A direct first Chromium screenshot exposed a subtle **fail-closed truth/display discrepancy**: with two videos and one same-episode subtitle genuinely tied, native pairing returns **one actionable tie selector but zero executable job rows** and disables Start, as intended. The new test initially and incorrectly assumed two executable rows would exist before resolution; a subsequent test assumed the native summary would say "待处理", but it literally rendered "0 个拟输出 · 无可执行任务". The opt-in UI now prepends a reason grounded in the real selector count, `待处理：1 条字幕配对歧义，需人工确认`, rather than implying a content-free empty plan. CSS visibly dims the already-disabled native Start button so a green primary fill does not falsely signal executable readiness. The underlying authorization gates and job list were not changed.

**Candidate refinement, not Canonical**: A non-mutating multi-context shell can reconcile visible professional depth with a single native business owner. Assess **operability** through real negative and positive state transitions, not nav count or snapshots; for intentionally fail-closed flows, the UI should distinguish "no job because none imported" from "no job because an ambiguity is waiting for human resolution", without guessing or auto-resolving the conflict. Verify status and button visual semantics against actual disabled/execution state. Visual variants, UI state, native business progress and independently verified output remain distinct evidence layers.


### Exact-head confirmation and responsive clipping closure — 2026-11-08

Softmux [Draft PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), commit `7bf4bbc50b65c4661fda7f7f2435aad4b4bfa371`: [V3 Pilot #42398683308](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683308) **SUCCESS** including Node tests, Vite build, source/target/ASS navigation and actual 8-phase Batch Chromium + real output E2E. Independent [blank-MKV #42398683363](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683363) **SUCCESS**. Full [Browser E2E #42398683260](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683260) was still in progress at intake; cannot inherit release signoff. Exact-head [artifact #13584795952](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42398683308/artifacts/13584795952) contains 27 new *actual* Chromium task screenshots, real JSON v2 recipe export, `finished-B.mkv`, output audit report and run record. Independent native ffprobe/ffmpeg verifies SubRip text and changed title `Review confirmed subtitle`, language `zho`, SHA-256 output receipt, and unchanged inputs; native batch terminal generated 1, audited 1, failed 0. The 8 contexts are visible in 1440, 820 and 620; 27 screenshots are viewport/task-state captures, **not 27 independently implemented capabilities**.

**New reproducible UI bug and fix:** Initial 820px phase-nav steps had real pointer interception by the underlying `#batchAssetDropzone` after scrolling, despite phase buttons being semantically visible. Isolating the `.batch-drawer` stacking context and raising the sticky native phase toolbar fixed it; real E2E now tests `document.elementFromPoint` at each of the 8 phase button centers in 820 and 620. A second screenshot review showed the top global 58px header and 11-category toolbar clipped after page-level scroll because an unrelated 56px source-only footer remained rendered while the Batch/Tools viewport-height page was active. Restricting the source status footer to its true owner and bounding Batch/Tools root prevented this; final E2E asserts global header position and task navigation visibility after *every* phase transition, and final 820/620 screenshots were inspected.

**Evidence-layer refinement:** user-visible controls may be in the DOM and have `aria-pressed` but **not be physically hit-testable** due stacking; phase scroll may preserve local inspector visibility while globally removing header/navigation from view. Both visible command center and native content must be tested, including pointer hit target, document scroll, bounded pane scrolling, focus and real output lifecycle. This is a single-project Candidate follow-up, not Canonical promotion. Still Pending: physically held tablet, >1 GB / long heterogeneous sources, actual Group ASS font closure, 55-state design parity, approval for default UI and all 44 inherited capabilities.
