# Cross-project State

Source max updated at: 2026-10-03T09:24:35Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `73c09f4052` | Android CI: success (HEAD)<br>Android Emulator Regression: cancelled (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 30 | 30 | 20 |
| Character-Voice-Service | `41fb27d0bd` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `3041c75f1e` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `671bb6684c` | Browser E2E mux tests: success (HEAD)<br>Deploy to GitHub Pages: success (HEAD) | 12 | 12 | 9 |
| Quick-Automatic-Hardsub-Encoder | `09b67ee4ed` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (HEAD)<br>Compile Android media tasks: success (HEAD)<br>Test frontend: success (HEAD)<br>Windows local smoke: success (HEAD) | 50 | 51 | 16 |
| UIGS-Foundry | `56e1a31d4b` | Validate Foundry: success (older SHA)<br>Collect UIGS Outboxes: success (older SHA)<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (HEAD)<br>Capture UI Reference Baselines: unknown<br>Refresh UI Search Index: unknown<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 13 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
