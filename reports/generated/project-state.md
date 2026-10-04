# Cross-project State

Source max updated at: 2026-10-04T07:43:38Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `5e1be4dc9f` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 67 | 67 | 20 |
| Character-Voice-Service | `41fb27d0bd` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `3041c75f1e` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `671bb6684c` | Browser E2E mux tests: success (HEAD)<br>Deploy to GitHub Pages: success (HEAD) | 16 | 16 | 9 |
| Quick-Automatic-Hardsub-Encoder | `a9be63cb00` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (HEAD)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (older SHA)<br>Windows local smoke: success (HEAD) | 137 | 138 | 16 |
| UIGS-Foundry | `5b6f731ed1` | Validate Foundry: success (older SHA)<br>Collect UIGS Outboxes: in_progress (older SHA)<br>Triage UIGS Pending: unknown<br>Generate UIGS Project State: in_progress (older SHA)<br>Capture UI Reference Baselines: unknown<br>Refresh UI Search Index: unknown<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 14 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
