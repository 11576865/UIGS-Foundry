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
