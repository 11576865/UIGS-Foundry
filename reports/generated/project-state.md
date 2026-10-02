# Cross-project State

Source max updated at: 2026-10-02T08:29:54Z

| Project | HEAD | Tracked workflow state | Pending | Triage | Foundry records with provenance |
| --- | --- | --- | ---: | ---: | ---: |
| ASS-Workbench-Android | `235f9c8d89` | Android CI: success (HEAD)<br>Android Emulator Regression: success (HEAD)<br>Fontconfig renderer native probe: success (HEAD) | 0 | 0 | 14 |
| Character-Voice-Service | `747e7998cb` | CVS tests: success (HEAD) | 0 | 0 | 4 |
| HSR-Voice-Archive-Builder | `8777851bf8` | tests: success (HEAD) | 0 | 0 | 12 |
| MKV-Fast-Muxer | `e625c2b04d` | Browser E2E mux tests: success (older SHA)<br>Deploy to GitHub Pages: success (HEAD) | 0 | 0 | 6 |
| Quick-Automatic-Hardsub-Encoder | `d62dd49637` | Build Android Native Core Release: unknown<br>Build Web Core Release: unknown<br>Build Android and Deploy Frontend: success (older SHA)<br>Compile Android media tasks: success (older SHA)<br>Test frontend: success (older SHA)<br>Windows local smoke: success (HEAD) | 0 | 1 | 15 |
| UIGS-Foundry | `4c4c59fb45` | Validate Foundry: failure (HEAD)<br>Collect UIGS Outboxes: success (older SHA)<br>Triage UIGS Pending: success (older SHA)<br>Generate UIGS Project State: in_progress (HEAD) | 0 | 0 | 9 |

## Interpretation boundary

- A successful latest workflow from an older SHA is reported as **older SHA**, not as validation of current HEAD.
- Path-filtered workflows may intentionally not run for every commit.
- CI status is not equivalent to real-device, renderer, release-artifact, or final-output validation.
- API/report generation failure leaves the previous report untouched and makes the report workflow red.
