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


## 2026-11-04 V3 owner-approved implementation pilot: real Chromium evidence and unresolved domain gate

**New evidence, not a new Canonical norm:** After the owner explicitly approved V3 design and authorized implementation, the product branch `feat/softmux-v3-approved-ui-20261104` opened [draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239) from exact `main@5ce85fc8d1657797809d25b51c8b51512f762406`. It committed a recoverable contract, implementation map, progress file, opt-in V3 source-first view, source-only projection from live `source:` rows, and reuse of the original File/dropzone/mux DOM. Default product and `?ui=legacy` were retained, V3 pilot exposed at `?ui=v3`.

**Executed test at branch HEAD `7cb6fd62655494c57aa0789eb912616636d2586b`:** [GitHub Actions #41708165401](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41708165401) passed unit tests, Vite production build, and a real Chromium smoke scenario using an FFmpeg-generated MKV. The browser asserted initial empty source without target; real imported source observation; target hidden until an explicit edit action; unchanged native File input and mux control identities after switching to output plan and back; preservation of source filename after 1440×900, 820×1180 and 620×900 reflow; no page errors. Screenshots plus a JSON receipt were uploaded as GitHub Actions artifact `ui-v3-pilot-source-first-evidence`, id `13267111641`. This tests DOM continuity and a limited visible workflow; not full output, cross-source composition, or Figma pixel comparison.

**Critical partial-implementation distinction:** Merely showing a source-only projection while CSS hides the preexisting editor does *not* prove the underlying domain has a genuinely optional OutputPlan. The live legacy implementation still computes a prospective output composition on source import; the branch exposes this as `编辑拟输出` compatibility bridge. The semantic authority change remains WU-02 pending and blocks full V3 acceptance. This is a concrete product instance of the existing optional-source-output Candidate, not a separate generic rule.

**Other observed integration issue:** A new dedicated UI CI initially ran `npm ci` without a package lock (run `41707839232`), then assumed runner FFmpeg presence (run `41707986570`); subsequent revision aligned with actual repository install procedure and conditionally provisioned FFmpeg and CJK fonts. Both initial failures were environment bootstrap, not product UI test failures. Avoid treating first red CI as UI regression without stage attribution.

**Acceptance boundary:** Product UI remains unmerged and opt-in. The first slice uses temporary glyphs, not downloaded V3 exact SVG assets. No reviewed actual-browser-vs-Figma overlay, pointer/keyboard audit, real target transaction, final MKV, motion specification, or physical tablet acceptance. No Canonical change. Related knowledge is already recorded in `inbox/candidates/2026-10-15-version-vector-and-atomic-ui-cutover-gate.md` and `inbox/candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md`; do not create duplicate normative candidates.


## 2026-11-04 WU-02 evidence — source tabs, exact target gate and actual cross-MKV SubRip

**Real product implementation and evidence:** The V3 [draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239) now exposes multiple MKV source tabs, exact `File`-bound source observation, an explicit target picker with cancellation, and a guarded real single-task writer. A source tab may switch the *observation* source to A without authorizing any output. Confirming B requires exact resource key + same `File` object + current source adapter. Main validates this via `src/softmux-v3-intent.js` and `src/main.js`; the UI is only a presenter. Source File removal/replacement/rebind revokes the target gate. A's secondary SubRip track is inspected via the existing FFmpeg.wasm source-bound scan and native extraction path, not a parallel mock editor.

**Passed actual browser test** at SHA `3741534f83c6228f5bf60a89cff2fcc52766d1bf`: [Actions #41761600859](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41761600859) passed 880+ unit tests/build, original V3 source pilot, and new real Chromium flow using independently generated A-with-SubRip.mkv and B-base.mkv. The test explicitly observes A without target authority, cancels target selection, chooses B, extracts A SubRip through the production executor, generates real B output, verifies output codec/language/title with native `ffprobe`, and confirms both original A and B SHA-256 values are unchanged. Evidence artifact `ui-v3-pilot-source-first-evidence` id `13291130846` contains screenshots and JSON. These are bounded, not complete container preservation or font-render acceptance.

**New UI regression discovery and correction:** Rebuilding tabs on every asynchronous inventory repaint can detach the focused source-tab element and drop keyboard focus, despite the visual screen looking unchanged. The V3 UI was changed to reconcile source tabs by stable resource keys without removing existing matching nodes. The follow-up Chromium test asserts exact DOM focus persistence after a synthetic observed-source repaint. [Actions #41761904796](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41761904796) passed. This is a specific observation, not license to amend Canonical from one instance.

**Important boundary:** The approved V3 requirement that OutputPlan be *truly optional in the domain* is **not fully implemented**. The existing legacy domain still derives a candidate composition during source selection; V3 now requires explicit target authority before any single-task writer can execute, but the internal eager composition still exists. The ASS+font dependency closure is in independent unmerged draft PR #233; WU-02 evidence covers only SubRip. Exact Figma SVG assets, animations, final visual diff, all object actions, and actual tablet acceptance remain open. PR #239 stays Draft. Do not promote a product milestone to general Foundry Canonical.

**Deduplication:** This extends the existing Softmux Figma/semantic-ownership Case and is already compatible with `inbox/candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md`, the source-identity/target-relation observations and the general single-authority design gate. No new candidate file required.


## 2026-11-04 WU-03 — V3 source scan projection gates construction of output document

**Context:** Continuing owner-approved Softmux Figma V3 on draft PR #239; the previous WU-02 solved exact-File target authorization but still constructed an internal output composition on every observed source. That was not a truthful optional-output domain, even when the target tab was hidden by CSS.

**Implemented and tested design-specific refinement:** In the V3 branch, `src/main.js` `renderOutputComposition()` now publishes separately bound source attachment/Chapter/Tag observation, then returns **before** calling `buildContainerDocument()` if `currentV3Target()` is null. It clears the previously displayed composition rows, counts and selected object and disables composition mux actions; with an authorized target, it still uses the existing production composition and execution authority. `src/softmux-v3-surface.js` derives source rows directly from exact File-bound `trackState.streams` projected through the resource-registry event rather than reverse-engineering a hypothetical output DOM. The target heading uses the one real base File, live composition counts and mux-disabled readiness instead of another second editor.

**Evidence:** [Actions #41764035078](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41764035078) on product commit `7ba667b5be8a6b86d756992d33ab714b387b38a5` passed Node tests/build and real Chromium scenarios, including real A SubRip → B output and selecting the output subtitle in the single existing editor. Unit test now asserts short-circuit order and zero output-row DOM on source-only view. Browser evidence uploaded as `ui-v3-pilot-source-first-evidence` artifact id `13291638553`.

**Concrete QA issue:** Additional browser test for revocation after removing B initially timed out because it clicked the existing `#assetInventory` Remove button while the V3 source drawer was intentionally collapsed. The actual mux had finished; this failure was not media output failure. The test was adjusted to open the real source drawer via `#sf14SourceToggle` before triggering Remove and checking target-tab/composition/writer revocation. As of this entry that extra check remains **awaiting exact-head CI**, not a passed assertion.

**Interpretation boundary:** This removes eager `buildContainerDocument` from the *primary V3 composition render path* but does not remove every legacy auxiliary `buildMuxPlan()` calculation or every special-case container tool from the codebase. It is a step toward an optional OutputPlan, **not evidence that the entire old program now has one unified optional-output domain**. Exact icon assets, motion specifications, target panel pixel diff, full source read-only permission coverage, ASS/font closure and complete 1.0 release acceptance remain open. No Canonical promotion from this single product sequence.

**Dedup:** Existing Candidate `inbox/candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md` already specifies the principle. Keep this as a versioned empirical Case for that Candidate; do not duplicate it.
