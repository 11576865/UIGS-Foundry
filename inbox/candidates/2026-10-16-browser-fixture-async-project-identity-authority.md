# Candidate — Browser fixtures must preserve application project identity across asynchronous status hydration

Date: 2026-10-16  
Status: Candidate / code submitted / Pending CI  
Scope: browser E2E, visual evidence fixtures, asynchronous project hydration and selection  
Source: [HSR PR #187](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/187), follow-up to [#186](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/186)

## Observation

A Chromium visual regression selected a legitimate project cue but reported `expected=11, actual=null, project=null, corpus=0`. The browser fixture manually assigned `currentProject` after load, while its mocked `/api/status` still returned `project: null`. Production `refresh()` asynchronously calls `fillProject(status.project)`; a late status response therefore could invalidate the injected project and cause the protected cue-selection path to reject the operation. The test failure is not evidence that production must permit selection without a project.

## Candidate rule

For browser test environments, fixture API responses and UI state must agree on identity and ownership of the active domain object. Prefer the real app hydration flow over directly mutating a transient JavaScript global, and await the hydrated identity before exercising user interaction. Preserve production fail-closed checks, and place assertions at the resulting UI interaction rather than reducing validation to a static source-string match.

## Submitted bounded repair

- The HSR browser router returns the same fixture project identity from `/api/status` as from its project-scoped subtitle endpoints.
- The browser harness waits for `currentProject.root === '/qa/fixture'` before entering Layout/Effects, rather than overwriting it manually.
- It preserves deliberate subtitle selection and real user-visible error checks; no project gating was relaxed.
- The same PR revises obsolete UI assertions after a documented product contract change and makes phone-size cue / preview controls accessible without changing the authoring engine.

## Evidence boundary

The previous Chromium run failed with the explicit project-null diagnostic; PR #187 contains the proposed repair but is Pending CI and has no physical Termux/browser device acceptance at time of submission. This is a bounded cause-and-fix hypothesis until an exact-head rerun succeeds. The mock project is **test data**, not production project evidence.

## Deduplication

Queried Foundry for browser fixture/project identity races and neighboring async readiness candidates. The located entries concern storage namespace, batch preflight readiness and preview/audio provenance; none documents the specific conflict between an injected `currentProject` and the authoritative asynchronous `/api/status` response. This remains a Candidate. No Canonical promotion.
