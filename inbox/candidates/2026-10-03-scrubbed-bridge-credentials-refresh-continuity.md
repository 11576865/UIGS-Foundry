# Candidate: Scrubbed one-shot bridge credentials need scoped refresh continuity

Status: candidate
Date: 2026-10-03
Domains: native-bridge, browser-session, reliability, security-boundary
Evidence type: concrete user-visible bug plus browser regression

## Summary

A browser-controlled native helper can receive a one-shot localhost endpoint/token through the launch URL and then scrub that credential from the visible URL. If normal page refresh is expected to preserve the native session, credential scrubbing must be paired with a deliberately scoped continuity mechanism.

Otherwise the first load is Native, the URL is cleaned, and the next refresh silently falls back to Web.

## Observed case

Quick-Automatic-Hardsub-Encoder Windows Native launches the hosted Web UI with:

- a loopback Bridge endpoint;
- a random per-launch token.

After a successful health check, the Web client removes those query parameters from browser history. Before PR #41, nothing retained the connected Bridge identity after that cleanup. Refresh therefore lost the only discovery inputs and the page re-entered Web/WASM mode even while the same Bridge process was still alive.

PR #41, merged as `04bdf5764a4850a931cf93bec80de423de97afb8`, now:

- validates that the endpoint is loopback HTTP;
- persists endpoint/token only after successful Bridge health validation;
- stores them in tab-scoped `sessionStorage`, not durable local storage;
- reconnects from that scoped session after refresh;
- removes stale stored credentials if the Bridge is gone or authentication fails;
- still strips the launch secret from the visible URL.

A Playwright regression performs the real browser boundary: first launch with query credentials -> URL scrub -> page reload -> Native identity remains connected.

## Candidate rule

For browser-to-local-helper launch credentials:

1. Treat URL credentials as bootstrap material, not long-term visible state.
2. If refresh continuity is part of the product contract, persist validated session identity before scrubbing the bootstrap source.
3. Scope persistence no wider or longer than needed; tab/session lifetime is preferable to durable storage when a native helper is itself ephemeral.
4. Revalidate the local helper on every page load; stored identity is discovery state, not proof that the backend is alive.
5. Self-clear stale credentials on failed liveness/authentication checks.
6. Regression tests must cross the actual reload boundary, not only call the detector twice in one JavaScript lifetime.

## Scope / non-claims

This does not claim `sessionStorage` is universally correct. Desktop shells, browser extensions and longer-lived trusted helpers may need different credential stores. The reusable point is that one-shot credential scrubbing and intended refresh continuity are a coupled design problem.

This is a Candidate only. It is not Canonical.
