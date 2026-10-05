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