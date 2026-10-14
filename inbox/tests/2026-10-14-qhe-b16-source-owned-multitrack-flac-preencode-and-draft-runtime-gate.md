# Test — FLAC pre-encode packet observation across multiple full/trim tracks is not an exact final-mux budget

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact submitted product head: `83a37a10f1ea10b3fa4f2669c628478e94d29025`
Status: implementation submitted; real Windows/Node/browser hosted acceptance Pending
Requirement: B16 partial; complete initial-version B01–B25 / A01–A10 still open.

## Distinct reusable engineering boundary
Previous Foundry B16 Tests cover *copied* auxiliary packet costs before or after a mixed-media run:
- `inbox/tests/2026-10-14-qhe-b16-trimmed-copy-post-output-packet-cost-audit.md`
- `inbox/tests/2026-10-14-qhe-b16-isolated-preencode-trim-copy-remux-observation-and-stale-ledger-gates.md`
- `inbox/tests/2026-10-14-qhe-b16-preencode-isolated-trim-copy-packet-observation-boundary.md`

The present Test is **not a duplicate**: it concerns *actual FLAC re-encoding*, which is inherently content-dependent and cannot be inferred from a target bit rate, and its explicit time-window/output-track identity. It also tests a new *Draft-scoped Windows media acceptance* boundary that prevents build-only tests from masquerading as platform runtime proof.

## Invariants tested
- A single pre-encode request may map multiple audio ordinals to `full` or `trim` input timelines with explicit sample rate and channel layout, but only when the caller's request and Native selected source match and the original complete-source packet measurement ID is current.
- A bounded Windows FFmpeg worker produces real FLAC packets in a **separate** audio-only Matroska remux; an independent FFprobe worker measures per-output stream packet bytes. The worker has bounded time (360 s encode, bounded 270 s independent packet work), disk usage (1 GiB checked while encoding), track count (16), and requested range (4h). If limits prevent full completion, results become unavailable, not a rate-based extrapolation.
- A source-length/FILETIME change, source selection change, full-source ledger ID replacement, reordered streams, mismatched source ordinals or settings, incorrect receipt method, forged negative/overflow cost, or missing audio source ledger must prevent observation admission.
- The UI may show a **read-only diagnostic** but cannot cause the formal `sizeBudget` to substitute observed FLAC bytes. Until the exact mixed video/audio/softsubtitle mux semantics are verified, `FLAC` within strict size target still fails closed. A completed audio-only output is not a final container-size or user-delivery certificate.
- Native start/status APIs run as source-owned async single-flight jobs and do not run concurrently with final encoding or the existing copy preflight. Every GET includes live source and ledger revocation, not only the first result.
- A focused Windows runtime workflow on a Draft PR includes PowerShell 5.1 source parsing, JS evidence tests, an actual two-audio `full`+`trim` FLAC encoding, independently repeated FFmpeg/FFprobe packet oracles and an auxiliary copy baseline. It does not trigger unrelated Android/VVC/all-Windows test matrices.

## Implementation evidence and external gaps
- `windows/flac-encode-preflight.ps1`, `windows/flac-encode-preflight-bridge.ps1`, `windows/native-bridge.ps1`; `src/flac-encode-preflight.js`, `src/auxiliary-preflight-request.js`, `src/windows-native-client.js`, `src/main.js`, `src/media-workspace.js`.
- `scripts/check-flac-encode-preflight.ps1`, `src/flac-encode-preflight.test.mjs`, `src/auxiliary-preflight-request.test.mjs`, `.github/workflows/windows-b16-runtime.yml`.
- **Bounded evidence:** 16 isolated actual-module JavaScript behavioral checks PASS, two standalone source wiring checks PASS, selected front-end module parse checks PASS. A Linux FFmpeg 3-second dual-track local reproduction succeeded with one full FLAC audio track 39300 packet bytes and a second 0.4–2.4s trimmed track 27599 packet bytes. This is not a Windows Native Bridge runtime acceptance or long-form guarantee.
- Immediate exact-head workflow lookup showed `Windows B16 runtime acceptance`, `Test frontend`, and `UIGS Evidence Coverage` queued. No hosted PASS claimed. Real Windows PowerShell/FFmpeg, browser source switching, endpoint lifecycle, mixed-mux equivalence, FLAC longer than current bounds, and Android/Web still Pending.

## Promotion
Test-level source-backed observation only. Do not modify UIGS Canonical or mark B16 fully complete. Future promotion requires independent Windows execution, task-matched mixed mux packet/PTS equivalence, boundary/error validation and repeatable real-world complex-media fixtures.
