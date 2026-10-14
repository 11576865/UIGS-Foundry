# Test — QHE WU10 source-bound must-copy UserIntent through actual Native artifact packet identity

Date: 2026-10-15
Status: PASS, bounded real hosted Windows Native fixture; P2/A02 overall OPEN
Code SHA tested: `54ca3a4e2f7a8fd4222d7f31bca957577b98b539`
Evidence: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38597508774
R19 §03 / §16 P2; R24 §05 / §11; B02, B05, B06, A02.

## Dedup / difference from existing Foundry entries

The existing Test `2026-10-14-qhe-wu07-source-bound-must-copy-audio-intent-compiler.md` proves a user-explicit, source-bound audio mustCopy action is enforced by the official task compiler and controlled Chromium hook, **without** real packet evidence. `2026-10-13-qhe-heterogeneous-audio-plan-and-source-owned-ui.md` and earlier B16 FLAC packet parity tests exercise mixed audio and real compressed packets **without tying the proof to the exact protected WU07 UserIntent and an actual completed Native job**. This entry only adds the source-lock → official v4 → Native execution → final payload identity linkage, without proposing another Canonical model.

## Falsifiable acceptance

- Real Windows FFmpeg generated a 3-second H264 + FLAC(a:0) + AAC(a:1) Matroska source.
- Actual Native localhost `/api/probe` supplied source track facts to existing `compileTask` schema v4. Source identity and `mustCopyAudioOrdinals:[0]` explicitly protected the FLAC; a:1 requested AAC 96kbps transcode.
- Negative formal task compilations must refuse a foreign source identity or a change of the protected FLAC to AAC.
- Actual Windows Native Bridge `/api/encode` completed the job. Output private MKV measured **121,709 bytes**, agreeing with the job receipt.
- Independent FFprobe source/output `-show_packets -show_data_hash sha256 -show_entries packet=data_hash` on audio a:0 yielded **141 of 141 SHA-256-compressed-packet hashes identical by order**. Output a:1 had AAC codec and a different compressed-packet hash sequence from source AAC, confirming independent re-encode.
- Real CI `38597508774` SUCCESS; same code SHA frontend `38597508576` and UIGS Coverage `38597508191` SUCCESS.

## Precise boundary

This establishes preserved compressed packet *payload* equality for one complete-duration synthetic FLAC stream in the same exact user-locked formal Native task. It does **not** establish equal container bytes, clip/PTS/DTS equivalence, full A/V sync, metadata and disposition retention, arbitrary codec/container, actual user film or target playback and Android/Web. A02/P2 overall still incomplete.

## Separate observed blocker

The checked-in `public/vendor/ffmpeg-kit-next-web/README.txt` requires locally built `dist/index.js` and `lib/...` FFmpegKitNext Web assets. They are absent in this branch, and `src/engine.js` returns `missing-core` when dynamic import fails. Do not use successful controlled Chromium WU08 batch hooks to assert real WebAssembly video encoding. Web two-source real-media acceptance remains Pending; no Canonical promotion.
