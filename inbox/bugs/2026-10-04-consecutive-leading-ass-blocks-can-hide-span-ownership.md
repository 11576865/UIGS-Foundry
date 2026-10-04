# Bug: Consecutive leading ASS override blocks can hide later-span ownership conflicts

Date: 2026-10-04
Status: Bug
Lifecycle: recorded
Scope: ASS semantic parsing / ownership guards / generated FX composition

## Symptom

ASS Workbench Android PR #93 still failed after its exception-type assertions were corrected.

The remaining failing test was:

`AssFxCompositionTest.glowRejectsKaraokeSpanAlphaButLeadingBaseAlphaRemainsAllowed`

The conflicting input was:

`{\\alpha&H40&}{\\k20\\1a&HFF&}A`

The generated Glow layer owns alpha semantics and is expected to reject the later Karaoke span's `\\1a`, but no exception was raised.

## Root cause

The ownership guard computes a `leadingEnd` from `leadingOverridePrefix(text)`.

That helper treats every consecutive override block at the beginning of the Event as one leading prefix. Therefore both:

- `{\\alpha&H40&}`
- `{\\k20\\1a&HFF&}`

are classified as part of the leading prefix.

The later `\\1a` is then excluded by the guard's `tag.start >= leadingEnd` span-conflict test even though semantically the Karaoke block is already a later authored span and re-owns alpha.

This is a structural boundary error: lexical adjacency of override blocks is not equivalent to Event-wide ownership.

## Reusable rule

Do not use a generic "all consecutive leading override blocks" helper as a semantic ownership boundary.

Where ownership differs between Event-wide base overrides and later span/Karaoke overrides:

1. determine the semantic span boundary explicitly;
2. stop the Event-wide region when Karaoke timing or other span-start semantics begin;
3. inspect later direct tags even if their block is textually adjacent to the first override block;
4. keep lexical prefix extraction separate from semantic scope classification.

## Evidence

- project: `11576865/ASS-Workbench-Android`
- PR: #93
- revision: `a81d4934dce58feb993860057582751ffa51bc0b`
- failing workflow: Android CI #929
- failing test: `glowRejectsKaraokeSpanAlphaButLeadingBaseAlphaRemainsAllowed`
- implementation: `requireCompositionOwnershipCompatible` + `leadingOverridePrefix`
- deduplication: searched UIGS-Foundry for consecutive-leading-block / Karaoke ownership-boundary equivalents; no direct duplicate found

This Bug record is evidence. It is not Canonical.
