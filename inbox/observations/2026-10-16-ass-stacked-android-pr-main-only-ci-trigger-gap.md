# Observation — Stacked Android PR to a feature base has no default CI trigger

Date: 2026-10-16
Status: Observation / branch validation workflow committed / run result Pending
Project: https://github.com/11576865/ASS-Workbench-Android
Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Implementation branch: `feat/fixed-v11-event-grid-20261016`
Validation source commit: `0c4b62980b3f305defefe967295587ed77936a09`
Later repository checkpoint/PR head: `98c87f1b6ceb70f9edfe35ffbc9e3acea269f4ba`

## Concrete observed gap
The production repository's `.github/workflows/android.yml` and `emulator.yml` both declare automatic `push.branches: [main]` and `pull_request.branches: [main]`; they also allow workflow_dispatch. The current FIXED UI PR #149 deliberately targets stacked R3 feature PR #148's branch, not main. Therefore **the existing automatic PR trigger does not match**. Previous calls to `fetch_commit_workflow_runs` for the stacked feature head returned zero workflow runs, and combined commit statuses were empty. This proves **only absence of returned PR-triggered evidence**, not a build failure or successful compile.

## Product-side bounded mitigation submitted
Added `.github/workflows/fixed-v11-validation.yml` exclusively on the FIXED V1.1 feature branch. It listens for `push` to its exact branch and optional manual dispatch and runs targeted Java 21 / Android SDK 36 / Gradle 9.7.1 `:app:compileDebugKotlin`, `:app:compileDebugAndroidTestKotlin` and core/app JVM tests. No APK or retained artifacts. Existing mainline Android CI and Emulator workflows, PR base, renderer and SPATIAL sources unchanged.

One immediate exact-head status query for commit `0c4b6298` returned no PR-triggered runs and no combined statuses. The GitHub connector's commit workflow lookup is specifically filtered to `pull_request` trigger; it cannot by itself establish branch-push run IDs or conclusions. **Branch validation run start/completion is UNKNOWN** at this checkpoint. More source commits can supersede pending runs, hence the final head still requires authoritative CI evidence.

## Reusable, bounded observation
Before interpreting “0 workflow runs” on a stacked PR, inspect the actual workflow event filters and the branch against which it is based. A PR based on another feature branch may never trigger main-only checks. A branch-scoped fast validation can bridge compile feedback without pretending to satisfy all emulator/release gates, but must be measured on the precise tested SHA. Avoid changing PR base to main merely to force checks when that would expand the diff and defeat review isolation.

## Evidence limits and follow-up
- The specific branch workflow has been committed; it is **not confirmed as executed or passed**.
- No Android SDK/Gradle/physical emulator was available in the current container; no local build was performed.
- Follow-up needs authoritative Actions run ID / job logs. If failed, one bounded repair. Emulator visual/IME and real editor draft remain separate pending gates.
- Closest related Foundry Candidate: `inbox/candidates/2026-10-14-stacked-draft-pr-ci-validation-cadence-and-verified-heavy-cache.md`, which concerns QHE heavy matrix gating and cache cost. This Observation is narrower: event-branch filter mismatch on an Android stacked draft PR.
- No Canonical changes from a single incident.
