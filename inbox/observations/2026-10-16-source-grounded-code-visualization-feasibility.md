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

## Implementation experiment — Code Atlas PR #38 (2026-10-16)
The user explicitly authorized bounded implementation of UIGS-integrated browser code observation and permitted context-dependent scope expansion. This is **execution evidence**, not promotion of the proposal.

- Submitted read-only Code Atlas work in [UIGS-Foundry PR #38](https://github.com/11576865/UIGS-Foundry/pull/38), head `39b08babaaf5a889200a5368c217bfeabbab516c` at submission.
- Python AST indexer generates file and symbol nodes, static import/call relationships with source lines, and explicit unresolved-call and parse-error counts; unverified dynamic calls are not presented as confirmed edges.
- Browser UI supports navigation and source inspection; dedicated tests include shadowed import names, nested-function attribution, syntax failures, same-tool self-index, and cross-file UIGS epistemic graph evaluation.
- An offline standalone HTML export and CI artifact path were included to reduce deployment prerequisites.
- Local isolated tests and Chromium smoke checks were performed, but this does not substitute for GitHub Actions on the complete repository. At the first immediate read, `Code Atlas Source Observation` and `Validate Foundry` were **in_progress**.
- The current accepted scope is Python static analysis, no runtime trace, no multi-language semantic coverage, no autonomous correctness assertion; all source authority remains in the product repository.

**Review gate:** confirm CI and real source edge assertions independently before considering the code observer validated; then assess false positives and update cost. Do not create a new knowledge family or promote existing Candidate/Observation to Canonical based solely on this change.

## Follow-up — 2026-10-16 bounded false-positive gate
In Code Atlas PR #38, a concrete static-resolution defect was identified with an adversarial corpus: 'from foreign.api import run' could be falsely linked to a repository-local 'api.py' (dotted-import basename fallback). Module-name collisions also caused a missed correct link: top-level 'api.py' ceased to resolve when 'pkg/api.py' existed. Local/module-level rebinding, local imports and exception-handler shadowing may cause false positive call edges unless conservatively handled.

A bounded source-reference checker explicitly asserts 3 known positive and 9 forbidden negative synthetic relationships. It also checks three source-inspected Foundry edges on a full checkout. Local partial-checkout results: 3/3 positive and 9/9 forbidden edges passed. Full-checkout CI is Pending on PR #38 at commit 12d0da4b834935fff8a3d112694fd834cf1760e5. The fixture pass counts are NOT general precision/recall, and do not establish dynamic runtime behavior.

Reusable Candidate only: source-code observability needs falsification tests for false edges, not merely proof-of-existence examples. The separate Foundry baseline validation issue arises from already-present Bug markdown lacking Lifecycle fields. No unsupported lifecycle states were invented. No change to Canonical authority.
