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


## Correction — 2026-10-17 ChatGPT-hosted app eligibility gate

Official ChatGPT documentation confirms that MCP Apps can render an optional embedded HTML/JS component (iframe) next to the conversation, while the ChatGPT host supplies model reasoning. However, **technical SDK capability is not equivalent to the user's permission to connect or test a custom MCP app**. The current official ChatGPT Help Center eligibility documentation emphasizes custom MCP app creation/testing for Business and Enterprise/Edu web workspaces, with admin/owner authorization and a beta rollout for full write/modify actions. Some earlier/other help pages mention Pro read/fetch developer configurations, but that is not a blanket Plus entitlement and the individual account's enabled features must be checked. Do not promise this route is immediately deployable for a user's plan without verifying controls.

Source:
- https://help.openai.com/en/articles/12584461-creating-custom-mcp-apps-in-chatgpt (availability/permissions, updated 2026-10)
- https://developers.openai.com/plugins/build/app-quickstart (embedded iframe implementation)
- https://developers.openai.com/plugins/build/chatgpt-ui (MCP Apps UI bridge)

Recommended delivery choice: (a) immediately prototype a turn-scoped interactive map inside a ChatGPT response using supported response UI without pretending it is a persistent installable plugin; (b) if user has rights, trial a custom MCP app with dedicated server; (c) otherwise provide an independently hosted browser atlas displaying durable precomputed AI analyses, with fresh semantic analyses run by an explicitly started ChatGPT/agent handoff rather than magically invoked in the site. Do not present an ideal ChatGPT sidebar as guaranteed. No deployment or account changes performed.


## Follow-up — 2026-10-17 no-inference workbench with durable on-demand ChatGPT handoff

**Need:** The user explicitly requests a workable compromise because a persistent visual product/architecture workbench needs semantic AI, but Foundry has no callable model API and custom ChatGPT-hosted apps may be ineligible or undesirable.

**Candidate architecture (not built):**
- **Standalone low-dependency browser** reads project-scoped, commit-pinned capability and relationship records, supports semantic zoom, bidirectional UI entry↔actual behavior navigation, actual/approved-target/delta, evidence drill-down and staleness display **without model inference**.
- Existing UIGS Code Atlas AST index (currently Python-focused and experimental) supplies mechanical source facts; model-curated cross-language UI/JS/FastAPI/business/outputs links remain distinct, source-anchored and explicitly not assumed complete.
- ChatGPT is **user-invoked** only when an analysis item is unknown/stale/disputed or new design reasoning is requested. Browser prepares a compact task packet containing repo, pinned SHA, capability ID, changed scope, present record, evidence gaps and the owner's question. Initial handoff can be copy/paste; do not claim a standalone webpage can silently invoke the ChatGPT model or safely access ChatGPT private conversations.
- The AI returns versioned structured records and concise explanatory graph, pushed through permitted GitHub-connected agent operations or reviewed PR. A deterministic validator checks schema, referenced file/link existence, SHA, identity, relation types and completeness labels; **it cannot certify semantic truth**. CI can regenerate HTML/JSON snapshots and mark affected records stale after commits; static host or local file is enough for the first prototype.
- Prior useful interpretation is durable in repo data rather than hidden model memory. Owner signs off To-Be changes separately. Product source remains the execution authority; Foundry retains governance; no automatic Canonical promotion.

**Minimum viable pilot:** One HSR function group (e.g. subtitle save/preview/internal-vs-external ASS) with 3–6 actual UI actions, full frontend handler→API→job/artifact trace; one reverse capability→entry coverage check; three views (Product Map, Functional Model, Source Evidence), As-Is/To-Be/Delta and one offline browser snapshot; one update to the pinned commit to prove staleness and refresh mechanics. Keep source-side runtime/media evidence separate. Stop if the agent cannot recover and update the graph without hand-editing hundreds of unrelated relationships.

**Limits:** HTML/static map can answer questions already encoded in the records and visualize/filter graph, but **cannot generate new semantic conclusions itself**. Auto-responding AI chat or unattended refresh needs a real model-call bridge (cloud API, local model or supported host), a distinct later architecture requiring consent. Do not publish private-source-derived graphs via public Pages. Offline exported HTML needs a replacement export/import or a local server to see updated records.

