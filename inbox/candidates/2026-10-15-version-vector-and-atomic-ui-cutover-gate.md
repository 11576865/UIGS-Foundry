# Candidate: Separate product/specification/code versions and integrate a full UI replacement behind one coherent cutover gate

Date: 2026-10-15
Status: **Candidate / product-owner concern and proposed workflow; NOT validated by a completed UI migration**
Domains: engineering-process, interface-grammar, reliability
Project discussion: `11576865/MKV-Fast-Muxer`

## Trigger and observed context

After a multi-threaded, rapidly merged soft-mux/Matroska development period, the product owner identified **weakly distinguished version identities** and **fragmented UI implementation** as likely drivers of duplicate work and semantic drift. This is a hypothesis, not a demonstrated sole cause.

At the inspected main commit `8b8ec0e30908a3960da5f9f26f6acf7444ecb60c`, `package.json` identifies `version: 1.2.2` and `name: mkv-fast-muxer-v3`; `README.md` names the product `MKV Fast Muxer v3`. Separately, a 2026-10-12 product strategy v1.0 establishes a target design, the 2026-10-13 UI report defines a new object-centered workbench, the current domain exposes `container-document-projection-v0`, and an October engineering stack is divided into P0–P6 and R1–R7. Those labels identify **different objects**; there is no evidence that simple lack of a numeric label alone caused all duplicate PRs. Git commit SHAs and ancestry already provide exact code order; they do not establish which product specification each branch intended to realize.

## Proposed distinction: independently versioned authorities

- **Product/release version:** publicly delivered application identity and compatibility promise (use its existing authoritative package manifest; do not scatter literal copies).
- **Approved UX/specification revision:** frozen whole-workbench requirements, information architecture, interaction contracts, and acceptance examples. This is not the same as the application version.
- **Source integration identity:** exact `main` SHA and PR head SHA; stale ref changes invalidate previous verification until reconciled.
- **Persisted schema/protocol versions:** `ContainerProject`, recipe, job plan, report and draft compatibility, migrated independently and tested at producer/consumer boundaries.
- **Feature evidence state:** planned, represented-only, limited/guarded, production-connected, exact-head tested, and actual-file/field accepted. A version number does not imply all goals are complete.

Do not introduce redundant versions when an existing manifest or schema authority already covers the same object. Each code PR must reference the target UX revision, base SHA, scope and acceptance evidence, without pretending the version string itself prevents branch concurrency conflicts.

## Candidate UI cutover method (proposed, not executed)

The owner preferred a **single cohesive final UI handoff**, rather than publishing or merging multiple long-lived partially redesigned UI versions.

1. **Freeze the complete target UI before implementation:** desktop/tablet/narrow layout, source inventory, prospective output-object tree, selected-object inspector, footer execution/audit, batch job matrix, settings/help, empty/busy/error/unavailable states, existing-feature migration map, keyboard/focus/draft ownership and critical user journeys.
2. **One integration owner and branch against a pinned main:** implementation may use many small internal commits, tests, and previews, but there is **one authoritative complete UI integration PR**. Do not repeatedly merge incomplete layouts into product `main`.
3. **Maintain actual-state honesty:** present read-only facts if available; explicitly guard unsupported edits, never construct a second canonical resource model, and do not call demonstration data or UI-only state a real saved artifact.
4. **Cut over atomically from the user's perspective:** when and only when all approved core user journeys, preserved legacy capabilities, responsive layouts, production screenshot comparisons, and actual backend/output checks pass at the exact integrated HEAD, merge/deploy the new workbench together. Prefer rollback or feature-flagged isolation if the release gates fail. Internal review checkpoints are not separate published UI generations.
5. **After cutover:** incremental development is permitted inside the **same frozen information architecture/interaction contract**; changes to that contract require explicit revision, impact analysis, and targeted regression.

## Why this is not a universal recommendation for giant PRs

An all-or-nothing *product UI version* does **not** imply writing everything in one monolithic commit, deferring testing until the end, or ignoring hard code-ownership conflicts. Large implementation branches can accumulate merge conflicts and regressions; mitigate with a pinned baseline, frequent read-only reconciliation and testable internal checkpoints while forbidding partially adopted UI as a new authority.

## Existing Foundry relationships / dedup

- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` already covers the prospective MKV container as the primary visual object (do not duplicate its semantics).
- `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` already covers retaining legacy capabilities.
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` already separates implementation and evidence.
- `inbox/candidates/2026-10-03-schema-version-producer-consumer-drift.md` and `inbox/bugs/2026-10-11-mkv-e2e-version-assertion-drift.md` already describe concrete schema/app version failure modes.
- `inbox/cases/2026-10-13-ass-ui-design-freeze-rc-prototype-honesty-and-handoff-gates.md` is an example of design closure separate from production integration.

**Novel proposed combination:** distinguish a version *vector* across product/spec/code/schema/evidence, coupled with one reviewed full-workbench UI cutover rather than intermediate published partial UIs.

## Evidence boundary and open test

This is a **Candidate**, deriving the proposed gate from product-owner concern plus verified repository labels. It does not prove that version labels caused the prior engineering disorder, that an atomic UI cutover is lower cost in this repository, or that any future UI has been built. Validate against a complete production UI replacement with no lost legacy workflows and a single exact-head visual + runtime + output acceptance record before considering normative promotion.

No Canonical change.
