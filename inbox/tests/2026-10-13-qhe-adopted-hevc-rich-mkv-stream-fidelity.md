# Test: QHE Manual VBR-approved formal HEVC task preserves rich MKV audio/subtitles/attachments/chapters

Date: 2026-10-13 Asia/Shanghai
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104 (Draft, not merged)
Status: **PASS: actual hosted Windows full v4 output and local independent replay**, exact-head follow-up PCM CI pending
First Windows success after AAC zero-seek bug fix: `38286715465` at `45f5538f714dcd952f03324bffa2e4bf325f73cc`
Previously distinct Test: `inbox/tests/2026-10-13-qhe-full-formal-v4-hevc-flac-output-and-independent-ssim.md` (only one FLAC track, no embedded ASS, no font, no chapters).

## Test fixture and execution

`scripts/build-manual-rich-native-fixture.mjs` constructs a deterministic **valid Matroska** source: 5.021s input timeline; FFV1 video 320x180/12fps; FLAC audio `jpn`; AAC audio `eng`; embedded ASS subtitle `jpn` (two timed events); **one valid 1000-byte self-generated TrueType font attachment**, with original filename/MIME; two chapters 0–2.5s and 2.5–5s; container title. Font is deliberately synthetic and ships as in-script base64; it is not a proprietary or downloaded font. It supports attachment structural checks; *no libass visual/glyph rendering fidelity is claimed*.

Original code path: actual Windows Native `/api/sample` runs x264/x265 12 CQ windows + two x265 bitrate-mode source SSIM tests. Native VBR receipts are strictly admitted. `commitVerifiedManualCandidate` atomically updates form codec/encoder/preset/rate, `compileTask` constructs **real v4 HEVC/libx265 600kbps** task with audio=copy, keepSubtitles/Attachments/Metadata/Chapters=true. `POST /api/encode` dispatches genuine Windows Native `Start-MediaTaskJob`, not a hand-written reference FFmpeg substitute.

Independent `scripts/verify-manual-adopted-native-output.mjs` probes the output and source. Exact assertions: stream count/order/codecs; distinct audio language identities; per-stream packet SHA256 in strict order for both audio tracks and ASS subtitle; ASS codec-private and TTF attachment extradata SHA256 unchanged; font filename and mimetype; chapter titles and times; container title; actual whole-container size equal to Native and FFprobe; 60/60 video frames; full duration; full decoded source-reference SSIM; volume accounting only from observed bytes, no strict whole-file size promise. Later amendment also decodes entire copied FLAC/AAC to fixed mono 48kHz PCM and compares SHA256 plus PCM sample length; check latest CI of that additional assertion.

## Measured Windows test output after fix

- Formal HEVC Matroska file: **422802 B** actual.
- Video payload packet bytes: **268272 B**.
- Copied audio + subtitle payload bytes: **145440 B**.
- Font bytes + metadata + container headers/indices/overhead residual: **9090 B**. This is an **observed** accounting identity on the fixture, NOT a predicted overhead budget.
- Requested video target bitrate: 600000 bits/s; nominal clip video budget **376575 B** using source format duration 5.021s. Do **not** compare the actual full container size to that video-only nominal budget as though it were a strict ceiling.
- Video input FFV1 / output HEVC, 60/60 frames; full-duration decoded source-reference SSIM **0.999738** on this artificial clip.
- FLAC 235/235 packet SHA256 matched.
- AAC 236/236 packet SHA256 matched **including codec priming packet**.
- ASS 2/2 packet SHA256 matched; codec-private bytes unchanged.
- Valid TrueType font attachment SHA256 unchanged; filename and mimetype unchanged.
- Two chapter titles/timing and Matroska title preserved; language jpn/eng/jpn preserved.

Windows run artifact `11763342739` from `38286715465`: real generated input, actual formal Native HEVC output and machine-readable acceptance JSON. Downloaded the artifact into the conversation and **independently locally re-ran** FFprobe metadata/stream checks and SHA256 packet/codec-private/attachment checks on both media files. Additionally decoded both complete audio tracks to identical s16le 48kHz mono PCM and compared lengths/SHA256. FLAC length = **240000** samples in both; AAC length = **241664** samples in both; both exact decoded PCM SHA256 matched. These are independent replayed media bytes, not mock UI data.

## Incident / regression preserved

First rich-MKV Windows full job **red** (`38286010896`), due to AAC pre-roll loss from universal output `-ss 0`; diagnostic repeat `38286271487` showed AAC source 236/output 235 packets, first PTS `-0.021s`, skip_samples 1024 and 1024 fewer decoded PCM samples. Fail artifact `11764055574` was downloaded and analyzed independently. This caused an actual product compiler change, not a relaxation of tests: only tasks with `hasTrimRange` still emit `-ss 0`. Dedicated Bug `inbox/bugs/2026-10-13-qhe-zero-output-seek-drops-aac-priming-packet.md`.

## Limits

Still CI-generated 5-second artificial video; no external player validation, subtitle visual rendering, real-world subtitle/attachment/font compatibility, multi-hour material, physical Windows user hardware, strict size ceiling, AV1/NVENC/HDR/VFR, or actual user save-dialog export path. This is a Test/Observation tier, never automatic Canonical promotion.


## Automated full PCM CI (stronger than prior local-only replay)

Later exact QHE commit `0feed738042745ace6c031f726a3ad93561e56e8`, Windows Manual paired codec workflow `38287162844` **SUCCESS**. New `scripts/verify-manual-adopted-native-output.mjs` automatically decodes *both* source/output audio streams in Windows FFmpeg 9.0.2 to 48kHz mono s16le and requires identical byte lengths AND SHA-256 for each:
- FLAC: source/output **240000** decoded samples, SHA256 `4052aa3c9285665291b020a058f8c7987185062f3b9b34431c33dec62125a579`;
- AAC: source/output **240640** decoded samples, SHA256 `ac1795f1b7b61d528539a02e347f244b8fc1d270ca3b5363f8544f88f2bf5c6c`;
- both `identical:true` in the machine-readable report;
- 235/235 FLAC packet hashes, **236/236 AAC including pre-roll**, 2/2 ASS payloads, unchanged ASS codec private and synthetic TTF attachment extradata hashes, two chapters and both language identities;
- whole MKV still 422802B; full video SSIM 0.999738.

**Cross-FFmpeg decoded sample counts are not a universal invariant:** In local Linux FFmpeg 7.1.5 independent replay, decoded AAC source/output were both **241664** samples, while Windows FFmpeg 9.0.2 pair decoded to **240640**; source vs output equality within the *same specified runtime* is the acceptance criterion, not numerical equality across decoder versions. Packet payload hashes and stream structure were identical across source/output on both checks. Avoid reporting different decoder versions' PCM count as evidence of file damage.

Machine-readable artifact from `38287162844`: `11763144697`, containing generated source `553096B`, actual output `422802B`, independent `full-output-acceptance.json`. The artifact was downloaded into this conversation and its three files and report content inspected. Additional workflows for exact QHE head should be checked separately before a whole-commit green claim.
