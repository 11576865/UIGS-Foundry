# Candidate: Core workspace substrate should not be modeled as a peer UI mode

Status: **Candidate / design-review observation**
Date: 2026-10-04

## Observation

A spatial/infinite workspace may begin life as one selectable UI realization among several alternatives. Once it becomes the presentation substrate that hosts tools, fixed workbenches, overlays, bookmarks, lenses, and other interaction patterns, keeping it as a peer item in the same UI selector creates a conceptual inversion: the system asks the user to choose the container from inside the container-selection layer.

This is especially visible in tablet-first professional applications where the spatial workspace is intended to be the normal operating environment rather than an optional experimental view.

## Reusable rule

If a workspace model becomes the primary presentation substrate:

- Treat it as the **default workspace shell**, not as a peer tool or ordinary UI preset.
- Keep alternative fixed layouts, workbenches, or specialized views as **workspace layouts / projections / presets / regions hosted by that shell** when feasible.
- A selector may still exist for switching workspace shells at an architectural or settings level, but it should not present the substrate as if it were equivalent to a transient panel arrangement.
- Prototype the substrate with neutral test fixtures rather than domain-specific tools unless those tools are necessary to test a particular interaction invariant.
- For tablet-first products, validate the spatial shell first against tablet viewport, posture, multi-touch reach, and landscape/portrait adaptation; phone behavior should be treated as an adaptation, not as the design baseline.

## Why this generalizes

This applies to professional editors, CAD/EDA environments, node workspaces, whiteboards, spatial IDEs, and other systems where an initially optional canvas evolves into the persistent host for multiple interface realizations.

## Evidence boundary

This is an architectural inference from current prototype/design discussion. It does not prove that every product should default to a spatial workspace, nor does it prescribe a specific tablet size, orientation policy, or migration path.

Do not promote to Canonical from this observation alone.
