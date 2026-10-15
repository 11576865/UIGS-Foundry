# Observation: Softmux concept UI failure — backend capabilities were promoted into primary user navigation

Date: 2026-10-15
Status: Observation / design-output critique; no product code change, no acceptance evidence
Product: 11576865/MKV-Fast-Muxer
Context: user requested tablet-only concept UI layouts exposing all eventual user-accessible capabilities, including not-yet-implemented ones, with correct placement and ownership rather than visual polish.

## Direct user correction

After multiple assistant-produced concept images and a 9-frame Figma rough draft, the user challenged the result: "你是不是把后端功能都当成前端入口了？" The critique accurately described the failure. The screens promoted technical implementation and evidence mechanisms into standalone user destinations or large explanation cards, rendering an implementation taxonomy rather than an operable media workbench.

Examples of invalid direct promotion:
- FFprobe readback and separate V1–V5 verification tiers as always-visible feature pages, instead of detailed evidence behind output/diagnostics for a concrete artifact.
- JobPlan freezing, BatchRunner stages and Blob lifetime as conceptual top-level UI actions, instead of review/execute/manage-result commands and observable status of a selected job.
- EBML, CRC, SeekHead and UID relationship maintenance as primary UI destinations, instead of advanced fields in the relevant container/object inspection context.
- HarfBuzz and libass implementation specifics as unrelated main screens, instead of user-configurable font policy, contextual preview, validation and optional advanced diagnostics.

## Boundary that the failed design crossed

Distinguish four layers before layout:
1. Domain/implementation capabilities: algorithms, internal identities, plans, stages and executors.
2. User jobs: assemble a target MKV; inspect, extract or modify a supported object; subtitle-and-font delivery; review/execute a batch; inspect/save actual artifacts.
3. User commands and contextual controls: add/keep/exclude/reorder, per-track flags, preview, inspect font dependencies, preflight, mux, save, inspect evidence.
4. UI presentation: one dominant output-composition object or batch task matrix; selected-object/job inspector; optional source drawer; fixed action/status region; progressively disclosed details.

“All eventual UI entry points must be present” does NOT imply one top-level tab/button/card per backend module or every future control simultaneously visible. Required capabilities can be navigably available from relevant objects, menus, diagnostics, or future-disabled contextual affordances. Group by user task, not by internal architecture. A backend algorithm with no user-level decision, command or review need should have no independent UI entry.

## Observed failure and needed validation

The generation produced an explanation-heavy, repetitive navigation hierarchy and too many separate pages, even after previous guidance called for composition-first tablet two-area layout. Before accepting a future mockup, perform an entry inventory with columns: user goal; owning object; visible or contextual command; UI home; required state; evidence/implementation dependency; implemented / restricted / planned. Require a realistic path such as 'add ASS → select prospective subtitle track → set language → inspect font issue → preflight → mux → view evidence → save' to occur without routing through standalone diagnostic module pages. Match the 2026-10-12 product decision and 2026-10-13 tablet proposal; inspect actual screenshot flow, not just whether the labels are all present.

## Dedupe / authority boundary

- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` already establishes output-composition as primary object and observes card-heavy UI, but this note records the later *concept design* failure caused by direct backend-capability-to-navigation mapping.
- `inbox/cases/2026-10-15-softmux-1014-e2e-green-visual-hierarchy-rework.md` addresses a code-backed visual hierarchy error despite green E2E, whereas this observation concerns unimplemented image/Figma proposals, not production regression.
- `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md` addresses product domain scope and tool authoring boundaries.

No Canonical change and no claim that a corrected mockup has passed review.
