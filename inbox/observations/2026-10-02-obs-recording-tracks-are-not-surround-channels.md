# Observation: OBS recording tracks are not surround channels

Date: 2026-10-02
Status: Observation
Scope: OBS recording / multitrack audio / capture diagnostics

## Observation

OBS exposes up to six recording tracks in Advanced Output mode. These tracks are independent audio streams used to route different OBS sources or mixes for post-production. They are not equivalent to 5.1/7.1 surround channels.

Selecting tracks 1-6 does not preserve six spatial channels by itself. If the same source is routed to every track, the recording can contain multiple duplicate mixes.

Surround channel count/layout is a separate setting under OBS audio channel configuration. A single recording track can itself contain stereo, 5.1, 7.1, etc. depending on the configured channel layout and source/capture path.

## Reusable setup pattern

For ordinary editing-oriented recording:
- Track 1: complete monitor/playback mix
- Track 2: game/system audio only
- Track 3: microphone only
- Track 4+: communications/music/other sources as needed

Enable only the recording tracks that actually carry intentionally different mixes.

When diagnosing missing dialogue or spatial-audio capture, changing the number of OBS tracks is not a substitute for checking channel layout, capture source, downmix/rematrixing, and OS spatial-audio processing.

## Evidence status

Supported by OBS official multi-track and surround-sound documentation and by the current troubleshooting context. Do not promote to Canonical automatically.
