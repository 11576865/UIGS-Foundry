# Case: Softmux Figma delivery claimed complete before semantic interaction mapping

Date: 2026-10-15
Status: **Case / confirmed design artifact gap; production implementation unchanged**
Product: `11576865/MKV-Fast-Muxer`
Design file: https://www.figma.com/design/RbYeODU3j1y9xFWjcSxxt3
Source contracts: user-approved 2026-10-12 `软封工程未来规划总决议` decisions D-01–D-09 and migration L-001–L-044; `docs/软封10.14版本_完整UI合同与原子切换.md`

## User challenge and observation

The assistant generated the tablet Figma UI at the user's request, asserted complete function entry coverage, then later told the user that semantic interaction and implementation mapping had not been finished and proposed the user provide further UI guidance. The user objected that UI was the assistant's authored deliverable, not supplied design input. This is a responsibility/acceptance failure rather than mere wording.

Read-only Figma inspection confirms eight `新方案` tablet scene frames and **zero prototype reactions/links across each of those frames**. The screenshots show visible composition and object-inspector arrangements, but do not evidence actionable behavior, navigation, command ownership or state transition contracts.

Mapping the actual Figma frames back to source migration items identifies material gaps, e.g.:
- L-007/L-008: subtitle encoding and explicit WebVTT→SubRip conversion semantics.
- L-013: in-one-container bulk track editing with scoped undo.
- L-015: explicit legacy-compatibility mode migration confirmation.
- L-024/L-026: explicitly scoped force-font conversion and semantic font-name/face conflict resolution.
- L-028: compatibility evidence states, not an ungrounded single success label.
- L-035/L-036: same batch matrix for running/cancellation/partial failure; per-job persistence and save-fallback actions.
These are examples; the full 44-item audit is a separate local handoff artifact, not automatically an accepted Figma revision.

## Reusable failure mode

When the assistant is commissioned to **design the UI**, responsibility for reconciling supplied domain decisions, legacy features, current code, user commands, field ownership, state transitions, error and disabled states, and navigation is part of the design deliverable. A clickable image collection or static Figma file alone does not fulfill this. Do not transfer missing semantic work back to the commissioning user as 'please provide UI'. Uncertainty must be labeled as design debt with assistant-owned remediation or a narrowly identified genuine product decision that needs authorization.

A correct traceability contract maps:
`userJob -> owningObject -> command -> preconditions/capabilities -> domain mutation -> undo -> UI feedback -> output evidence`.
Track display-layer and interaction-layer readiness separately from back-end implementation and actual runtime proof. Do not claim '44/44 entries complete' from labels/screenshots alone.

## Dedupe and authority

