# Test: Independent FFmpeg smoke for mixed per-stream audio copy/transcode

Date: 2026-10-12
Status: Test / **executed locally in assistant research container** (not QHE runtime or user's Windows/Android device)
Product context: Quick-Automatic-Hardsub-Encoder task model discussion
Duplicate review: extends `inbox/candidates/2026-10-12-qhe-per-output-audio-track-intent-and-encoder-capability-layers.md`. QHE's pre-existing stream-plan v4 runtime acceptance has related video-copy + *one* audio transcode; this test checks **simultaneous audio copy and audio transcode** in a single output, independently of QHE.

## FFmpeg runtime
`ffmpeg version 7.1.5-0+deb13u1`, Linux software-only execution (local container). FFprobe same runtime.
No H.266 encoder `libvvenc` listed in the actual local `ffmpeg -encoders` output, while the native `vvc` decoder is listed. This observation illustrates decoder/encoder capability separation, not universal FFmpeg feature coverage.

## Input fixture (synthetic, two seconds)
```bash
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i testsrc2=size=160x90:rate=12:duration=2 \
  -f lavfi -i sine=frequency=400:sample_rate=48000:duration=2 \
  -f lavfi -i sine=frequency=800:sample_rate=48000:duration=2 \
  -map 0:v -map 1:a -map 2:a \
  -c:v libx264 -threads:v 1 -preset ultrafast -crf 32 \
  -c:a:0 flac -c:a:1 aac -b:a:1 96k \
  -metadata:s:a:0 language=jpn -metadata:s:a:1 language=eng source.mkv
```
ffprobe: source MKV has H.264 video, FLAC 48 kHz mono (jpn), AAC 48 kHz mono (eng).

## Action
```bash
ffmpeg -hide_banner -loglevel error -y -i source.mkv \
  -map 0:v:0 -c:v copy \
  -map 0:a:0 -c:a:0 copy \
  -map 0:a:1 -c:a:1 libopus -b:a:1 64k \
  -map_metadata 0 output.mkv
```

## Independent observations
ffprobe result: output has H.264 video, FLAC 48 kHz mono (jpn), Opus 48 kHz mono (eng). For each selected stream, used `ffprobe -show_packets -show_data_hash sha256 -show_entries packet=data_hash`, comparing packet hash sequences:
- `v:0`: 24 vs 24 packets, **same per-packet data-hash sequence**.
- `a:0`: 21 vs 21 packets, **same per-packet data-hash sequence**.
- `a:1`: 95 vs 102 packets, **different per-packet data-hash sequence**, as expected after AAC→Opus.

This supports executable FFmpeg behavior for selective copy + audio encoding on this synthetic fixture, not bitwise file identity, subjective audible quality, synchronization for complex sources, metadata preservation beyond the probed language tags, or QHE feature parity. Packet data hashes exclude timestamp and container structural bytes.

## Related product model finding
QHE current `src/media-task.js` invokes `-c:a <single codec>` for all mapped output audio; `audioTrack` allows all or one. Therefore this verified native FFmpeg operation is **not** evidence QHE can express it today without task model changes.
`src/media-planning.js::sizeBudget` explicitly rejects copied audio for a size target, because current budget planner does not measure its payload; it is a planner limitation rather than a reason copied audio is theoretically impossible to budget. Future experiments should measure fixed copied-stream packet bytes under exact trim/source mapping, and bound container overhead separately, while refusing to assert a guaranteed target from mere nominal bitrate.

## Next falsification
Replay with external video source and 5.1 audio, metadata dispositions, differing trims, clipped start packet, VFR/complex timestamps, decoded A/V integrity, and actual Web/Android/Windows execution. Compare output against explicit `OutputAudioTrackIntent` references and independent packet metadata, not only whether FFmpeg exits zero.

This record is Test evidence only, no Canonical changes.
