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
