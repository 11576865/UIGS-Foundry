# Candidate: Programmatic spatial recall should interpolate camera state

Status: candidate
Date: 2026-10-04
Domains: interface-grammar, spatial-workspace, motion, navigation
Evidence type: code review plus direct visual comparison

## Trigger

A direct comparison between a user-provided Android recording with continuous destination motion and the current ASS Workbench spatial implementation exposed a specific gap.

Current ASS Workbench spatial code has two different navigation classes:

1. Direct manipulation: pointer-driven pan/zoom updates the workspace camera continuously from gesture deltas.
2. Programmatic navigation: Focus / Recall / Overview / zoom buttons assign a new camera state immediately.

On current main, the legacy SpatialWorkspace directly assigns scale / offset values in focus and overview actions.

On open PR #107 (Infinite Canvas replay), InfiniteCanvasCamera provides pan() and zoomAt(), and InfiniteCanvasHost supports unbounded world-space movement, recall and focus. However, focus(), overview(), recall and zoom buttons still replace the camera state synchronously. No camera interpolation primitive (Animatable / tween / spring / equivalent) is used in the infinite-canvas host.

## Candidate rule

Spatial workspace navigation should distinguish direct manipulation from programmatic travel:

- Direct manipulation should remain 1:1 with pointer input and must not be delayed by decorative easing.
- Programmatic Focus / Recall / Overview should normally interpolate camera position and scale so the user can perceive spatial origin, destination and continuity.
- Long-distance travel may use a zoom-out / translate / zoom-in trajectory or a bounded abstract transition rather than a long high-speed pan.
- Persistent screen-space chrome should remain stable during camera travel.
- Camera motion remains presentation state and must not enter document Undo.

## Acceptance direction

A regression or visual-evidence case should verify:

- recall/focus does not hard-cut camera x/y/scale in one frame;
- destination becomes visible through bounded transition time;
- direct pinch/pan remains immediate;
- cancellation or new navigation input supersedes the old camera transition safely;
- document state and Undo history remain unchanged.

## Evidence boundary

This is a Candidate derived from current implementation review and a two-app visual comparison. It does not establish one mandatory easing curve, duration, or motion style for every spatial workspace.

No Canonical promotion.
