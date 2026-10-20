# Bug: browser Stream Copy MKV mux shifts newly added ASS Dialogue timestamps

Date: 2026-10-13
Status: **FIXED for independently verified browser fixture in PR #116; broader source/device cases remain unverified**
Product: `11576865/MKV-Fast-Muxer`
PR under verification: https://github.com/11576865/MKV-Fast-Muxer/pull/116
Baseline before the P3 check: main `15ca805db83e640f867bcbc6e36502d89af25f61`

## Verified observation

The real Chromium scenario (MP4 with source AAC audio, external FLAC, two ASS subtitles, deduplicated font attachment) completes the legacy FFmpeg.wasm mux and passes existing stream/metadata/attachment checks, but a NEW finished-MKV ASS event comparator detects a common +2 centisecond offset on the first `Dialogue` start timestamp of both new ASS streams. This is an actual output difference, not only a source-plan or ffprobe stream-count mismatch.

- Exact-head Chromium failing run [38371164912](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38371164912), source head `d340b3b5aec92d112b3100ae36744cee7fc68904`, pinpoints `start` changes.
- Exact-head failing run [38371816676](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38371816676), source head `805e6aa7327829e6f8b977da75e229fc4049d7d9`, adds `-copyts` to internal ASS extraction, yet still observes +2 centiseconds.
- Exact-head failing run [38372283002](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38372283002), source head `b7e7cd6e204fd9fae17c4bc67fc2befa07ab84bd`: an INDEPENDENT host FFmpeg invocation with `-copyts`, on the REAL downloaded browser-produced MKV, extracts source `zh.ass` expected `0.00–1.50 s` as `0.02–1.52 s`; text content is unchanged in that comparison. This refutes the hypothesis that the new auditor alone invented the offset.

## Important distinction

A separate local system-FFmpeg synthetic experiment showed that re-extracting ASS WITHOUT `-copyts` may itself add about 2 centiseconds when the container contains negative AAC priming timestamps; applying `-copyts` to that extraction restored the original timing. This *extractor-side artifact* exists, but the real Chromium-produced MKV still exhibited +2 centiseconds when independently extracted WITH `-copyts`. Do not conflate these two failure modes.

## Proposed scoped experiment, not verified fix

On PR #116, the work branch is testing adding input `-copyts` to the MUX command only when new ASS subtitles are included, to stop the FFmpeg.wasm Stream Copy mux from shifting the subtitle event timeline. New unit assertions require unaffected non-ASS paths to retain their legacy command. This is NOT approved until exact-head Node/build AND full Chromium E2E, independent actual output ASS audit, and existing P0/batch/original track regression all pass. If it fails, retain the red evidence, do not silently allow a broad timing tolerance or declare the mux safe.

## Reusable lesson candidate

Independently verify *finished subtitle event time and text*, not only codec/count/language or attachment FileData. Always distinguish timestamp rebasing introduced by an export/check tool from real source-to-output media time drift. Capture an exact-original-vs-output time delta under a known time-base and clear source/output identity; do not promote any bug-specific workaround to canonical rule from one fixture.

## Scope

Current evidence: controlled 2-second synthetic browser fixture on the specified FFmpeg.wasm/Chromium CI environment, two new ASS tracks in one mixed media job. Not proven for every browser, large media, all codecs, all ASS, or the root causal mechanism. Issue remains open pending a real mux-level remediation with independent proof.

## Deduplication

Existing Foundry `inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md` concerns valid ASS centisecond persistence normalization; `inbox/candidates/2026-10-13-final-artifact-font-filedata-hash-verification.md` concerns output attachment bytes. Neither records this exact final subtitle packet timeline regression. The test-level tracking entry `inbox/tests/2026-10-13-mkv-finished-ass-event-roundtrip-pending-ci.md` is complementary.


## Verified scoped repair — 2026-10-13

