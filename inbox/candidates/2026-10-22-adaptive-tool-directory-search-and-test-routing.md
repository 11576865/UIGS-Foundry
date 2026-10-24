# Candidate / Test Case: Search reachability and host-specific navigation in adaptive tool directories

Status: **Candidate / Pending exact-head Android Emulator CI**  
Date: 2026-10-22  
Origin: [ASS Workbench Android PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149) (stacked on Draft PR #148)  
Maturity: candidate; Authority: non-canonical; Epistemic state: supported for source and observed prior-test failure, unverified for post-fix runtime behavior.

## Evidence and diagnosis

At exact head `753e5f34de250580c210b00f4cf292385a571b7a`, [Android Emulator Regression #39020954103](https://github.com/11576865/ASS-Workbench-Android/actions/runs/39020954103) executed **171 tests / 6 failures / 0 skipped**. Three failing `EditorRegressionInstrumentedTest.openTool()` paths searched for legacy Compose test tags `tool-BATCH`, `tool-EVENT`, and `tool-EFFECTS`.

The application has two legitimate FIXED tool-directory presentations: compact `WorkspaceToolDirectory` publishes `tool-*` and `tool-search`, while expanded R3 `R3ToolCatalogDialog` publishes `r3-tool-*` and `r3-tool-search`. The old test helper assumed only the compact directory. **This mismatch explains the missing-selector assertions; it does not independently prove that a user could not open those editors.**

Source inspection of `R3ToolCatalogDialog.kt` also found that text search filtered each group's tools but retained *all eight group shells*, including groups with zero matches. The catalog then used `visibleGroups.chunked(4)`; a single match in the seventh group (e.g. BATCH) remained in the second LazyColumn row behind a first row of empty columns. This is a source-grounded search-discoverability/layout risk; its actual impact across hardware and keyboards remains unverified.

## Bounded implementation (product-owned)

- [`fd73fa2c`](https://github.com/11576865/ASS-Workbench-Android/commit/fd73fa2c2f663c70a55de4deeaacb28839db909f): filter out empty catalog groups *before* four-column chunking; render explicit tagged empty state when no tools match.
- [`048005e7`](https://github.com/11576865/ASS-Workbench-Android/commit/048005e73d3384d842dcd774910ef0b1a18cbac7): test helper routes by **actually composed** directory host (R3 vs compact); SPATIAL retains its existing navigation.
- [`e4a779bf`](https://github.com/11576865/ASS-Workbench-Android/commit/e4a779bf026162476a64d51468702455a2d0604f): connected Compose regression covers filtered BATCH hit, disappearance of nonmatching tool, and explicit no-results UI.
- Task-state checkpoint: [`.uigs/tasks/ass-fixed-v11-android-implementation-20261016.json`](https://github.com/11576865/ASS-Workbench-Android/blob/feat/fixed-v11-event-grid-20261016/.uigs/tasks/ass-fixed-v11-android-implementation-20261016.json).

## Reusable candidate

When one task has multiple adaptive presentations of a searchable command catalog:

1. Filter empty *sections* before pagination, grid chunking or virtualization; matching items should not be obscured by placeholders representing groups with zero results.
2. Show an explicit no-match state rather than an unexplained empty surface.
3. Regression helpers must navigate through the **actual rendered host/consumer**, not assume one obsolete test tag applies to every responsive variant.
4. Keep the behavioral assertion intact: a visible control must dispatch the real production command; passing a tag lookup alone cannot count as completed end-to-end authoring.
5. Classify test-driver selector failures separately from proven product route failures; reproduce with actual semantics and independently verify device interactions.

## Limits, follow-up and anti-promotion

All observations share one ASS/R3 implementation lineage and do not count as independent cross-project confirmation. The new commit has **no confirmed exact-head emulator result yet**, and the same prior run also failed inspector IME, SPATIAL unpin and shear field lifecycle tests. Those remain separate. Do not use this record to declare FIXED V1.1 complete or update UIGS Canonical rules. Next step is the exact-head branch emulator suite and tablet/device evidence.


## 2026-10-23 addition — SPATIAL search result and IME lifetime

Exact head `bb0e2ce3602d38fbcc8ef7de328c6cad9b0cb436` [Emulator Regression #39877625021](https://github.com/11576865/ASS-Workbench-Android/actions/runs/39877625021) completed **172 tests / 5 failures / 0 skipped**, with valid R3 full-size compositor PNG. This is the first discriminating full-suite receipt after the prior foreground/no-XML run. `EditorRegressionInstrumentedTest.invalidEventFieldsExplainErrorsAndCannotCommitAcrossHosts` failed in the **SPATIAL** branch of `openTool`: lookup of `tool-EVENT` failed after searching and calling `hideKeyboard()`.

Production's shared `WorkspaceToolDirectory` does render a filtered LazyColumn entry tagged `tool-EVENT`; the test helper's unguarded `hideKeyboard()` call between search and click may cause an IME/back/dismissal lifecycle transition. **That dismissal is an unproven explanation, not an established product bug.**

The bounded [test helper repair `5be6bc45`](https://github.com/11576865/ASS-Workbench-Android/commit/5be6bc45f486e604d5d578e6f9f9466e5c4ff269) selects the visible real tool result while search IME is still active and preserves the downstream ASS edit assertions. The next exact-head connected emulator run is **Pending**. Other independent failures (IME after rotation, SPATIAL resident rail, batch focus and Transform field disposal) remain unclosed. No production UI changes or Canonical promotion.

**Refined candidate:** searchable modal command results should remain actionable with the IME open; test harnesses should navigate through the current presented route, avoiding incidental keyboard-hide operations that can change transient dialog ownership before the command is invoked. Treat this as one product/test lineage rather than independent confirmations of a new rule.

## 2026-10-25 continuation — Pin the complete catalog outside a scrolling short rail

Source evidence: [ASS PR #149](https://github.com/11576865/ASS-Workbench-Android/pull/149) at pre-change head `8d1d77102ef04bd2409617c99ae6c7f1977907dd`. [FIXED source/JVM #40115404478](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40115404478) **passed**. [Android Emulator #40115404368](https://github.com/11576865/ASS-Workbench-Android/actions/runs/40115404368) **failed** with 63 tests / 4 failures / 0 errors / 0 skipped in the recorded main connected attempt. Two compositor PNG capture jobs succeeded independently. One failure in `inspectorDraftSurvivesToolSwitchAndRotation` was the real `fixed-tool-CAPABILITIES` control **not displayed** when the test attempted to navigate via the catalog after keyboard/text entry. Source does not yet establish whether this exact failure arose in the compact top task bar or the tablet rail, so do not assert the old rail placement was its proven cause.

Independent source finding: `FixedV11TaskRail` originally put **all eight** 64dp tool buttons inside one scrolling Column with 16dp inter-item gaps, with the complete-catalog command at the end. On reduced available height, the complete catalog can scroll out of view. This is a product affordance risk even when a test can programmatically scroll to it. The user should not have to search through the shortcut rail to access the full directory.

Proposed product correction [8274fa3d](https://github.com/11576865/ASS-Workbench-Android/commit/8274fa3d0f55699b19b8e6a88a7765b7123bd734): regular shortcut tools remain in a dedicated scrollable column; the complete catalog command stays pinned at the bottom of the same real rail, with the original selection semantics and ViewModel callbacks. Android test [29bda707](https://github.com/11576865/ASS-Workbench-Android/commit/29bda707555f7b5576928b1add140f0999bc1b73), import correction [6f7bb4f7](https://github.com/11576865/ASS-Workbench-Android/commit/6f7bb4f7fe73838f11f4a5a4f7d66554bf21dc46), constrain it to 56×340dp and demand the catalog is visible/clickable and that the ordinary subtitle task still dispatches its production callback.

Test-routing correction [ce46b8a2](https://github.com/11576865/ASS-Workbench-Android/commit/ce46b8a23dc7d898c184feb0617377dce0028647): in the shared regression helper, TEXT/EFFECTS draft-switch scenarios now use their existing direct task commands rather than arbitrarily opening the full directory, while tests for directory discovery still exercise real searchable catalog entries. A non-direct tool still uses the actual rendered catalog with visibility assertions. These changes do not prove the historic screenshot/full-suite pass and do not suppress any failure.

Reusable candidate extension: **high-priority escape/discovery commands should not share the scroll fate of lower-priority shortcuts in a constrained navigation rail**; assertions for switching within an existing task should exercise the direct workflow, while directory-specific tests separately cover global discovery and selection. Source-backed candidate only; exact-head Android/runtime device validation pending; do not promote Canonical.
