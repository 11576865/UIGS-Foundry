# Candidate: Spatial workspace acceptance must not collapse into a fixed dashboard

Date: 2026-10-04
Status: Candidate
Scope: tablet-first spatial professional interfaces

## Observation

When validating a spatial/infinite workspace with a realistic editing workflow, there is a recurring design failure: the acceptance task is translated into a conventional fixed split-pane layout. This preserves simultaneous visibility but defeats the architectural hypothesis being tested.

The workspace should not be accepted merely because a static arrangement can complete the task, nor rejected because every useful element is not permanently visible.

## Candidate rule

Evaluate the spatial workspace by **working-set continuity**, not by one prescribed layout.

- No specific tool, preview shape, pane ratio, or fixed region is mandatory unless required by the domain task itself.
- Users should be able to place, resize, group, overlap, focus, temporarily summon, or dismiss tools while preserving task context.
- Simultaneous context means the information needed for the current decision remains visible, glanceable, or recoverable with negligible friction; it does not imply a permanent split-pane dashboard.
- High-frequency operations should remain available within the current spatial working set without forcing page navigation or camera travel, but the working set itself may be user-arranged and fluid.
- Prototypes should use neutral fixtures or multiple alternative arrangements to test the workspace substrate rather than accidentally standardizing one application layout.

## Evidence boundary

Derived from design correction during a subtitle-authoring acceptance discussion. Exact working-set policies, auto-layout behavior, tool summon semantics, and visibility thresholds remain product-specific.

Do not promote to Canonical from this observation alone.
