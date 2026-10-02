# Cross-project State

Source max updated at: 2026-10-02T10:14:07Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `fe8c618440` | Android CI: in_progress (HEAD)<br>Android Emulator Regression: in_progress (HEAD)<br>Fontconfig renderer native probe: in_progress (HEAD) | 1 | 1 | 18 |
| Character-Voice-Service | `41fb27d0bd` | CVS tests: success (HEAD) | 0 | 0 | 5 |
| HSR-Voice-Archive-Builder | `62df3afe48` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `f78f00c57f` | Browser E2E mux tests: success (older SHA)<br>Deploy to GitHub Pages: success (HEAD) | 0 | 0 | 9 |
| Quick-Automatic-Hardsub-Encoder | `5cf3acd713` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (older SHA)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (older SHA)<br>Windows local smoke: success (older SHA) | 19 | 20 | 16 |
| UIGS-Foundry | `01cec24966` | Validate Foundry: success (HEAD)<br>Collect UIGS Outboxes: success (older SHA)<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (HEAD)<br>Capture UI Reference Baselines: success (older SHA)<br>Refresh UI Search Index: success (older SHA)<br>Propose UIGS Promotions: success (HEAD)<br>Review UIGS Promotion: unknown | 0 | 0 | 13 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
