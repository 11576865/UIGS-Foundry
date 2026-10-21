# Candidate — Semantic icon roles + contextual density in dense desktop workbenches

Date: 2026-10-21
Status: **Candidate with editable Figma evidence; owner acceptance Pending**
Origin: User-supplied screenshots of earlier U-I-G-S design reasoning, adapted to HSR Voice Archive Builder experimental UI.
Artifact: [HSR Experimental Figma Design](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx)
No product source code modified, no Canonical promotion.

## Source proposal and product-specific interpretation

User-provided screenshots distinguish four mutually non-interchangeable icon roles:

1. **Object**: audio, video, subtitle, attachment, chapter, tags (a thing; never itself an action).
2. **Action**: add, inspect, extract, save, compare, render, verify, play (an executable verb).
3. **State**: verified/succeeded, warning, blocked, unknown, checking/running (observed/derived outcome, not command).
4. **Explanation**: help, context explanation, documentation (explain terms/rules, not “unknown”).

Examples of semantic distinction: `Action/Verify` is a shield action while `State/Verified` is a success-circle result; `State/Unknown` must not reuse `Explanation/Help`. `Action/Render` is separate from both verification action and verified state. A small warning triangle conveys that something needs attention, not the complete explanation, and must expose human-readable cause/next step.

Density is task-context-sensitive, not one global icon-only preference:
- **Standard toolbar**: icon + visible verb for discoverability, especially infrequent or high-risk actions.
- **High-frequency compact toolbar**: icon-first can be tested only with meaningful tooltip, keyboard focus name and assistive label; the static Figma mock is not evidence these behaviors exist.
- **Data/resource rows**: filename, track name, language, value, object identity and blocking evidence remain visible; icon is supplemental.
- High-risk confirmations still require explicit wording even when an icon is present.

## Figma integration and evidence

- Native, editable 24px SVG-vector icon component inventory: 22 role-distinct base icons (21 icon families + separately created Verified) plus `Action/Render` and contrast-only `Action/Render-onAccent` variant, totaling **24 vector icon components**. Existing semantic color variables are reused.
- Added one [semantic grammar and density design board](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx?node-id=17-14), with the four icon categories and three toolbar/data density examples.
- Added two reusable semantic `HSR/ActionButton/IconLabel` component variants with editable `Label` and `Icon` swap properties. Applied to the [HSR Subtitle Studio](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx?node-id=2-42) so fast inspection, real ASS rendering, effect playback, and style saving have distinct action symbols **while retaining visible labels**.
- Applied outcome/status icons to Archive source and output health, proofread draft state, unverified libass evidence, delivery audio/subtitle staleness and verified MKV. Added contextual explanation icon by evidence receipt and an audio object symbol to the WAV panel. Original body labels and verification distinctions remained.
- Figma screenshots were inspected; during QA the data density specimen had unintended white auto-layout backgrounds (removed), and an action-render blue icon became invisible against the accent-blue button (replaced by dark-on-accent vector variant). Last screenshot of Studio and Delivery confirmed contrast correction; this visual QA is **not a user interaction acceptance test**.
- Main source `11576865/HSR-Voice-Archive-Builder` and legacy UI are untouched.

## Distinct reusable candidate and deduplication

Foundry search for `图标语义`, `图标密度`, `icon semantic`, `icon-only action` located existing relevant records, notably:
- `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md`: visible primary actions and semantic recognition in dense UI;
- `inbox/candidates/2026-10-12-single-source-contextual-help-and-settings-scopes.md`: contextual help and setting authority;
- `inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md`: contextual specialist commands and visual hierarchy;
- `inbox/observations/2026-10-21-hsr-task-domain-ui-ia-research-before-layout-selection.md`: the specific HSR redesign experiment.

This Candidate is **not** another generic “icons are useful” note. Distinct, falsifiable contribution: semantic role should be an explicit type dimension independent of density/size/color, verified with a concrete render-vs-verified action/state split, and tested at three contextual densities.

## Pending acceptance

- No prototype is wired: icon-only tooltip, keyboard behavior, accessible names, high-risk confirmation, focus order, and assistive technology behavior remain unimplemented and untested.
- Desktop screens only; tablet/mobile breakpoint/geometry acceptance not assessed in this change.
- No measurable task completion, confusion rate, or user preference evidence; owner must review Figma and compare icon-label vs icon-only for repeated tasks.
- Do not infer colors alone encode state; label and evidence are authoritative.
- Preserve native project source and prior HSR UI until an independently approved implementation and regression plan exists.

**Decision:** Candidate only. No automatic Canonical modification.
