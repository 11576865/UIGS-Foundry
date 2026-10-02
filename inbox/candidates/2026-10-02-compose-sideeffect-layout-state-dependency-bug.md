# Candidate / Bug: Compose SideEffect does not establish layout-state recomposition dependencies

Status: **Candidate / product bug with regression-test evidence**
Date: 2026-10-02

## Incident

ASS Workbench published touch Interaction Proxy handles from a Compose `SideEffect` after reading overlay geometry written by `onGloballyPositioned`.

The relevant layout values (`IntSize` / window origin) were stored in `mutableStateOf`, but they were read only inside `SideEffect`, not during composition.

Observed behavior:
- renderer-backed preview became ready;
- the interaction overlay itself was composed;
- the registry sometimes never received the expected `position-1-pos` proxy, even after 30 seconds;
- earlier runs could pass when unrelated recomposition happened to occur.

The root cause is that state reads performed only inside `SideEffect` do not establish a snapshot read dependency for the composition scope. The first side effect can observe zero-size pre-layout state, and a later `onGloballyPositioned` write is not guaranteed to invalidate that composition scope.

## Reusable rule

When a post-composition side effect depends on mutable layout state:

1. read the relevant state during composition;
2. pass/capture those composition-read values into `SideEffect`, or use an effect API whose keys explicitly include the state;
3. never assume that reading `State<T>` only inside `SideEffect` will subscribe the composition to future changes.

Conceptually:

`layout callback -> mutable state -> composition read -> recomposition -> SideEffect publish`

not:

`layout callback -> mutable state -> SideEffect-only read`

## Applied fix

ASS Workbench now takes composition-time snapshots of overlay origin/size for:
- Position proxy publication;
- Move start/end proxy publication;
- rectangular Clip proxy publication.

The existing renderer-backed regression then waits for the real registry entry and separately asserts the semantics node is visible before capture.

## Why this generalizes

This applies to Jetpack Compose overlays, popups, drag handles, window-coordinate adapters, accessibility geometry, test adapters, and any post-composition publication mechanism derived from `onGloballyPositioned` or other layout callbacks.

## Evidence boundary

This is supported by one product failure reproduced through Android Emulator Regression and by direct inspection of the Compose state-read topology. It does not imply that every `SideEffect` using state is wrong; the issue is specifically relying on side-effect-only reads to trigger future recomposition.

Do not promote to Canonical from this incident alone.
