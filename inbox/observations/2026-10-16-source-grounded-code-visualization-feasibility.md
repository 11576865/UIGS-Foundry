# Observation: Code visualization must be source-grounded and gated by a minimal execution trial

Status: Observation / unvalidated method proposal (not Canonical)
Date: 2026-10-16
Source: User feedback in the U-I-G-S project conversation about AI-generated code implementation diagrams.

## Direct observation
User rejected a five-diagram, Mermaid/YAML/SVG/Figma workflow as too crude and cumbersome, with unknown real-world execution success. This is explicit user feedback on proposed engineering workflow, not evidence that a replacement visualization tool works.

## Narrow reusable lesson
For AI-maintained, poorly understood codebases, attractive diagrams can create unjustified confidence. Before promoting any visual code atlas workflow, require a bounded proof of feasibility on one existing UI action or bug. Use actual repository entities and source locations as node provenance; clearly separate statically observed edges, dynamically observed behavior, hypotheses, and missing evidence. Figma visual polish does not validate execution semantics.

## Proposed trial (not implemented)
1. Select a single existing, reproducible flow.
2. Trace actual source entry points, state owners, side-effect triggers, and corresponding tests; use runtime traces where needed.
3. Generate one editable, navigable map directly from evidence, with clickable source anchors; do not require manual maintenance of multiple DSL intermediates.
4. Independently verify every displayed path and owner against the exact commit, then try updating after one narrow code change.
5. Abort broad rollout if graph correctness, usability, editable output, or update effort fails acceptance.

## Evidence and limits
- Evidence: user's reported friction and lack of confidence in execution success.
- Unverified: any automated Figma/code-map integration, visual design, runtime trace fidelity, and reduction in regressions.
- No architecture canonicalization or code changes authorized by this observation.

## Follow-up — browser-native interactive code map
The user proposed making the visualization itself an interactive browser page rather than routing intermediate DSL drawings through Figma. Working hypothesis: a web application with a repository index and evidence-backed graph, navigable from UI actions to source code, state writes, execution traces, related tests, and failures; Figma remains the UI design tool, not the implementation-map runtime. Source indexers and runtime observations are distinct evidence sources. Cross-language dynamic calls and implied state ownership must remain explicitly unknown where unverified. Start with one flow and test node/edge accuracy and update cost before expanding. This remains an unverified Candidate-level design hypothesis, not an implemented system or Canonical rule.

## Follow-up — UIGS integration and reflexive self-observation
The user asked whether browser-native code visualization should be integrated into UIGS and whether the analyzer should analyze its own implementation. Architectural assessment (proposal only, not yet implemented): integrate as a UIGS observability/inspection capability and browser-facing workbench, while keeping product repositories authoritative and preserving Foundry's Claim/Evidence control-plane role. Reuse existing architecture precedent `ARCH.SYSTEM_GRAPH_INTEGRATION` (from Character-Voice-Service's real system graph) for stable identities, ownership, runtime dependencies and provenance; do not equate that domain/runtime system graph with a source-code call/dataflow graph.

Proposed reflexive acceptance criterion: the tool's own repository, analyzer adapters, generated graph, UI components, and tests must be indexable by the same general process and visibly marked with identical evidence limits. Self-indexing/self-observation is distinct from self-validation: run independent parsers, build/tests, runtime instrumentation and external or human checks to prevent circular self-certification. Avoid circular authority where a self-generated graph claims its own correctness without external evidence. Graph freshness is pinned to commit/runtime versions. Missing/unsupported edges must remain unknown. Begin with a narrow source-grounded graph, not a second independent governance product or an unbounded rollout.

Observed evidence is the user's design question and the prior-art documents; feasibility, accuracy and usefulness remain unverified. This addition does not change Canonical rules or executable product code.

## Local feasibility result — 2026-10-16 (not merged into product)
After checking the live UIGS-Foundry tree and its actual Python files, a single-file static HTML browser prototype was generated as a conversation-local artifact and smoke-tested with headless Chromium. It displays a narrow UIGS self-observation slice pinned to repository commit `a56e43fa9d2a9dc11b1e8398a9f39654966e5ee3`, comprising 15 nodes and 14 source-checked relationships between Claim/Evidence/Change inputs, `evaluate_epistemic_graph.py`, `generate_validation_missions.py`, tests, a scheduled workflow, and derived report artifacts. Browser smoke test confirmed DOM node/edge counts, node selection and source link changes, search, zoom, and absence of reported page JavaScript exceptions at desktop and mobile viewport sizes.

Critical limits: hand-curated graph data rather than a working automated source indexer; no dynamic trace collection, no CI run verification, no graph relation precision/recall benchmark, and no live deployment. Browser success establishes only that the visualization mechanics can run, not that a general code understanding system works or self-validates. Product repository source files were not modified.

Next go/no-go gate: extract the exact same slice automatically from a pinned checkout and compare to the hand-checked reference; handle false positives/unknown edges explicitly. Do not promote this approach or add an entire standalone governance stack until this gate is passed.
