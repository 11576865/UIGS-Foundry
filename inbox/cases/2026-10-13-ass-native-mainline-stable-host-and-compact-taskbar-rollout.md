# Case: Native ASS UI rollout on main — stable host + minimal compact toolbar

Date: 2026-10-13
Status: Case / code committed to production repository main / PENDING Android CI, emulator and screenshot acceptance
Repository: 11576865/ASS-Workbench-Android
Authoritative task: .uigs/tasks/ass-native-ui-minimal-rollout-20261013.json

## User direction
After iterations of disconnected offline HTML prototypes, user said to proceed with actual Android implementation and specifically authorized **direct changes to main**. Preserve tablet priority and sparse explanatory copy, but do not hide critical operations, units, writing scope or professionally useful controls.

## Grounded code change
- Native `UiVariantRegistry.default` changed SPATIAL_EXPERIMENTAL -> FIXED. A missing/null persisted layout resolves to FIXED, while explicit SPATIAL_EXPERIMENTAL and archived legacy UI tokens retain their historical migration to the unified spatial experiment. Stable Event and ToolInstance state are not rewritten.
- `UiVariantRegistryTest` amended: tests check main UI default, null mode and legacy aliases.
- Native `UiVariantLabDialog` replaces permanently visible explanatory paragraph, oversized cards, disabled status chip and repeated selection wording with two compact rows, experimental status indicator and a real Material3 `TooltipBox` explaining each variant on long press/hover. Existing selection testTags retained.
- In native `ModernEditorScreen`, the global direct workspace switch now uses existing `TooltipIconButton` and labels the destination as experimental. Existing semantics/testTag retained. Workspace selection remains global, not a 19th professional tool.
- In native `WorkbenchTaskBar`, <600dp compact windows use icon-first task entries with Material3 tooltips and explicit contentDescription/testTags; wide tablets retain short, discoverable task labels. The existing complete 18-item tool directory is not replaced.
- Product docs updated with historical state distinction; durable task checkpoint committed at main SHA `2a41e9ce7ec10886c59b985735faf2e39c592057`.

## Evidence
Specific pushed native code commits: a3af731, 954a002, 1c86237, b21a818, e55353e, ae09d87, 8a7e960, 3f81b36, plus task checkpoint 2a41e9c. These are **real GitHub writes** on main, not an HTML prototype or artifact rendering.
Android Gradle compilation, Compose runtime and emulator visual capture have NOT been run or confirmed in this conversation. GitHub connector workflow query for code commit 3f81b36 returned zero PR-triggered runs; by connector contract it does not report push-to-main actions, so native CI status remains **Pending External Validation**, not passed or failed.

## Reusable execution insight
For a complex editor with two presentation Hosts, 'stable UI is default' and 'legacy workspace token decode' are **distinct policies**. A safe rollout changes only new/unset workspace selection and product chrome; do not inadvertently remap already saved experiment surfaces, or silently overwrite draft documents. UI explanation can move to tooltips only if explicit primary actions and testable a11y names remain discoverable.
Direct-main authorization affects branch targeting but does not waive native compilation, test evidence, or rollback discipline. Track multi-unit implementation in durable repository task records.

## Dedupe / limitations
Foundry searches for 'ASS FIXED default native main branch compact tooltip implementation', 'experimental host migration null default legacy tokens' and 'icon only compact task bar longpress Android Compose' found no equivalent native mainline implementation Case. Earlier related observations concerned prototypes, not committed native code.
No Canonical promotion. Remaining effects, Karaoke and true renderer-bound source edits are not implemented by these commits.