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


## 2026-11-04 — Native ASS preview follow-up (PR #239, pending exact-head CI)

**Product commit:** [`ada99f76`](https://github.com/11576865/MKV-Fast-Muxer/commit/ada99f76cbe969d644cd3ed9946a8740c88fabe7), still on Draft PR #239; V3-only and unmerged.

New bounded integration: a user selects a *real, primary, scanned ASS/SSA source track* within V3-05 before any target document exists. The new `softmux:v3-preview-source` intent is accepted by the existing source/preview owner only if the imported resource key, exact File reference, active source, scanned source and native embedded-preview stream index all match. A forged same-metadata File cannot inherit permission.

The actual existing `#sf14PreviewDrawer`, preview select/time/image/status controls and FFmpeg/libass renderer are **moved rather than copied** into the V3 source object inspector. Closing the inspector or changing the source restores the original DOM. Preview does not grant output membership, create a plan, or claim a mux result. Unsupported ASS+font cross-source **addition** remains gated separately.

A new isolated Chromium scenario generates a real ASS-bearing MKV and asserts native image rendering, exact original preview singleton, forged-File refusal, unchanged source SHA-256, and absence of target/mux authority. At the time of this entry CI was **in progress**: [V3 #41809258342](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41809258342), [Browser E2E #41809258174](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41809258174), [S12 #41809258307](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41809258307). No new pass claimed.

**Knowledge decision:** This continues the same source-selection-before-authority Observation and already-known single-authority DOM rehosting patterns (see `inbox/cases/2026-10-15-softmux-figma-semantic-ownership-and-entry-contract-gap.md`). Keep this as follow-up evidence rather than a new Candidate or Canonical modification. The fixture has no embedded fonts and does not prove complete preview font closure, ASS extraction UI, complex target transfer, pixel fidelity or touch accessibility.

 
## 2026-11-04 — V3-05 source ASS Stream Copy extraction follow-up (PR #239)

**Product commit:** [`40db4fef`](https://github.com/11576865/MKV-Fast-Muxer/commit/40db4fef72b1f3c1723848561767d6b65b24f32d), Draft PR #239 (not merged). **Exact-head CI pending at intake**: [V3](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41814198690), [Browser E2E](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41814199074), [S12](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41814198749).

The same selected source ASS/SSA object now offers an actual `提取 ASS（不含字体）` action. The transient UI request `softmux:v3-extract-source` is checked against the imported resource key, exact current `File`, active/scanned `File`, native stream index and ASS/SSA codec, then dispatched into the original `extractOriginalTrack(index,'native')` executor. That existing executor handles Stream Copy, independently probes the generated file, performs `auditExtractedOriginalTrack`, computes SHA-256, and publishes original download/report links; no second data/model or writer permission exists. The original `#originalTrackExtractionPanel` is temporarily rehosted in the source sheet, returning to its previous parent when the source selection is dismissed.

The real-browser V3 ASS fixture was extended with a forged-`File` rejection, actual `.ass` download, independent native `ffprobe`, extracted byte hash/report agreement, negative output-target assertions and unchanged original source hash. **Assertions are code submitted, not pass evidence until exact-head CI is green.** The generated native ASS stream includes neither fonts, Chapters nor global Tags. A native ASS extraction cannot prove absolute source-container timing equivalence or complete cross-MKV ASS+font transport.

**Dedup decision:** append to this prior Observation, which already covers source-object selection, exact identity and native preview; older `inbox/cases/2026-10-15-softmux-figma-semantic-ownership-and-entry-contract-gap.md` covers single DOM owner/rehosting. This is a bounded product Case extension, not a new Canonical rule, nor a second Candidate. Scope and Figma visual acceptance remain distinct.


**Executed follow-up (same commit):** [V3 Pilot #41814198690](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41814198690) completed **success** at `40db4fef72b1f3c1723848561767d6b65b24f32d`, including the new real-source ASS extraction/download/ffprobe/report test. Independent Browser E2E and S12 workflows were still running when checked. This updates the exact-head V3 evidence only; it does not grant final Figma or product acceptance.
