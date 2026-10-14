# Bug: eagerly formatted absent cut prediction taints unrelated time inputs

Date: 2026-10-14
Status: Bug / fixed, exact-head production Chromium CI PASS
Product: QHE B08/A04 WU-04
Proof: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38562651510

## Symptom

In the real Chromium Guided/Manual workbench, a user inspected a Stream Copy timeline, changed the selected media source (making prior keyframes stale), then deliberately switched to transcoded trimming. The actual `taskRun` click did not reach `compileTask` and appeared inert. Browser's native `:invalid` query showed BOTH `start` and `end` text fields invalid, carrying `Cannot read properties of null (reading 'toFixed')` as their custom validation messages.

## Root cause

`syncCopyStrategy` chose a status string with a JavaScript object literal whose `predicted-early` field eagerly evaluated `assessment.delta.toFixed(3)` even while `assessment.state==='unknown'` and `delta === null`. This error propagated through `syncWaveformMarkers` into the catch of `normalizeTimeControl`, which incorrectly treated a presentation bug as invalid user time input via `setCustomValidity(error.message)`. Form native validation therefore prevented submission.

## Contained fix

QHE commit `501974713ad6ee3fc184b20bb1fbb2ed93fc5396` changes status selection to lazy conditional evaluation, formatting the numeric delta ONLY when state is `predicted-early`. Model and real browser source-drift / user-mode-switch test is rerunning at exact head.

## Generalizable guard

Do not eagerly compute branch-specific nullable values in object literals used as state maps. UI presentation exceptions must not be swallowed by unrelated input-parsing catch blocks that set persistent form validity errors. A failure in an optional visualization may otherwise silently disable a critical user workflow.

Evidence boundary: fix submitted, CI result must be read before marking recovered. Do not auto-promote a single bug to Canonical.

## Verified recovery

`501974713ad6ee3fc184b20bb1fbb2ed93fc5396` passed the QHE WU04 model plus actual Chromium workbench click/submit acceptance in workflow `38562833192`. The test deliberately changes media source after learning keyframes, observes an UNKNOWN prediction rather than false carryover, cancels then accepts an explicit switch to transcoded trim, confirms semantic IN/OUT preservation, and observes the official shared compiler task reaching its controlled run hook. The previous input validity blockage no longer occurs. The verification does not inspect actual video packet timestamps or establish A04 physical film acceptance.
