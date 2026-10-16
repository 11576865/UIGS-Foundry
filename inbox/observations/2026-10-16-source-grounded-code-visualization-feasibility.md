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
