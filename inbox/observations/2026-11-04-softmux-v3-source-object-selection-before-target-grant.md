# Observation: Source-object selection is a reversible observation state, not output authorization

Date: 2026-11-04
Status: **Observation / code submitted; exact-head CI Pending; not Canonical**
Product: [Softmux V3 Draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239)
Implementation commit: `8d6d4dc8fcc133409b15a9370631c7aa093c4a60`
Design authority: approved Figma V3-05 (`33:2`), V3-02 (`30:2`).
Scope: UX observation, interaction contract, regression design. No release acceptance claim.

## Trigger and observed gap

The frozen 820×1180 V3-05 Figma frame explicitly shows a selected source ASS object with its own contextual bottom sheet. The prior production-branch V3 source list had a directly executable “加入到…” action but no intermediate *source object selected* state. Although the real SubRip A→B mux path had already passed Chromium, that success did not validate the designed *observe → select → inspect → decide whether to act* interaction.

## Bounded implementation submitted

- The existing exact-`File` source registry still owns imported resource identity. `#sfv3SourceInspector` presents the selected row's observed title, source file, group, and real stream detail without creating a writable shadow object or an output plan.
- Source row selection is keyboard accessible and exposes `aria-expanded`. Close/Escape dismisses the sheet and restores focus; source tab changes and stale source removal revoke the transient selection. 820/620 sheets have viewport-bound regression assertions.
- A supported SubRip object's contextual “加入到…” opens the *existing* explicit target picker and continues through existing writer/authorization code; cancellation remains no target. Unsupported ASS+font cross-container capability cannot be advertised as verified; no Preview/Extract success is fabricated.
- Chromium source-selection, cancelled target, actual A SubRip→B output, responsive geometry and keyboard regressions were **added to tests**. At submission their new exact-head execution is **Pending CI**.

## Reusable distinction (provisional)

A source *focus* or *selected object* is neither (a) permission to edit an input nor (b) a target-output membership grant. Functional end-to-end tests can pass while a required intermediate selected-object UI state is missing. Treat each approved transition as an independently testable contract: **source observed → source object selected → optional action capability verified → explicit target intent → execution result**. Actions must be gated by actual engine capability and ephemeral source identity, not merely an attractive state in static Figma.

## Dedup and evidence limits

- [Read-only source inspection candidate](../candidates/2026-10-02-read-only-source-inspection-must-not-inherit-downstream-gates.md) already establishes upstream inspection independent of downstream prerequisites. This Observation adds a specific *selected-object interaction/state parity* failure, not a duplicate general principle.
- [Optional-output resource/document candidate](../candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md) already separates source focus from output membership. This record adds an actual approved Figma→branch implementation/test trace.
- [Flat observation to bounded writer observation](2026-10-17-softmux-flat-observation-to-bounded-writer-tool-identity-gate.md) already separates navigation identity and write permission. This record is limited to interactive read-only selection before the target picker, not EBML writer re-inspection.
- [Single-source contextual help candidate](../candidates/2026-10-12-single-source-contextual-help-and-settings-scopes.md) covers explanatory topic ownership; this record does not establish a unified HelpTopic system.

**Not proven:** exact Figma pixel match, complete ASS/font closure, independent source Preview/Extract, physical device accessibility, final exact-head CI or production release. No Canonical change authorized.
