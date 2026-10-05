# Cross-project State

Source max updated at: 2026-10-05T10:48:58Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `554100fdb4` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 88 | 88 | 20 |
| Character-Voice-Service | `d818bee338` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `5dde8e3d8a` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `9eb28679fd` | Browser E2E mux tests: success (older SHA)<br>Deploy to GitHub Pages: success (HEAD) | 16 | 16 | 9 |
| Quick-Automatic-Hardsub-Encoder | `8a3ba82e45` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (HEAD)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (HEAD)<br>Windows local smoke: success (older SHA) | 148 | 149 | 16 |
| UIGS-Foundry | `47041f2c99` | Validate Foundry: success (older SHA)<br>Collect UIGS Outboxes: success (older SHA)<br>Triage UIGS Pending: unknown<br>Generate UIGS Project State: in_progress (HEAD)<br>Capture UI Reference Baselines: unknown<br>Refresh UI Search Index: unknown<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 15 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
