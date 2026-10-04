# Candidate: Look-ahead depth and backend concurrency should be independent controls

Date: 2026-10-04
Status: Candidate
Domains: prefetch, media pipelines, constrained accelerators, scheduling, backpressure

## Problem

A UI may benefit from preparing multiple future items while its backend can safely process only one expensive generation job at a time.

Treating look-ahead depth as equivalent to request concurrency causes two bad extremes:

- depth > 1 fans out competing GPU/model requests;
- forcing concurrency = 1 is misinterpreted as allowing only one future item to be prepared.

## Candidate rule

Separate **window depth** from **execution concurrency**:

1. expose or compute the desired look-ahead window independently;
2. create future work entries for the whole window so state is observable;
3. execute expensive backend generation serially when the backend is single-concurrency;
4. after N+1 succeeds, continue to N+2 until the window is filled;
5. when the consumer advances, consume the prepared N+1 and refill the tail;
6. if an earlier prefetched dependency fails, stop the later chain rather than fan out work that may no longer be useful;
7. allow depth 0 without changing the state-machine contract—next content is then generated only on demand.

## Evidence

Character Voice Reader PR #8 preserves the existing user-configurable `prefetchAhead = 0..4` while rebuilding resilient playback.

The queue can hold a multi-item look-ahead window but serializes TTS generation for the single-engine/single-GPU model. Regression coverage verifies:

- depth 2 does not issue N+1 and N+2 concurrently;
- depth 0 disables look-ahead;
- failure of N+1 prevents N+2 fan-out;
- advancing refills the configured window.

## Provenance

- project: `11576865/Character-Voice-Reader`
- replacement PR: #8
- revision: `a00f42ff17250bdb6ad8335cbbe1334b9e43aad1`
- evidence at intake: implementation + direct Node queue tests authored; asynchronous CI pending
- deduplication: searched Foundry for sequential prefetch, single-GPU look-ahead, and failure fan-out equivalents; no direct duplicate found

This is a Candidate only. It is not Canonical.
