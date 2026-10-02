# Platform Realizations

This directory stores **how a UIGS Pattern is actually implemented**.

The evidence layers are separate:

- Pattern — reusable semantics and constraints.
- Generic realization recipe — framework/platform implementation guidance.
- Production Realization — concrete implementation in a real project at an immutable repository revision.
- Reference Demo — executable mechanism example maintained by Foundry.
- Visual Baseline — deterministic screenshot of a declared reference-demo state.
- Production Visual Evidence — screenshot/recording from a real product state.

Production Realization manifests live in `realizations/manifests/`. Each record names its project/platform, immutable commit, source file Git blob identities, validation files, effects, responsive behavior and known limitations.

`index.json` maps Pattern IDs to concrete implementations. `coverage.json` reports implementation coverage separately from visual-production evidence.

The verifier checks declared files at the immutable revision and also reports whether that revision still equals the source repository's current default-branch HEAD. Historical evidence is not deleted merely because HEAD moves.
