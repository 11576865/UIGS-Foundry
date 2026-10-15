# Observation: One durable integration mainline instead of accumulating suspended feature branches

Date: 2026-10-16
Status: Observation — user-approved project workflow; not a Canonical rule
Project: https://github.com/11576865/MKV-Fast-Muxer

## Trigger and confirmed action

User explicitly rejected “分支叠分支的空中楼阁” for ongoing 1.0 joint UI/domain development and requested all changes land in `main`. Existing Draft PR #156 was checked at its exact head `c97928f5af4c94729e652d3aa720acb66bec5477`: project build and complete Chromium mux E2E had concluded successfully. PR was marked ready then merged into `main` at merge commit `04b2c4144332fc3af747fef7f832a9d455769844`.

Subsequent bounded R1 commits to `main` added verified scanned attachment stream indices, semantic selection/read-only evidence for chapters/tags, an explicit click path from scanned attachment to the **pre-existing** source attachment inspector, presentation, and test assertions. UI events are routed to the existing object editor; no secondary write-capable state is introduced. These new direct-main commits still require checking push-triggered CI; a successful earlier PR is not evidence for newly pushed commits.

## Reusable design/delivery consideration

For a project where the user wants a single continuously accumulating product, an indefinitely unmerged Draft PR can create the illusion of progress while the actual published mainline remains stale. Close genuinely verified upstream work before starting dependent features. If the user explicitly approves direct-main development, preserve per-commit acceptance boundaries, run exact-commit CI and fix failures directly, and avoid claiming a deploy succeeded without evidence. This is a context-dependent execution policy; code review and protected branches may be appropriate in other organizations.

## Dedupe

Foundry search: existing `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md` concerns preview/mainline delivery gaps in a different project, while `UIGS_分支提交是异步CI的默认执行边界` concerns async CI boundaries. This entry records explicit rejection of stacked feature branches while **preserving exact-main-commit verification**; do not automatically modify Canonical policy.

## Open acceptance

The newly committed R1 selection/editor integration was not yet independently verified by completed push-triggered Chromium E2E in this task. Product 1.0 release gates remain open; the only claim here is mainline inclusion of the bounded change.
