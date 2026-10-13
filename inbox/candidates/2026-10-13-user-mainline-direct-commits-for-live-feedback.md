# Candidate / explicit execution preference: publish future engineering updates directly to main for live feedback

Date: 2026-10-13
Status: **User-authorized workflow preference; Candidate for cross-project method, not Canonical**
Source: explicit user instruction in HSR / UIGS discussion
Scope: subsequent engineering updates requested by this user across their repositories, where repository access and branch policy permit; HSR was the immediate trigger

## Explicit request and rationale

The user instructed: **“以后的更新都直接在主分支里进行，不然我无法实时反馈，uigs”**.

Interpretation for future agent execution: **main-first, directly visible commits**, not the previously used feature-branch → draft PR → wait CI → merge sequence. The purpose is to make each coherent, bounded piece of active engineering progress immediately visible on the authoritative project branch so the user can inspect and give prompt, iterative feedback. This instruction is prospective and does **not** retroactively invalidate historical feature PRs or their CI evidence.

This is a user-specific execution preference and an explicit override of *branch choice* for future work; it is **not** evidence that untested changes are safe or that the repository's UI deploy automatically refreshes upon push.

## Operational execution contract

1. Read the current `main` and project task state first; preserve changes from other collaborators and avoid replacing a newer main snapshot.
2. Implement one coherent feature slice or repair and perform available fast, relevant local/source tests **before** publishing when practical.
3. **Commit and push directly to `main`**, in small, self-contained checkpoints that the user can inspect. Report the resulting main commit SHA or link; do not substitute a detached feature PR as the only user-visible result.
4. Start/observe CI as appropriate. If asynchronous checks are still running, report **Pending CI**, not “verified” or “deployed”; a visible CI failure is repaired with a subsequent bounded mainline commit rather than silently left unacknowledged.
5. Do not create or rely on feature branches or PRs **by default** for ordinary approved engineering updates. Exceptions require a concrete blocker (e.g. enforced branch protection / missing permission, sensitive or high-risk irreversible operation) or a newer explicit user instruction; surface the blocker instead of bypassing protection or secretly reverting to a branch-only delivery.
6. Make failures recoverable: preserve prior working artifacts, prefer additive/migratable changes, and avoid force-pushing or rewriting shared `main` history. When a change has unusually large blast radius, split it into reversible incremental commits and record validation limits.
7. “Live feedback” means changes are discoverable in repository `main` as they are submitted. **Runtime UI freshness requires separately verified deployment/build behavior**; a pushed main commit is not itself proof of a fresh user-facing deployment.
8. Each work unit retains the UIGS Intake Check and creates or updates a Foundry Observation/Candidate/Bug/Case/Test only when warranted; no automatic Canonical promotion.

## Relation to existing UIGS policy

- `governance/AGENT-EXECUTION.md` is currently **Canonical**. Its durable checkpoint, bounded-work-unit, resumability, asynchronous-validation, and evidence-level requirements remain in force. A pushed commit on main is a durable checkpoint just as a pushed feature commit would be; mainline publication replaces the ordinary branch/PR submission location, **not** the need for verification or task handoff.
- `inbox/candidates/2026-10-02-branch-submission-default-execution-boundary.md` is a historical candidate incorporated into that Canonical on 2026-10-07. The user's new instruction changes the preferred **ref**, not the prohibition on unbounded CI polling.
- This candidate records an **explicit user-specific operating directive** and a possible generalizable “feedback-driven mainline checkpoint” pattern. It does not itself modify Canonical governance or authorize relaxing branch protections. Do not generalize the preference to other users without evidence.

## Intake evidence and limits

Trigger: user feedback that delayed branch/PR publication obstructs timely review. This is a reported workflow constraint, **not** a measured usability experiment or an observed CI failure. It should remain Candidate until independently studied; it nevertheless takes immediate precedence as this user's workflow instruction for upcoming tasks.

Acceptance for subsequent work: latest `main` commit link and status are reported promptly; no branch-only completed work is described as deployed/current main; CI Pending/Failed/Passed states are explicit; user can review intermediate mainline checkpoints. Canonical unchanged.
