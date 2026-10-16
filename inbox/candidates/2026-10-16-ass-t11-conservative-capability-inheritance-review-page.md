# Candidate — Conservative capability-inheritance review as isolated Figma page

Date: 2026-10-16
Status: **Candidate / Pending owner design acceptance** (not Canonical, not native implementation)
Product: 11576865/ASS-Workbench-Android
Figma file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
New review page: 26:2

## User instruction
After coverage review identified that T1.1 represented a complete catalogue without complete task UIs and omitted some historical interaction innovations, the user authorized continuation **with caution**. Interpret as a strict change boundary: preserve established T1.1 and make reversible, independently reviewable candidate additions; do not infer approval to replace production design or merge Android UI.

## Read evidence
- Actual repository `app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt` currently defines 18 stable persisted Tool IDs and `TEXT` as a first-class `WorkbenchTask`.
- `docs/MULTI-UI-CAPABILITY-MIGRATION-2026-10-11.md` documents 8 historical interaction families and their then-current implementation and outstanding production Host gaps. This 2026-10-11 document is a *dated audit*, not a certified latest state for 2026-10-16.
- Current Figma T1.1 has 9 editable frames; existing IDs: `2:21`, `2:612`, `4:2`, `5:2`, `6:2`, `7:2`, `8:2`, `16:2`, `18:2`.

## Actual Figma edits, verified
Only created **one independent page** named `T1.1 · 能力继承审查（候选，不替换）`, id `26:2`. Within the page:
1. `26:3` (1680×1770): audit board of exactly **18 unique Tool IDs** plus 8 historical model rows. T1.1 design status counts: catalogue-only 1; partially designed 7; missing complete workflow 10. These counts express Figma design coverage only, **not** Android functional completeness or release readiness. https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=26-3
2. `27:2` (1440×900): TEXT first-class task candidate, Event #39 Focus, draft Event Text distinguished from saved Raw, Style source shown read-only, explicit target `Event Text #39` while shared Style remains unselected. Draft adds a punctuation mark; before text lacks it; the receipt matches the actual sample difference. `TEXT` does not pretend to have `PinnedEvent` or duplication it does not declare. https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=27-2
3. `28:2` (1440×900): independent SPATIAL Host candidate containing `STYLE` instance A following Focus #39 and `POSITION` instance B pinned to #38, visible distinct binding. Draws four edge locations and one bottom Timeline Dock, with caution that four-edge/docking/gesture completeness is **not** currently proved by existing implementation. A caption-overlapping rectangle in the preview was corrected to outline only after actual screenshot inspection. https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=28-2

Read-only structure audit after authoring: original page still contains exactly 9 frames with the same exact IDs; review page contains exactly 3 top-level editable frames with 104, 72 and 60 text nodes respectively. All added figures are Figma-native, editable layer trees (not imported flattened screens). Actual screenshots were retrieved and reviewed for all three new frames, and both candidate screens after fixes.

## Hard boundaries
- Original 9 Figma frames and their Prototype reactions were **not mutated** by this turn.
- No change to ASS Android code, main, Stable Tool IDs, old-mode resolution, saved project formats, user data or Canonical rules.
- No new working prototype navigation or live save/edit behavior claimed for candidates. Illustration and labels are **nonfunctional design fixtures**.
- No full restoration of all 18 tool UI workflows, no 240-item compliance claim, no redesign freeze, no Android performance or visual acceptance.
- Do not silently convert dated migration findings into latest production status; verify exact current code/screenshot/device evidence before implementing each ability.

## Reusable candidate rule
For a cautious UI inheritance iteration: (1) freeze existing reviewed screen IDs as a baseline; (2) construct a source-grounded **capability-to-surface matrix** before any replacement; (3) model one or two highest-impact missing interactions as isolated candidates; (4) separately verify sample data invariants, layer editability, visual geometry and document untouchedness; (5) request owner selection; only then merge *approved fragments*, one at a time, into mainline design and native UI. This is a Candidate for reuse, not Canonical evidence from one task.

## Dedup
Searched UIGS-Foundry with phrases about T1.1 reversible capability parity page, TEXT/Style source target candidate and SPATIAL instance inheritance. No exact duplicate. Prior records:
- `inbox/observations/2026-10-16-ass-t11-visual-catalogue-parity-and-legacy-interaction-loss.md` (coverage problem, prior to actual cautious design);
- `inbox/cases/2026-10-16-ass-tablet-t1-figma-task-semantic-seven-screen-prototype.md` (original T1);
- `inbox/observations/2026-10-16-ass-tablet-t11-source-severity-separation-karaoke-quantization-and-adaptive-drawer.md` (T1.1 localized fixes).
This new candidate captures a **tested, conservative change-isolation process**, not a repeat of the gaps, and makes no automatic Canonical edits.
