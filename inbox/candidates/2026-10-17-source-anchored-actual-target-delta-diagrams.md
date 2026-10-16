# Candidate: Source-anchored Actual/Target/Delta diagrams for controlled software evolution

Date: 2026-10-17
Status: Candidate — design method; no new product implementation or empirical validation
Domain: Code comprehension, engineering visualization, architecture migration, change impact
Provenance: User's UIGS discussion of HSR-Voice-Archive-Builder and the actual-vs-ideal relationship.

## User need and distinction

The user wants an assistant not merely to narrate repository source or draw plausible diagrams, but to **correctly comprehend real code** and render both (1) the actual implemented relationships and (2) a simple, precise, comprehensible ideal model. The diagrams must actively support moving existing implementation toward approved goals. Diagrams should be Chinese-primary with English technical terms retained and source identifiers intact.

This is a **three-model requirement**, not a claim that source alone supplies product intent:
- **As-Is / Actual**: commit-pinned, source-grounded implementation graph, distinguishing verified calls, writes, scheduler paths, static inference, dynamically observed events and unknowns.
- **To-Be / Ideal**: separately authored target contract derived from product/user requirements and accepted acceptance criteria; not reverse-engineered as an inevitable property of current code and not silently elevated to Canonical.
- **Delta / Migration**: matched relations classified keep / split / move / remove / add / unknown, with explicit change ownership, prerequisites, compatibility and regression or scenario-based acceptance checks.

A useful diagram is a reasoning/falsification artifact: it should predict which operation updates which state or artifact, what does not change, what is triggered implicitly, and where evidence is missing. A good-looking graph alone is not evidence of semantic correctness.

## Concrete bounded HSR example (source verified, target is only a candidate)

HSR main commit `dea5411312ed3e819864f1915f4f2008f938cba3`: `app/server.py::api_status` (GET `/api/status`) calls `maybe_queue_complete_mkv(config)`, which may enqueue MKV republishing if bundle status/source identity/queue guards permit; `app/server.py::api_output_ass` also offers an explicit command and `app/auto_delivery.py` implements source-generation dedupe/retry/backoff. That means a read-looking status request can participate in write-job scheduling. It is conditional and not every status request causes production.

A **possible, not yet authorized** target separates read-only status-query contract from event-/explicit-command-driven reconciliation, while preserving desired automatic updates and dedupe policy. Delta acceptance would check: status-only polling starts no new jobs; approved update events still produce exactly one valid republish; old verified MKV stays intact on failure; two server runtimes maintain equivalent semantics.

Source evidence:
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/server.py#L1005-L1026
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/auto_delivery.py#L195-L270

## Minimal acceptance of diagram quality

- Every asserted **actual** node/edge has an exact revision and navigable code anchor; unsupported links are unknown, not invented.
- The graph distinguishes invocation, reads/writes, data derivation, async scheduling, and publication verification, using brief Chinese labels and English source terms.
- Each **target** relation has a named intent/requirement provenance, or is explicitly labeled proposal pending confirmation.
- Each delta is testable on one executable user journey, with before/after artifacts and failures tracked.
- The diagrams update after implementation; avoid saying a proposed target has landed until checked against actual code and tests.

## Dedup and authority

Extends `inbox/observations/2026-10-16-source-grounded-code-visualization-feasibility.md` (source-backed experimental Code Atlas and diagram reliability) and complements `inbox/candidates/2026-10-16-hsr-generation-intent-destination-and-preview-defaults.md` (specific HSR user actions/ownership). This candidate adds **As-Is/To-Be/Delta matching as a migration contract**, not another code-indexer proposal. Do not modify Canonical based on this conversation alone. No implementation or measured effectiveness has been established.


## Follow-up — 2026-10-17 external semantic worker when Foundry has no model runtime

**Problem:** UIGS-Foundry and the experimental Code Atlas do not themselves invoke a reasoning model. AST indexing, evidence receipts and browser graphs cannot reliably invent an approved To-Be architecture or interpret cross-domain responsibilities. Do not misrepresent deterministic static analysis as AI semantic comprehension.

**Proposed minimal integration (not automatically installed or authorized):**
- A model-enabled **external interactive agent** (for example, a ChatGPT session with authorized GitHub read/write access) reads commit-pinned product evidence and existing scoped UIGS knowledge, explains uncertainties, drafts bilingual As-Is / To-Be / Delta relations, and requests confirmation for substantive target choices.
- Source files and tests remain authoritative in **product GitHub repositories**. The agent writes a bounded, reviewable report or task/PR artifact with revision, code anchors, relation type, confidence/evidence class, proposed target authority, and acceptance checks. A persistent structured artifact is required for continuity; ephemeral conversation text is not the only copy.
- Foundry/Code Atlas performs **deterministic** indexing, provenance linking, schema checks, evidence validation, graph rendering, drift checks and intake. It neither pretends to invoke the model nor silently promotes Candidate to Canonical.
- CI and workflows may detect that analysis is needed and create a durable **Pending AI Analysis** request, but without an external model invocation mechanism they cannot execute semantic analysis automatically. A user launches/reviews the interactive agent work. Full unattended execution would need a separately authorized model-capable runner/service and credentials; do not silently introduce those dependencies.
- GitHub transport does not establish semantic correctness: enforce a narrow source-linked claim/edge contract, user approval for the target, and one executable before/after regression gate.

