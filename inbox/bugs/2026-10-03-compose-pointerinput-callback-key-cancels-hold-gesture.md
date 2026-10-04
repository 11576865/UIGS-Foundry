# Bug: Callback lambdas used as pointerInput keys can cancel a hold gesture during recomposition

Date: 2026-10-03
Status: Bug
Lifecycle: recorded
Scope: Jetpack Compose / long-press repeat / continuous gesture controls

## Symptom

A press-and-hold transport control may start repeating once and then stop immediately, or cancel as soon as it updates visible UI state.

## Cause

A `pointerInput(...)` modifier was keyed by callback lambdas captured from a composable. The hold action updated state, which triggered recomposition. Fresh callback identities changed the `pointerInput` keys, causing Compose to restart the pointer-input coroutine and cancel the active gesture.

The same failure can occur even earlier when press-start itself changes parent state.

## Fix pattern

Keep the gesture coroutine on a stable key such as `Unit` or a true semantic identity, and read evolving callbacks through `rememberUpdatedState`.

Also clear press-owned parent state in `finally` so pointer cancellation or disposal cannot leave the UI permanently pinned in an interacting state.

## Reusable implication

Do not use frequently recreated callback lambdas as `pointerInput` keys for gestures that are expected to survive recomposition, especially:

- long-press repeat;
- drag loops;
- press-and-hold acceleration;
- controls that update their own labels or parent interaction state while held.

Do not promote to Canonical from this single bug observation.
