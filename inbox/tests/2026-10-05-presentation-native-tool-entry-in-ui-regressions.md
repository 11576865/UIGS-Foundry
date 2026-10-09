# Presentation-native tool entry in UI regressions

## Status
Test

## Observation
ASS-Workbench-Android PR #118 exposed a regression-test harness error rather than a product failure: the new spatial-workspace extraction test switched to `SPATIAL_EXPERIMENTAL` and then reused the generic `openTool()` helper. That helper falls back to the `workspace-tools` control, which exists in the fixed/canvas presentation but is not part of the spatial presentation. The emulator run failed before exercising the feature with `Expected exactly '1' node ... TestTag = 'workspace-tools'`.

## Reusable rule
When a test changes presentation/workspace mode, navigation into a tool must use an affordance that is actually owned by that presentation. Do not assume a cross-presentation helper remains valid merely because the underlying command is semantically the same.

## Test pattern
1. Switch to the target presentation.
2. Assert the presentation root exists.
3. Enter the tool through that presentation's own visible navigation contract.
4. Wait for the resulting presentation-specific surface/node.
5. Only then exercise the feature under test.

For the spatial workspace, the corrected path is: `＋ 工具` -> wait for `spatial-node-CAPABILITIES-primary` -> use the capabilities directory -> select `tool-POSITION` -> wait for `spatial-node-POSITION-primary`.

## Evidence boundary
This records a test-harness/navigation contract. It does not imply all presentations must expose identical controls, nor that `workspace-tools` should be added to the spatial workspace. No Canonical rule is promoted from this single incident.
## 2026-10-09 follow-up: presentation redesign, stable action identity, and lifecycle handoff

ASS-Workbench-Android PR #138 replaced the prior scaled live-window canvas with a semantic board and a native-density focused-editor stage. Its first Emulator Regression run `37903981669` executed 107 tests, with 7 failures. Four extraction regressions stopped at the previously textual locator `＋ 工具`, removed from the newly designed toolbar before the test reached parameter extraction. They demonstrated a **presentation-native navigation contract mismatch**, not four verified parameter-model defects.

This repairs rather than weakens the harness:

- the actual tool-directory trigger receives stable action identity `spatial-add-tool` (and visible copy remains `＋ 工具`);
- entering the directory must compose `spatial-native-content-CAPABILITIES-primary`, rather than a low-zoom card;
- selecting a newly created or already-existing ToolInstance must hand the native focused editor to that instance through `WorkspaceState.activeInstanceId`, without creating a second authoritative active-tool state;
- extraction regressions verify the real projection in its native focused editor and then check that its workspace node still exists.

Other failures from the same run concern rail residency and birdseye persisted scene recall and are documented in the PR's workspace-v2 evidence report; they are not classified as parameter-extraction model failures.

**Evidence:** first-round emulator failures confirmed; follow-up fixes committed to PR #138; post-repair Emulator CI **Pending**. This supplements this Test record and the existing Stable Action Identity Candidate. No automatic Canonical promotion.
