# Case: Rehosted output hub was queried as its own descendant, hiding a real disclosure control

Date: 2026-10-16
Status: **Case / reproduced CI red, corrected at same PR, exact-head Chromium green**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/155
Source area: `src/softmux-10.14-workbench.js`, `src/softmux-figma-tablet.css`, `tests/e2e/browser-mux.e2e.mjs`

## Evidence and failure mechanism

A 1280px real-browser screenshot showed the persistent output bar crowding live execution state, a planned output summary, and the full plan into narrow equal slices. A design correction introduced an explicit `检查与计划` disclosure with `aria-expanded` and Escape closing, keeping the real plan panel, mux/cancel/save/report controls and data authority unchanged.

The first code revision used `const output = workspace.querySelector('.output-hub')`, rehosted this node into `#sf14Output`, then mistakenly searched `output.querySelector('.output-hub')` to insert the disclosure. `Element.querySelector()` searches **descendants only**, so it did not match the `output` element itself; the conditional branch silently skipped creation. New 1280px E2E caught `#sf14PlanToggle` invisible at `browser-mux.e2e.mjs:5977`, head `a829b7ceadea9e4fdab651660a477700fa19d5fe`, Actions run 38772574225 (failure).

Fix: reuse the authoritative `output` node directly as `outputHub`, rather than looking for a nested same-class child. Head `9eba07bf9e0d27749876860bb49ab933e67112d6`, browser E2E run 38773077574, completed/success; build/unit CI run 38773077547 completed/success. The final screenshot artifact 11993070513 shows the new persistent output dock and existing object Inspector/plan still available. No production merge.

## Reusable check

When working with DOM rehosting, write down whether an object is **the selected node** or a **container within the selected node**. `querySelector` and `querySelectorAll` do not include the receiver itself. A null-guarded branch may suppress important UI with no runtime exception. Tests must assert the actual control's existence/visibility, then its click and keyboard behavior, not merely a build and a screenshot of unrelated workspaces.

Visual contract: priority action dock contains current status and controls; full technical plan must remain discoverable in a contextual disclosure rather than become a permanently visible column that crowds all actions. Do not replace live plan evidence with a static label or a fabricated success indication.

## Dedupe and authority

Earlier Foundry case `inbox/cases/2026-10-15-softmux-1014-e2e-green-visual-hierarchy-rework.md` covers visual hierarchy despite green E2E, not this DOM-self-selection defect. Earlier `inbox/observations/2026-10-15-softmux-global-add-active-task-context.md` covers routing a global command to the active task. Searches of Foundry for rehost `querySelector` self selection and output dock disclosure found no matching case. This is a bounded regression and fix, **not Canonical UX authority**.
