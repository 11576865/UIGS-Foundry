# Candidate: Frame-jog controls should emit authoritative frame steps, not fixed-time approximations

Date: 2026-10-03
Status: Candidate
Scope: subtitle timing / media transport / VFR-safe interaction

## Problem

Precision subtitle timing often needs three transport scales at once:

- single-frame step/back for exact boundary inspection;
- continuous traversal while a frame button is held;
- a small local slider for several-frame micro-adjustment.

A tempting implementation converts these gestures to estimated milliseconds from nominal FPS. That breaks the semantic contract on VFR media and can drift away from actual displayed frame boundaries.

## Candidate rule

When the playback backend exposes authoritative frame-step operations, all frame-jog interactions should compile to those operations.

- Tap: emit one forward/backward frame command.
- Hold: repeat that same frame command with a bounded cadence.
- Fine slider: quantize the local slider to integer frame deltas and emit only the delta from the last slider position.
- Slider release: recenter the control without issuing a compensating seek.

The UI may show estimated FPS and frame number as diagnostics, but they should not become the authority for frame boundary navigation.

## Why

This keeps CFR and VFR behavior aligned with the actual decoder/presenter and prevents a precision UI from silently becoming a fixed-millisecond seek UI.

## Limits

- Backend frame-step correctness remains an implementation dependency.
- Repeat cadence is an interaction/performance parameter, not a definition of media FPS.
- Exact subtitle serialization may still have coarser time precision than the playback frame boundary.

Do not promote to Canonical from this single implementation.
