# Bug: unconditional output-side `-ss 0` drops negative-PTS AAC priming during no-trim MKV transcode

Date: 2026-10-13 (Asia/Shanghai)
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104 — Draft/unmerged
Status: **Observed and fixed with actual Windows-hosted Native regression; full cross-platform field acceptance pending**
First red Windows run: `38286010896`; diagnostic repeat `38286271487`; first green after fix: `38286715465`, QHE commit `45f5538f714dcd952f03324bffa2e4bf325f73cc`

## Distinct symptom and exact packet evidence

A real formal `Start-MediaTaskJob` using task schema v4 took a 5s synthetic Matroska with FFV1 video, copied FLAC (jpn), copied AAC (eng), embedded ASS, one self-generated TrueType attachment and chapters. The Windows-hosted FFmpeg **9.0.2** HEVC formal task completed. Independent FFprobe could read its HEVC video and copied streams, but the second AAC output audio contained **235 packets** versus the source's **236**.

The omitted exact packet was source a:1 first AAC packet:
- PTS/DTS **-0.021s**;
- SHA256 `d8e43266d6c01bcc890490cf606af8c713301a9b013c79fb8560f5271a16fbbd`;
- `side_data_type: Skip Samples`, `skip_samples: 1024`.
- output a:1 first packet was the source's **second** AAC packet, PTS 0, with `Skip Samples: 1024` propagated to it.
- All subsequent AAC packet payloads were identical and ordered, so dropping a priming packet was not apparent from codec/stream-count probes alone.
- Downloaded failing source/output artifacts `11764055574` (CI-synthetic) were independently decoded to mono 48kHz PCM: source **241664 samples**, output **240640 samples** (exactly **1024 fewer**). The PCM SHA256 values differed. This proves a real decoded-audio discrepancy, not merely a harmless change to Matroska metadata.
- Local Linux FFmpeg 7.1.5 initially retained the pre-roll packet even under an equivalent task, whereas Windows 9.0.2 omitted it, illustrating version-sensitive timestamp/copy behavior. Do not infer all platforms behave identically.

## Root cause and concrete repair

`src/media-task.js` compiled **every** task with an unconditional output-side `['-ss','0']`, including requests with `hasTrimRange=false`. A zero-time output seek is not semantically guaranteed to preserve negative-PTS preroll; it can discard AAC codec-priming packets at a nominally untrimmed boundary. This was especially visible when multiple audio streams were copied with a transcoded video.

Change: `const args = t.hasTrimRange ? ['-ss','0'] : []`. **Only explicit trimmed-range tasks retain output-side timeline rebasing; full-range tasks omit the artificial seek.** Added `src/media-task.test.mjs` regression checking full transcode and video Stream Copy have no output `-ss`, while a genuine trim retains `-ss 0`. We did not weaken the independent per-packet hash acceptance criteria.

In Windows Native PR run `38286715465` after the fix: complex formal MKV HEVC conversion succeeded with source/output:
- AAC **236/236** payload hashes identical including initial preroll;
- FLAC **235/235** hashes identical;
- embedded ASS **2/2** payload hashes, codec-private SHA256 same;
- synthetic TTF attachment SHA256 equal, chapters/metadata retained;
- video 60/60 frames, full-file source SSIM `0.999738`, measured MKV `422802B`.
The actual source/output artifacts were downloaded; independent local FFprobe+full PCM decode comparison confirmed AAC and FLAC decoded PCM sample counts and SHA256 exactly matched after the repair. A following code change incorporated those full PCM checks into CI and requires new exact-head confirmation.

## Generalizable engineering observation (NOT Canonical)

`-ss 0` must not be treated as a mathematically empty operation in an FFmpeg remux/copy pipeline when streams have negative timestamps/decoder priming. To assert copy integrity, distinguish *container stream exists*, *payload packet multiset/order*, *codec delay/side-data* and *full decoded audio PCM*. This one reproducible host-dependent case is a **Bug** and associated **Test**, not a universal FFmpeg guarantee. Real long-form, Bluetooth/player gapless playback, alternate AAC sources, genuine trim effects and all field devices remain separate acceptance tasks.
