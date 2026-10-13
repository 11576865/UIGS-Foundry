# Bug: ASS UI v5 effects prototype is visually interactive but not semantically authoritative

Date: 2026-10-13
Status: Bug / confirmed from delivered offline HTML source; source-level reproductions, not native Android
Severity: High for design-baseline credibility; NOT evidence of native production defect
Artifact: ASS_Workbench_UI_Prototype_v5.html (conversation-local)
Related case: inbox/cases/2026-10-13-ass-v5-temporal-curves-precision-geometry-and-responsive-tools.md

## Observed concrete issues
1. **Wrong Karaoke tag taxonomy.** In `effect()`, a single `effectMode` dropdown permits `k,kf,ko,kt` and the generated token stream is `'\\'+S.effectMode+dur[i]+glyph`, treating all as centisecond syllable durations. Aegisub official current documentation says `\\kt` sets the **next syllable's onset relative to the Event's start**. Unlike `\\k/\\kf/\\ko`, `\\kt` is not a duration variant. Supporting `\\kt` requires a separate time-origin/write model and explicit support limits, not another dropdown option. Source: https://aegisub.org/docs/latest/ass_tags/
2. **Effects UI cannot Commit.** `case 'apply'` only commits Raw draft, event fields and X/Y geometry drafts. It does not serialize/update effect values (Fade/Transform/Karaoke), while the effects pane has a `预览效果` action; `case 'style-preview'` only notifies, no formal effect history or ASS write. The visual edit controls are real demo controls but are not a corresponding ASS document transaction.
3. **Playback mode diverges from edited temporal model.** Scrubbing computes `motionValue` from Fade and `\\t` parameters and updates graph/sample; `.effect-running .effect-result .subtitle { animation:effect-demo-appear 3.3s ease-in-out infinite }` uses fixed CSS keyframes (11%, 42%, 88%, .96/1/1.12), independent of current Fade and Scale X/acceleration. The played visual trend therefore can contradict configured values, even though scrub sample is synchronized.
4. **False temporal affordance and small touch target.** The graph paths are read-only SVG computed lines, but look like an editable graph tool. `.motion-grip` is 12×23px and `.syllable-grip` 11×21px; physical Android dp cannot be inferred from HTML CSS px, but those HTML pointer-hit zones are small for touch. All timeline rows should share one time ruler and enable accurate coarse/fine handles.
5. **Static blur mixed into time lanes.** The `Blur / \\blur` row presents a static, untransformed 2.0-value as if it occupied a dynamic time track. Separate static base properties from actual time-dependent effect curves; if `\\blur` is transformed through `\\t`, show that property as animated instead.
6. **Model input constraints look like ASS validity.** `scaleEnd` is hard-clamped 50..250 and accel allows only 0.5/1/2 presets, with no custom numeric input. Those can be convenient default manipulation windows but are not the full ASS parameter domain.

## Required fix contract
- Formal authoring model: source token/override scope; Event-relative times; explicit target; partial/unknown token preservation; reversible preview/commit history; renderer-backed sample and compatibility status.
- Separate UI animation transitions from ASS-authored animation preview. Do not run an unrelated looping animation after a change; playback samples from same selected temporal model as scrub and numeric fields.
- Add `\\kt` as explicit onset-offset construct or leave unsupported in an acknowledged partial-scope section, never serialize it as a duration.
- Present graph as read-only visualization until drag/edit is implemented and acceptance-tested; meaningful touch zone independent of narrow visual grip.
- Add tests: edit parameter→seek→play at sample timestamps; apply→Undo→Redo; source token preservation; `\\kt` versus `\\k`; static vs animated blur presentation; gesture capture cancellation; invalid and out-of-range numeric inputs.

## Evidence and boundary
This is a review of the exact shipped offline HTML. The 105/105 and 35/35 earlier browser smoke checks did not cover these domain-semantic requirements. This Bug does NOT establish problems in `11576865/ASS-Workbench-Android` Kotlin engine.
 
## Dedupe
Foundry searches for 'ASS kt karaoke semantic start time versus duration', 'effect prototype UI animation preview diverges from parameter', 'slider inspector mixed temporal scrub motion', 'UI domain state vs visual graph editing' returned related interface evidence and v5 Case but no prior Bug enumerating these observed faults.
No Canonical change.