**Dedup:** Extends this existing Candidate rather than inventing a second system. Related Foundry records include Code Atlas source-grounded visualization Observation (2026-10-16), durable-agent execution Canonical (2026-10-07) and existing project-adapter outbox. No Canonical or product code changes authorized by this ideation.


## Follow-up — 2026-10-17 shared engineer–owner comprehension, not a diagram product

**Direct owner diagnosis:** The user is continuously changing several complex AI-implemented products but cannot tell what existing code does, where UI entries lead, what is absent/duplicated, what changed in each AI-reported implementation, or whether sequential changes converge on an owner-defined theoretical model. Different AI sessions can each have different incomplete local interpretations; the owner is forced into reactive bug reporting and cannot learn the product through controlled operation. This is an explicit **dual-black-box / joint-comprehension and controllability failure** report, not measured proof that every agent lacked understanding.

**Correction to scope of this Candidate:** A persistent visualization workbench or no-model-API handoff is an **interface/transport component**, not the central success condition. The central requirement is a source-grounded, reviewable **shared engineering state** that allows both owner and any newly started AI worker to reestablish the same current implementation, approved target, outstanding deltas and evidence gates. The owner must be able to decide and learn during operation; a model's statement 'implemented X' has no independent authority.

**Proposed falsifiable engineering loop:**
1. **Product coverage baseline:** compact capabilities/workspaces, bidirectional UI entry↔business outcome, artifact/state ownership, and explicit intentional API-only / missing / conditional UI routes; source evidence at pinned commits, selective runtime probes.
2. **Approved theory / specification:** durable user-intent and product invariants with stable requirement IDs and explicit acceptance criteria, separate from model-generated optional target proposals.
3. **Before each change:** identify the exact target requirement/delta, current actual behavior and evidence, proposed changed responsibilities, preserved capabilities, source and tests likely touched, and scope/permission gate. If no root-theory traceability or conflicting active work, stop for owner review.
4. **During execution:** versioned checkpoints at PR/commit granularity; observe scope drift, duplicate implementations, missing state ownership and feature-entry gaps; AI-created successor task suggestions remain non-authoritative until reconciled to the owner's root.
5. **After each change:** show a user-comprehensible **before/after semantic diff** in addition to code diff: which visible action/behavior changed, which data/artifact is affected, which graph edges and capabilities were added/removed/moved/retained, with actual code links, tests, runtime outcomes, failures/unknowns and remaining delta. Separate submitted, tested, visually verified, owner-accepted, and overall theory-complete states.
6. **Across AI sessions:** each worker reconstructs scope from repository-persisted approved target + exact current source revision + shared actual/delta/validation records. No assumption of shared hidden reasoning or that one snapshot remains valid across commits. AI must actively check source and mark stale/uncertain relationships rather than merely repeat prior claims.
7. **Owner's learning loop:** let the owner choose a visible UI action or capability and see purpose, conditions, operations, outcomes, where it is in current-vs-target state and what was recently changed; selective semantic zoom then source evidence. Ask comprehension questions before/after changes to measure improvement, not number of pretty diagrams.

**Necessary architecture controls:** Require one declared state/data owner per critical responsibility where applicable; detect suspected overlapping feature implementations or write paths before adding new ones; check cross-feature invariants and saved settings; block unauthorized 'cleanup' that removes old entries. Static graph and CI are independent evidence but cannot fully establish business semantics; the model provides context-specific interpretation and must cite source and real tests. Parallel agents must check fresh HEAD/diff and ownership before conflicting writes.

**Success criteria (proposal, not yet empirically met):** The owner can explain a chosen function's actual entry/outcome and approve or reject its intended change; a new AI chat can resume the same target without reconstructing it from transcript; each delivered work item has root requirement, explainable semantic diff, evidence and explicit residual debt; no user-facing features silently disappear from an approved workflow; changed actual graph converges to approved target with acceptance evidence rather than task count or green CI as proxy.

**Related existing controls / dedup:** `governance/AGENT-EXECUTION.md` already defines durable agent state and completion boundaries; `inbox/candidates/2026-10-14-agent-generated-next-units-goal-drift-guard.md` already addresses follow-up drift toward AI self-generated tasks; `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` separates implementation from validation and user-visible proof. This extension adds the **owner's real-time comprehension and semantic before/after change contract** to the existing 2026-10-17 As-Is/To-Be/Delta candidate; it does not duplicate or replace those narrower controls.

