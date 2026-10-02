# Cross-project State

Source max updated at: 2026-10-02T09:05:28Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `818a26d202` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: in_progress (HEAD) | 1 | 1 | 17 |
| Character-Voice-Service | `747e7998cb` | CVS tests: success (HEAD) | 0 | 0 | 4 |
| HSR-Voice-Archive-Builder | `62df3afe48` | tests: success (HEAD) | 0 | 0 | 15 |
| MKV-Fast-Muxer | `f2a29c0b3e` | Browser E2E mux tests: success (older SHA)<br>Deploy to GitHub Pages: success (HEAD) | 0 | 0 | 9 |
| Quick-Automatic-Hardsub-Encoder | `d62dd49637` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (older SHA)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (older SHA)<br>Windows local smoke: success (HEAD) | 19 | 20 | 15 |
| UIGS-Foundry | `cb190ac838` | Validate Foundry: success (older SHA)<br>Collect UIGS Outboxes: success (older SHA)<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (older SHA)<br>Capture UI Reference Baselines: success (older SHA)<br>Refresh UI Search Index: success (older SHA)<br>Propose UIGS Promotions: success (older SHA)<br>Review UIGS Promotion: unknown | 0 | 0 | 12 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
