# Bug candidate — SPATIAL resident rail toggle exposes icon-only accessibility description

Date: 2026-10-14
Product: 11576865/ASS-Workbench-Android
Status: Bug / Pending exact-head Emulator verification; no Canonical change.
Source regression: Emulator run 38558602308, EditorRegressionInstrumentedTest#spatialWorkspaceExposesBoardAndNativeEditorWithoutMovingWorldNodes, assertion at line 516 after pinning left edge rail: `onNodeWithContentDescription("取消驻留").assertIsDisplayed()` fails.

Previous production code nested `Icon(Icons.Filled.PushPin, contentDescription = if (toolDrawerResident) "取消驻留" else "驻留")` inside an `IconToggleButton`, with no direct semantic description on the clickable parent. Compose child icon semantics may be merged/inaccessible, causing a failure to identify the *working toggle*, especially under size/rail overlay constraints.

Scoped product fix committed on R3 PR #148 head family `eb5caf5d7cc1b4d04f70093a47554a88f6b4955d`: move the dynamic contentDescription to `IconToggleButton` via `.semantics { ... }`, and set nested icon contentDescription to null; preserve click handler, tested tag, checked state, rail residency and independent SPATIAL UI. Do NOT infer the actual tap or pin operation failed from absent child semantics alone. Android CI/Emulator exact-commit proof still pending; if failure persists, investigate overlay bounds, collection focus and node merged tree before classifying root cause.

Reusable principle: on interactive toggles, put the accessible action/state description on the **interactive control** rather than depending on the decorative nested icon. This preserves UI-test discoverability and accessibility semantics without changing domain writes. Single case, so do not promote to UIGS Canonical.

Dedupe search across Foundry: resident rail contentDescription, IconToggleButton parent label, and toolDrawerResident toggle yielded no exact match. Recorded as Pending Bug rather than a verified fix.
