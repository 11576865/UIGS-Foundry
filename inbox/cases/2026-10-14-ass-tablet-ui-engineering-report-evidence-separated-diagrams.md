# Case: ASS tablet-first UI and engineering report with separated evidence levels

Date: 2026-10-14
Status: Case / authored and PDF-rendered; documentation evidence only
Product: ASS-Workbench-Android

## Artifact
Conversation-local PDF: ASS_Workbench_Android_工程进展与平板UI完整设计报告_2026-10-14.pdf
26-page A4 PDF, with authored diagrams, engineering tables, visual UI designs and real prior HTML prototype screenshots. The PDF is supplied to the user as an attachment, not committed to the Android repository.

## Basis and observation
The 2026-10-03 240-item UI ledger is a historical snapshot (Implemented 51, Partial 108, Planned 79, Blocked 2). It cannot be used as today's native completion percentage. Android main source changes can be confirmed through GitHub, while old-style commit statuses did not confirm a current Android build or emulator result. Independently, HTML v6.3 screenshots are evidence of the browser prototype only; new tablet landscape/portrait, compact, timing and animation illustrations are proposal diagrams only.

## Reusable reporting approach
1. Distinguish historical inventory, current source, committed test code, executed CI/device evidence, captured prototype UI, and unimplemented concept art. Label each visual with its real evidentiary status.
2. In design reviews, preserve the user's hierarchy: tablet-first operations, terse contextual controls and long-press help, stable FIXED main Host, separately enabled SPATIAL experiment.
3. Attribute only confirmed main changes to native implementation: authoring draft source guards, validated Fade/Blur and Transform operations, and preview/Apply boundaries. Do not infer APK readiness, actual media timestamps, libass fidelity, arbitrary ASS tag round-trip or device accessibility from commits.
4. Provide explicit test IDs and exit criteria for real Gradle, AndroidTest, tablet orientation, IME, Undo, save/reopen, compatibility and renderer outcomes.
5. Review the final PDF using page rendering, inspect representative pages at a readable resolution and verify source-based historical numbers before delivery.

## Evidence status
The completed PDF was verified locally: 26 pages, extractable Chinese text, embedded pictures and link annotations; representative pages and a contact sheet inspected. This is documentary verification, not new Android CI or device testing.

## Governance
Existing Foundry ASS UI prototype Cases and control-grammar Observations were consulted as related prior topics. This Case captures the distinct documentation/traceability artifact and its source/proposal distinction. No Canonical rules changed.
