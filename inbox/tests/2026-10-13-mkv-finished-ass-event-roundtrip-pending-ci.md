# Test: MKV soft-subtitle output ASS Dialogue event round-trip

Date: 2026-10-13 (Asia/Shanghai)
Status: **PENDING CI** — code and tests committed; no passing exact-head Chromium evidence claimed
Product: `11576865/MKV-Fast-Muxer`
Source branch: `feat/p3-ass-dialogue-output-roundtrip-20261013`
Source branch head at intake: `acdb8dca95c38530d4ddd6d66697b93c90896f6b`
Expected PR: new P3 subtitle-delivery verification PR, to be linked after submission
Baseline main: `15ca805db83e640f867bcbc6e36502d89af25f61`

## Exact verification claim

This new optional, bounded verification checks **newly added .ass tracks** only: the actual finished MKV is reopened and demuxed to ASS, then its ordered `Dialogue` events are compared to the exact prepared ASS text being passed into FFmpeg. The comparison includes event count, text (including ASS inline override tags), centisecond timestamps, layer, style reference, actor/name, margins, effect and order. It preserves event multiplicity and does not treat same-count changed events as a pass.

The implementation exposes `pass`, `warning`, `unavailable`, and `not-requested`. The recorded output report property is `audit.assEventAudit`. A real detected mismatch downgrades the overall audit status but preserves the downloadable artifact. Unsupported and resource-bounded cases remain separately marked unavailable rather than masquerading as verified.

## Scope and independent evidence

- `src/ass-event-output-audit.js`: separate no-DOM comparator, bounded to 8 ASS tracks, 2 MiB per ASS text, 50000 events, and a 512 MiB output artifact.
- `src/main.js`: single and frozen-batch shared mux executor uses final output file through `ffmpeg.wasm` demux, not the staged source. Output audit and scoped UI summary are attached to the same report, not a duplicate state.
- `tests/ass-event-output-audit.test.mjs`: positive, wrong-text, changed timing, missing track, malformed format, duplicate mapping, resource limit and demux-failure tests.
- `tests/e2e/browser-mux.e2e.mjs`: actual Chromium muxes MP4+two ASS+FLAC+font, downloads MKV and report, requires the scoped audit to pass. A separate system `ffmpeg` executable independently demuxes both tracks from the downloaded MKV and matches event sequences to original source .ass fixtures.
- Existing Node and full Chromium suites remain mandatory. At intake time, the exact-head CI has not been run or confirmed by this record.

## Out of scope

Does **not** verify all source-MKV ASS tracks, SSA, SRT, PGS, Style/extradata fidelity, glyph shaping, libass rendering, font availability in target players, exact EBML relationship preservation, arbitrary file sizes, or user-device playback. Demux through two FFmpeg executables is still not a proof of independently correct ASS interpretation by unrelated players.

## Deduplication / governance

Existing Candidate `2026-10-02-persistable-semantic-roundtrip-verification.md` describes the general canonicalized persisted-semantics rule. Existing Candidate `2026-10-13-final-artifact-font-filedata-hash-verification.md` covers exact font attachment FileData hashes. This entry is a narrower **Test** proving a distinct *subtitle event stream* final-artifact property, not a new general Canonical principle.

Do not promote the result or mark PASS without the precise PR head's CI and artifact evidence.
