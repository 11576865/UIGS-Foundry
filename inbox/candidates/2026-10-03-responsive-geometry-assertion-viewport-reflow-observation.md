# Observation: Responsive geometry assertions can race viewport reflow

Status: **Bug / reusable E2E synchronization failure**
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


## Repeated evidence and fix — MKV-Fast-Muxer PR #60

The same `preview ratio at 390: NaN` failure occurred again on the merged `main` run for PR #59, so the condition was no longer only a one-off flake signal.

Root cause analysis showed a specific synchronization race:

```text
setViewportSize(390)
  -> test immediately checks current visibility
  -> matchMedia change handler has not yet re-initialized phone disclosure
  -> test may decide no expand click is needed
  -> handler then marks preview collapsed
  -> geometry is measured as 0 × 0
  -> 0 / 0 => NaN
```

PR #60 fixes the test contract rather than changing product behavior. The test now waits for the mobile disclosure to report initialization, synchronizes on `aria-expanded`, expands if necessary, and waits for a non-zero preview bounding box before aspect-ratio assertions.

PR #60 merged as `671bb6684c29403fbfca74e6fcf7f51c68d53d0e` after full Browser E2E success.

This is now Bug-level reusable evidence for UI E2E synchronization, but it remains non-Canonical and project-scoped.
