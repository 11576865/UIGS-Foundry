# Candidate: Mutually exclusive mode controls must not remain visually active

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, interaction-state, testing
Evidence type: direct user-observed UI inconsistency plus code/test gap

## Summary

When a control only applies to one mutually exclusive mode, leaving that mode must remove both its operational availability and its active visual affordance.

A control that is technically disabled but still looks like an ordinary active input is an interaction-state defect, because the user must infer hidden state from unrelated mode selectors.

## Evidence

In Quick-Automatic-Hardsub-Encoder, the media workspace supports three mutually exclusive rate modes:

- fixed quality (CRF / CQ);
- target bitrate;
- target size.

The implementation did set the target-size fields to `disabled` when another mode was active, but the workspace styling did not visually distinguish disabled text/select controls strongly enough. The target-size box therefore still appeared active to the user while fixed-quality mode was selected.

The existing Playwright regression only tested entering size mode:

- size field becomes enabled;
- quality field becomes disabled.

It did not test the reverse transition from size back to quality, so a stale visual/semantic state could escape regression coverage.

## Candidate rule

For controls whose relevance is conditional on an exclusive mode:

- inactive controls must not look equivalent to active controls;
- prefer removing irrelevant controls from the active decision surface when they have no value in the current mode;
- keep the underlying controls disabled as a semantic and programmatic backstop;
- disabled controls that remain visible must have an explicit inactive visual treatment;
- regression tests must cover mode transitions in both directions, not only entry into the alternate mode;
- state-dependent tests should check both semantics (enabled/disabled) and presentation (visible/hidden or clearly inactive).

## Scope

Applies to codec/rate modes, export modes, editor tool modes, mutually exclusive configuration strategies, and other stateful parameter panels.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- source: direct user report, 2026-10-02
- implementation follow-up: PR #32
- evidence level: direct user-observed affordance failure plus identified regression-test asymmetry

This is a Candidate only. It is not Canonical.
