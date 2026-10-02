# Observation: Replaying a real-time game scene is not a pixel-identical benchmark

Date: 2026-10-02
Status: Observation
Scope: game capture / video quality benchmarking / rendering determinism / display validation

## Observation

A scripted real-time game scene can be semantically identical across runs while still producing different rendered frame sequences.

Potential sources of run-to-run variation include:
- temporal anti-aliasing / temporal upscaling history;
- stochastic sampling in ray tracing or path tracing;
- particle systems and procedural effects;
- physics and animation timing;
- asynchronous asset streaming;
- dynamic resolution or quality adaptation;
- frame pacing and sampling at different presentation times;
- non-fixed random seeds or nondeterministic GPU scheduling.

Even if every visible event appears the same to a viewer, the exact pixels of corresponding frames may differ.

Display presentation introduces another layer of variability:
- variable refresh rate;
- refresh cadence and scanout timing;
- LCD overdrive / OLED response characteristics;
- HDR tone mapping, local dimming and panel processing;
- temporal dithering, motion persistence and black-frame insertion.

These display effects usually do not enter a normal desktop/game capture because capture occurs before panel presentation, but they matter when evaluating what a viewer physically sees.

## Reusable testing implication

Do not use repeated launches of the same real-time game cutscene as the reference source for precise encoder A/B comparison unless the game provides a deterministic replay/capture path and determinism has been verified.

Preferred benchmark pattern:
1. capture the scene once at the highest-quality practical source setting;
2. freeze that captured source as the canonical input;
3. encode all candidate settings from exactly the same source file;
4. compare encoded outputs against the same reference frames.

If display quality itself is under test, use a camera/photometric measurement path and treat display validation separately from encoded-file validation.

Do not promote to Canonical from this single observation.
