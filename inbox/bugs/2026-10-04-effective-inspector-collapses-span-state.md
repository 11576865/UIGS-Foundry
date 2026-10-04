# Bug: Event-wide effective-value summaries can collapse span-local ASS state

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: effective-state inspection / ASS override semantics / preview targeting

## Symptom

A scalar “effective value” inspector can report the last matching override found anywhere in an ASS Event as though that value described the whole Event.

For mixed-span content such as:

`{\fs56}A{\rAlt}B{\fs80}C`

a last-tag implementation can report `80`, erasing the fact that the first span starts at 56 and later spans may reset or override the state again.

The same failure mode becomes more dangerous when downstream logic consumes the summary as geometry/layout truth.

## Additional failure

A lexical ASS scanner may intentionally expose nested tags inside constructs such as:

`\t(0,500,\fs80)`

for syntax highlighting and diagnostics.

If a semantic inspector treats every lexical tag as a direct top-level override, the transform target can masquerade as an immediately active static value.

## Mitigation implemented

ASS Workbench Android PR #99 now:

- defines effectiveValue as the initial rendered span rather than an Event-wide scalar claim;
- marks properties span-dependent when later spans or transforms can change them;
- resolves leading `\rStyle` against an exact referenced Style;
- fails closed on missing Style references;
- filters lexical tags by override-block parenthesis depth before using them as direct top-level semantics;
- decouples preview anchor resolution from the scalar effective-value summary.

## Reusable lesson

An Event that contains span-local formatting does not necessarily have one meaningful scalar “effective value”.

Any inspector or downstream consumer should state which scope it represents: initial span, current span, time-dependent state, or a conservative summary. It should not silently collapse those scopes.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #99
- evidence level: concrete semantic defect + downstream preview risk + regression coverage
- deduplication: searched UIGS-Foundry for effective-value span collapse, style reset inspection, and Event scalar summaries; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
