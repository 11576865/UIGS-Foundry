# Candidate: Interactive previews over expensive backends need explicit backpressure and stale-result control

Status: candidate
Date: 2026-10-03
Domains: interaction, async-systems, media-processing, native-bridges, performance

## Summary

Interactive UI gestures can generate requests much faster than an expensive execution backend can satisfy them. A timeline scrubber backed by FFmpeg/FFmpegKit is one example: pointer movement can produce dozens of desired preview positions while each decoded frame may require process/session startup, seek and decode work.

A correct implementation should not translate every pointer event into an unconstrained backend job.

## Observed case

Quick-Automatic-Hardsub-Encoder PR #40 adds source-frame previews to the media timeline across Web, Windows Native and Android Native.

The implementation uses several separate controls:

- debounce cursor preview requests rather than decoding every pointer event;
- deduplicate requests for the same timestamp;
- serialize expensive frame extraction so Web/native backends are not flooded with concurrent FFmpeg work;
- keep a bounded frame cache and evict old entries;
- separate cursor-preview generation from requested-vs-actual boundary-preview generation;
- invalidate stale results when the source/timeline generation changes;
- avoid issuing new preview work while a production encode task owns the backend;
- retain backend authority: preview results do not replace execution-time boundary validation.

## Candidate rule

For high-frequency interaction backed by expensive asynchronous/native work:

1. Treat interaction rate and backend service rate as different domains.
2. Add a small debounce or coalescing window at the presentation boundary.
3. Deduplicate identical in-flight work.
4. Serialize or explicitly bound concurrency when the backend/session model is not safely parallel.
5. Cache only a bounded working set; release resources on eviction.
6. Attach results to a source/generation identity and discard stale completions.
7. Separate independent preview purposes when one should not invalidate another.
8. Suspend opportunistic preview traffic while a higher-priority owned task is using the backend.
9. Test the state/control contract, not only whether one preview call succeeds.

The exact debounce, cache size and concurrency limit are implementation-specific. The reusable requirement is explicit backpressure plus stale-result ownership.

## Evidence

Source project: `11576865/Quick-Automatic-Hardsub-Encoder`

Implementation:
- PR #40, merged as `09b67ee4ed774fa258365e9aee2717e23855efca`;
- timeline frame cache bounded to a small working set;
- pending-request deduplication and serialized extraction queue;
- cursor and boundary preview generations are independent;
- timeline/source generation invalidates stale results;
- preview requests are suppressed while the media backend is busy with owned production work.

Validation:
- source-frame preview wiring test covers Web, Windows Native and Android Native;
- Web frame-extraction unit test checks exact seek and bounded scaling;
- real FFmpeg integration extracts distinct source frames at different timestamps;
- Playwright exercises cursor preview and requested-vs-actual boundary images;
- frontend, Windows smoke, Android compile and UIGS Evidence Coverage passed before merge;
- all main push workflows, including Android/Web build and deployment, passed after merge.

## Relationship to existing UIGS knowledge

This is distinct from the existing requested-vs-realizable-boundary Candidate. That record concerns semantic honesty about constrained edit values. This record concerns the asynchronous execution topology needed to make interactive previews safe and responsive when the backing operation is expensive.

This is a Candidate only. It is not Canonical.
