# Candidate / Test: Wait on authoritative interaction state before asserting rendered semantics

Status: **Candidate / regression-test observation**
Date: 2026-10-02

## Incident

An Android renderer-backed visual evidence test intermittently failed after the production renderer had already reported `Preview subtitle`. The remaining failure was a 10-second timeout while repeatedly polling the Compose semantics tree for the position manipulation rod.

The product code under test had not changed in the failing PR, and the same visual test had passed in earlier runs. The unstable boundary was therefore the test synchronization path: it used presentation semantics as both readiness signal and final assertion.

## Reusable rule

For asynchronous UI whose presentation is derived from an authoritative state/registry:

1. wait for the authoritative source of readiness (domain state, interaction registry, renderer state, etc.);
2. after readiness is observed, let the UI reach idle;
3. then assert that the expected semantics/pixels are rendered.

Do not use a rendered semantics node as the sole readiness source when that node is downstream of additional asynchronous composition/layout work.

Conceptually:

`producer state ready -> UI idle -> presentation assertion -> capture`

rather than:

`poll presentation until producer and presentation happen to settle together`.

## Applied fix

The ASS Workbench renderer-backed visual capture now:
- waits up to 30 seconds for `InteractionOverlayRegistry` to contain `position-1-pos`;
- calls Compose `waitForIdle()`;
- asserts the rod semantics node is displayed;
- preserves the existing short compositor settle before screenshot capture.

This does not weaken the evidence contract: the final rendered node is still asserted. It only separates readiness from presentation verification.

## Why this may generalize

The pattern applies to Compose, SwiftUI, React, web component tests, renderer-backed editors, and any system where a UI element is generated from asynchronous producer state. It helps distinguish product failures from test-contract races.

## Evidence boundary

This is based on one intermittent renderer-backed instrumentation failure and its targeted stabilization. It does not establish that all semantics-tree waits are wrong; direct semantics waiting remains appropriate when the semantics node itself is the authoritative condition.

Do not promote to Canonical from this observation alone.