**Fit with existing Foundry authority:** `governance/AGENT-EXECUTION.md` already states interactive agents are disposable workers and durable state is Git commits/PRs/task-state; `intake/project-adapter-protocol.md` already provides outbox and Pending handoff; `governance/EPISTEMIC-MODEL.md` keeps source artifacts, Evidence, Claims and knowledge views separate. This is an application of those rules to AI-assisted architecture comprehension, not a new foundation.

**Scope and limits:** No claim of a connected autonomous ChatGPT-to-Foundry daemon, no guaranteed scheduled ChatGPT execution, no product-code changes or deployment, and no new Canonical rule. Pilot one HSR action and validate source anchors and usability before expanding.


## Follow-up — 2026-10-17 owner-readable bidirectional UI-capability map

**Direct product-owner need:** The user cannot make informed product direction or UI decisions because they cannot tell what each button actually invokes, which business outcome it achieves, and which existing capabilities have no discoverable user route. Repeated bug-report-and-fix loops are a poor substitute for inspecting the product as a whole.

**Distinct contribution:** Add an owner-readable **bidirectional join** to the existing As-Is/To-Be/Delta method:
- Forward: visible button / context -> handler -> API or bridge -> actual domain function / job -> state mutations and published artifacts -> observed/tested user outcome.
- Reverse: implemented business capability -> reachable UI context(s), CLI/HTTP-only entry or missing/hidden/disabled/deprecated entry -> accessibility and task-flow evaluation.
- Do not equate an endpoint absent from UI literal search with a product defect. Exclude private diagnostics by explicit intent; dynamic and delegated event handling may defeat static matches. Distinguish source-connected, runtime-demonstrated, hidden by conditions, no intended UI, UI-only/dead, unimplemented, and unverified.
- Maintain stable business capability identity even if multiple buttons point to one action; two affordances may be justified shortcuts rather than duplicated domain logic. Conversely an accessible endpoint is not evidence of a comprehensible user path.
- View modes: simple owner-facing product map; drilldown source provenance; capability-entry coverage matrix; approved To-Be arrangement and change/acceptance plan. Prefer concise Chinese-primary labels with English term and actual symbol IDs in drilldown.

**Narrow HSR source evidence** at `dea5411312ed3e819864f1915f4f2008f938cba3`:
- `app/static/index.html` line ~5986: `overviewBuildBtn` delegates to `buildBtn.click()`, which saves config and POSTs `/api/project/build` at ~5794. Thus two UI controls, one business build invocation; do not automatically delete either.
- `generateSubtitleAssBtn` and `generateSubtitleExternalAssBtn` at ~3496–3497 map to `startAssExport('internal'/'external')` near ~9810 and API `/api/output/ass` or `/api/output/ass/external` near ~5819. Explicit publication semantics diverge.
- `app/server.py` exposes `POST /api/project/forget` (~1306) while the examined production `index.html` does not contain that literal API route. **Candidate API-only route**, not established as unwanted or missing UI until business intent and any alternate callers are reviewed.
- An exploratory regex count found 99 literal `<button>` tags and 55 matched FastAPI route decorators, but these are deliberately not treated as authoritative exhaustive inventory: source contains dynamic controls, delegated handlers and differently formed definitions.

**Acceptance:** For selected product owner workflows, verify exact UI rendering and triggering (not just DOM presence), linked code action, effects, user outcome, absence of overwritten drafts, and source/CI evidence; classify every uncovered capability with an explicit owner decision. Audit across two runtime backends where applicable. No UI modifications authorized by this note.

**Dedup:** Existing `inbox/cases/2026-10-15-softmux-ai-concept-images-feature-catalog-vs-operable-ui.md` already warns against mapping every capability to an always-visible dashboard; `inbox/observations/2026-10-14-ass-r2-18-tools-and-legacy-8-parity-gap.md` addresses 18-tool coverage between Android UI hosts; `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` handles requirements and evidence. This is a specific **product-owner architecture comprehension + two-way source/UI reachability map** extension of the existing candidate, not a duplicate policy or Canonical promotion.


## Follow-up — 2026-10-17 owner-facing information density and semantic zoom

**Direct requirement:** The project owner needs useful, accurate software relationship diagrams that are neither generic/empty summaries nor hundreds of raw code-level nodes and edges. This is not a request to reduce precision; it is a request to control **presentation granularity** while retaining implementation evidence.