The experiment above succeeded on exact-head tests. PR [#116](https://github.com/11576865/MKV-Fast-Muxer/pull/116), head `aaa79341acd780830610a8969cc514c807c75fc1`, was independently checked by the actual full [Chromium E2E run 38373112896](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38373112896) and [Node/build run 38373112879](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38373112879) (417/417 tests). The passing fix is **scoped** to the mux command when new ASS tracks are present: `-copyts` and output `-avoid_negative_ts disabled` are used together. The new final-MKV audit reads delivered ASS Dialogue sequences; an independent system FFmpeg reads the actual downloaded file and finds the expected exact fixture times. The non-ASS command path remains unchanged. PR #116 was squash merged as `45ff4edb847ae164946d3d070a947c80cfd8cbb4`.

**Resolution boundary:** bug verified fixed for the specified synthetic mixed-input browser fixture; no assertion that every Matroska input, negative-timestamp variant, player, or hardware browser is fixed. Additional cases should be separately tested. This remains a Bug record, not a Canonical mandate to use particular FFmpeg flags universally.


## 2026-10-20 recurrence: independently recovered SRT is +21 ms (Candidate correction pending)

The prior scoped ASS repair (PR #116) did **not** establish strict SRT cue-time parity for all input codecs. In Softmux 0.1022 batch failed-job retry E2E, the actual newly muxed second SRT has a uniform **+21 ms** start/end offset relative to its source `Batch S01E02.en.srt`:

- Source `00:00:00,100–00:00:01,500`, output `00:00:00,121–00:00:01,521`;
- Source `00:00:01,550–00:00:01,900`, output `00:00:01,571–00:00:01,921`.
- Exact real Chromium/native failure: [PR #163 CI #39360187046](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39360187046). The batch process successfully retried only the failed Job, retained the first output and produced a valid SRT stream, but the strict original-vs-extracted cue text assertion correctly failed due to timing.

Independent local native-FFmpeg (7.1.5) reproduction generated the same source type (24-fps MPEG4 video + 48-kHz AAC audio, stream-copy Matroska, `-copyts`, `-avoid_negative_ts disabled`) and precisely recreated +21 ms. First AAC packet shows `pts_time=-0.021333` and `Skip Samples=1024` at 48 kHz. A bounded input `-itsoffset -0.021` applied to **new SRT only** restored both cues to exact source times in that experiment; original video/audio remain stream copy. This is an empirical correlation and tested correction for the fixture, **not** a general AAC/Matroska guarantee.

Current PR #163 introduces an independent staged-source first-packet ffprobe check and only computes a millisecond correction for a single AAC stream in ISO-BMFF/MOV when negative PTS agrees with `Skip Samples / sample_rate`. No unsupported/non-evidenced source gets an assumed 21 ms offset. Exact-head **bundled browser WASM** Node/build/Chromium/native CI on this new code is **PENDING** as of this entry. Retain strict subtitle timestamp equality and do not promote any general FFmpeg workaround to Canonical.

Distinction from the Oct 13 Bug: the earlier fixture verified ASS Dialogue centiseconds and original `-copyts`/negative-ts policy; the new case exposes SRT millisecond-level priming under batch failure retry and tests a **measured packet-proven correction**, not merely a user setting or the host extractor.


## 2026-10-20 final correction — SRT packet PTS was correct; the original no-copyts extractor rebased it

**Evidence status: verified, scoped to actual supplied 2-second AAC+MPEG4 fixture and finished MKV on Chromium/FFmpeg.wasm.** Earlier section above is historical experiment context, **not an endorsed correction**.

The first R7 acceptance test extracted SRT using external host FFmpeg `-i output.mkv -map 0:s:0 -f srt -` and saw all cues +21 ms. That export invocation re-based timestamps in an MKV with negative AAC priming PTS; it was **not** sufficient to infer the MKV's stored subtitle PTS had moved. An experimental input `-itsoffset -0.021` made that unqualified *export text* match, but introduced a real regression: the production finished-MKV verifier uses `-copyts` when demuxing to compare source and output, and its strict SRT audit became `warning`. CI [39390401636](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39390401636) exposed that second job completed while its source-bound subtitle integrity audit correctly rejected its contents. An earlier broad offset also made the existing ASS dialogue check fail by two centiseconds (CI [39362435108](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39362435108)); and a mixed-format case flagged new SRT (CI [39362854668](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39362854668)). Therefore neither a general `-itsoffset` rule nor the narrower one-SRT rule is accepted.

**Merged final repair:** Remove all experimental packet-based `-itsoffset` logic and keep pre-existing `-copyts` + `-avoid_negative_ts disabled` mux policy. Verify two independent *actual container* oracles in the failed-job retry fixture:
- native `ffprobe -show_packets -select_streams s:0` on the **real downloaded MKV** yields SRT starting packet PTS **[100, 1550] ms** (matches original cue starts);
- independent host `ffmpeg -copyts -i final.mkv -map 0:s:0 -f srt -` produces exactly the source SRT cue start/end times, text, and sequence.
- The production Chromium in-app `-copyts` readback independently returns a `pass` SRT audit. The second Recipe v2 job transitions from `auditWarning` back to `awaitingSave` without changing UI status semantics or weakening asserts.
- Mainline merged [PR #163](https://github.com/11576865/MKV-Fast-Muxer/pull/163), `main@2368422dd11dabf9f6ef26532505515400ddd531`. Exact integration head `4d236eb9bad1e45592f7cb3efa503b4f575afe80`, [complete Node (632/632), Vite build, Chromium/native E2E green #39391267167](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39391267167). Log contains `R7 ACTUAL MKV SRT PACKET PTS [100,1550]`, `R7 actual failed-job retry PASS`, `Batch Recipe v2 independent output and execution audit PASS`, `All browser E2E scenarios PASS`.

**Reusable bug criterion:** A tool-created *display or exported subtitle text timeline* is not automatically the same as the media container's **packet timestamp timeline**. When streams with priming/negative start timestamps are present, test input-vs-final **packet PTS** first, then compare source vs independently demuxed subtitles with intentional timestamp preservation. Never 'fix' the producer by negating an offset observed solely after a default extractor rebase. Treat a partially generated batch output with an audit warning as real completion plus **unverified output**, not as a UI state synchronization failure.

This entry refines the existing Bug/Case, not a Canonical change. The scope is the verified AAC/MPEG4 fixture and browser run; no claim all AAC priming variants and Matroska players have identical behavior.
