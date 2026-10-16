# Case — ASS Tablet V1.1: Desktop-pro workflow density without copying mouse-centric controls

Date: 2026-10-16
Status: Design Case / Pending owner review and native device implementation
Figma file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
New page: `56:2` — `ASS Workbench · Tablet UI V1.1 / 专业参考`
Predecessor: `inbox/cases/2026-10-16-ass-tablet-v1-integrated-first-product-ui-figma.md`

## Owner request and interpretation
After an integrated tablet V1 was actually drawn, owner said: "参考桌面其他专业软件". Work was directed to **improve real V1 product layout** using grounded specialist software patterns, not write another report or spawn unrelated isolated tool explorations. Prior explicit caution: preserve original V1 and T1.1 frames.

## External desktop references consulted (public documentation)
- Aegisub official overview: https://aegisub.org/docs/latest/overview/ — subtitle grid and edit box as primary areas; video and audio support timing; selected, comment, visible-current-frame and overlapping cues distinguished in grid.
- Subtitle Edit current main window docs: https://subtitleedit.github.io/subtitleedit/features/main-window.html — text editor, video player, waveform/spectrogram with colored subtitle spans, start/end draggable edge markers, media cursor, snapping.
- Subtitle Edit audio visualizer docs: https://github.com/SubtitleEdit/subtitleedit/blob/main/docs/features/audio-visualizer.md — waveform and spectrogram as separate views, configurable toolbar, multi-track audio picker.
- Adobe Premiere help: https://helpx.adobe.com/premiere/desktop/get-started/tour-the-workspace/dock-group-undock-panels.html — docking vs panel grouping vs floating windows, stacked and tabbed state.
- Blender manual: https://docs.blender.org/manual/en/5.0/interface/window_system/areas.html — task-specific workspaces, editors in areas, resizing/docking, touch corner handles.
- DaVinci Resolve Edit page was visually reviewed for viewer/timeline/inspector proportion and task-oriented workspace, but no particular claim of specific current version behavior has been used as implementation evidence.

## Actual Figma-native screen results
One **new independent page** with four editable Frame trees:
1. `56:3`, 1440×900, `01 / V1.1 · 专业字幕主工作台`: three production areas plus task tabs: (i) nine-row professional subtitle **grid with columns** #, start, end, Style, text, Focus/selection (replaces long card stack); (ii) centered saved-media reference preview (source fixture sized 453×255, ~16:9), transport, waveform, cue interval lane with two exposed selection boundary handles and visible media PTS, bilingual Event Text editor plus Raw/draft affordances; (iii) Event/Style/position context inspector with source provenance and compact QC signal. Native icon geometry replaces single-character task glyphs.
2. `59:2`, 1440×900, `02 / V1.1 · 专业校时工作区`: selected TIMELINE task, preserves same document, list and media clock, **shrinks preview, enlarges waveform/optional spectrogram and cue region**, adds time-specific inspector with Start/End/duration/media PTS/snap actions. Prototype switch from #56:3 and back is connected.
3. `61:2`, 1024×768, `03 / V1.1 · 紧凑专业工作台 1024`: Event grid collapses to explicit top bar entry instead of scaling three fixed columns, smaller 16:9 preview, retained wave/cues, bilingual editor, contextual inspector and QC, touch fields as native editable Figma layers. Actual screenshot exposed overlay collisions in toolbar/QC; subsequently fixed by relocating event list action to task bar, reducing source chips to 22px (non-interactive labels) and repositioning QC/review.
4. `63:2`, 1024×768, `04 / V1.1 · 紧凑平板事件表格抽屉`: uses **the same table representation** over a dimmed editing scene, not an unrelated card navigation. Seven rows fully visible with other rows represented as scroll content; after screenshot spotted overlap with bottom status, hides clipped rows #43-#44 and moves grid footer.

Verified page frame count 4 (two 1440×900 and two 1024×768); screenshot inspected on all four, including rechecks after geometry repairs. Figma control link count=5: main↔timing, compact↔drawer and selecting current Event #39. Other sample Event rows are visual samples only; no false selected-document mutation.

## Design decisions vs rejected copying
- **Adopt:** tabbed task workspaces, high-density table/list, explicit source/target indicator, independently resizable visual zones, multi-track cue/waveform model, conditional source provenance, compact diagnostics.
- **Do not copy mechanically:** desktop-only keyboard shortcuts and hover target dependency, cramped drag edges, unrestricted splitter proliferation, multiple mouse-driven windows on a 1024 tablet, or native media timeline operations not yet implemented.
- Figma splitter handles and playbar are static; nav tabs have prototype links only for grounded screens. Reusable tool instance identity, binding, and save safety must be tested later in Kotlin/Android.
- Video illustration, audio waveform, frequency spectrogram, media PTS and texts are intentionally **design fixtures**, not real decoded audio/video, libass test output or end-to-end validation.
- This is a V1.1 candidate for visual evaluation, not a production Android UI or a change to 18 Tool IDs. Source text (English) and Chinese are placeholders for two-language affordance, not a parsed dual-track document.
- No code or prior Figma frames on original V1 page `43:2` or legacy T1.1 `0:1` modified by this turn. No canonical guidelines changed.

## Source comparison takeaway
User intent was to reach a professional product **initial UI**, not accumulate case studies. Desktop pro design informed higher information density, central task surface and contextual panel behaviors, but the tablet V1.1 still prioritizes touch reachability, single task focus, draft/write separation and a compact responsive scene. Best next action: owner evaluates `56:3` and `59:2` side-by-side before replacing any previous V1 screen.

## UIGS intake and dedup
Searched Foundry for the exact Aegisub/Subtitle Edit V1.1 workflow-dense tablet design and professional-app Figma prototype, no exact duplicate. Adjacent previous V1 and tool-footprint Candidates are not the same actual prototype changes. Do not promote single-source comparative conclusions to Canonical.
