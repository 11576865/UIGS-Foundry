# Case: ASS tablet-first native UI evidence-bound design synthesis

Date: 2026-10-14
Status: Design/report Case; source-backed and PDF-render reviewed; **not Android UI acceptance**
Product: 11576865/ASS-Workbench-Android
Related: inbox/cases/2026-10-14-ass-native-fade-preview-parity-malformed-raw-safety.md
Related: inbox/cases/2026-10-13-ass-v6-3-minimal-ui-revision-not-design-freeze.md

## Delivered work
Compiled a 26-page PDF engineering and tablet UI report in the active conversation: ASS_Workbench_Android_工程进展与平板UI完整设计报告_2026-10-14.pdf. Included actual browser screenshots (offline v6.3, clearly labeled), five newly drawn UI concept plates (tablet landscape, tablet portrait, compact, animation, timing), state ownership diagram, source-guarded edit transaction diagram, the historical 240 UI ledger visualization (51 implemented, 108 partial, 79 planned, 2 blocked on 2026-10-03) and a qualitative risk matrix.

## Grounding
Read and incorporated attached UI Constitution, Workspace Architecture, 240 UI/UI Contract progress, infinite canvas status, engineering principles, long multi-UI synthesis, and Designing Interfaces 3rd ed. Also verified current main files for native Fade proposal/draft states, CI workflow definition, and Gradle configuration. Historic figures are not converted into present-day completion percentages.

## Reusable distinction
A single design-and-implementation report should distinguish (1) past requirements ledger, (2) current GitHub source evidence, (3) executed CI result, (4) real native visual/device evidence, (5) new speculative design drawings. An offline HTML Chromium screenshot is legitimate visual evidence for that prototype, never a Compose/libass screenshot. Source-only commits do not imply native Gradle/build/device success. Present the *same* feature/classification across functionality, code, UI target, test gate, and evidence state.

## User design constraints represented
Tablet is primary. Compact mode is separately composed, not desktop panes scaled down. Persistent text is minimized without hiding safety-critical actions. Existing 18 tool identifiers remain stable. FIXED primary host is distinct from opt-in SPATIAL experimental canvas. Sliders supplement exact-value/real ASS time semantics. Motion for editor UI must be separated from subtitle-authored animation.

## Evidence limits
PDF generation and page rendering checked: 26 A4 pages; 10 verified document hyperlinks; actual screenshots alongside explicitly labeled synthetic design plates. No Android Gradle success logs, emulator tests, device gestures, actual libass render or .ass save/reopen completion was established while preparing this report. No changes to Android repo or Canonical rules in this reporting task.

## Dedupe/governance
Foundry searched phrases: ASS Workbench October 14 tablet first PDF original UI design plates source evidence; ASS tablet UI visual design report snapshot source code CI device evidence; ASS main UI concept diagrams 240 historical ledger no completion percentage. Prior individual native UI Cases and earlier HTML Cases do not encompass this new cross-layer evidence-separated report and graphics. Keep as Case, not Canonical.
