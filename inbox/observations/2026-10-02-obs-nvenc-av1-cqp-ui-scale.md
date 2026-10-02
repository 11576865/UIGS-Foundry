# Observation: OBS NVENC AV1 CQP UI value is scaled to codec QP

Date: 2026-10-02
Status: Observation
Scope: OBS Studio / NVENC AV1 / rate-control diagnostics

## Observation

Current OBS NVENC code exposes AV1 CQP in a compact UI range of 1-63, but internally multiplies the selected value by 4 before assigning NVENC constant QP for I/P/B frames. H.264/HEVC CQP values are passed without that AV1-specific multiplication.

Therefore an OBS NVENC AV1 setting shown as CQP 1 corresponds to an NVENC AV1 constant QP value of 4, not literal codec QP 1.

## Reusable implication

When comparing OBS AV1 CQP values with FFmpeg/NVENC documentation, encoder logs, other codecs, or external tools, do not assume identical numeric scales. Always verify how the application maps its UI control to the codec's native quantizer domain.

This matters especially in "extreme quality" tuning, where apparent one-step numeric differences can be misinterpreted as equivalent across codecs.

Do not promote to Canonical from this single implementation observation without checking future OBS versions.
