# Observation: attractive UI references and specs do not guarantee implemented Android visual quality

Date: 2026-10-13
Status: Observation / direct owner feedback + design-process hypothesis; no pixel-level diagnosis yet
Product: 11576865/ASS-Workbench-Android
Scope: UI design-to-implementation fidelity, evidence and acceptance

## Owner correction
The owner expressly rejected the explanation that ASS progress and interface dissatisfaction came from an ongoing expansion of UI variants. The stated problem is that GPT can search attractive UI references, draw attractive concepts, understand design language and cite good examples, yet repeatedly fails to deliver a genuinely good implemented application interface.

Treat this as a user-reported product quality gap, not as evidence of scope creep, a specific Compose rendering defect, or objectively proven aesthetic ratings.

## Distinct failure boundary
Reference screenshots/concept art, layout specifications, Kotlin/Compose component behavior, captured production surfaces and actual on-device experience are distinct deliverables. Correct Compose compilation, semantics-tree interaction tests, screenshots existing in an evidence registry, and user-visible visual quality are **not interchangeable** claims.

The suspected missing operation is a closed visual iteration loop using the exact implementation: render the current SHA with representative content and device metrics; inspect side-by-side against task-specific reference/design intentions; identify concrete hierarchy, density, typography, alignment, whitespace, affordance, and focus/IME differences; modify implementation; recapture and repeat. This causal hypothesis requires verification against actual screenshots and code.

## Recommended bounded experiment
Choose ONE actual ASS production screen and 2-3 representative states (working video/subtitle, tool/inspector editing, compact with IME, tablet/landscape as appropriate). Freeze task, baseline, viewport, text scaling and expected information hierarchy. Record exact SHA and screenshot/recording evidence. Produce an issue list with actionable discrepancies, not vague adjectives. Review successive actual product captures, including navigational and content density tradeoffs; accept only after direct visual and user/task review. Use pixel/visual regression for unwanted change, not as a substitute for judgment.

Success indicator: explicit visual issue closure plus task access; do not count number of mockups, redesign PRs, generic screenshot captures, or CI green as aesthetic acceptance.

## Foundry deduplication
Queried code search for 'visual fidelity', 'screenshot review', 'UI design implementation', 'visual regression'.
Related but not equivalent:
- inbox/cases/2026-10-11-qhe-functional-ui-rebuild-low-copy-workbench.md: actual QHE spatial priority and hierarchy lessons.
- inbox/observations/2026-10-11-mkv-billboard-displaced-first-action.md: MKV first-action visual defect.
- inbox/candidates/2026-10-02-automated-production-visual-evidence.md: automated capture evidence.
- domains/interface-grammar/showcases/README.md: evidence tiers and visual baselines.
Those do not specifically record this direct ASS owner correction that design fluency cannot be inferred to deliver visual quality and the requirement to assess actual implementation against design.

No Canonical change or repo UI modification is authorized by this observation. Do not present the hypothesis as a root-cause diagnosis until screenshots and rendered states are audited.
