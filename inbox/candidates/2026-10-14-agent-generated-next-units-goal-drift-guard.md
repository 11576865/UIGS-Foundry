# Candidate: Re-anchor agent-generated next units to the owner-approved root goal

Status: Candidate / unvalidated mitigation
Date: 2026-10-14
Domains: operations, software-engineering, reliability, agent-execution
Source project: `11576865/Quick-Automatic-Hardsub-Encoder`
Reviewed PR: #105, head `b22f5fae2ee49d6dd3e442781729b808c89e55e8`

## Observed problem and evidence boundary

The project owner reports that execution direction tends to drift within at most three successive tasks. This is a reported operational observation; the precise frequency and causal attribution have **not** been independently measured.

QHE `AGENTS.md` correctly requires durable `.uigs/tasks/*.json` goals, completed units, generated `next_units`, and recovery from repository state. However, it does not require that every regenerated next unit carry a demonstrable dependency on a specific original theoretical-report requirement, nor force an authority check between agent-generated follow-ups and the root scope. The current `qhe-initial-version-full-report.json` has 28 completed-unit entries and 18 next-unit suggestions, including overlapping historical B16 subtask continuations. A next-unit suggestion is not necessarily an approved, prioritized work item.

This creates a plausible failure mode: a completed local implementation identifies further instrumentation/validation prerequisites; those are appended to `next_units`, then recovered and optimized as if the newly generated queue were the primary specification. The technical work can be real and locally valuable while the global task selection becomes biased. This mechanism is a risk supported by the record, **not** a proven explanation for every reported drift episode.

## Proposed bounded control (requires testing)

1. Freeze the owner-approved report/version and product acceptance matrix as root authority. Never let `next_units` override or shrink that denominator.
2. Before **every** unit, write a short task authorization record: root requirement ID and exact source anchor; user-visible acceptance criterion; what output or verification will close the requirement; impact on remaining project-critical path; and explicit reason this task outranks alternatives.
3. Distinguish `authorized_next`, `dependency_candidate`, `discovered_issue`, `evidence_pending`, and `optional_experiment`. Newly discovered technical prerequisites go into candidate/dependency queues, not the authoritative execution queue.
4. Cap unattended continuation at two bounded work units; before a third, perform a root-goal re-anchoring and owner-visible review of what was closed, what remains, and any new dependency. This limit is a proposed guard calibrated to the owner's “at most three tasks” observation, not a universal empirical threshold.
5. If a proposed unit has no traceable root requirement, primarily measures the previous implementation rather than closing a product acceptance criterion, changes user-approved scope, or cannot justify priority against open core requirements: mark `DIRECTION_REVIEW_REQUIRED` and do not silently execute it.
6. Make drift detection falsifiable: compare planned requirement IDs and acceptance criteria with resulting changed files, tests and verification evidence, and record when task selection changed without approval.

## Relationship and dedup

Related: `inbox/cases/2026-10-13-qhe-report-baseline-cannot-be-replaced-by-scoped-ci-delivery.md` already documents a bounded-delivery scope replacing the owner's theoretical-report baseline; `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` already separates implementation from validation status. This new Candidate is narrower: **authorization and provenance of the agent-generated successor queue during multi-turn recovery**, rather than baseline-completion claims or requirement-level evidence coverage.

## Required follow-up tests

- Replay three consecutive QHE task-selection checkpoints from an immutable root-report snapshot, with and without the proposed re-anchoring gate; audit unapproved priority changes and closure of original acceptance criteria.
- Verify that self-generated B16 follow-ups cannot displace a higher-priority B01–B25 requirement merely through recency or queue order.
- Verify that true blocking dependencies can still be performed after explicit root traceability and priority review; the guard must not force artificial refusal of legitimate prerequisites.
- Do not promote to Canonical from one reported experience and one repo-state observation.

## 2026-10-14 QHE route checkpoint implementation

The previously proposed guard now has a concrete **project-local process implementation**, not just an advisory note:

- QHE docs/qhe-initial-version-route-reanchor-2026-10-14.md traces B01–B25/A01–A10 and separately records verified implementation, hosted validation, field pending and integration state.
- QHE AGENTS.md adds a per-work-unit root-goal re-anchor check and a mandatory review after at most two consecutive authorized work units.
- QHE .uigs/tasks/qhe-initial-version-full-report.json preserves 18 former generated next-unit suggestions as non-authoritative history; the executable queue contains only two named units WU-01 (Guided/Manual compile-to-output) and WU-02 (rich-MKV preservation/embedded ASS), both traced to source requirements.
- QHE branch feat/qhe-five-round-delivery-20261013 at commit dc2e68e98dc4a6f37dc8f8c5241442733004a91f contains the documented checkpoint. No product feature or release was claimed, and these planning edits have not yet proved that direction drift frequency decreases.

Evidence level: process rule implemented in a real repository with task queue transition; effectiveness against a three-step drift recurrence remains TEST-PENDING. This continues to be Candidate, with no Canonical promotion.