# Case: Spatial-audio post-processing can expose capture-path channel loss

Date: 2026-10-02
Status: Case
Scope: desktop audio capture / game recording / spatial audio diagnostics

## Observed behavior

In a game using a "3D headphones" output mode:

- game 3D-headphone mode ON + system Dolby headphone processing ON -> recorded video retains sound effects but dialogue is missing or nearly missing;
- same game mode ON + system Dolby headphone processing OFF -> recording contains the complete mix.

This is a single observed case and does not establish the exact internal routing of the game or Dolby processor.

## Reusable diagnostic interpretation

Do not jump from "dialogue missing in a recording" to "the source has two audio tracks".

A more likely class of causes is a mismatch between:
- game mix buses / multichannel or spatial-object output;
- OS spatial-audio rendering;
- recorder capture tap point;
- recorder downmix/channel mapping.

Dialogue is often routed strongly to a center-like channel or spatial object, while ambience/effects occupy left/right and surrounding channels. If the capture/downmix path drops or mis-maps the center/object contribution, effects may remain while dialogue disappears.

A second possible contributor is double spatialization: game-side binaural/3D-headphone rendering plus system-side Dolby headphone virtualization. That can alter localization and timbre, but by itself does not prove why a recorder loses dialogue.

## Minimal test matrix

Hold the scene and recorder settings constant and compare:

1. game Headphones + system spatial OFF
2. game 3D Headphones + system spatial OFF
3. game Headphones + Dolby Headphones ON
4. game 3D Headphones + Dolby Headphones ON

For each output, inspect:
- number of audio streams;
- channel count and channel layout;
- whether dialogue is audible in live monitoring;
- whether dialogue is present in the recorded file;
- recorder capture source (system mix / application capture / device loopback).

If only recordings fail while live monitoring is correct, prioritize capture tap/downmix investigation.

## General lesson

"Track", "channel", "mix bus", "spatial object" and "post-processed headphone output" are different concepts. Troubleshooting should identify which layer loses the signal before changing content or assuming the source contains separate tracks.

Do not promote to Canonical from this single case.
