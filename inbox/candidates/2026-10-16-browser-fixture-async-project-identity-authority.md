# Candidate — Browser fixtures must preserve application project identity across asynchronous status hydration

Date: 2026-10-16  
Status: Candidate / HSR PR #187 merged / exact-head CI passed / device acceptance pending  
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

## Exact-head CI and integration outcome

PR #187 was merged into HSR main as `348ac1295f91e1ac9ccb4c3d4d10ed998e12c386` from `afba6504bd43ec99fc3507ca56c276d9b3afe9da`. The exact-head checks succeeded:
- General tests (Python 3.11, 3.12, 3.13): GitHub Actions run `38851017618`
- Seven ASS requirements: `38851017634`
- Chromium visual evidence and real FastAPI + FFmpeg/libass preview E2E: `38851017631`

The CI repair uncovered four distinct fixture mistakes without weakening production identity requirements:
1. A mocked `/api/status` project contradicted a manually injected `currentProject`.
2. A generic `{"ok":true}` settings-save mock omitted `project`, allowing an autosave to null the active UI identity. The real UI now refuses partial/foreign project receipts and preserves its current project.
3. An initial Review subtitle fetch after `fillProject` was counted as an explicit Review → Layout duplicate. Tests now wait for initial hydration before measuring workflow-owned requests.
4. The real video E2E mocked browser project state but never opened a server-side project. Its fixture now persists a temporary ProjectConfig, real decoded FLAC and manifest-backed cue, calls `_set_active`, and requires the API's `X-HSR-Preview-Audio: project` evidence rather than bypassing backend ownership.

The gradient background fixture additionally needed an explicit force-refresh because the chosen project root was already active; production draft-preservation remained intact.

## Evidence boundary

These results validate the bounded synthetic CI scenarios and artifact checks, **not** physical Android/Termux playback, the user's real voice asset, perceptual sound sync, or the screenshot-specific tactile experience. Candidate remains Candidate pending cross-project corroboration. No Canonical promotion.

## Deduplication

Queried Foundry for browser fixture/project identity races and neighboring async readiness candidates. The located entries concern storage namespace, batch preflight readiness and preview/audio provenance; none documents the specific conflict between an injected `currentProject` and the authoritative asynchronous `/api/status` response. This remains a Candidate. No Canonical promotion.
