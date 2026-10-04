# Cross-project State

Source max updated at: 2026-10-04T17:25:17Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `1f88268c6d` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 78 | 78 | 20 |
| Character-Voice-Service | `41fb27d0bd` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `3041c75f1e` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `9eb28679fd` | Browser E2E mux tests: success (older SHA)<br>Deploy to GitHub Pages: in_progress (HEAD) | 16 | 16 | 9 |
| Quick-Automatic-Hardsub-Encoder | `2e45453cc8` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (older SHA)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (older SHA)<br>Windows local smoke: success (older SHA) | 139 | 140 | 16 |
| UIGS-Foundry | `57f240aebc` | Validate Foundry: success (older SHA)<br>Collect UIGS Outboxes: failure (older SHA)<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (older SHA)<br>Capture UI Reference Baselines: unknown<br>Refresh UI Search Index: unknown<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 15 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
