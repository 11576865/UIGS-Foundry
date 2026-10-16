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
