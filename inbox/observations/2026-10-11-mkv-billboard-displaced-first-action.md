# Observation: an onboarding billboard displaced the first action in a media tool

Date: 2026-10-11
Status: **Observed product visual regression; correction submitted, CI and new visuals Pending**
Product: `11576865/MKV-Fast-Muxer`
Correction: [PR #74](https://github.com/11576865/MKV-Fast-Muxer/pull/74)
Previous baseline: merged PR #73 at main `60d41336ed7d6df5a422001289824510ea823d9e`
Related existing Foundry cases: `inbox/cases/2026-10-11-qhe-functional-ui-rebuild-low-copy-workbench.md`, `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md`.

## Direct observation, not generalized aesthetic doctrine

The already-rendered, CJK-correct 390px screenshot at baseline contained the logo, a four-item task navigation, and an entire workflow-overview block with slogan, paragraph, capability chips, and three numbered explanatory cards. The actual `添加文件` control was **below the first 844px viewport**. At 1440px, the same explanatory section occupied roughly 280px vertically before the three-pane workspace. Its text explained the task concept but neither manipulated the media objects nor exposed executable operations.

This is a concrete failure of **first-action reachability and visual priority**, not primarily of wording quality. The user explicitly rejected descriptions masquerading as interface structure and cited familiar tools whose operation should be discernible from the objects and controls themselves.

## Correction scope and safeguards

PR #74 removes the onboarding overview and its CSS, moves the file/folder/drop affordances to the entry surface, keeps file identity and primary-source selection in the inventory, prioritizes the MKV export button over static claims, and collapses format support in a native `<details>`. The four-anchor task navigation remains accessible on narrow/stacked layouts but hides at wide desktop, where all three regions are already visible. Copy in idle states is shortened rather than replaced with competing explanations.

The existing file input IDs, source inspector, original stream editor, preview, batch queue, real mux, cancel, download and audit paths are preserved. Source contracts check IDs and screen structure; browser E2E adds actual 1600px and 390px primary file-action position checks.

**Evidence boundary:** the old failure is visible in existing screenshots; the new layout remains **pending full Node/Chromium CI and new viewport pixel review**. Static DOM predicates alone cannot guarantee clear spatial relationships or working drag/drop.

## Reusable testable hypothesis

For task-centric creation tools, measure whether the first actual user action is immediately visible and whether the current objects and next consequential action can be located without reading expository text. Put rare format/capability information into request-driven disclosure while retaining safety warnings, action labels, unsupported-file feedback and audit evidence in context. Do not substitute icon-only ambiguous actions for prose.

This refines the QHE low-copy experience with independent MKV first-fold visual evidence, but is one observed UI regression and remains an Observation. No automatic Canonical promotion.