**Scope and authority:** User feedback confirms desired product-development control and learning outcome. Implementation method, instrumentation and efficacy are still Candidate-level. Do not auto-promote to Canonical, claim cross-thread model understanding is solved, or modify any product code without separate authorization.


## Implementation probe — 2026-10-17 self-contained HSR Owner Atlas prototype (local artifact)

**Task boundary:** In response to the user's “继续” after repeated concerns about theory/design talk without a concrete tool, a **local downloadable prototype** was built in the conversation runtime. Neither HSR nor Foundry executable product code, site configuration, credentials, PRs, or Canonical was modified. This note is intake only.

**Delivered local files:** `UIGS_HSR_工程认知工作台.html`, `hsr_snapshot.json`, `app_template.html`, `build_demo.py`, `test_offline_atlas.js`, `README_使用与验收.md`, and zipped source/readme. Exact artifact SHA-256: HTML `c2c2afa3b401ba7697189118328961c699be16b44250a2b22ff4fbf60c883e6f`, ZIP `811717d128a6d558b9b2ac853bbf44b0dab690f77645f2999536848102b89bf6`. These are local conversation attachments, **not** uploaded to GitHub repository; do not infer deployability or link permanence from this record.

**Verified source snapshot:** Product `11576865/HSR-Voice-Archive-Builder` main `dea5411312ed3e819864f1915f4f2008f938cba3` (confirmed current main at inspection). Nine selected capability records: archive build, subtitle edit autosave, layout save, real libass preview, internal ASS, external ASS, full MKV bundle, remote index check, and `POST /api/project/forget` as an explicitly uncertain UI entry. Eight have inspected source paths with precise SHA-anchored URLs; the ninth route has code evidence but its **UI exposure is not established**. This is a scoped example, not full-project coverage. In particular, internal ASS must verify source integrity and (in complete mode) update/verify MKV; live preview is distinct from publication.

**Actually functional in this artifact by implementation / static JS smoke:** Standalone HTML+inline JSON, business capability search/list, owner-readable consequence/precondition summary, clickable four-column typed relationship graph, reverse capability→entry table, As-Is vs **unapproved** candidate To-Be, source link inspector, version/validation disclosure, generated ChatGPT handoff task, snapshot import/export and record-level snapshot difference. No external model API or backend required for ordinary browsing. The page does not automatically understand new code; subsequent semantic work still requires an external model invocation, and snapshot diff is explicitly not semantic code diff.

**Verification and found defect:** 9-record Python shape checks, `node --check`, and dependency-free Node smoke of view generation, graph, entry matrix, authority labelling, evidence, handoff, invalid JSON rejection passed. Initial test exposed a malformed `ass-out` record caused by shifted positional builder arguments; fixed before final archive. This illustrates the need for schema validation at data-production time; a green JS parse check alone does not prove correct model records. **Browser/device validation Pending:** Playwright was installed but Chromium environment policy returned `ERR_BLOCKED_BY_ADMINISTRATOR` for local file/data/http navigation, so no live DOM click or screenshots can be certified.

**Limitations and next evidence gate:** This is a seed UI+hand-curated source-backed manifest, not integrated with unmerged Code Atlas PR #38, automated JS↔Python extraction, approved theoretical baseline, multi-agent recovery or real semantic before/after Git diff. The next independently authorized work package should prove a production-browser click test (in suitable environment), owner comprehension on a selected operation, and one actual authorized implementation delta with verified source and runtime evidence. Do not promote to Canonical from prototype existence.


## Implementation continuation — 2026-10-17 HSR Owner Atlas v0.2, historical PR semantic change + AI handoff

**Bounded result:** Built a reproducible **local, standalone HTML prototype** in this conversation runtime based on the v0.1 Owner Atlas, not a hosted Foundry service. No HSR product or Foundry executable source/Canonical changed. The artifact is supplied to the user as a conversation download, not merged into any repository.

