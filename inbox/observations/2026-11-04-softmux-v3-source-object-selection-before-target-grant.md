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


## 2026-11-04 — V3 explicit A ASS+font → B integration (CI pending; selected backport)

**Product:** [Draft PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239), first integrated code `0681f21d69876953565fc2e9f2ec8398fa9df661`, correction `59ee3cea76a1ddd70e6bcfaeaf3607c076029c82`. **Upstream bounded source:** [independent Draft PR #233](https://github.com/11576865/MKV-Fast-Muxer/pull/233), `e38c98a7`, with earlier green Node/Browser E2E/S12; neither PR is merged. This is **not** a green claim for the newly integrated V3 head.

The V3-02/V3-05 selected source ASS/SSA object now exposes an explicitly qualified “加入到…（校验 ASS 与字体）” request. Merely selecting the source never authorizes an output. The V3 target picker asks the user to select the real B File. Only under authorized target plan does the existing secondary-source probing and native PR #233 bundle logic run. The selected backport includes `prepareSecondaryAssFontBundle` and its negative tests, actual Stream Copy ASS extraction, attached-font name/face/weight/italic/cmap tests, atomic submission of *both* subtitle and matching font members, partial-failure rollback and revocation on removal of any member or its source File.

**New V3-specific guard:** asynchronous Add-to currentness now also requires `v3MayEditOutput()` for mutation; simply viewing sources keeps independent inspection capability. Returning to source mode while an Add-to runs invalidates pending write authority and should abort/rollback. This is submitted code and must not be described as tested without a real interrupt scenario.

**New browser proof added, pending exact-head CI:** reuses the previously isolated real A ASS+named font/B media fixture, but exercises the V3 selected-source sheet and explicit target picker, downloads the real B MKV, verifies native video/audio packet hashes and PTS/DTS, checks named-font libass rendering, then tries a source A missing embedded fonts and requires zero derived members. Screenshots, final MKV and JSON receipt are captured by the complete Browser E2E workflow.

**Observed test-spec drift and immediate repair:** the first V3 pilot run on `0681f21d` failed **one stale static unit assertion** requiring literal `stream?.codec==='subrip'`, although ASS support had been explicitly added. Product [V3 CI #41836503171](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836503171) had **888/889 Node tests pass** and stopped before build/browser; this was not a runtime media failure. Correction `59ee3cea` updates the assertion to the new allowlisted codec relation while retaining target permission gates. The corrected exact-head CI was running at intake ([V3 #41836813707](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836813707), [Browser E2E #41836813530](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836813530), [S12 #41836813976](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836813976)).

**Deduplication/knowledge boundary:** this extends the existing source-selection-before-output Observation with a new *validated-native-closure integration* and *test assertion drift* instance. Earlier `inbox/bugs/2026-11-03-softmux-cross-source-subtitle-async-intake-race.md` already establishes async source-member reconciliation, and `inbox/cases/2026-10-15-softmux-figma-semantic-ownership-and-entry-contract-gap.md` covers Figma vs real DOM authority. Do **not** create a second generalized Candidate or update Canonical based on this single integration. Figma pixel parity, device accessibility, multiple ASS bundles per source and UID/Tag preservation remain unproven. PR #233/#239 code overlap is a **merge reconciliation obligation**, not independent proof of two successful features.


## 2026-11-04 — WU-05 real derived font-member plan projection and stale source ASS E2E contract

**Product:** Draft [Softmux V3 PR #239](https://github.com/11576865/MKV-Fast-Muxer/pull/239), submitted code `567837b8be343559aec7d4ac7959ea4926295e17`. **Exact-head CI queued at intake**, no acceptance claim.

After the bounded P3 ASS+font closure was backported, exact-head `59ee3cea` passed complete Browser E2E, S12, and Pages, but [V3 Pilot #41836813707](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836813707) failed at the older real ASS preview scenario, line 43: it expected `#sfv3SourceInspectorAdd` hidden, although new capability now permits a *gated attempt* to choose a separate B MKV. The correction tests an actual visible request, explicit chooser, disabled confirmation with only A imported, cancellation, and continued absence of output authorization. This is a change in the capability contract, not evidence that the original native render/extraction had failed.

New code projects `assFontBundles` from the existing `importedAssetEntries` only where real derived ASS/member `embeddedOrigin` matches a real attached font group. The `bound` indicator requires the same actual source `File` still imported, the exact subtitle `File` present in the canonical subtitle input and each exact dependent font `File` present in the canonical font input. The V3-04 `#sfv3AssFontDependencies` view displays source, stream number, actual filename and real font filenames ONLY under an authorized target plan. It does not own a second editor or claim completion: wording distinguishes in-editor membership from mux success, final attachment audit or universal glyph shaping. In a missing-font negative workflow the plan must display no phantom bundle.

This submission adds Chromium positive/negative checks in the existing real A-with-ASS-and-named-font → B test, plus static unit assertions for owner/capability boundaries and responsive CSS. **CI pending, Figma visual parity/touch/a11y/final release not accepted.**

**Intake disposition:** this is new concrete UI evidence for the existing distinction *observed source → proposed target membership → actual delivered output*. Deduplicates against `inbox/candidates/2026-11-01-softmux-resource-document-output-optional-single-surface.md`, `inbox/candidates/2026-10-04-container-inventory-stable-identity-diff.md`, and prior blocks in this Observation. Append here; do not create new Canonical or automatic normative rule.


## 2026-11-04 — V3-04/V3-06 source-bound ASS row state, and E2E prose drift

**Product submission:** [PR #239 `c19b58848f085af5959b91703aaf19e2e8c9c0a3`](https://github.com/11576865/MKV-Fast-Muxer/commit/c19b58848f085af5959b91703aaf19e2e8c9c0a3), still Draft. **Exact-head CI in progress at intake**: [V3](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41850975186), [Browser E2E](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41850975078), [S12](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41850975154). No green claims for this head.

Reviewed approved Figma target frames V3-04 (node `32:2`, 1440×900) and V3-06 (node `35:2`, 820×1180): in both, a source-added ASS subtitle appears as a highlighted row with explicit source and font dependency count. The existing V3 already rendered the *actual editable composition row* and an auxiliary readonly dependency panel, but that row did not distinguish a real, source-bound ASS/font member unless the user clicked it. Code now decorates the original `button[data-composition-id]` ONLY if the matched external `newSubtitleState` `File` is the identical file inside the imported ASS member and its original source is still present and all source-scoped font members are the same actual registered font `File` objects. The row has a V3-only green background and a readable source/font-count note. No second row or new target identity is created. Actual Chromium A→B scenario now asserts positive row and 820/620 in-viewport geometry, while missing-font negative requires zero falsely highlighted rows. This is **semantic and responsive convergence**, not exact pixel/physical-device evidence.

**Red-light repair:** Previous [Browser E2E run #41844741977](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41844741977) at `567837b8` failed after true ASS source/font binding because E2E expected the old literal “待封装与成品审计” whereas the actual UI correctly said “尚未执行最终封装及成品审计”. The test was updated to assert the actual, scope-correct phase; native V3 output download/render had **not yet been reached** on that failing run. An unchanged product renderer cannot be called verified due to earlier green V3/S12 if the required Browser E2E stopped before its final oracle.

**Dedup:** Existing `inbox/bugs/2026-10-11-mkv-e2e-version-assertion-drift.md` already covers brittle literal test contracts and this record already covers single authoritative target vs source. This adds exact source-Font/file identity and target-row visual-state proof as an **Observation** rather than a duplicated general Bug or promoted Canonical rule.


## 2026-11-04 — WU-06 contextual inspector keyboard return and Chromium simulated touch

**Implementation submitted:** [Softmux V3 PR #239 `ae7b4c30f51713d1886924e144c5ce4d35ffe870`](https://github.com/11576865/MKV-Fast-Muxer/commit/ae7b4c30f51713d1886924e144c5ce4d35ffe870). Draft/unmerged and opt-in `?ui=v3`.

Concrete gap: approved selected-object source and target UI had contextual panels, but the source panel did not reliably move focus into its controls, and the target panel always returned focus to the unrelated target tab/dock on Escape or Close rather than the exact composition object that launched it. This loses interaction continuity especially when native composition rows rerender on selection.

Bounded correction: source selection now focuses its one real panel Close, and deliberate dismissal returns to the matching selected source object. Target inspection tracks the initiating *real* `data-composition-id`; open focuses the original inspector Close, while Escape/Close restores focus to the corresponding currently live row even when the previous DOM node was replaced. Dock-opened inspection restores to the dock. Passive source/plan surface changes do not steal focus from newly chosen tabs. Existing editor and `File` authority remain unchanged. V3-only CSS enforces a minimum 44px height for contextual Close/preview/extract/Add, source object selection and the target chooser.

Extended actual Chromium `tests/e2e/v3-responsive-geometry.e2e.mjs` to instantiate `hasTouch:true`, exercise genuine `Locator.tap()` at 820/620 widths and assert the active focus target, Escape and tap-close return, in-viewport sheet geometry, unmodified original source `File`, and one editor/inspector instance. **This is browser touch emulation**, not physical Android/tablet input or screen-reader validation; the assertion is not passed merely because it is authored.

At intake, same-head GitHub CI was **in progress**: [V3 #41855410885](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41855410885), [Browser E2E #41855410546](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41855410546), [S12 #41855410792](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41855410792). Previous `c19b5884` had passed Browser E2E/S12 and Pages; its V3 run had not reported a final conclusion when checked and cannot establish passing evidence for the new commit.

**Dedup/authority:** append to this existing source-object-selection Observation, and cross-check earlier `inbox/cases/2026-11-01-softmux-candidate-membership-capture-output-identity.md` (focus loss after underlying UI remount), rather than creating duplicate general Candidate/Bug. This remains scoped to V3 product. No Canonical modification. Open: exact-head browser success, assistive technology, physical touch, full Figma pixel comparison, and final product release gate.
