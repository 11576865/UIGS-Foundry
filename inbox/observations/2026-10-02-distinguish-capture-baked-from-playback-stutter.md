# Observation: Distinguish capture-baked stutter from playback-only stutter

Date: 2026-10-02
Status: Observation
Scope: OBS recording diagnostics / media playback / encoder validation

## Observation

A game can remain visually smooth while the recorded file is choppy. This does not by itself distinguish between:
- OBS-side recording/render/encoding lag baked into the file; and
- playback-side decode/render/display drops when reviewing the file.

OBS can miss or skip recorded frames under GPU/encoder pressure even when the game itself appears smooth. Conversely, very high-complexity/high-bitrate AV1/HEVC recordings can play poorly if the player is software decoding or cannot render frames on time.

## Diagnostic split

Capture-baked evidence:
- OBS log/statistics report rendering lag or encoding lag during the recording;
- multiple competent players reproduce the same cadence;
- transcoding/decoding from the file reveals missing/irregular timestamps or repeated gaps.

Playback-only evidence:
- OBS recording log shows no meaningful render/encode lag;
- another player or hardware decoding plays the same file smoothly;
- player statistics show dropped/late frames while decoding/rendering.

## Minimal workflow

1. Inspect OBS last log for rendering/encoding lag.
2. Play the same file in mpv with statistics visible.
3. Toggle hardware decode and compare dropped-frame counters.
4. If ambiguity remains, decode a representative segment with FFmpeg and inspect timestamps/frame cadence.
5. Do not change recording parameters until the fault layer is identified.

## Reusable principle

Treat smooth gameplay, smooth capture, and smooth playback as three separate evidence layers. A smooth game preview does not prove a smooth recording, and choppy playback does not prove the file itself is damaged.

Do not promote to Canonical from this single observation.
