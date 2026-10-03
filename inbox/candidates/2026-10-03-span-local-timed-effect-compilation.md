# Candidate: Prefer span-local time compilation when layout measurement is unnecessary

Status: candidate
Date: 2026-10-03
Domains: authoring-tools, text-animation, subtitle-rendering

## Summary

For timed text effects, splitting one logical line into many independently positioned objects is not always necessary.

When the source format already has stable span boundaries and per-span timing, an authoring tool can often compile an effect directly into those spans:

- preserve the original line as one canonical object;
- derive each span's absolute-in-event timing from existing timing metadata;
- write span-local base state plus time-scoped transforms;
- let normal text layout keep glyph positions authoritative;
- avoid synthetic width measurement and per-span position reconstruction.

This can reduce layout drift, font-metric dependence, object explosion, and synchronization bookkeeping.

## Candidate rule

Before generating one positioned object per syllable/word/token for an effect:

1. Check whether the format already provides stable span boundaries and timing.
2. If the effect can be expressed as span-local style/transform changes, prefer compiling into the existing object.
3. Use event-local absolute timing for the generated transforms so spans remain synchronized with the source timing model.
4. Reject timing modes whose semantics differ from the compiler's assumptions instead of coercing them.
5. Reject existing controlled effect syntax when safe composition rules are not defined; do not silently layer a generated transform over an ambiguous existing stack.
6. Generate separate positioned objects only when the effect actually needs independent geometry, z-order, motion paths, or origins.

## Evidence

ASS Workbench Android PR #83 adds a first karaoke FX compiler that:

- parses existing `\k / \kf / \ko` syllable timing;
- computes cumulative millisecond windows inside the Event;
- inserts per-syllable alpha/blur `\t(...)` reveal transforms into each karaoke marker block;
- preserves the line as one canonical ASS Event, so normal ASS layout retains the correct glyph positions;
- rejects `\kt` because its absolute karaoke timing semantics differ from the cumulative model used by this compiler;
- rejects pre-existing alpha/blur/transform syntax in the controlled spans instead of guessing composition precedence.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #83
- evidence level: implemented domain compiler + regression tests; CI and device visual evidence pending at intake time
- deduplication: searched UIGS-Foundry for equivalent span-local timed-effect / glyph-measurement guidance; no direct duplicate found
- status rationale: reusable authoring heuristic, but not yet validated across multiple timed-text formats

This is a Candidate only. It is not Canonical.