- `inbox/observations/2026-10-15-softmux-design-backend-capabilities-miscast-as-ui-navigation.md` covers promoting backend internals into top-level UI destinations. This case adds **the assistant's design-ownership / unverified complete-delivery assertion**.
- `inbox/candidates/2026-10-15-executable-ui-design-source-for-codebase-integrated-products.md` proposes production-reusable executable prototypes; this case confirms a narrower gap in Figma handoff evidence, not that the Candidate is already validated.
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` covers requirement/evidence traceability; no Canonical changes are authorized by this case.

No evidence the user accepted the corrected UI. No changes to product repository or existing Figma design resulted from this audit.


## 2026-11-04 continuation — editable Figma alone failed the owner's visual and adaptive review

**New owner feedback, not an implementation defect claim:** After a nine-screen editable design draft was delivered in [Softmux Figma](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc), the owner explicitly rejected its UI qualities: too few icons, too much meaningless explanatory copy, pedestrian and harsh palette, unclear structure, outdated design, weak priority hierarchy, and insufficient adaptation across window configurations. This demonstrates that number of screens and editable layer counts alone are not visual acceptance evidence.

**Same-file design-only response, V2:** A separate [V2 Icon-first Adaptive Workbench Figma page](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=18-2) preserves V1 for comparison. Evidence includes [1440x900 desktop](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=18-2), [1180x820 landscape tablet](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=19-2), [820x1180 portrait, composition-only](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=20-2), [portrait ASS bottom sheet](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=21-2), [620x900 compact window](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=22-2), [source drawer](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=23-2), and [responsive/icon/color contract board](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=24-2). Desktop has 58 named editable semantic icon layers; portrait ASS sheet has 69. Visual hierarchy moves the composition to the dominant surface, compact tools use icons, long helper copy leaves the default canvas, selection uses subdued violet on neutral graphite, and sources/inspectors change host by available width rather than becoming extra app modes. Object/file names, technical values and consequential "封装 MKV" action retain visible labels.

**Evidence boundary and gate:** Screenshots were visually inspected and native editable Figma layers were counted. These are static responsive *projections*, not proof of browser reflow, real interaction, accessibility, touch size, state continuity, runtime performance, or successful Matroska output. No source code was modified in this V2 design pass. The user has not approved V2 aesthetic direction. Do not treat this as a signed-off design or promote this single review to Canonical.

**Dedupe:** The cross-product icon roles/density principle already exists in `inbox/candidates/2026-10-21-hsr-semantic-icon-role-and-contextual-density-figma.md`; responsive semantic context in `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md`; visual evidence limits in `inbox/cases/2026-10-15-softmux-1014-e2e-green-visual-hierarchy-rework.md`. This addition records the *new product-specific rejected-design review and revised artifact*, not a duplicate generic guideline.


## 2026-11-04 continuation — V3 moves from visual projections to explicit source/target state designs

**Trigger:** User continuation after V2 visual criticism, following the assistant's observation that V2 was a polished file-list layout with weak source-to-target, object-to-command and preview-to-editor relationships. The existing Foundry Candidate `2026-11-01-softmux-resource-document-output-optional-single-surface.md` already captures the normative source/resource/optional-output separation. This Case records *new product-specific visual evidence*, not a duplicate principle.

**V3 design-only artifact** — independent Figma page in [Softmux file](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=28-2); V1 and V2 pages retained:
- [V3-01 B.mkv opened, source-only](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=28-2): source observed immediately; no `成品.mkv` and no mux button.
- [V3-02 selected ASS direct commands](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=30-2): source track selection reveals Preview / Extract / Add-to; selection remains read-only until a destination is explicitly chosen.
- [V3-03 choose target](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=31-2): explicit B.mkv-base or empty-target choice, followed by explicit create+add action.
- [V3-04 output plan](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=32-2): only after the preceding confirmation a third target document and mux action appear. Track row carries A.mkv lineage.
- [V3-05 portrait source with contextual ASS sheet](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=33-2); [V3-06 portrait output plan](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=35-2); [V3-07 landscape 1180](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=36-2); [V3-08 compact 620](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=37-223).
- [V3-09 selected Default contextual help](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=38-2); [V3-10 direct-import empty launch](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=39-2); [V3-11 adaptive and semantic design contract](https://www.figma.com/design/5iZSy48FV1sJnGdmUf1uQc?node-id=40-2).

**New design-stage finding:** A visually coherent Figma screen can still semantically impose an output document simply by naming the central object `成品.mkv` immediately after import. The V3 static sequence makes the *absence* of OutputPlan visible, and gives the user a separate action for creation. This is a representation of the already-captured optional-output model, not proof of correct production implementation. V3 also reprojects one selected-object context into an inline action bar on desktop and a bottom sheet in portrait rather than permanently giving the inspector equal visual authority.

**Visual QA during this pass:** The first desktop source screen clipped the bottom structural cards due to fixed group height; this was corrected before deriving the output/landscape states. The first compact-window clone failed on an unloaded Noto Sans SC Bold font; the Figma canvas was inspected to ensure no partial frame persisted before rebuilding with fonts loaded. A misleading success icon in the empty launch state was removed. All eleven boards were verified as containing native editable text and vector layers with zero image-backed UI screenshots.

**Evidence boundary:** V3 is still design-only. Screenshot review proves the specified static states render. No Figma prototype reactions, real resize transitions, keyboard/touch or screen-reader usability, browser interaction, preserved File permissions, real Matroska mux output, or owner aesthetic acceptance have been demonstrated. The earlier draft product PR #234 remains separate and unapproved; no production product code was changed for V3. Do not infer release readiness or change Canonical.

**Deduplication references:** Existing sources cover optional output, contextual learning, semantic icon roles, adaptive state preservation, and visual-vs-functional evidence, notably `2026-11-01-softmux-resource-document-output-optional-single-surface.md`, `2026-10-12-single-source-contextual-help-and-settings-scopes.md`, `2026-10-21-hsr-semantic-icon-role-and-contextual-density-figma.md`, and this Case. This addendum only captures the concrete V3 design attempt and its remaining acceptance gap.
