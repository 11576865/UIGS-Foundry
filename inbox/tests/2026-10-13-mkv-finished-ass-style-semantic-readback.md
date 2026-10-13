# Test: P3 final-MKV ASS V4+ Style semantic readback

Date: 2026-10-13 (Asia/Shanghai)
Status: **PASS — exact-head 425/425 Node + build and full Chromium E2E, merged PR #117**
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

## Final exact-head acceptance — 2026-10-13

- Product PR: [#117](https://github.com/11576865/MKV-Fast-Muxer/pull/117), tested head `9ae1d821cebce4c0c24af8659afff25445f95cd1`, baseline `main@45ff4edb847ae164946d3d070a947c80cfd8cbb4`.
- [Node/build run 38386963519](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38386963519): **PASS**, 425/425 Node tests, Vite production build.
- [Full actual Chromium E2E run 38386963388](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38386963388): **PASS**, all scenarios. Two actual new ASS streams are verified in the downloaded browser-produced MKV. The `assStyleAudit` report passes 2/2 tracks (2 V4+ Style rows), and independent system FFmpeg demux compares Style semantics against fixture originals. The existing Dialogue, font bytes, batch and complex source protection scenarios remain on the same required suite.
- Initial red PR run 38386722808 was caused by obsolete static test assumptions and negative fixture construction. Corrected while retaining mismatch/refusal assertions; not treated as runtime Style corruption evidence.
- PR #117 squash merged into `main` at `22255a4130ecf04aaf8a0b494bd107ea1f868777`.

**Evidence boundary:** independent FFmpeg demux confirms 23 known V4+ Style metadata fields in specific synthetic two-track fixtures; no actual renderer output comparisons, custom Style columns, `[Script Info]` preservation, source MKV partial-edit preservation, large-file field media, or actual end-user device compatibility. The result remains a Test, not Canonical promotion.

## Squash-merged main verification

Main commit `22255a4130ecf04aaf8a0b494bd107ea1f868777` also passed its own post-merge required checks:
- [Main Node/build and Pages deployment 38387562480](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38387562480): **PASS**.
- [Main complete Chromium mux E2E 38387562385](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38387562385): **PASS**.

These are separate from the PR exact-head acceptance and are not evidence of real-player libass rendering or universal compatibility.
