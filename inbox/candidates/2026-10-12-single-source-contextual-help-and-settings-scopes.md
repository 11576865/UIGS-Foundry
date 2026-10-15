# Candidate: One knowledge authority, multiple contextual presentation depths, and separately scoped settings

Date: 2026-10-12
Status: Candidate / product-design proposal only; unimplemented, untested, not Canonical
Products: `11576865/MKV-Fast-Muxer`, potentially ASS Workbench and other professional tools
Related:
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`
- `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md`
- `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md`
- `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md`

## User proposal and product audit

User noted absence of a narrow-sense Settings system and desired a consistent small icon language: diagnostic warning triangle is a signal whose detailed cause is inspectable, help `?` opens context-specific professional explanations, and dense explanatory prose should migrate off the permanent canvas. User proposed an optional icon-only mode, documentation index, encyclopedia-style cross-linking, and requested a coherent system rather than isolated bubbles or a disconnected manual.

At audited product main (2026-10-12, commit `7781a4f410a9c6edb9a1f3d056091e6ace333cc4`), `index.html` includes `icon-button` with `aria-label`/HTML `title` for some actions; the primary markup has no explicit Settings / Help navigation entry. This is not a claim that all input controls/settings are absent.

## Candidate design contract

### Settings scope and authority
Define distinct semantics for:
- persistent **application/user preferences**: theme, display density, toolbar label density, shortcut/help behavior, workspace arrangement, accessibility preferences;
- **project defaults/presets**: future output naming and new-object defaults, stored independently from each existing object's values and migration rules;
- **current object/domain properties**: actual track/attachment/chapter/tag metadata, not hidden in global settings;
- **execution/verification policy**: selectable safe strategies, runtime capability and validation budget with explicit applicable scope. A compact interface must never suppress blocking errors, pretend a validation passed, or silently weaken data-integrity guarantees.

Define precedence explicitly; do not retrospectively mutate existing content when defaults are changed. When a setting affects reproducible output, record its effective value or freeze a plan snapshot. Support reset and safe import/export migration.

### Knowledge architecture
Maintain a versioned, identifiable `HelpTopic` as the single source for:
- short action label and optional tooltip;
- contextual one-paragraph definition, consequence and caveat;
- persistent inspector/help drawer with examples and related concepts;
- searchable, deep-linkable full documentation/handbook;
- diagnostic explanations linked by structured issue codes and current evidence; current project facts MUST come from real inspection, not static help text.

Example `matroska.track.flags.forced` links UI label, contextual help, detailed article, diagnostic explanations, standard references and related Default topic. Knowledge is shared, UI surfaces are projections. No four separately maintained copies. Concept-level help is distinct from real-time operational status and action.

### Icon and density semantics
Allocate separate icon categories to **domain object**, **action**, **status/severity**, **explanation/help**. Avoid assigning one shape to multiple unrelated meanings. An alert glyph signals a grounded inspectable issue, not a general Help anchor. Success, warning, blocked, unknown/not checked and in-progress are separate states; status icons must carry text/accessible labels somewhere appropriate.

Do not attach '?' to every row. Use discoverable context help near ambiguous controls, F1 on focused contexts, global help/search, and documentation links; minimize visual noise.

Allow optional compact/icon-only **toolbars**, not mandatory whole-application "zero text" behavior. Keep essential file/track identities, technical values, high-risk commands and actionable errors visibly labeled. On touch, tapping must work; long-press is only an accelerator and may conflict with drag/reorder. Focusable popovers with links are not plain ARIA tooltips. Hover-activated content needs WCAG 1.4.13 dismissible, hoverable, persistent behavior and icon targets need WCAG 2.5.8 sizing/spacing.

## Acceptance test proposal

One ambiguous real parameter, one missing-font warning, one output blocking error, one context-sensitive external-standard reference:
1. All connect to stable topics without inconsistent prose in popover vs docs.
2. Warning displays grounded affected object, severity, evidence, impact, corrective action, verification status and knowledge link.
3. Switching label density preserves object selection, typed drafts, focus and diagnostic readability.
4. Mobile touch help works without long-press; desktop hover/focus and keyboard F1/Escape work; links in help popup remain accessible.
5. Change project default language never mutates existing track language; change application density never changes MKV output.
6. Expanded settings and help remain useful even when all transient tooltips are disabled.
7. Validate 390/768/1024/1440 widths, 200% zoom, screen reader names, color contrast and icon recognizability.
8. Versioned docs reference actual implemented behavior, not future design proposals.

## Prior art and evidence limit

- https://www.nngroup.com/articles/onboarding-tutorials/ (layered contextual help)
- https://www.nngroup.com/articles/icon-usability/ (icon-only ambiguities; visible labels are important)
- https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html
- https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/
- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- `/mnt/data/ASS-Workbench-Android_UI宪法_替代版_2026-10-01.txt` observed principle: learning/professional presentation hybrid keeps concepts visible and explanations on-demand; no unvalidated Canonical update.

No code change or visual validation is claimed. This does not promote an assistant design recommendation to a UIGS Canonical rule.

## QHE desktop/tablet Figma design instance (2026-10-16)

Owner supplied reference screenshots reiterating the four icon categories and regional Standard/Compact/Auto label density, then requested an improvement of the existing QHE Figma designs. This is an instantiation of the contract above, not a newly invented or Canonical rule.

Updated the same eight desktop/tablet frames in Figma file FPHdsXxN7xNniLKjZQcVKd, plus static interaction sheet node 16:470. Added source-matched library object/action icons, six toolbar variants (Standard/Compact × Default/Focus/Disabled), and five status variants (Verified/Warning/Blocked/Unknown/Running). Toolbar Label and Icon swap properties retain semantic action identities when visual labels are hidden. Unknown/unconnected uses a neutral question-circle; explanations use Info; warnings/blocks use their own shapes and visible actionable text. Real filenames, track identities and parameter values remain visible. Tablet secondary operations move under More, and object metadata uses two lines when necessary.

The interaction sheet depicts Standard/Compact/Auto presentations, focus-name tooltip, touch help behavior, missing-font warning and blocking corrective action. These are static design states and specifications; screen-reader semantics, keyboard transitions, adaptive settings persistence and actual runtime interactions are NOT implemented or tested by this work. No product runtime files changed.

All eight screens and the interaction sheet were visually reviewed; Figma auto-layout frame-child bound checks returned zero horizontal overflows. Main work area starts at y=176 on desktop/landscape tablet and y=168 on portrait tablet (design coordinates). This is canvas geometry evidence, not measured usability, physical-device evidence, WCAG conformance, or proof that an arbitrary user recognizes every icon. Earlier proposal's no-visual-validation statement describes the original 2026-10-12 checkpoint; this update adds only static Figma visual evidence. Runtime acceptance tests proposed above remain open. No Canonical promotion.
