# Observation: ASS prototype conflated experiment Host with production tool, hid available capabilities, repeated template layouts

Date: 2026-10-13
Status: Observation / user correction + repository source review + prototype inspection
Domain: ASS-Workbench-Android, interface architecture / design fidelity
Scope: UI design prototype; no production Kotlin modification

## Trigger
Owner rejected the newly built six MagicPath ASS UI prototypes as generic, highly repetitive and inconvenient. They observed that an independent experimental infinite canvas was presented as one item among main-editor tools and that most already implemented ASS features were not represented. This explicitly corrects the previous visual strategy: icon-first is necessary but not sufficient for quality.

## Grounded repository facts
- `app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt` defines **18 tools**: SUBTITLES, TEXT, EVENT, BATCH, TIMELINE, FRAMES, STYLE, POSITION, VECTOR_CLIP, EFFECTS, KARAOKE, FONTS, FONT_REQUIREMENTS, QC, COMPATIBILITY, DIAGNOSTICS, PROJECT, CAPABILITIES. It groups tools by domain; `WorkbenchTask` is a smaller task-navigation subset, and `CAPABILITIES` is directory/access.
- `app/src/main/kotlin/io/github/assworkbench/app/ui/UiVariantRegistry.kt` exposes `FIXED` and `SPATIAL_EXPERIMENTAL` presentations; its current `default` still reads `SPATIAL_EXPERIMENTAL` despite FIXED being named the standard main UI in 2026-10-10 docs. This is a policy mismatch requiring explicit design/product decision; do not silently change default.
- `docs/UI-AUDIT-2026-10-01.md` separates existing edit closures, partially implemented Karaoke/VECTOR_CLIP and absent bilingual-review product entry. Tool appearance is not proof of verified support.
- `docs/superpowers/specs/2026-10-11-ass-authoring-main-canvas-design.md` already advocates task-centric main navigation, separate independent experimental presentation, stable shared canonical ASS/session state, and compact vs wide adaptive arrangements.
- `docs/MAIN-CONTENT-FLOW-2026-10-11.md` previously corrected duplicate navigation and text drafts in compact layout; the new design must not reintroduce them.

## Direct observation / reusable lesson
An editable prototype can be visually polished yet semantically misleading if it treats independent presentation Hosts as task tools, models all jobs with the same three-column layout, or represents only a few of many implemented capability families. A functional icon bar is not evidence of completeness.

Separate:
1. Product Host selector: FIXED default main editor versus SPATIAL_EXPERIMENTAL testing UI, accessed via global workspace switch/settings, not as a tool navigation item.
2. Task-specific composition: Event/text, time, typesetting, Karaoke/effects, resource/diagnostics, batch/review each require distinct visual layouts corresponding to primary objects and operations, not the same grid with different labels.
3. Full tool discovery: 18 exact persisted keys reachable in a searchable catalog; frequent tools are contextual, not all forced onto a toolbar. Preserve unique editor owners and object write-target distinctions.
4. Domain status: implemented, partial and conceptual features must be marked separately. No claim of available fully featured vector drawing or mature automated Karaoke alignment.
5. Adaptive constraints: target device and task determine the arrangement; repeated broad card frames and repeated side rails are not evidence of native UI quality.

## Provisional follow-up and validation
A replacement interactive UI concept was initiated in Lovable project `f6a9cba9-e90e-4048-9ab4-0aaebc729a12` to test distinct task-centered compositions; its existence does not imply build or screen quality acceptance.
Required checks after build: correct separate Host navigation; all 18 tool catalog keys route somewhere meaningful; distinct task layouts; phone/tablet size behavior; actual long-press suppresses action on release; realistic CJK content; visual snapshot review and human task tests. No claims about Android production without exact SHA evidence.

## Dedupe
Foundry searches: 'ASS spatial experimental primary navigation', 'ASS 18 tools catalog visual coverage', 'UI prototype same layout repeated', 'task category host layout'. Adjacent existing candidates (spatial camera / gesture ownership and MKV contextual navigation) do not record this specific direct prototype failure and correction.
No Canonical promotion or ASS source modification authorized by this Observation.
