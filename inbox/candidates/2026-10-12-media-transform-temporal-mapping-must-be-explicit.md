# Candidate: Media transforms need an explicit multi-stream temporal mapping contract

Date: 2026-10-12
Status: Candidate / research hypothesis, **not an observed QHE runtime bug or Canonical standard**
Context: `11576865/Quick-Automatic-Hardsub-Encoder`, task schema v4

## Distinct problem
Media files can contain separately timestamped video decode/presentation events (DTS/PTS), audio sample clocks and encoder delay/priming, subtitle event timestamps, chapter positions and container offsets. One user-supplied IN/OUT interval is not enough, by itself, to prove these clock relations remain correct after stream-copy trim, CFR/VFR transformation, rate changes, nonzero first timestamp, multi-input mapping or subtitle burn-in.

QHE `src/media-task.js` compiles `videoRange/audioRange/subtitleRange` into two input views (source whole vs `-ss/-t` trimmed), uses one input time pair, sets `setpts` around ASS in the hard-sub filter and derives durations from source duration/trim spans. `src/media-verification.js` maps output time using `actualStart + outputTime`. Existing V4 device acceptance verifies limited video/audio trim/full and packet durations. This is valuable, but neither a formal per-stream time function nor sufficient proof of sample-accurate A/V/subtitle/chapters for difficult sources. No particular current output failure is claimed.

## Reusable proposal
Before adding advanced trim, VFR, speed changes or time-based subtitle/multiple audio features:
- associate each selected output stream with `SourceClock`, `RequestedInterval`, `RealizedInterval`, `TimeMapping` and `ReferenceEvidence`;
- distinguish decode vs presentation timestamps, and source-local/global vs output-local time;
- measure copied video actual keyframe start, independently measured audio first presentation time, encoding priming/delay, subtitles event windows and chapter coordinate changes;
- do not infer synchronous playback from equal duration alone or from packet-data hashes (which exclude timestamps);
- define a playback-synchronization oracle for test cases: source differing stream start_time; edit lists; B-frames; VFR; non-integer fps; discontinuities; audio codec priming; both copy/transcode; subtitles/chapters around cut;
- retain task/compiler/source provenance and output audit in reports, including unsupported or unknown mappings.

## Dedup and evidence boundary
Foundry searches 2026-10-12 for temporal mapping, PTS/DTS cut sync, timebase chapter trim showed no equivalent Candidate. Adjacent `inbox/candidates/2026-10-02-media-format-support-is-a-compatibility-relation.md` covers codec/container/playback compatibility, not cross-stream clock correctness. QHE already has time trim tests and must not be characterized as ignoring time entirely.

Sources: QHE `src/media-task.js`, `src/media-verification.js`, `docs/stream-plan-v4-device-acceptance.md`; https://www.ffmpeg.org/ffmpeg.html (time base, -fps_mode, -copyts, -map, sync). No implementation authorization or Canonical promotion.