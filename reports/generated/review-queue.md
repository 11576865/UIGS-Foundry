# UIGS Review Queue

Generated: 2026-10-10T04:07:15+00:00

## Summary

- Durable Pending packets: 293
- Triage records: 293
- Needs-review packets: 238
- Needs-review families after grouping: 9
- Open promotion proposals: 3
- Reviewed packets: 1

Raw Pending count is durable storage. This report narrows review work to unresolved triage families and explicit open promotion proposals.

## Needs-review CI families

| Count | Repository | Workflow | Category | Matched rules | Related knowledge |
| ---: | --- | --- | --- | --- | --- |
| 82 | 11576865/Quick-Automatic-Hardsub-Encoder | Test frontend | unknown | — | — |
| 63 | 11576865/ASS-Workbench-Android | Android Emulator Regression | unknown | — | — |
| 58 | 11576865/Quick-Automatic-Hardsub-Encoder | Windows local smoke | runtime-smoke | runtime-smoke | ARCH.STRUCTURED_NATIVE_BRIDGE, REL.CAPABILITY_PROVEN_BY_OUTPUT |
| 13 | 11576865/ASS-Workbench-Android | Android CI | unknown | — | — |
| 12 | 11576865/ASS-Workbench-Android | Fontconfig renderer native probe | runtime-smoke | runtime-smoke | REL.CAPABILITY_PROVEN_BY_OUTPUT, TEST.RENDERED_EFFECT_DIFFERENTIAL |
| 4 | 11576865/ASS-Workbench-Android | Fontconfig renderer native probe | release-publication | release | BUG.ASS.RELEASE_PATH_ASYMMETRY, REL.RELEASE_PATH_PARITY |
| 2 | 11576865/MKV-Fast-Muxer | Deploy to GitHub Pages | release-publication | release | — |
| 2 | 11576865/Quick-Automatic-Hardsub-Encoder | Compile Android media tasks | unknown | — | — |
| 2 | 11576865/Quick-Automatic-Hardsub-Encoder | UIGS Evidence Coverage | unknown | — | — |

## Open promotion proposals

- `chat.ass-workbench.visual-capture-dependency-state-mismatch.20261002T122000Z` — bug — Visual capture contract can declare an impossible state when its fixture disables a required runtime dependency
- `chat.quick-hardsub.semantic-state-overridden-by-responsive-css.20261002T102700Z` — candidate — Responsive presentation CSS must not resurrect semantically suppressed surfaces
- `chat.quick-hardsub.windows-native-picker-offscreen-owner.20261002T102700Z` — bug — Hidden Windows bridge can anchor native OpenFileDialog off-screen

## Review boundary

- Grouping is operational deduplication only; it does not assert identical root cause.
- A family count is not a Bug count and does not create reusable knowledge automatically.
- Promotion still requires explicit accept/reject review.
- Canonical promotion remains governed separately by `governance/PROMOTION.md`.