**Proposed semantic-zoom contract (Candidate, not yet tested):**
1. Level 1 / Product Map: roughly 5–9 meaningful user-facing capabilities/workspaces per focused view, their purposes, outcomes, cross-capability dependencies and major entry coverage. Node counts are layout heuristics, not correctness targets.
2. Level 2 / Functional Model: one bounded workflow or diagnostic question, roughly 5–12 semantic objects/steps, typed relations, relevant conditions, side effects and failure/reuse paths. Organize by real business capability, not raw module/function count.
3. Level 3 / Implementation Evidence: exact GitHub revision and file/line, actual UI IDs, event handlers, API/CLI bridges, jobs, state owners, artifacts, tests and observed runtime evidence. Show by selection/drilldown, not as permanent graph clutter.
4. A shared underlying source/evidence graph drives question-specific projections: use/capability, UI reachability, data-write, change impact, failure, actual-vs-target and migration. Do not maintain independent diagrams whose claims silently disagree.
5. Semantic compression cannot discard distinctions that change user-visible behavior: save vs preview vs publish, internal vs external output, automatic vs explicit trigger, input identity/integrity guards, durable vs temporary state, and failure/verification boundaries. Put uncommon conditions and detailed proofs in an adjacent concise mechanism table/inspector; indicate uncertainty where semantic equivalence is unverified.
6. Success is tested with owner comprehension tasks: given a selected UI entry, identify real outcome, affected artifacts, preconditions, entry alternatives, and change impact; given an implementation capability, find an authorized user route or classify intentional API-only / missing / conditional. Verify against pinned source and at least one executable path; do not equate visual elegance with correctness.

**Narrow verified example:** HSR at `dea5411312ed3e819864f1915f4f2008f938cba3`, UI `generateSubtitleAssBtn` and `generateSubtitleExternalAssBtn` in `app/static/index.html` dispatch to `startAssExport('internal'/'external')` and distinct POST APIs; `app/auto_delivery.py::queue_ass_regeneration` verifies a trusted source in complete mode and repackages the MKV before reporting the internal result complete, whereas external export is separate. A minimal semantic map can retain four verbs — save, real preview, internal regenerate, external export — without displaying the entire code call graph.

**Dedup:** This follow-up belongs to the existing 2026-10-17 actual/target/delta Candidate; complements 2026-10-16 source-grounded Code Atlas Observation and the softmux 2026-10-15 functional-catalog-vs-operable-UI Case. No change to Canonical, no authorization to modify product UI or code, and no general effectiveness evidence.


## Follow-up — 2026-10-17 viable model-runtime boundary: ChatGPT-hosted MCP App

**New implementation feasibility clarification:** A browser-native source/product comprehension workbench cannot perform live semantic reasoning with only GitHub, static AST analysis and a web UI. At least one actual model execution environment is mandatory. The previous "external AI worker" formulation was insufficiently specific about interactive invocation.

**Three architectures and selection:**
1. **ChatGPT-hosted MCP App (preferred no-model-API pilot):** Build a small GitHub-aware MCP service with data/read tools, evidence/graph persistence and a separate render tool returning an interactive MCP Apps UI resource. ChatGPT is the semantic worker. The widget can call deterministic MCP tools via `tools/call` and request a new model-mediated turn via the standard `ui/message` bridge; do not mislabel arbitrary JS click handlers as direct model API invocations. The user runs the workbench inside a supported ChatGPT host, not a standalone website. Requires an accessible/authenticated MCP server and explicit GitHub access for it; GitHub credentials already available to a ChatGPT connector are not automatically delegated to a new MCP server. Richer ChatGPT extensions (sidebar/conversation panel) require compatible host support.
2. **Standalone web UI + backend model inference:** The service must explicitly connect to a model provider via an API (or equivalent independently available model execution service). ChatGPT subscription billing is separate from OpenAI API billing; do not assume subscription grants programmatic model inference.
3. **Standalone local inference:** Run a local inference server/model with bounded hardware/context/quality tradeoffs and separate verification. This removes reliance on a paid hosted inference API but still requires model runtime capacity and permissioned source access.

**Concrete minimal interaction contract:** A GitHub-pinned business capability ID and selected node -> UI `ui/message` user-requested analysis -> ChatGPT calls MCP source/evidence tools -> model emits structured `AsIs/ToBe/Delta` claims with typed relationships, per-edge source anchors, uncertainty and approval gates -> MCP tool stores versioned schema-validated result -> UI render tool shows owner-level relationship map -> node selection fetches already known data without a model call; further semantic questions explicitly request another ChatGPT turn. Deterministic tools must not fake semantic conclusions. Persist useful results outside the conversation and independently verify source anchors and regressions.

**Official platform evidence consulted 2026-10-17:**
- https://developers.openai.com/plugins/build/app-quickstart
- https://developers.openai.com/plugins/build/chatgpt-ui
- https://developers.openai.com/plugins/build/extensions
- https://developers.openai.com/plugins/reference
- https://help.openai.com/en/articles/9039756
- https://developers.openai.com/workspace-agents/trigger-runs (agent API trigger can queue a run, but its response cannot currently be fetched through that API, so it does not alone replace interactive model-backed widget messaging).

**Execution/authority boundary:** This is an architectural Candidate, not a deployed integrated app. Do not create servers, credentials, UI, PRs, or automatic analyses without the user's explicit project implementation authorization. Test one HSR functionality first and distinguish UI usability acceptance from real semantic correctness. No Canonical promotion.
