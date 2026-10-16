# Candidate — Source-grounded BATCH/QC tablet UI in isolated Figma review page

Date: 2026-10-16
Status: Candidate / PENDING owner visual and interaction acceptance; not Canonical
Figma file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Baseline: original nine T1.1 frames fully retained with exact IDs `2:21,2:612,4:2,5:2,6:2,7:2,8:2,16:2,18:2`.
Predecessor: `inbox/candidates/2026-10-16-ass-t11-conservative-capability-inheritance-review-page.md`.

## User approval scope
The user said “可以” in reply to a proposal to continue cautiously: preserve established T1.1, only propose isolated fragment candidates, do not drop older features without review. This does not authorize merging into Android, replacing the Figma baseline, declaring the UI final or changing UIGS Canonical.

## Live sources consulted
- `app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt` — 18 stable tool IDs with BATCH and QC.
- `app/src/main/kotlin/io/github/assworkbench/app/ui/RuleBatchPane.kt` — explicit scope, filter/recipe, preview/review and protected application flows.
- `docs/BATCH-REVIEW-2026-10-12.md` — scope modes (selection/results/intersection/document), stable Event IDs, empty scope not widened, session/revision/target invalidation, commit exact reviewed immutable result and a single history edit, paginated results and focus-only navigation.
- `app/src/main/kotlin/io/github/assworkbench/app/ui/AdvancedQcPane.kt` and `core/domain/src/main/kotlin/io/github/assworkbench/domain/AssLinter.kt` — QC severity, category/code, issue-specific quickFix presence; UNKNOWN_STYLE can offer UseDefaultStyle, VERY_SHORT_DURATION does not have a quickFix.

## New isolated Figma deliverables
Same preexisting review page `26:2`, added exactly two top-level 1440×900 native editable candidate frames:
- `33:2` BATCH: scope → filter → action → reviewed preview → guarded commit. Example selection exactly #39 and #40, SHIFT +200ms; before/after 01:20.800–01:22.400 → 01:21.000–01:22.600 and 01:22.500–01:24.100 → 01:22.700–01:24.300; no text/Style mutation. Distinct scope ID count, match count and changed count; revision/session identity, invalidation and no implicit rescan. Labels clearly state static mock not actual preflight. https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=33-2
- `34:2` QC: issue severity and category navigation, issue detail, rule evidence, conditional Quick Fix and re-check boundaries; sample #43 QC.UNKNOWN_STYLE / missing Ghost / sample available Default, and #42 QC.VERY_SHORT_DURATION 120ms which has no quickFix. Separates Event-only Style reference change from shared Style edits. Static fixture not a renderer or actual lint report. https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=34-2

## QA evidence / boundaries
Screenshots retrieved with Figma get_screenshot for both new frames and visually inspected. A subsequent read-only Figma API structural audit confirmed: original page still has exactly nine frames and same IDs; isolated review page now has five frames (audit + TEXT + SPATIAL + BATCH + QC), with 82 editable text nodes on BATCH and 73 on QC. Both BATCH and QC candidate frames have **zero prototype reactions**—dangerous actions are intentionally not wired or represented as successful commits. Preview numbers/sample issues are labeled demo data. No Android project writes, no original Figma frame edits and no Canonical changes.

## Design principles proposed for later validation
1. **Catalogue completeness ≠ functional UI coverage:** a stable Tool ID and a directory entry cannot replace an actual editable task scene with failure/recovery states.
2. **Preview receipt is a transaction artifact:** effective target ID set, session, revision and recipe changes must invalidate reviews; do not automatically rescan and commit different targets.
3. **Rule-based diagnostic ≠ authority over content:** severity and Quick Fix eligibility are separate; navigate an issue without mutating Selection/document, and label renderer/compatibility evidence separately from linter analysis.
4. **Safe Figma design iteration:** keep prior accepted frames untouched, isolate candidate screens, inspect actual renders, label design fixture truthfully, require owner approval to promote. These are CANDIDATE reusable learnings, not general Canonical directives.

## Pending
Await owner's design and workflow review. Remaining missing production UI designs for EVENT, STYLE, VECTOR_CLIP, FONTS, FONT_REQUIREMENTS, PROJECT, COMPATIBILITY, DIAGNOSTICS; partial operations remain pending. Real media, Android emulator screenshots, full navigation and actual writes were not exercised.

## Foundry deduplication
Searched before creating for `ASS tablet conservative candidate BATCH QC review Figma`, `AssBatchReview preset scope stale preview sample design`, `QC.UNKNOWN_STYLE conditional quick fix candidate design`; no exact duplicate. This captures new designed candidates/verified separation not included in prior isolated TEXT/SPATIAL candidate or the legacy coverage observation.