# Test: P3 final-MKV ASS V4+ Style semantic readback

Date: 2026-10-13 (Asia/Shanghai)
Status: **PENDING exact-head CI**; implementation and E2E assertions are submitted, not yet accepted
Project: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/117
Initial draft head: `63458351e1e1579f6fa295a4abda50a811248e8e`
Baseline: merged `main@45ff4edb847ae164946d3d070a947c80cfd8cbb4`

## Distinct delivery property under test

From the *actual finished MKV* and same bounded readback as its previously verified Dialogue events, separately parse and compare newly added ASS `[V4+ Styles]` definitions.

- `src/ass-style-output-audit.js` models exactly 23 known V4+ Style fields and uses the explicit `Format` mapping rather than assuming column order. Safe canonicalization covers numeric decimal display and hex color case/zero padding; semantics such as font family, size, color, bold/italic, geometric parameters, margins, encoding and row order remain strict.
- The verifier emits `pass / warning / unavailable / not-requested` independently under `audit.assStyleAudit`. A verified mismatch degrades output-audit truth without deleting a correct downloadable artifact. Missing, unknown/custom, ambiguous or exhausted input is not silently treated as pass.
- The single-task and frozen batch use their existing shared executor. Demux occurs once per final subtitle stream, with Promise caching across the event verifier and style verifier.
- The actual output inspector displays style audit coverage separate from event and font FileData findings.
- Submitted negative Node tests mutate fontname, fontsize, backcolour, count/order, unknown columns, ambiguity and resource budgets; external system FFmpeg E2E must demux the **downloaded** browser-produced MKV and compare two ASS style tables against staging fixtures.

## Why separate from existing Foundry entries

`inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md` already establishes the general need for format-domain canonicalization. `inbox/tests/2026-10-13-mkv-finished-ass-event-roundtrip-pending-ci.md` verifies delivered Dialogue events, not Style definitions. `inbox/candidates/2026-10-13-final-artifact-font-filedata-hash-verification.md` verifies attachment FileData, not Style mapping. This entry is a **separate Test evidence** without proposing a new Canonical rule.

## Explicit non-claims

No assertion of `[Script Info]` fidelity, custom ASS fields, full ASS font resolution, glyph shaping/libass rendering, player equivalence, original source MKV subtitle preservation, general EBML structure safety, mobile/large-file acceptance, or arbitrary user content. This is only an additional **scoped delivery proof** when supported, not a universal mux contract.

Do not mark PASS until the final exact PR head's Node/build and full Chromium E2E are green and the real Style comparison has passed.
