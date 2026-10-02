# Candidate: Touch-centered temporal zoom invariant

Status: **Candidate / implementation + unit-test evidence**
Date: 2026-10-02

## Observation

While implementing pinch zoom for a subtitle timeline, simply changing the visible duration around the viewport center caused the temporal point under the user's fingers to drift. On touch screens this makes pinch zoom feel detached from the object being inspected.

## Reusable rule

For a temporal viewport, pinch zoom should preserve the time coordinate under the gesture centroid whenever possible.

Given:
- old viewport duration `D0`;
- new viewport duration `D1`;
- current center `C0`;
- touch centroid fraction `f` in [0, 1];

derive the touched time from the old viewport, then choose the new center so the same time remains at fraction `f` after zoom.

Conceptually:

`anchorTime = oldStart + D0 * f`

`newCenter = anchorTime + D1 * (0.5 - f)`

Then clamp against the domain boundary (for subtitle timelines, time >= 0).

## Why this generalizes

This applies to audio editors, video timelines, subtitle editors, annotation timelines, traces, charts, and any touch UI where the user pinches around a specific temporal feature. It is the temporal equivalent of cursor-centered zoom in spatial canvases.

## Validation notes

ASS-Workbench-Android now has a pure policy test verifying:
- a non-centered pinch preserves the touched time;
- zoom near timeline origin does not expose negative time.

The gesture layer also separates this projection invariant from gesture policy: the UI decides the new duration and pan delta; the domain policy calculates the stable center.

## Evidence boundary

This does not prescribe:
- zoom sensitivity;
- discrete vs continuous zoom;
- minimum/maximum duration;
- semantic layer thresholds.

Those remain product-specific and require device testing.

Do not promote to Canonical from this implementation alone.
