# Candidate: Compile unsupported spatial gradients into disjoint canonical bands

Status: candidate
Date: 2026-10-03
Domains: authoring-tools, rendering, text-effects, geometry

## Summary

A source format may support opacity and clipping but not a true per-pixel opacity gradient for arbitrary text. An authoring tool can still offer a spatial fade without adding a proprietary renderer by compiling the requested gradient into multiple ordinary objects:

- duplicate the same visual object into a bounded number of layers;
- assign each duplicate a non-overlapping spatial clip band;
- sample the desired opacity curve once per band;
- preserve the source format as the canonical output.

This is an approximation, but it is portable and inspectable.

## Candidate rule

When compiling a spatial effect into fixed screen-space bands:

1. Make the approximation explicit and bound its expansion cost.
2. Use disjoint clips so generated layers do not alpha-accumulate over one another.
3. Intersect generated bands with any compatible pre-existing rectangular clip instead of overwriting the source restriction.
4. Translate compatible source clip geometry together with translated companion geometry.
5. Reject moving objects when the generated mask cannot follow the same motion semantics.
6. Reject incompatible clip or opacity controls whose composition precedence is not defined.
7. Never silently truncate a user-requested spatial extent at the canvas boundary; report the available extent and require an explicit correction.
8. Show the estimated generated-object count before a large batch is committed.

## Evidence

ASS Workbench Android PR #84 implements reflection fading by compiling one reflected Event into multiple ASS Events with disjoint rectangular `\clip` bands and progressively lower `\alpha`.

The implementation also:

- intersects bands with one supported leading rectangular source clip;
- translates that source clip with the reflection's Y offset;
- rejects `\move` because the band masks are fixed in screen coordinates;
- rejects vector/iClip, extra inline clips, and existing alpha/fad/fade controls rather than guessing precedence;
- rejects fade depth that would cross the available screen boundary instead of silently shortening it;
- exposes estimated companion-Event expansion in the UI;
- includes domain regression and production mpv/libass runtime capture coverage.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #84
- evidence level: implemented + domain tests + renderer-backed instrumentation added; final CI state pending at intake time
- deduplication: searched UIGS-Foundry for equivalent disjoint clip-band gradient / screen-space motion-safety guidance; no direct duplicate found
- status rationale: reusable rendering/authoring technique, not yet broad enough for Canonical

This is a Candidate only. It is not Canonical.
