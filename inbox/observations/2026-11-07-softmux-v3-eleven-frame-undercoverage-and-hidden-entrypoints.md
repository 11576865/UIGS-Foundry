# Observation: Softmux V3's 11 design states underrepresent the feature-entry surface

Date: 2026-11-07
Status: Observation / user feedback; redesign proposal not approved, no product code/Figma change
Project: `11576865/MKV-Fast-Muxer`
Evidence: direct user complaint + inspected design contract, current repository audit and exact UI issue

## User feedback
The owner states: “11张图片还是太少了，而且实际UI有很多功能被隐藏”. This is a **coverage and discoverability** objection, not a request to make every parameter permanently visible.

## Verified source boundary
- `docs/ui-v3/UI_DESIGN_CONTRACT.md` covers 11 IDs V3-01–V3-11. `docs/ui-v3/V3_11_STATE_VISUAL_AUDIT_2026-11-07.md` says **10 are visual states, V3-11 is a state/adaptive rules board**, not a screenshot of an application screen.
- The approved V3 contract explicitly defers batch as a legacy entry instead of a first-class required 1.0 UI workflow, though real batch capabilities remain in code. This is a product-visibility/design-scope tension, not proof those code capabilities are deleted.
- `docs/ui-v3/UI_ACCEPTANCE.md` and open Issue #256 explicitly separate functionality/Chromium evidence from full visual, touch and release signoff. Open PR #265 provides a scoped opt-in shell but records unapproved Figma mutable-reference drift.
- No complete current UI click-depth/hidden-controls inventory or measured user-discovery failure rate was obtained in this intake. Do not claim an enumerated number of inaccessible functions.

## Candidate design-analysis principle (not Canonical)
A small storyboard can explain the principal journey without covering a complex tool's functional entry system. Measure UI design completeness against a cross-indexed **capability × object/task context × screen/state/viewport** inventory. Each capability needs an observable entry, action owner, effect/denial, ability/permission boundary and concrete verification. Track separately:
1. implemented product capability,
2. discoverable/reachable affordance,
3. design-state representation,
4. exercised browser path,
5. physical-device acceptance.

Avoid both extremes: hiding professional functionality behind obscure legacy/advanced paths and presenting a dense always-on feature brochure that makes the primary workflow unusable. Prefer persistent **category/task entry points**, object-context actions and on-demand high-complexity editors; important irreversible actions should remain semantically labeled at execution.

## Proposed next validation
Inventory all retained legacy and mainline product functions (including batch, subtitles/font delivery, attachment/chapters/tags bounded actions, inspect, verification, recovery); link each to actual V3 route/click path and Figma state; mark visible / contextual / legacy-only / unsupported / unreachable. Use this to design additional functional states instead of picking a screenshot count before assessing coverage. Verify real Chromium geometry and interactions and obtain owner approval before changing the frozen design contract, Figma or production default. “~50 states” is an exploratory planning target, not a design acceptance criterion.

## Dedupe
- `inbox/cases/2026-10-15-softmux-ai-concept-images-feature-catalog-vs-operable-ui.md` records the opposite earlier error: showing a feature catalogue as static UI and confusing simultaneous exposure with operability.
- `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md` covers hidden action labels and contextual editors in concrete layouts.
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` separates requirement completion from visual/device coverage.
- This Observation adds the **current V3 storyboard-count vs whole-product route completeness mismatch** and the owner's explicit rejection; it neither replaces prior records nor warrants a Canonical change.

Sources:
- https://github.com/11576865/MKV-Fast-Muxer/blob/main/docs/ui-v3/UI_DESIGN_CONTRACT.md
- https://github.com/11576865/MKV-Fast-Muxer/blob/main/docs/ui-v3/V3_11_STATE_VISUAL_AUDIT_2026-11-07.md
- https://github.com/11576865/MKV-Fast-Muxer/issues/256
- https://github.com/11576865/MKV-Fast-Muxer/pull/265


## 2026-11-07 same-task implementation evidence (design only)

Owner said “做” to execute the proposed full-state redesign. In the existing Figma file `5iZSy48FV1sJnGdmUf1uQc`, a separate **V3.5 Draft page** was created without modifying the approved V3 page:
- Page: https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=60-2
- 55 unique editable Frames after 44-capability coverage review: A6/B9/C9/D8/E8/F5/G4/H6, with 1440 desktop, 1180 landscape, 820 portrait and 620 compact samples.
- Important source/context/target/validation boundaries are represented; specialist pages include ASS preview **illustration**, ChapterUID/Tag relation, batch matrix, queue, output audit, empty-state drop target and 1GB nonblocking warning. The sample data and static preview are not real media evidence.
- Reusable navigation component `V3.5 / Nav Entry` is used as 495 linked Figma instances across all 55 screens. One inspected visual bug (white auto-layout gap leakage) was corrected.
- A draft **docs-only** review PR [#266](https://github.com/11576865/MKV-Fast-Muxer/pull/266) adds the mapping of original L-001—L-044 to proposed design entries and an index of 55 direct frame links.

**Evidence boundary:** Figma structural/editable-layer checks and selected screenshot spot-checks support a real design artifact, but they do not prove 55 uniquely implemented production actions, pixel parity, usability, full-device accessibility, executable Figma prototype navigation, or product release readiness. Original 11-state Figma source authority drift remains unresolved; Batch first-class navigation is a candidate scope change requiring approval. No `Canonical` rule was changed and this existing Observation remains the appropriate classification.

**Revised interpretation of the earlier planning count:** the initial “~50” was a nonbinding discovery estimate. The four added states B09/C09/D08/E08 explicitly close uncovered legacy capability *design representation* (L-013/L-024/L-018/L-034), showing why **requirement-driven coverage** is more appropriate than predeclared frame count.


## 2026-11-07 next-step production entry pilot (partial / CI exact-head pending)

Source inspection in `11576865/MKV-Fast-Muxer` confirmed the batch engine and editor **already exist** under the actual `#sf14Batch` DOM: `src/softmux-10.14-workbench.js` rehosts `.stage-batch` and keeps its `#batchPlan` / `#batchUnifiedInput` / existing handlers. The V3 presentation moved the only `[data-sf-view=batch]` control to `.sfv3-legacy-menu`, leaving just icon-only source and add rail actions. This is a concrete **navigation/accessibility and functional-entry layering** mismatch, not evidence of missing batch computation.

