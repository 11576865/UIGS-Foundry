# Case: ASS prototype v6.2 source-aware effects review, guarded Raw proposals and Karaoke round-trip

Date: 2026-10-13
Status: Case / reproducible offline Chromium testing; not Android / libass acceptance
Domain: Android tablet-first ASS editor UI
Product: 11576865/ASS-Workbench-Android (prototype-only, no Kotlin source edits)
Prior: inbox/cases/2026-10-13-ass-v5-temporal-curves-precision-geometry-and-responsive-tools.md
Prior risk: inbox/bugs/2026-10-13-ass-v5-effects-prototype-semantic-binding-and-commit-gaps.md

## User request and rationale
Owner requested continuing the tablet-first ASS UI after v6.1. Prior open critique: animation scrubbing and displayed values may appear coherent without being tied to actual ASS source; source modification, draft ownership and Undo must not be mere UI metaphors. Preserve the independent SPATIAL_EXPERIMENTAL presentation and full 18-item capability directory.

## Offline prototype changes
Artifact: conversation-local /mnt/data/ASS_Workbench_UI_Prototype_v6_2.html, standalone HTML/CSS/JS.
1. Effect write proposal `fxWritePlan`: before/after Raw ASS strings are visible in a review dialog, opened from the current animation tool header without searching a long scroll. It exposes bounded write support and a refusal reason, plus an explicit button '确认修改示例 Raw'. Dialog is sized for tablet and phone, closes with Escape, restores entry focus, honors reduced-motion for its brief UI fade.
2. For simple single-Event ASS source, Fade + Transform tokens are appended within the initial override block (or a new leading block), preserving unrelated existing \\pos, \\fs, \\c tags. Simple Karaoke produces tagged text from the *current Event's* Unicode characters, with a separate \\kt onset distinct from duration tags.
3. Refuse merges when prior effect/Karaoke tags exist and ownership is untracked, when Raw or time/style draft is dirty, or when Karaoke text has multiple override blocks, line escapes and other source structures the demo cannot safely rewrite. This is conservative *prototype scope*, not a complete ASS parser.
4. Commit now changes the sample Event Raw string and associated `fxCommitted` in one formal prototype revision, supporting Undo/Redo. Managed re-edit uses `fxManaged.baseRaw` only when last written Raw still matches; otherwise it falls back to ordinary conflict checks, avoiding blind reapplication.
5. The source inspection and runtime screenshots revealed a new semantic defect: written inline Karaoke tokens remained in `current().txt` because `visibleText` stripped only brace blocks. This garbled the Event label and next editing pass's syllable count. Fixed by stripping bounded inline \\k/\\kf/\\ko/\\kt sequences for display, and deriving stable glyphs from the owned pre-edit plain text when re-editing managed Karaoke.
6. Dynamic glyph count and centisecond duration allocation now adapt to Event #40 and other simple text, rather than hardcoding the nine glyphs of #39; reediting managed Karaoke after Undo/Redo does not duplicate inline timing tags.
7. Confirmed timeline ruler playhead uses `100*currentMs/fxEventMs()`, not a stale fixed 3300 ms divisor; graph's rightmost label uses the Event's actual duration. Remains demonstrative, not media PTS.

## Executed tests
- Headless Chromium/Playwright, 5 viewport sizes (360x780, 390x820, 800x1280, 1280x800, 1440x850).
- Main suite: 142/142 passing checks for rendering six task surfaces without horizontal overflow, modal access, source plan, preservation of non-effect tags, commit/Undo/Redo, safe repeated edit and dynamic Unicode Karaoke length.
- Supplemental suite: 36/36 passing checks across tablet and phone: modal bounds/Escape; proposal/edit/commit/raw/Undo/Redo; Event #40 Unicode Karaoke, \\kt onset, exact visible plain text after commit, managed re-edit without accumulating duplicate tags, no runtime exceptions.
- Two previous v6.1 suites were attempted but stalled in the updated dialog-driven flow, and are **not** counted as passing tests; the 178 checks above are executed against final v6.2. Browser screenshots of tablet and phone review panels were captured and visually inspected. Node syntax check passed.
- Temporary dialog integration exposed a Playwright strict selector conflict (two source-toggle buttons) and a test timeout because a source modal covered the controls the old script expected to edit. Tests were corrected to close dialog before editing, then reopen to approve; no product crash claimed.

## Limits / follow-up
**Do not call this a production ASS writer.** The source adapter only demonstrates a constrained simple-event subset. It does not parse arbitrary override sequences, nested transforms, reset semantics, karaoke syllable timing from audio, line escapes and grapheme clusters, Hardsub render compatibility, MPV/libass result, font shaping, actual Android touch/IME, persistent save or MKV.
Before native adoption: AST/Raw-preserving replacement from the real engine, per-tag source spans, stable ownership and write target, rendering tests with actual media and fonts, concrete same-action device gesture evidence, source-aware conflict UI for complex tags. No Canonical mutation; no Android repo changes.
## Dedup
Foundry searches: 'ASS prototype managed effects raw write preservation conflict scope', 'karaoke inline tags visibleText incorrect', 'ASS effects writing source comparison transactional preview', 'compact source diff modal plan guard' found adjacent prior Cases but not this source-bound end-to-end prototype correction.
