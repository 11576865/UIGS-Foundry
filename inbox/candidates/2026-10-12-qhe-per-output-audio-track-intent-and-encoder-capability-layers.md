# Candidate: Separate per-output audio track intent from runtime codec capability

Date: 2026-10-12
Status: Candidate / comparative design hypothesis; **not an approved implementation or Canonical rule**
Product: `11576865/Quick-Automatic-Hardsub-Encoder`
Reviewed main: `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`
Related existing:
- `inbox/candidates/2026-10-02-media-format-support-is-a-compatibility-relation.md`
- `inbox/candidates/2026-10-03-cross-boundary-invariant-coverage.md`
- `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md`

## Trigger and observed product boundary

Owner asked what FFmpeg fundamentally does within QHE's Windows Native / Android Native / Web implementations, whether H.266/VVC and other encoder families are accessible, how to improve audio handling, and what MKV-Fast-Muxer domain modeling and mature competitors teach about these relationships.

QHE currently maps audio via one task-level `audio=copy/aac/libopus/none` policy and `audioTrack=all|index`; compiler appends one `-c:a` strategy. This is not per-output-track heterogeneous audio processing. A source MKV with FLAC 5.1 plus AAC stereo might reasonably need to preserve one and encode the other, with independent channel layout, rate, language, default disposition and time strategy. The code's video operation modes `hardsub/transcode/copy` are distinct from audio and container decisions, but the audio granularity remains limited.

FFmpeg framework supports per-stream mapping and stream-specifier codec selections (e.g. `-map 0:a:0 -map 0:a:1 -c:a:0 copy -c:a:1 aac`), subject to actual selected stream order/codec/target container. HandBrake's per-language track selection, Auto Passthru with explicit fallback, and StaxRip's separate audio encoders/muxers are relevant documented baselines; they do not prove QHE should imitate silent fallback or every advanced setting.

FFmpeg upstream documents H.266/VVC encoding via optional `libvvenc` (configure `--enable-libvvenc`); QHE's compiler and shipped Web/Android cores presently whitelist only H.264/HEVC/AV1. Upstream codec presence != local build feature != actual encode/decode smoke != QHE compiler allowance != output mux/playback compatibility. This is an application of existing compatibility-relation Candidate, not an assertion that VVC is already QHE-supported.

## Proposed narrower model (tentative)

Define `AudioOutputTrackIntent` separately for each resulting track:
- stable source stream identity and intended output order;
- operation: `copy | encode | omit`; chosen encoder/parameters for encode;
- channel layout/mixdown/resampling/loudness or timing transformation when explicitly selected;
- output metadata, language/disposition, policy provenance and preservation expectations;
- target container compatibility and concrete per-runtime checks;
- expected streams, duration, channel layouts, codecs and content evidence for output verification.

A global audio preset may create defaults, but must not silently overwrite explicit track overrides. A fallback path (e.g., copied FLAC blocked by MP4 profile -> transcode AAC) requires an explicit user-approved policy and logged conversion, not silent repair. Distinguish encoded packet copying from perceptual quality preservation or target-player audible playback.

For codecs, separate `CodecStandard`, `EncoderImplementation`, `DecoderImplementation`, `RuntimeCapability`, `TaskCompatibility`, and `OutputVerification`. Reserve experimental plugin/adapter status for `libvvenc` until matching input, actual encoder, output-container mux, independent decode and device playback tests succeed.

## Evidence boundary and tests

Source links:
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/src/media-task.js
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/src/media-container.js
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/src/engine.js
- https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/blob/main/docs/manual-media-workspace.md
- https://www.ffmpeg.org/ffmpeg.html
- https://ffmpeg.org/ffmpeg-codecs.html#libvvenc
- https://handbrake.fr/docs/en/latest/advanced/audio-subtitle-defaults.html
- https://handbrake.fr/docs/en/latest/technical/audio-codecs.html
- https://github.com/staxrip/staxrip/wiki/Full-list-of-features
- User discussion 2026-10-12 and attached `软封工程_未来规划总决议_2026-10-12(1).txt` (especially source/document/artifact, explicit intent, independent capability, five-level validation, frozen jobs).

Recommended falsification cases:
1. Two source audio streams, preserve track 0 byte-for-byte and encode track 1 AAC at a chosen bitrate; verify mapping and output channel layout independently.
2. Keep source audio while burn-in video encoder runs; ensure no audio transcoding despite video change.
3. MKV->MP4 source FLAC with explicit copy request: block or offer declared fallback; do not silently switch codec.
4. Source metadata languages/default flags and different audio trim/full policies; preserve declared semantics.
5. VVC: decoder/encoder capability statuses tested separately; do not expose executable policy without native build and mux/reopen fixture.

No QHE code or Canonical spec was changed. The user has not yet chosen a new audio/product strategy.