[Draft PR #267](https://github.com/11576865/MKV-Fast-Muxer/pull/267) introduces a strictly opt-in `?ui=v3&nav=full` pilot with four clearly labelled native routes (source, explicit output plan, Batch, container tools). It clicks the original `[data-sf-view]` owner rather than creating duplicate DOM File inputs/editors; adds specific CSS precedence for `[hidden]` in batch/tools mode, and tests exact `File` identity and unconfirmed-target blocking. **The accepted/default UI remains unchanged; this is not nine-route V3.5 completion or approved Figma parity.**

Exact-head new CI runs are in progress, so no pass is claimed. Two earlier red test observations were narrowed:
1. The first Chromium test used MP4 yet assumed the same MKV-specific scanned track rows as the existing V3 Matroska fixture. Code inspection (`publishV3ResourceRegistry` / `sourceRowsFromObservation`) supports keeping those evidence types separate; the red test alone is **not** a verified MP4 import product bug.
2. `#batchUnifiedInput` is intentionally cleared immediately after `change` in `src/main.js`, while the actual `batchImportEntries` and `#batchAssetInventory` own identified imported objects. A new test incorrectly asserted input.files still held selections and was changed to inspect actual inventory rows. Reusable testing note: **do not equate native picker input.files lifecycle with transferred domain-owned source identity**.

Related existing entries: `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md`, `inbox/observations/2026-10-15-softmux-global-add-active-task-context.md`, and `inbox/cases/2026-10-15-softmux-ai-concept-images-feature-catalog-vs-operable-ui.md`. This is a deduplicated follow-up to the current Observation. No Canonical modification; device/browser visual acceptance and full feature-coverage audit remain Pending.


### Exact-head confirmation for the opt-in native-entry slice

Commit `6e2a8b0e471d3917f50a044f5fe6b30475b1e591` of Softmux [Draft PR #267](https://github.com/11576865/MKV-Fast-Muxer/pull/267) passed [V3 Pilot Actions #42368921969](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42368921969): Node tests, build, the new actual Chromium native Batch/Tools entry test, and pre-existing V3 browser scenarios. Independent new-MKV [#42368921943](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42368921943) passed. V3 screenshot/JSON artifact [#13572408502](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42368921969/artifacts/13572408502) was uploaded.

**Evidence limit:** full Browser E2E [#42368921977](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42368921977) was still in progress when checked; neither production default switch, physical tablet operation nor 55-state design/implementation parity is proven. The earlier CI-red test fixture and cleared-file-picker assumptions were corrected without altering the canonical batch importer. Keep Observation classification, no Canonical promotion.


### 2026-11-07 continuation: ten genuinely connected native task entries

[Draft PR #267](https://github.com/11576865/MKV-Fast-Muxer/pull/267) now exposes **ten named task routes** under only `?ui=v3&nav=full`: source, output plan, tracks, subtitles, fonts, attachments, batch, verification, project/recovery, and bounded container tools. These are not 55 implemented states: each category delegates to one original native route / drawer / verification object and retains File authority. Track/subtitle/font/verification defers to the original target picker if the output plan is unauthorized. The 620px layout makes all ten categories visible in a 2×5 grid rather than relying on horizontal hidden scrolling.

The implementation and real-browser E2E were subjected to screenshot review after a green first run; that uncovered a second-order **UI visibility regression**: expanded unrelated recovery/preview and a selected video card made native subtitle/font controls fall below the inspector viewport. It was corrected without a duplicate editor, then the follow-up full-screen screenshot showed global header clipping from `scrollIntoView`, fixed by native-pane-only scrolling. See [the existing Editor Discoverability Candidate](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md) for this *deduplicated, reusable* implication.

**Exact-head evidence:** `56a26df3d234043a8a50c98174ab0b23f2b5f457` [V3 Pilot #42372513201](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513201) PASS; [new-MKV #42372513241](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513241) PASS; [actual Chromium screenshots #13574686515](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42372513201/artifacts/13574686515), including inspected final subtitle/font visible controls and fixed top bar. As of this writing, exact-head full Browser E2E #42372513264 was still in progress; an earlier head #42368921977 failed an independent batch stop-mode run-record download wait and must not be described as green.

**Remaining Pending:** Figma freeze/source drift, visual approval of all 55 states, physical devices, true broad media corpus, full 44-legacy-feature end-to-end recheck, default UI promotion, and full Browser E2E. No Canonical changes.
