# Candidate: Async playback sessions should combine active cancellation with revision fencing

Date: 2026-10-04
Status: Candidate
Domains: async state machines, media playback, network generation, cancellation, stale-result isolation

## Problem

AbortController or equivalent active cancellation is necessary but not sufficient for correctness in an asynchronous playback/generation pipeline.

A request may already be completing, a backend may not observe cancellation promptly, or a callback may arrive after the user has jumped, stopped, retried, or changed source. If acceptance is based only on whether cancellation was requested, stale work can still mutate the current playback session.

## Candidate rule

For user-visible asynchronous playback/generation sessions:

1. keep active cancellation for resource cleanup and responsiveness;
2. also maintain a monotonic generation/session revision;
3. every produced result is accepted only if its captured revision still equals the current revision;
4. user actions that invalidate pending work (jump, source change, stop, retry) advance the revision before accepting any later result;
5. keep playback-target revision separate when the current target can advance without invalidating the whole generation context;
6. an error state should preserve the current target when recovery is possible, rather than clearing all state or silently skipping content;
7. manual retry creates a new revision so late responses from the failed attempt cannot win.

This makes cancellation an optimization/cleanup path and revision equality the final correctness fence.

## Evidence

Character Voice Reader PR #8 rebuilds Online Reader v1 on current main with:

- `generationRevision` and `playbackRevision`;
- AbortController cancellation of ReaderQueue-owned requests;
- stale-result rejection after jump/stop/retry;
- explicit `error` state retaining the failed segment;
- one automatic retry followed by explicit manual recovery.

## Provenance

- project: `11576865/Character-Voice-Reader`
- superseded PR: #5
- replacement PR: #8
- revision: `a00f42ff17250bdb6ad8335cbbe1334b9e43aad1`
- evidence at intake: implementation + direct Node regression suite + browser regression updates authored; asynchronous CI pending
- deduplication: searched Foundry for generation/playback revision, AbortController stale-result, retry/error target-retention equivalents; no direct duplicate found

This is a Candidate only. It is not Canonical.
