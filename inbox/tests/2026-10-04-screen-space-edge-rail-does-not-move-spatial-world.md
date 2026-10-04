# Test: Screen-space edge rail must not move the spatial world

Status: test
Date: 2026-10-04
Domains: spatial-workspace, edge-navigation, regression, motion
Related candidate: inbox/candidates/2026-10-04-hidden-edge-rail-screen-space-spatial-workspace.md
Implementation evidence: ASS-Workbench-Android PR #110

## Purpose

Verify that a hidden edge summon rail is implemented as screen-space chrome rather than by resizing, translating, or re-laying out the infinite world.

## Setup

Use a spatial/infinite workspace with at least one visible world node and a collapsed edge handle.

Capture the visible node bounds in root coordinates before opening the rail.

## Procedure

1. Open the hidden edge rail using the explicit handle.
2. Wait until the rail is fully present in the semantics tree.
3. Capture the same world node bounds again.
4. Compare pre-open and post-open bounds.
5. Dismiss the transient rail using the outside-dismiss surface.
6. Re-open the rail, pin it resident, activate an existing node entry, and verify the rail remains present.
7. Close the resident rail explicitly.

## Expected result

- Opening the rail does not change the sampled world node bounds.
- Transient outside dismissal removes the rail.
- Resident/pinned state survives entry activation until explicit close.
- The same workspace node identity remains present.
- The interaction does not require document mutation or document Undo.

## Current product mapping

ASS-Workbench-Android PR #110 adds this coverage to EditorRegressionInstrumentedTest.spacialWorkspaceExposesRealNodesAndNavigationControls (function name in product remains spatialWorkspaceExposesRealNodesAndNavigationControls).

The test records spatial-node-preview bounds before and after spatial-edge-handle-left opens spatial-edge-rail-left and requires exact equality.

## Evidence boundary

This Test specifies a reusable regression condition. Passing it alone does not prove visual quality, touch ergonomics, system-back gesture compatibility, or animation smoothness on device.

No Canonical promotion.
