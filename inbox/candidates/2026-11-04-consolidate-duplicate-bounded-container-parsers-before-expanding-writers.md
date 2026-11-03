# Candidate: Converge duplicated bounded media-container parsers before adding writer paths

Date: 2026-11-04
Status: **Candidate / submitted code; exact-head full browser CI pending**
Domain: EBML, Matroska, media editing reliability, code reuse, parser consistency
Source project: `11576865/MKV-Fast-Muxer`
Product Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/237
Exact head: `cb98e86499f2157d3a769dc288c8ff1a0ebb351a`

## Problem observed in current code

Four separately implemented existing-MKV attachment FileData writers each carried their own ~25-line EBML element ID + size VINT reader, with different function names (`elementAt`, `readElement`, `header`, `header`) and slightly different diagnostics. All actually implement the same finite EBML element-header grammar, even though subsequent per-writer layout and CRC/SeekHead/UID proofs differ. Multiple local decoders increase audit surface and risk inconsistent future handling of corrupt element boundaries.

## Concrete product change

PR #237 introduces `src/matroska-bounded-ebml-header.js` as a **read-only**, 12-byte-max-per-header decoder for finite-addressable EBML Element ID and Data Size. It rejects invalid ID widths, size-VINT unknown/oversize lengths, non-addressable and out-of-parent bounds. All four writers now call this one parser through *thin, explicit adapters* retaining their original field layout and public error code namespaces. The actual writers' separate geometry, attachment bytes, source immutable output, CRC and Tag UID checks are NOT merged or relaxed.

Direct tests in `tests/matroska-bounded-ebml-header.test.mjs` exercise 1–8-byte size VINT widths, virtual gigabyte payloads without staging FileData, unknown-length sentinel, truncated and malicious headers, parent-overrun and error-translation behavior. On first exact-head run, the existing Node unit test workflow stage completed successfully; full Chromium/independent native media execution remained in progress. Thus no general release or complete compatibility conclusion is claimed.

This changes actual production import paths, not just documentation or UI; no GPL source is copied. It reduces duplicated code while retaining the already verified special-purpose writer algorithms, rather than implementing yet another general Matroska writer.

## Tentative reusable lesson

When several media writer backends each reimplement a normative, read-only primitive, centralize that *primitive* with a strict typed error domain and keep backend-specific mutation rules separate. A shared reader can reduce divergent validation but does **not** by itself prove all source layouts or avoid the need for independent output oracles. Error adapters should preserve existing programmatic contract, especially when a route selector uses particular failure codes to decide fallback.

## Dedup

Searched `duplicate EBML parser across writer`, `shared EBML VINT`, `multi backend shared parser consistent`, `reuse existing reader across writers`.
Related existing: `inbox/candidates/2026-10-15-mkv-multiple-bounded-writers-one-router-with-output-oracle.md` covers routing and external output audit across writers, not shared raw element decoding; `inbox/candidates/2026-10-15-upstream-code-reuse-semantic-contract-license-gate.md` covers upstream source reuse and licenses, not local parser deduplication. This Candidate is the narrower domain primitive consolidation.

Do not auto-promote to Canonical. Remains TEST-PENDING until exact-head Chromium, native output parity and negative tests all complete.
