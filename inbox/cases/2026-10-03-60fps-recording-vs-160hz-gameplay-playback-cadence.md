# Case: Smooth high-FPS gameplay can look much less smooth in a correct 60 FPS recording

Date: 2026-10-03
Status: Case
Scope: OBS recording / playback cadence / display refresh / stutter diagnosis

## Evidence from one OBS log

- Display: 3840x2160 at 160 Hz.
- OBS output: 3840x2160 at 60/1 fps.
- Recording encoder: NVENC AV1, CQP 14, P5, quarter-resolution multipass, B-frames 4, look-ahead enabled, AQ enabled.
- Recording duration: ~212.4 s.
- OBS reported 9 frames lagged due to rendering stalls (0.1%) and 9 frames skipped due to encoding lag (0.1%).

The observed complaint was that playback looked much more stuttery than the game itself.

## Interpretation

The OBS-reported lag is too sparse by itself to explain continuous severe playback stutter. A separate and expected perceptual difference exists when gameplay is rendered well above 60 FPS but the recording is fixed at 60 FPS.

At 160 Hz display refresh, 60 FPS content also has a non-integer refresh cadence if playback is presented at a fixed 160 Hz without effective VRR or refresh-rate switching:

160 / 60 = 2.666...

Therefore consecutive video frames cannot each occupy the same integer number of refresh intervals. This can produce periodic judder even when the file contains a correct 60 FPS cadence.

## Reusable diagnostic implication

When users report "game smooth, recording looks choppy", distinguish at least four layers:
1. game render FPS/frame pacing;
2. OBS capture FPS;
3. OBS render/encode lag baked into the file;
4. playback decode/render/display cadence.

A clean 60 FPS recording of 120-160 FPS gameplay will necessarily look less temporally smooth. Playback on a refresh rate that is an integer multiple of the video frame rate (e.g. 120 Hz or 240 Hz for 60 FPS) can remove one source of cadence judder, but it cannot recreate the temporal information that was never captured above 60 FPS.

Do not promote to Canonical from this single case.
