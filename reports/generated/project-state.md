# Cross-project State

Source max updated at: 2026-10-02T17:48:51Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `9ea7947ace` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 2 | 2 | 20 |
| Character-Voice-Service | `41fb27d0bd` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `3041c75f1e` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `a63dec9972` | Browser E2E mux tests: success (HEAD)<br>Deploy to GitHub Pages: success (HEAD) | 0 | 0 | 9 |
| Quick-Automatic-Hardsub-Encoder | `880dfe393b` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: in_progress (HEAD)<br>Compile Android media tasks: success (HEAD)<br>Test frontend: success (HEAD)<br>Windows local smoke: success (HEAD) | 21 | 22 | 16 |
| UIGS-Foundry | `ab3304d85a` | Validate Foundry: in_progress (older SHA)<br>Collect UIGS Outboxes: unknown<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (older SHA)<br>Capture UI Reference Baselines: unknown<br>Refresh UI Search Index: unknown<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 13 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
