# Bug: Rendering code can crash when it performs persistence with locals owned by another execution path

Date: 2026-10-04
Status: Bug
Scope: browser UI / render purity / persistence ownership / runtime ReferenceError

## Symptom

Character Voice Reader `main` contained a progress write inside `renderBody()`:

- it attempted to send `position.index` and `time`;
- neither `position` nor `time` existed in `renderBody()`;
- the block became reachable when a saved book was open, the Reader was online, and the body rerendered.

That made an ordinary rendering path capable of raising a runtime `ReferenceError`.

## Root cause

A persistence side effect had drifted from the execution path that owns playback position/time into a DOM rendering function.

The render function knew how to rebuild visible document structure, but did not own the authoritative progress tuple. Referencing variables that only make sense in queue/progress code coupled view reconstruction to state that was not in scope.

## Fix

ASSociated project fix: Character Voice Reader PR #6.

- remove the server progress write from `renderBody()`;
- keep progress writes in explicit progress/navigation paths that own the relevant state;
- add a regression contract test that prevents `renderBody()` from regaining `/progress` side effects or the undefined `position.index` / `audioTime: time` references.

## Reusable rule

Rendering/reconstruction functions should not opportunistically persist domain state unless the required state is passed explicitly and the render path is intentionally the owner of that persistence.

If persistence belongs to playback, navigation, save, or transaction state, keep it at that boundary rather than borrowing ambient locals from another path.

## Evidence

- project: `11576865/Character-Voice-Reader`
- main before fix: `984a229674e35e20512332f270353d25e20f9693`
- fix commit: `051144949c46b0ffebeeaa4c10bf52a860af7630`
- PR: #6
- evidence level at intake: static defect confirmed in current main; fix + regression test authored; asynchronous CI pending
- deduplication: searched UIGS-Foundry for render-side-effect / undefined-local / progress-write equivalents; no direct duplicate found

This Bug record is evidence, not a Canonical specification.
