# Test: QHE P2 source-owned per-audio must-copy intent is enforced by authoritative compiler

Date: 2026-10-14
Status: PASS — bounded Node schema-v4 compiler and actual Chromium production UI, real output packet evidence pending
Product: Quick-Automatic-Hardsub-Encoder PR #105
Tested code SHA: 38d4b04e8b1edfac99dc3116f4931c310b075d08
CI: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38580653413
Requirements: owner R19 §03/§16 P2; R24 §05/§11; B02/B05/B06/A02

## Dedup

Existing Foundry Candidate `inbox/candidates/2026-10-12-qhe-per-output-audio-track-intent-and-encoder-capability-layers.md` describes the desired separate per-stream audio intent, codec capability and non-silent fallback; existing Test `inbox/tests/2026-10-13-qhe-heterogeneous-audio-plan-and-source-owned-ui.md` proves mixed Copy/Transcode/Drop output plans and copied FLAC packet hashes under separate synthetic fixtures. This new Test is narrower and distinct: it proves a **user-explicit, source-bound mandatory Copy guard** prevents a later plan from silently removing or recoding a protected source audio track. It does not propose a new audio domain model or promote Canonical.

## Product action and compiler boundary

- Existing per-track UI adds an explicitly opt-in `mustCopyAudioOrdinals` checkbox and a bound `audioKeepSourceIdentity` field. The data remains in the sole existing schema-v4 form/task, not a parallel task authority.
- Selecting must-copy changes only that selected row to Copy. If the row later becomes AAC, Opus, FLAC or Drop with the lock still set, authoritative `compileTask` raises a conflict and does not authorize execution. Missing or foreign source identity, duplicate/invalid audio ordinals also reject. The output plan and task review disclose the chosen lock.
- Canceling a global audio-plan reset leaves locks intact; confirmation explicitly releases them. Source change invalidates the old per-source lock.
- Other, unlocked audio streams remain eligible for explicitly selected transformations; source FLAC a:0 Copy + source AAC a:1 AAC encode is one supported plan.

## Acceptance at exact head

Official `compileTask` unit tests validate mixed audio output plan, protected Copy, Drop/Transcode refusal, wrong source, duplicate/invalid ordinals and explicit unlock.
Real Playwright/Chromium production workbench clicks the protected FLAC checkbox, sets the other track to AAC, inspects and runs the actual compiled v4 task through controlled backend hooks; then deliberately changes the protected track to AAC and verifies refusal, checks reset cancel/confirm and source-identity drift. Workflow `38580653413` SUCCESS. Test frontend `38580653495` and UIGS Evidence Coverage `38580653198` SUCCESS.

## Unproven properties

The lock asserts track inclusion and Copy codec behavior in task compilation. It does **not** by itself prove packet-for-packet identity, timeline mapping, audio priming/sync, metadata/disposition preservation, installed-device playback or every Windows/Android/Web execution path. Existing WU02 synthetic FLAC packet hash proof is independent and not the same exact locked-task run. Thus R19 P2/A02 remains incomplete, and the test must not be relabeled as full packet preservation.
