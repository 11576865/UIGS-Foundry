# Observation: Tab navigation temporal continuity is distinct from loading

Status: observation
Date: 2026-10-04
Domains: interface-grammar, motion, navigation, visual-evidence
Evidence type: direct comparison of two user-provided Android screen recordings

## Observation

Two Android recordings show materially different destination-switch presentation even though both use persistent bottom navigation.

In the dark-themed recording, a tab switch keeps the bottom navigation chrome visually stable while the outgoing destination and incoming destination are simultaneously visible during a horizontal push/slide. The old surface translates out while the new surface translates in. This overlap gives the user continuous spatial evidence of where the new destination came from and prevents a blank/intermediate frame.

In the white-themed recording, destination content changes between adjacent captured frames with no visible spatial interpolation, cross-fade, skeleton, spinner, or other transition state. The new destination appears as an immediate replacement under the same bottom navigation shell.

The second behavior should not be described as “loading” from visual evidence alone. Immediate replacement is a presentation transition policy; data loading is a separate asynchronous state. A destination can replace instantly while reading cached/local data, or it can animate while still loading data.

## Reusable implications

- Evaluate navigation motion separately from data-loading behavior.
- A persistent application shell plus overlapping outgoing/incoming destination surfaces can create strong temporal/spatial continuity without changing domain semantics.
- Hard replacement is not inherently a performance failure, but it provides less motion continuity and can feel more abrupt.
- Capture frame cadence materially affects perceived smoothness; recording FPS is evidence about the recording, not proof of the application's actual render FPS.
- Visual evidence for “smoothness” should record transition duration, overlap/interpolation behavior, frame pacing, and shell persistence separately.

## Evidence boundary

This is a two-recording observation. It does not establish a Canonical requirement that all tab navigation must slide, nor does it identify the exact UI framework or animation API used by either application.

No Canonical promotion.
