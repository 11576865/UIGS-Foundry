# Bug: Aspect-ratio lock must preserve the baseline ratio

Status: **Bug / reusable interaction failure**
Date: 2026-10-02
Project evidence: `11576865/ASS-Workbench-Android`, PR #73

## Failure

The touch Interaction Proxy implementation for X/Y scaling previously handled an enabled ratio lock by averaging the candidate absolute X and Y percentages and assigning the same value to both axes.

For a non-square baseline such as:

`ScaleX = 120%, ScaleY = 80%`

the locked manipulation could therefore collapse the object toward:

`ScaleX == ScaleY`

instead of preserving the baseline ratio `120:80 = 3:2`.

This disagreed with the existing direct scale-handle path, which already used a multiplicative factor and preserved the initial X:Y ratio.

## Reusable rule candidate

A constraint called **aspect-ratio lock / X:Y ratio lock** must preserve the ratio at interaction begin (or the explicitly selected baseline), not normalize two axis values to equality.

For a baseline `(x0, y0)` and scale factor `k`:

`x = x0 * k`
`y = y0 * k`

A single-axis touch control may use that axis as the driver while still applying the derived factor to the other axis when ratio lock is enabled.

`X == Y` is a separate “square/equal axes” operation and must not be silently substituted for ratio lock.

## Fix and regression evidence

PR #73:
- extracted `TouchScalePolicy`;
- XY, X-driven, and Y-driven locked paths preserve the existing ratio;
- added unit tests using a 120:80 non-square baseline;
- explicit X / Y / XY touch axis presentation remains separate from the ratio-lock constraint.

## Scope

Applicable to subtitle geometry, image/vector editors, crop/resize tools, CAD-like manipulators, layout tools, and any multi-axis numeric transform.

Do not promote to Canonical from this single project fix without broader validation.
