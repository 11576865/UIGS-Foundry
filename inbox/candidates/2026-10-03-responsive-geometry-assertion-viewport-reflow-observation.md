# Observation: Responsive geometry assertions can race viewport reflow

Status: **Observation / test-stability signal**
Date: 2026-10-03
Project evidence: `11576865/MKV-Fast-Muxer`, PR #59 CI attempt 1

## Observation

A browser E2E run failed in an existing responsive-layout scenario before reaching the newly added compatibility-evidence scenario.

The test changed the viewport back to 390 px and immediately measured:

```text
previewStage.getBoundingClientRect().width
/
previewStage.getBoundingClientRect().height
```

The resulting ratio was `NaN`, which implies a transient `0 / 0` geometry measurement. The same unchanged commit passed on workflow retry, including the responsive scenario and all later tests.

This is evidence of a timing-sensitive test condition, not evidence of a confirmed product layout defect.

## Reusable observation

For responsive browser tests that change viewport size, disclosure state, or CSS-driven visibility and then assert exact geometry:

- event completion such as `setViewportSize()` or a toggle click does not necessarily prove that the target has reached a non-zero stable layout box;
- avoid dividing dimensions until both width and height are explicitly observed as greater than zero;
- synchronize on the semantic geometry condition being asserted, for example “visible with non-zero bounding box and stable aspect ratio”, rather than only on the preceding interaction;
- if a failure disappears on an unchanged retry, retain the first failure as a flake signal rather than silently treating it as product evidence.

A stronger assertion pattern is:

```text
change viewport / disclosure
  -> wait until target is intended-visible
  -> wait until bounding box width > 0 && height > 0
  -> measure ratio / adjacency / overflow
```

## Evidence limits

This was observed once and passed on immediate workflow retry without code changes. It should not be promoted to a general Bug or Canonical rule without repeated evidence across projects or browsers.
