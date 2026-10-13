# Case: ASS UI Design Freeze RC — close prototype phase with truthful status and Android integration gate

Date: 2026-10-13
Status: Case / reproducible browser-tested design handoff, **not** Android product acceptance
Product: 11576865/ASS-Workbench-Android (offline UI prototype only)
Prior: inbox/cases/2026-10-13-ass-v6-2-source-aware-effects-review-and-cjk-karaoke-roundtrip.md

## Trigger
Owner indicated that the successive UI prototype iteration is nearly done and asked to continue. The appropriate closure is a bounded design freeze candidate with exact evidence and Android handoff, not another multi-page redesign or a claim of finished Kotlin delivery.

## Delivered artifacts
Conversation-local (not GitHub Android app):
- /mnt/data/ASS_Workbench_UI_Design_Freeze_RC.html
- /mnt/data/ASS_Workbench_UI_Design_Freeze_RC.zip
- Inside package: index.html, Chinese handoff/readme mapping to native Kotlin entry points, 10 actual Chromium screen captures, test scripts, 3 JSON test reports, SHA256 file manifest.
This is an offline single-file HTML design demonstrator. No Android source, Canonical spec or actual .ass/.mkv was modified.

## Confirmed closure fixes
1. Selected Event reference time is derived dynamically from its start/end rather than leaving the fixed #39 01:19.320 on the top header, player-reference clock and event time inspector when #40 is selected. This is labelled Event entry/reference, NOT actual media PTS.
2. No longer calls in-memory simulated Save a disk save. Tooltip, project status and persistent footer label describe demo-only storage. Mobile explicitly displays a compact DEMO badge where responsive CSS hides detailed status. The compact header required a follow-up allocation fix: first attempt rendered the badge over the filename, then a mobile width allocation and secondary-action removal from compact header prevented overlap, while settings/help remain reachable through existing global UI.
3. The sample Event table shows its actual seven in-memory rows, not a fictitious 187 document events.
4. User-provided Event text, searching, video subtitle and workspace breadcrumb are HTML-escaped at render boundaries. Earlier implementation used unescaped user text in innerHTML template strings. This is only a local prototype risk reduction, NOT a certified sanitization mechanism or a supported file-import pipeline.
5. UI footer no longer asserts arbitrary-ASS Raw-preserving production validation or real media decoding.

## Tests on exact RC bytes
- Original v6.2 primary browser test: 142/142 passing, rerun with RC file.
- Source-proposal/modal/Undo/Karaoke test: 36/36 passing, rerun with RC file.
- New audit: 90/90 passing at 1280×800, 800×1280, 390×820, 360×780. Covers all six tasks, 18 catalog entries, event #39→#40 time continuity, mobile DEMO visibility and filename non-overlap, visually escaped subtitle text, runtime errors and prototype status.
- 10 Chromium screenshots captured from exact UI RC. No JS page exceptions during capture.
These are **268 assertions across overlapping browser suites**, not 268 independent product requirements, human usability conclusions or Android native tests.

## Android interface mapping / next boundary
- app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt — persisted 18 WorkbenchTool keys and descriptors; no renames.
- app/src/main/kotlin/io/github/assworkbench/app/ui/EventTextDraftStore.kt — session/instance/Event-owned drafts and IME semantics.
- app/src/main/kotlin/io/github/assworkbench/app/ui/UiVariantRegistry.kt — FIXED stable vs SPATIAL_EXPERIMENTAL, currently new-session default is still SPATIAL_EXPERIMENTAL and requires separate approved native change.
- core/domain/src/main/kotlin/io/github/assworkbench/domain/AssKaraoke.kt / AssKaraokeFxAuthoring.kt and AssFxComposition.kt — existing domain-side Karaoke and specialized effect plans; cannot assume HTML writer supports real tag spans.
- app/src/main/kotlin/io/github/assworkbench/app/ui/ModernEditorScreen.kt / VideoPreview.kt and EditorViewModel.kt — actual editor/render/session composition.
Recommended native vertical slice: target Event → effective source and precise Write Target → transient edit → actual mpv/libass sample → Raw diff approval → domain Undo → .ass save/reopen round-trip, on a tablet.

## Evidence exclusions
No Kotlin Compose UI modification, Android emulator/device acceptance, real PTS, real libass output, signed APK, arbitrary ASS semantic writer, MKV/ASS disk save or release-quality task benchmark. This is **design phase closeout**, not software product completion.

## Dedupe
Foundry searched 'offline prototype claimed file saved without disk write', 'ASS UI demo incorrect sample Event count', 'responsive DEMO status hidden on compact layout', and 'subtitle text unsafe injected innerHTML prototype'. Adjacent historical HSR save evidence and v6.2 ASS case exist but no matching RC closeout plus executed corrections.
No Canonical promotion.