**Scope and real product evidence:** HSR main remained `dea5411312ed3e819864f1915f4f2008f938cba3`. Source commit was compared to its parent `01ad440bf77ea6cfec4ba24c494bd38cd8205053` and merged [HSR PR #194](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/194). The prototype records the commit's 10 changed files and three source-backed owner-readable Before→After semantic change cases, each with pinned old/new source anchors and explicit missing runtime evidence:
1. `app/static/index.html::startAssExport` added `/api/project/active/audio-integrity` preflight for **internal ASS only**, a failure prompt and explicit recovery actions before starting the internal job. This should not be conflated with external ASS generation or proof of recovery.
2. `app/archive_bundle_lifecycle.py` added sealed MKV content SHA-256 checks and tightly keyed cache/legacy-receipt preservation. Byte identity can remain verified after metadata-only changes for hashed receipts; legacy unsigned receipts are still fenced.
3. `app/effect_voice_preview.py` + FastAPI/Lite UI/render paths added explicitly labelled **visual-only, silent Fade** when project audio provenance is unverified; it is not verified sound.
Expanded selected capability ledger from **9 to 10** by adding effect-preview so this change has a navigable product capability anchor. All existing owner views remain.

**New user workflows:** `真实变更` tab shows approved old/new pinned Git SHA, change in user-observable behavior, explicit non-claims, source/test-code evidence and outstanding acceptance. Includes mechanical file-to-capability overlap as `may affect` rather than proof of semantic behavior; `跨线程交接` tab serializes the selected capability's source anchors, current interpretation, historical PR delta, unapproved theory authority, unknowns and mandatory next-agent verification conditions. User can copy or export the packet; no model API invocation or hidden cross-thread state sync is claimed.

**Local deliverables and SHA-256:** `UIGS_HSR_工程认知工作台_v0.2.html` = `9bc2708674c914f1654668441cd4d747cb171d3ab364e3e4b1a39856e97b6cdc`; ZIP source/tests = `0a1b6d68a7ba572a6ba02d618c15278a4dedd4fda457cd2198e888bf45c6c753`. Includes v0.1 immutable seeds, deterministic upgrade script, JSON snapshot, inline UI template, schema/evidence validator, Node browserless tests and a Playwright smoke script. These filenames/hashes are evidence pointers to downloadable conversation artifacts, NOT assertions of repository storage.

**Verification:** Python validates 10 capability identities, graph edges, source URL/SHA integrity, 10 changed paths, 3 impact records and exact HTML/JSON parity; Node smoke passes view generation, handoff packet production, source evidence, invalid imported case rejection; syntax check passes. Rebuilding twice yields unchanged HTML SHA. **Actual Chromium browser click/render and Android visual verification remain Pending**: local browser navigation fails with `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Neither HSR product tests nor FFmpeg/media output were run this turn, so don't report production validation.

**Limits / next gate:** The model manually curated this single source-reviewed historical semantic delta. The viewer does not automatically parse full GitHub diffs into trustworthy product behavior, automatically discover theory authority, fetch fresh HEAD, or perform live AI calls. Next bounded work should test the HTML in an authorized normal browser, obtain an approved target requirement for one affected HSR operation, then validate a real authorized before/after change without claiming all-project progress from one case. Continue to keep source evidence, AI interpretation, theory authority and runtime acceptance separate. Candidate remains unpromoted.


## Implementation continuation — 2026-10-17 Owner Atlas v0.3 documentary-goal traceability

**Bounded local delivery**: Extended the downloadable HSR standalone Atlas prototype, without changing HSR product code, Foundry executable tools, UI or Canonical. The single HTML and full reproducible source/test ZIP were built as conversation artifacts, **not published to a repository**. HTML `UIGS_HSR_工程认知工作台_v0.3.html` SHA-256 `3982549b2d450410ced72e4dad145bcb782373ec74ac4dda2f122ec3146fbcec`, complete ZIP `UIGS_HSR_工程认知工作台_v0.3_源码与验收.zip` SHA-256 `f220a032a154d67165d00404d66b89d7f730e49e8aff0d65395f6acb3d806e9b`.

**Real source scope**: The HSR source remains pinned at `dea5411312ed3e819864f1915f4f2008f938cba3`. Six `HSR.DOC.01–06` repository-documented expectations were extracted from `README.md` and `docs/architecture.md`: deterministic timeline/source identity, non-destructive proofreading overrides, verified full MKV publication, conservative incremental update, trusted audio provenance, and explicit full-MKV/FLAC-only/independent export boundaries. Each row links exact SHA/path/line evidence, 1–3 business capabilities, source mappings, proposed not-yet-run acceptance scenarios, and a user-readable design question. **All are marked `documented-not-owner-approved`, not accepted theoretical target.** The previous ten selected capability records and three PR #194 behavior cases are preserved; coverage is still sampling, not exhaustive.

**Real documentation contradiction surfaced**: HSR `README.md` around line 199 describes default complete MKV as black background; `app/archive_bundle_lifecycle.py` lines 278–284 falls back to a default red-cloud image for unknown/no receipt, and `tests/test_hsr_ass_export_modes_and_redcloud.py` lines 35–43 assert new image/red-cloud background. Record as `HSR.DOC.DRIFT.01` with source links and **runtime / product intent review pending**, not automatic documentation repair or authority promotion. This complements the preexisting separate default-MKV background observation, so do not duplicate that bug report.

**Functional interface added**: A new `目标台账` tab and revised `理论与差异` tab show documentary goals → selected capability → source paths → proposed acceptance checks; source discrepancy visible; per-goal local owner review draft (pending / inclined to adopt / revise / reject, with note), exportable as JSON. The resulting handoff packet includes related documentary goals, unverified local review drafts, and contradiction evidence. Draft choices are explicitly *not* authenticated owner-approved specs or implementation permission, and the browser has no background persistence; export is necessary before reload. Import rejects another SHA, forged `owner_authorized_theory`, changed goal authority, wrong source SHA/URLs, unknown capability IDs and bogus review record authority. A matching v0.2 seed can be conservatively upgraded while keeping zero approved goals.

**Actually tested**: `python upgrade_v03.py`, `python validate_v03.py`, `node --check _inline_v03.js`, `node test_v03.js`, and repeated deterministic build SHA; all pass. Import/handoff, evidence references, review draft safety and refusal to promote undocumented approval were covered by Node VM tests. **Browser/device test Pending**: Chromium/Playwright navigation via localhost returns `net::ERR_BLOCKED_BY_ADMINISTRATOR`; no live viewport/Android click pass. No HSR FFmpeg, E2E, audio media or production runtime acceptance was performed. This is not a fully automated GitHub diff-to-semantics pipeline.

**Next evidence boundary**: Owner must identify or explicitly authorize a versioned true HSR theoretical goal/acceptance contract. A later bounded implementation should test an authorized code change against the approved goal with owner-readable before/after behavior, source-and-runtime-backed acceptance and next-agent recovery. Do not treat these six repository-document statements as the author's complete theoretical model. No Canonical promotion.


## Implementation continuation — 2026-10-17 Owner Atlas v0.4: bounded analysis work packages and self-report quarantine

**User context and bounded output:** After the v0.3 documentary-target Atlas, built a locally downloadable offline v0.4 HTML and reproducible source/test ZIP without changing the HSR product repository or any Foundry executable code. This is a conversation artifact, not a deployed service. Both files were created and SHA-256 checked in the active runtime:
- HTML `UIGS_HSR_工程认知工作台_v0.4.html`: `05a6dedf35ad56b790d7edae9844181429713a5f41e7b42962eae53b0e3b7943`.
- ZIP `UIGS_HSR_工程认知工作台_v0.4_源码与验收.zip`: `e8c77d9a4b90c18baa90722ee5f5f8d8ddb80f800d3fb2e0bb25ed9c7f0fa14c`.

**Added operational behavior:** A separate `工程工作包` tab lets the owner select a code-linked HSR capability, associate an explicitly **unapproved** documented goal, and author a bounded intent, observable acceptance expectation, and preserved old behavior. Creates `WU-###` with `kind=local-analysis-draft`, `status=draft-not-authorized`, and pinned product SHA. A structured cross-thread handoff includes source-anchored As-Is capability, linked documentary goal with draft review status, historical reviewed PR impacts and mandatory source/permission checks. The tool exports a JSON template for an external AI's resulting commit/files/behavior/tests **self-report**, then permits import only at `authority=unverified-agent-self-report` with matching repo/base SHA/work ID. No automated AI call or PR acceptance is implied; the `result_sha` is *not fetched from GitHub* by the offline viewer.

**New validation/learning detail:** Import enforces an immutable source-evidence core from the embedded baseline, rejecting edited capability semantics, changed document goals or injected approval fields even when the apparent product SHA matches. This extends prior v0.3 basic schema/anchor checks: syntactically valid JSON plus matching SHA **do not prove that imported interpretation is authentic**. The protected core is tied to the delivered HTML, **not cryptographically signed**, and owner local drafts are not formal approval. Importing AI descriptions cannot set `verified` or `owner-approved` state.

**Tests and outcome:** `python build_v04.py` twice yielded identical HTML digest; `python validate_v04.py`, `node --check _inline_v04.js`, and `node test_v04.js` passed. Offline Node VM asserts draft creation, evidence-bearing handoff, AI report import, template placeholder rejection, forged approval/authorization/verified status refusal, wrong SHA rejection, unsafe path rejection, immutable-code/goal baseline checks and v0.3 JSON migration. **Real Chromium interaction Pending**: `browser_v04.py` ran but page navigation failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR` under the current policy. No Android screenshots, live browser acceptance, FFmpeg end-to-end, complete repository crawl, automatic SHA refresh, external agent result verification, model API call, owner-approved theoretical baseline, or authorized product implementation was claimed.

**Next meaningful gate:** Use an actual owner-approved versioned theory/acceptance criterion and one separately authorized real product change to verify the end-to-end requirement -> source implementation -> independent runtime effect -> owner-comprehensible verified diff -> cross-agent recovery. Do not promote this local UX or an unverified AI self-report to Canonical.


## Implementation continuation — 2026-10-17 Owner Atlas v0.5: explicit read-only GitHub metadata verification

**Bounded deliverables**: Local downloadable standalone HTML + reproducible source/test ZIP, **not** merged into HSR or UIGS executable repositories. Verified content digests: `UIGS_HSR_工程认知工作台_v0.5.html` SHA-256 `4d70d00dd84f04b4d3f9509e286a65cedad5f032907f45a7fb75990061e26da4` (122,171 bytes); `UIGS_HSR_工程认知工作台_v0.5_源码与验收.zip` SHA-256 `488c9755e406ded3a0340a95c43130cbdf165365e3b0b96476c56c378e18e779` (172,419 bytes). Existing v0.4 capability/goal/PR/analysis-work-package schema preserved.

**Actual advancement over v0.4**: An explicit, user-clicked `GitHub 核查` view retrieves publicly readable `https://api.github.com/repos/{owner}/{repo}/commits/main` and `compare/{base}...{head}` without private tokens, checks pinned baseline staleness, Git ancestry/merge-base, GitHub diff changed files versus AI self-reported file set, and rejects diverged/truncated/invalid results instead of marking self-reports as accepted. The snapshot's existing `unverified-agent-self-report` authority remains unchanged. Session-only check data may join cross-thread handoff but is labeled unsigned and must be fetched again independently; it is **not** an authorization mechanism or durable cryptographic proof.

**Fallback executable**: `verify_github_v05.py` is a stdlib-only read-only verifier for the historical HSR PR #194 or a `uigs-ai-claim/1` JSON report; optional `GITHUB_TOKEN` environment variable for caller-authorized private repo GitHub access. It emits `uigs-github-structural-receipt/1` with origin, revision chain, actual versus claimed paths, observed time, compare link, explicit `behavior_verified=false`, `tests_verified=false`, `owner_accepted=false`, `theory_approved=false`. Offline fixtures are unequivocally marked `fixture-only-not-live-github`.

**Independent real source check**: GitHub connector GET of HSR `compare/01ad440bf77ea6cfec4ba24c494bd38cd8205053...dea5411312ed3e819864f1915f4f2008f938cba3` returned `status=ahead`, `behind_by=0`, `total_commits=1`, `merge_base=01ad440...`, head `dea541...`, and exactly the ten file paths previously associated with merged PR #194. This corroborates the metadata example only, not the semantic correctness of its three explanations or runtime acceptance.

**Tests executed**: deterministic v0.5 HTML build and embedded v0.4 snapshot parity; JS parse; inherited v0.4 Node VM (work package/forgery rejection); new v0.5 Node VM (GitHub ancestry, report/diff file mismatch, truncated/diverged rejection, explicit GET without credentials, stale main detection, unsigned handoff, GitHub HTTP failure); six Python `unittest` tests (metadata/path/authority rejection, offline fixture tagging); ZIP integrity. All pass. Chromium actual navigation continued to fail with `net::ERR_BLOCKED_BY_ADMINISTRATOR`; therefore browser click, CORS/network interaction from file origin, Android UI, real multimedia effect and end-to-end product acceptance **remain Pending**.

**Critical epistemic invariant**: GitHub provenance of SHA and changed-file paths is different from semantic change, tests actually run, owner-approved theory, and owner-observed acceptance. A tool or AI may not promote metadata inspection to product completion. This extends the existing 2026-10-17 Candidate and cross-references existing provenance/cross-layer evidence Foundry knowledge without modifying any Canonical rule. A future fully effective workflow still needs an approved theory and one genuine authorized product change with independently observed user behavior. 


## Implementation continuation — 2026-10-17 HSR Owner Atlas v0.6: behavioral evidence chain and PR-HEAD CI boundary

**Local, downloadable artifact only:** `UIGS_HSR_工程认知工作台_v0.6.html` SHA-256 `aaeed5173def6ac45b6ed3404daa15b883710cc8bfac6d477a9eadb2813c1015`; full source/test ZIP `UIGS_HSR_工程认知工作台_v0.6_源码与验收.zip` SHA-256 `2fd634675d1ee00deaccbb33f253d3f7e0b69f3cdd03bc15d44cbc2639cf1565`. HSR product code, UIGS deployed code, and Canonical were not changed. No site/app deployment.

**New human-operable feature:** The `行为证据` view connects three bounded PR #194 semantic source hypotheses (internal ASS preflight, byte-identical sealed MKV authenticity, visual-only silent Fade preview) to owner-readable preservation questions, exact implementation anchors, individual test definitions at fixed HSR source SHA, GitHub Actions run-and-job metadata, explicit evidence gates, remaining runtime acceptance, and one-click export/copy of source-grounded next-agent verification task. Cross-thread handoff now includes selected capability's behavior case records without elevating them to approved targets.

**Actual remote-source verification in this turn:** Read GitHub Actions runs of PR #194's **development head** `b60f1be5b116772862d60c5b534ab87091fd6999`: `38935511796` tests, `38935511697` seven ASS requirements, `38935511721` subtitle browser evidence, and `38935768113` branch hygiene — all `completed/success` as observed through GitHub connector. Retrieved Job lists for the first three: unit (3.11/3.12/3.13), termux-lite-surface, real-libass-ink-evidence; seven-ass-contracts; libass-artifact + chromium-ui. **Merged product source commit is a different SHA** `dea5411312ed3e819864f1915f4f2008f938cba3`. Both the UI and stdlib-only Python verifier reject the logical leap from same-PR successful workflow metadata to exact-merge-SHA targeted test execution, individual function assertions, media runtime correctness, owner acceptance or approved theoretical-model progress. Test names/lines were located in HSR current source, but no actual test logs were individually correlated.

**Executable tools/tests:** Added opt-in GitHub REST read-only CI run+job verifier in browser and independent `verify_ci_v06.py` CLI supporting offline fixture or live API. It validates run ID/name/head SHA/status/conclusion and complete Job set vs observed expectations, rejecting truncated, missing, failed and mismatched records. Offline CLI fixture is explicitly marked `offline-fixture-not-live-evidence` and cannot be passed off as network evidence. Node VM UI/flow, Python 6 unit tests, static source-and-authority validation, inherited v0.5 work-package & GitHub compare tests, deterministic HTML build and ZIP CRC all pass. **Browser UI acceptance remains Pending** because actual Playwright Chromium navigation to file URL failed `ERR_BLOCKED_BY_ADMINISTRATOR`. The standalone CLI live-network mode and browser-to-GitHub fetch also were not end-to-end tested in this container.

**Reusable Candidate insight:** An owner-readable implementation-change receipt requires at least separately typed `source_observed`, `test_definition_located`, `pr_head_ci_run_job_metadata_checked`, `exact_target_sha_test_run`, `runtime_behavior_observed`, `owner_approved_theory`, and `owner_accepted` assertions with evidence provenance. These are not interchangeable and MUST NOT collapse into one 'green CI' or 'implemented' indicator. Source-to-test mappings are model-mediated hypotheses that may support test selection but do not prove tests ran; precise CI run revision is essential, especially across PR-head→merge boundaries. This extends the existing Candidate; compare with requirements/evidence traceability ledgers and prior PR CI boundaries rather than automatically changing Canonical.

**Next gate:** Execute exact merged/current source SHA product behavior tests in a permitted runtime and attach artifact/log-level evidence to each behavior case. Then perform owner observation against an explicitly authorized versioned theoretical contract; don't assert convergence absent that approval.
