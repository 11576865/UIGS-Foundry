# Observation/Test: Descendant visibility and local hidden state are different E2E assertions

Status: **Observation / Test**
Date: 2026-10-03
Project evidence: `11576865/Quick-Automatic-Hardsub-Encoder`, PR #39

## Observation

While adding codec-aware copied-audio guidance, browser smoke tests needed to verify that a warning element's own `hidden` state toggled when the audio policy changed.

The warning lived inside a UI subtree that could itself be hosted inside a currently hidden Guided/Manual container. A Playwright assertion based on `locator.isHidden()` therefore reported the descendant as hidden even when the warning element's own `hidden` property was `false`.

The test was asking the wrong question:

```text
wanted:
  "did this component set its own hidden state correctly?"

measured:
  "is this node currently visible through the entire ancestor layout tree?"
```

Those are not equivalent.

## Reusable test rule candidate

When testing a component embedded in a conditionally hidden, rehosted, tabbed, staged, or disclosure-controlled subtree:

- use rendered visibility assertions when the user-visible outcome is the contract;
- use the element's local state (`hidden`, `aria-expanded`, `data-state`, class, etc.) when testing the component's own state machine independently of its host;
- do not use ancestor-aware visibility APIs as a proxy for local component state;
- when both matter, test them separately.

Representative distinction:

```text
component.hidden === false
        does not imply
locator.isVisible() === true

because an ancestor may still be hidden.
```

## Evidence

PR #39 initially failed its browser UI smoke because the test used `isHidden()` after the shared audio controls had been mounted under a hidden host. The implementation state transition was correct; the assertion conflated local hidden state with effective layout visibility.

The corrected test inspects `element.hidden` for the component-state contract and retains normal visibility assertions elsewhere for actual user-visible surfaces.

This is a single-project Observation/Test and must not be promoted to Canonical from this evidence alone.
