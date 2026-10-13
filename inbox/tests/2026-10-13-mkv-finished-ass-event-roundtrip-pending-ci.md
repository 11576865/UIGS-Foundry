# Test: MKV soft-subtitle output ASS Dialogue event round-trip

Date: 2026-10-13 (Asia/Shanghai)
Status: **PASS — exact-head Node/build and full Chromium E2E verified; PR #116 merged**
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


## Post-intake exact-head acceptance — verified 2026-10-13

The initial PENDING state above records the submission point, not the final outcome.

- PR [#116](https://github.com/11576865/MKV-Fast-Muxer/pull/116) exact tested head: `aaa79341acd780830610a8969cc514c807c75fc1`.
- [Node/build workflow 38373112879](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38373112879): **success, 417/417 Node tests and production build**.
- [Full actual Chromium E2E 38373112896](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38373112896): **success, all scenarios PASS**; source MP4 + AAC, external FLAC, 2 new ASS, uploaded duplicate font were processed in the real browser. Scenario 1 requires `audit.assEventAudit.status = pass` for 2/2 added ASS and independently demuxes downloaded MKV with system FFmpeg `-copyts`; both ordered Dialogue sequences and times match source fixtures.
- A real **+2-centisecond timestamp drift** was first detected by the new audit and independently reproduced in the browser-written output (red runs 38371164912 / 38371816676 / 38372283002). Merely adding `-copyts` to the readback did not fix it. The passing change applies **`-copyts -avoid_negative_ts disabled` to the mux when NEW ASS tracks are included**, while non-ASS mux input remains on the legacy command path. The test preserves this gate.
- PR #116 squash merged into `main` as `45ff4edb847ae164946d3d070a947c80cfd8cbb4`.

This is scoped CI fixture evidence, not proven exact Style/extradata fidelity, real user-device playback, every codec/source start-time combination, large-file stability, or arbitrary EBML relationship preservation. Do not promote to Canonical based only on this one implementation.
