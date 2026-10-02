# Observation: Capture cadence should consider integer relationships between game present rate and recording FPS

Date: 2026-10-03
Status: Observation
Scope: OBS game capture / VSync / frame pacing / recording smoothness

## Observation

Game VSync can indirectly affect recording smoothness by constraining the game's present cadence to the display refresh rate. When OBS records at a different frame rate, a non-integer ratio between game presents and capture frames can create uneven source-frame sampling even if OBS outputs a nominally constant frame rate.

Example:
- display/game present cadence: 160 Hz with VSync;
- OBS recording: 60 FPS;
- ratio: 160 / 60 = 2.666...

OBS may therefore sample source frames in an alternating cadence (roughly 3,3,2 game-present intervals), which can produce visible judder in motion despite a correct 60 FPS output timeline.

An integer relationship is cleaner:
- game 120 FPS -> OBS 60 FPS: 2:1;
- game 180 FPS -> OBS 60 FPS: 3:1;
- game 60 FPS -> OBS 60 FPS: 1:1.

VSync off does not automatically solve the problem; if game FPS varies, capture sampling can become even less regular. A deliberate frame cap that is an integer multiple of the recording rate can be more useful than simply toggling VSync.

## Reusable implication

For high-quality game capture, diagnose separately:
1. game render/present cadence;
2. OBS capture/output cadence;
3. OBS render/encode lag;
4. playback display cadence.

When practical, cap game FPS to an integer multiple of the target recording FPS, provided this does not introduce GPU saturation or unacceptable gameplay latency.

Do not promote to Canonical from this single observation.
