# Observation: ASS Workbench competitive differentiation requires task-level evidence

Date: 2026-10-13
Status: Observation / external public product documentation + project code/document review; no field or timed benchmark
Product: 11576865/ASS-Workbench-Android
Scope: product positioning, competitive analysis, UI and acceptance methodology

## Trigger and factual context
The owner requested ASS Workbench competitive positioning, future directions, and corrections to possible product misunderstandings, explicitly following the deeper domain rethinking of MKV-Fast-Muxer and Quick-Automatic-Hardsub-Encoder.

ASS Workbench public README/ABOUT specify: ASS is canonical editable document, mpv/libass renderer authority, raw-preserving structured editing, Undo/recovery, font and container diagnostics, Fixed and Spatial working presentations. Current main merged PR #138 on 2026-10-13, but repository evidence does not amount to a fresh real-device authoring benchmark. The 240-item experimental UI ledger states its implementation classifications are not product maturity percentages; prior mode names can migrate while individual user operations remain inaccessible.

## External competitor evidence and limitations
- Aegisub official documentation documents audio timing, VFR timecodes, visual typesetting, macros/Lua automation, font collection and recovery; October 2026 v3.5.0 release adds more editing refinements and security updates. Mature desktop authoring throughput is a meaningful reference, not just a screenshot.
  Sources: https://aegisub.org/docs/latest/highlights/ ; https://github.com/TypesettingTools/Aegisub/releases
- Subtitle Edit covers waveform/spectrogram, timing, conversion and broad subtitle workflow. https://github.com/SubtitleEdit/subtitleedit/blob/main/docs/features/main-window.md
- AxiSubs Google Play listing advertises Android ASS/SRT text/timeline editing and export. Marketing claims are not comparative verification. https://play.google.com/store/apps/details?id=com.ekseninteractive.axisubs
- samgum/aegisub-android publicly describes broad Android ASS authoring functionality but lists libass JNI precise rendering as future scope. Its README is developer self-report rather than independent field acceptance. https://github.com/samgum/aegisub-android
- CapCut mobile supports rapid auto-captioning, timing and style editing, but is an adjacent general video/caption workflow rather than evidence of arbitrary ASS lossless authoring. https://www.capcut.com/help/how-to-recognise-subtitles

## Reusable observation
A project cannot infer its competitive value from feature count, unique interaction architecture, PR count, or successful unit/UI CI. Compare competitors using the SAME controlled representative user jobs, covering:
1. existing complex ASS opening and no-op save/reopen preservation;
2. editing timed dialogue to audio/video with documented target accuracy and required corrections;
3. styled scene sign positioning, animation and font diagnostics with actual renderer observation;
4. multi-event batch edits with exact write scope, preview and rollback;
5. MKV track import/replace and independent output check;
6. rotation, IME, long media and interruption/resume in the target device environment.
For each job record capability availability, correctness, time-to-completion, error/recovery, output fidelity, and source/CI/device evidence separately.

Potential differentiation hypothesis: an ASS-semantic, raw-preserving, renderer-backed, explainable authoring and validation workbench, not mere “Aegisub shrunk to Android” and not “240 novel UI items.” This is a STRATEGIC HYPOTHESIS, not a market need, usability measurement or authorized Canonical product scope change.

## Dedupe and governance
Checked Foundry search for competitor/task benchmark/feature completion. Existing 2026-10-12 QHE competitor-scope observation and 2026-10-13 HSR subtitle requirement-to-preview observation cover related evidence discipline, but not the ASS-specific mobile/editor competitive baseline and task battery documented here.

No Canonical promotion. No change to ASS repository, backlog, feature priorities or product charter. Actual selection requires owner approval and controlled device/real-project evidence.
