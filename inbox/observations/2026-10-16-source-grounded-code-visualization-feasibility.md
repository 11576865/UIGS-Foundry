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

## Runtime observation implementation — 2026-10-16

- Implementation: [Code Atlas PR #38](https://github.com/11576865/UIGS-Foundry/pull/38), experimental opt-in `tools/code_atlas_trace.py`, distinct runtime edge type `python_profile_observed`, revision/repository gating, bounded event collector, browser display.
- Evidence: [Code Atlas Source Observation run 38886009409](https://github.com/11576865/UIGS-Foundry/actions/runs/38886009409) completed successfully at PR head `f88628ef6a00c28e1cb007249eeb58461d5de28e`. Two sets of six local/CI contract tests passed, including observed call attribution and hook restoration.
- Scoped real run: `tools/test_epistemic_graph.py` produced 11,742 Python profile calls, 62 unique mapped call-site edges, zero unmatched edges in this sample, and no event truncation; the graph was pinned to a verified commit SHA. The static index reported 60 parsed Python files, 381 nodes, 722 static edges, and 2,905 unresolved static call sites.
- Important negative result/boundary: 62/62 matched in this chosen test run does NOT measure call-graph precision/recall across the repository. Over 11k profile events were outside source-to-source mapping; C calls, existing threads, subprocesses, Kotlin/JS, and unexecuted paths remain outside coverage. This does not prove the profiler or software correct.
- Reuse: opt-in runtime evidence should remain visually and semantically distinguishable from AST-inferred relationships. Evidence must be version-bound and mismatched revisions rejected. This reinforces established UIGS provenance and evidence-precedence principles rather than creating a new Canonical principle.
- Foundry-wide `Validate Foundry` still fails on pre-existing Bug records missing `Lifecycle:`; this must not be attributed to the Code Atlas collector or remediated by invented lifecycle states.

## Explicit operation correlation — 2026-10-16

- Implementation submitted in PR #38: explicit `contextvars` operation boundaries and bounded event annotations (`action`, `state_write`, `side_effect`, `checkpoint`), correlated with actually observed Python calls via operation IDs; parent-child operation spans and asyncio inheritance tested. A safe `code_atlas_causality_demo.py` fixture avoids effects outside the process. Browser inspector and CI demo were added in the same work unit.
- Falsification insight: Python profiler captures the instrumentation functions themselves; these must be excluded from operation-specific business-call attribution to avoid drawing observer-internal calls as observed product behavior. Baseline static and general runtime evidence retain their separate meaning.
- Evidence: 11 local Python tests passed in a synthetic fixture and a separate CLI demo yielded four annotation events and one business call-site relationship. These counts are deliberately scoped and not a project-level accuracy metric. Submitted implementation at PR head `57985f480fe36b4b45bc4fdea584fa4213098db7` before this observation; GitHub CI for that head was not yet available at the immediate status check.
- Semantics: a `state_write` or `side_effect` annotation is an instrumented program's declaration, **not** independently observed mutation or causation. Missing, truncated, or uninstrumented events remain unknown. No CI result, runtime probe or browser mock proves that a reported state change occurred. No Canonical promotion.

## Bounded state snapshot evidence — 2026-10-16

In Code Atlas PR #38, an experimental state probe was added in `tools/code_atlas_causality.py` with a safe example, unit tests, and a browser-inspector distinction. Unlike an unverified `state_write` annotation, a probe independently compares a *caller-selected* JSON-serializable value before and after an explicit operation; its exported result is `changed`, `unchanged` or `unknown`, never the raw value. Error/oversize paths yield `unknown`. Probe callbacks may have their own side effects and must be safe and deterministic; even a real observed difference does not demonstrate causation or completeness.

Implementation head at feature submission: `33b11906872ec6f1b2408b1ffe358effbe8fec18`. Scoped local evidence: 16 Python tests passed and JavaScript syntax check passed. Browser E2E was attempted but Chromium navigation and scripted page loading were blocked in the current environment; full UI acceptance is **Pending**, not passed. CI after this submission is independent and must be reviewed when available. No Canonical rule was modified.


## Browser evidence visibility regression / independent E2E gate — 2026-10-16
- Direct defect: Code Atlas narrow-width CSS hid all .rels sections, including the operation-evidence inspector. The trace JSON can be present yet its proof invisible to the user.
- PR #38 remediation: keep the inspector relation sections usable at small viewport sizes and add independent Playwright/Chromium tests at 1440x900 and 390x780. The E2E fixture is synthetic; a browser pass only proves interactive presentation, not the reality of any declared state update.
- Evidence: change submitted in feature branch in commit 1df017b44cb3de909315c807afb344be0e2ecbc4. Local Chromium blocked file and localhost navigation, so local UI E2E is not claimed as passing; exact-head CI remains pending.
- Reusable check: an observability product must test evidence *reachability* in supported layouts, not merely the collector's JSON. Do not promote one finding to Canonical.

## Selected-file effect observation / content witness — 2026-10-17

- Reusable observation: an opt-in, selected-file before/after witness can distinguish created/modified/removed/unchanged/unknown by bounded content comparisons without exporting raw bytes, digest, absolute path or probe error text. `unchanged` means same observed bytes within the probe, not metadata identity or global immutability.
- Context: code atlas operation tracing previously recorded `side_effect` only as a software-supplied annotation, not measured I/O. File sampling is separate measurement evidence but still cannot demonstrate causal responsibility for a write.
- Implementation on Code Atlas PR #38: `tools/code_atlas_causality.py:observe_file`, scoped Python tests, temporary fixture, correlated real Python call trace, and explicit browser evidence label. Probes reject direct symlinks/nonregular/oversized files as unknown; a 1-MiB per-snapshot cap and bounded event count apply.
- Important residual limits: caller-selectable subject labels can contain identifying information; symlinked ancestor directories, file access-time changes, concurrent writers, child processes and other unselected files are not universally characterized. Treat the evidence as local to the specified file; report `unknown` when a safe sample is impossible.
- Verification scope: code and tests were durably submitted to feature/uigs-code-atlas-readonly; last observed successful CI precedes this addition. The new exact-head CI and browser artifacts are Pending at this note. Do not promote to Canonical.

## Comparative runtime evidence and failure capture — 2026-10-17

- Observation / unpromoted reusable method: for AI-run software projects, comparing a good/bad run is only interpretable after aligning repository, pinned commit, selected operation boundary and collector completeness. The first observed divergence is not necessarily the first causal divergence.
- Implemented experimental CLI in PR #38: opt-in failure trace retention (nonzero process exit remains nonzero; exception type only, message omitted), same-revision comparison of instrumented event sequences and call-site counts, conservative input rejection, and CI synthetic positive/negative examples.
- Evidence at submission: source, tests and CI workflow committed through 4fc72b4ec068a8fb06029e2358141a2e05fe3be0. Latest-head CI was not yet checked at this observation. Exact-head external verification remains Pending. No independent real-product fault oracle or browser comparison view is claimed.
- Constraints: identical commit does not imply identical inputs/environment, event time ordering can interleave, and crashes/forced process kills do not produce retained traces. Do not promote Canonical from this bounded exercise.


## Proposed first usable product gate — 2026-10-17

Status: proposed product acceptance hypothesis (not approved, not Canonical, not implementation-complete).
Source: user asked what Code Atlas's first usable deliverable must look like and what problem it should actually solve, after several code-only prototype work units.

The baseline is a browser workbench for navigating **an actual user feature or reproducible failure** from user-facing entrypoint to source anchors and observed behavior, not simply rendering a project-wide function graph. Proposed acceptance gate: (1) select an indexed project/commit; (2) find a known feature/entrypoint and expand bounded multi-level dependencies with real source links; (3) inspect static vs actual runtime vs explicit annotation vs unknown evidence separately; (4) browse two reproducible execution records side by side with a bounded difference list; (5) inspect at least one non-Python product repository beyond UIGS-Foundry; (6) index and inspect Code Atlas's own implementation without granting it authority to certify its own correctness; (7) repeat analysis after a changed commit and make stale or missing evidence conspicuous.

UI proposal: project selector and search, bounded interactive graph at the center, source/evidence inspector on the side, operation/compare timeline underneath. The default view must avoid unreadable whole-repository graph hairballs; no raw state values, secrets or arbitrary repository code execution in the browser. Multi-language semantics need explicit adapters and evidence limits, not unsupported static guesses.

Go/no-go should include actual task usability: a non-code-reading maintainer can locate source of a known feature, explain one confirmed edge and one unknown edge, and differentiate actual run evidence from inference. A bounded real-product failure demonstration plus repeatable checks is needed before presenting Code Atlas as a generally useful engineering debugger. The existing Python-only AST viewer, safe sample traces and synthetic browser CI demonstrate technical feasibility but do not alone satisfy this proposed user-facing product gate.

This is a single-conversation provisional design observation. The user's question is not a final approval of a release contract or scope expansion, and this note does not authorize automatic code changes or Canonical promotion.


## External prior-art challenge to self-built Code Atlas — 2026-10-17

Status: Observation / candidate decision input only. The user expressed concern that the planned atlas would deliver low utility, high use friction and high maintenance. An external source review challenges the earlier assumption that UIGS should build and own a general code graph and browser UI.

Evidence references, as vendor/project claims unless stated otherwise:
- GitNexus upstream: https://github.com/abhigyanpatwari/GitNexus — prebuilt local code knowledge graph, multi-repo MCP/CLI queries, impact analysis, browser. License PolyForm Noncommercial 1.0; not a permissive OSS foundation for unrestricted incorporation. Maintenance risk illustrated by reported indexing/mapping and large-repo issues: https://github.com/abhigyanpatwari/GitNexus/issues/3474 and https://github.com/abhigyanpatwari/GitNexus/issues/2031 .
- CodeBoarding: https://github.com/CodeBoarding/CodeBoarding — MIT analysis engine, layered architecture diagrams, PR architecture comparison, standalone analysis.json and browser; LLM provider setup and language server maintenance required. Generated descriptions remain weaker evidence than source anchors/runtime checks.
- Aider repository map: https://aider.chat/docs/repomap.html — sends ranked concise code context to AI rather than asking human to traverse full dependency graph; important alternative product interaction.
- dependency-cruiser: https://github.com/sverweij/dependency-cruiser — JS/TS dependency validation and CI graph; narrower scope, stronger actionability.
- Existing GitHub navigation: https://docs.github.com/en/repositories/working-with-files/using-files/navigating-code-on-github — symbols, definitions and references with no installed UIGS product surface.
- CodeScene coupling/hotspots: https://helpcenter.codescene.com/articles/1844075-how-to-assess-coupling-health-in-codescene — history-based co-change relationship complements static calls but is correlational, not causal.
- Runtime: https://docs.sentry.io/product/ai-in-sentry/seer and https://opentelemetry.io/docs/languages/js/ — standard error/trace observability; browser OTel instrumentation remains experimental.

Decision hypothesis: pause feature expansion of bespoke graph engine until a side-by-side trial on one Python and one real non-Python repository measures time to useful diagnosis, precision of cited relationships, user effort and maintenance overhead against GitHub search plus a leading existing analyzer. A no-code evidence bridge into UIGS (source commit, CI run, output artifact, test and negative control) may have higher durable value than an owned multi-language visual platform. Do not silently replace previous proposed Beta contract, merge PR #38, import noncommercial code, or promote this single observation to Canonical.
