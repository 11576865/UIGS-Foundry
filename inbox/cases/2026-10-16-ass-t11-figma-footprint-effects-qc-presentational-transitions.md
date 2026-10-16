# Case — ASS T1.1 presentation footprint prototyping with safe view-only promotion

Date: 2026-10-16
Status: Case + Candidate observation / **Pending owner review and Android interaction evidence**
Figma: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Review page: 26:2
Source project: 11576865/ASS-Workbench-Android

## Trigger
Owner said "继续" following explicit agreement that some ASS tools deserve primary workspace area while others only need a compact status UI, popover or confirmation dialog. Previous candidate `inbox/candidates/2026-10-16-ass-tool-presentation-footprint-modal-progressive-disclosure.md` defines the suggested dimensions; this record captures new **actual, screenshot-reviewed editable Figma output** and separate behavioral evidence boundaries.

## Work completed
On the existing isolated review page **only**, added five editable Figma frames:
1. `38:2` — `05 / CANDIDATE · 18工具展示体量与升格规则` (1680×1750). 18/18 exact WorkbenchTool IDs appear **once each**, with default footprint, conditional expansion, active/passive/hybrid presentation and the invariant that must not disappear across the transition. The original first screenshot showed three headings for a two-column matrix; fixed alignment and re-checked.
   Link: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=38-2
2. `39:2` — `06 / CANDIDATE · EFFECTS 小面板与占屏收敛` (1440×900). A 466px inspector with `\fad` fade-in 220ms, fade-out 180ms, `\blur` 3.0px, while the media/timeline retains primary editing area. Candidate identity labels: EFFECTS, Instance `I_E39`, Follow Focus #39, Draft `D1`, PTS `01:20.800`.
   Link: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=39-2
3. `39:176` — `07 / CANDIDATE · EFFECTS 升格专业工作区` (1440×900). The **same design-fixture instance identity and values** are shown in full animation workspace with keyframe lanes; a caption warns graphical easing is not guaranteed to round-trip to ASS `\t` arbitrarily. On-click navigation connects (2) and (3) in both directions, showing a **presentation transition** only.
   Link: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=39-176
4. `40:2` — `08 / CANDIDATE · QC 内联状态小UI` (1440×900). An unobtrusive QC summary below a TEXT authoring scene shows 1 ERROR / 1 WARNING with one `查看检查详情` affordance; main editing and draft D1 remain visible. QC is described as reading the saved document, not implicitly consuming uncommitted TEXT draft.
   Link: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=40-2
5. `40:87` — `09 / CANDIDATE · QC 按需报告与条件修复` (1440×900). A 480px on-demand right sheet exposes two source-grounded rule examples: `QC.UNKNOWN_STYLE` on Event #43 with conditional `UseDefaultStyle` Quick Fix; `QC.VERY_SHORT_DURATION` on #42, **without** Quick Fix. View-layer navigation connects this report and summary in both directions. No autofix click-through, commit or fake success.
   Link: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=40-87

## Verification
- Read `app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt`; confirmed exact 18 stored tool IDs, including the fact that EFFECTS currently has FollowFocus but **not** PinnedEvent or duplicate permission. Do not implement unsupported pin/duplicate controls as if currently supported.
- Read `docs/FIXED-INSPECTOR-DRAFT-TOOL-SWITCH-2026-10-10.md`, `docs/SHARED-AUTHORING-2026-10-11.md`, `docs/INFINITE-CANVAS-WORKBENCH-V2.md`: various draft/Host lifetime behaviors have distinct scopes and incomplete device evidence. Candidate deliberately uses **same textual identity and values** in both EFFECTS screens; this **does not prove** runtime state persistence.
- QC conditional fix mapping grounded in existing `AdvancedQcPane.kt` and `AssLinter.kt` inspected earlier in the project (only relevant linter rules shown).
- Took actual screenshots of matrix, both EFFECTS states and both QC states, reviewed for readability and layout. Four view-only ON_CLICK Figma NAVIGATE sources exist (EFFECTS promote/collapse, QC expand/collapse).
- Independent readback of page `0:1` confirmed **exact original nine IDs** `2:21, 2:612, 4:2, 5:2, 6:2, 7:2, 8:2, 16:2, 18:2` unchanged as to identity/count. Isolated review page `26:2` now has ten top-level frames: prior audit + TEXT + SPATIAL + BATCH + QC plus these five new frames.
- Matrix readback: 18 total and 18 unique persisted Tool IDs. Both EFFECTS and QC added screens are 1440×900 with editable text/vector/rectangle hierarchy, not flattened screenshots.

## Limits and further test gates
- No code changes, merges, published component variants or Canonical mutation.
- Figma prototype NAVIGATE shows visual page-to-page transition, not shared memory or guaranteed StateFlow survival. Prove identity, Binding, draft, Focus, selection, write target, media PTS and Undo invariants through explicit Kotlin model tests and native instrumentation **after owner approves implementation**.
- Expanded QC sheet temporarily occludes a portion of the background inspector: further layout decision is needed for narrow tablets and actual touch interaction. Do not extrapolate 1440×900 to 1024×768.
- The L1–L5 design terms describe **presentation form**, not importance or warning severity; modal L5 should only gate explicit decisions, not spontaneous diagnostic conditions.
- Figma remains Candidate; there is no owner visual acceptance, real media rendering, or Android device screenshot parity.

## Intake and deduplication
Queried Foundry:
`ASS T1.1 footprint promotion EFFECTS compact expanded QC inline 2026`,
`ASS surface display states draft binding unchanged Figma candidate`,
`18 tools spatial hierarchy modal progressive disclosure candidate`.
A conceptual footprint Candidate was found; no duplicate actual Figma five-frame/screenshot-reviewed case exists. This record extends the conceptual candidate with traceable artifacts and limitations. Do not promote this isolated observation to Canonical automatically.
