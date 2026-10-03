# Bug: Async readiness rerenders can clobber live editor values

Date: 2026-10-04
Status: Bug
Scope: browser UI / asynchronous probes / editable repeated rows

## Symptom

A user edits track metadata in a rendered list, but a background probe completes and triggers a full UI rerender. The rerender rebuilds the row markup from model state that has not yet received the latest DOM value, restoring an inferred/default value over the user's edit.

In MKV-Fast-Muxer this surfaced in a ten-job browser E2E run as a subtitle title reverting from the per-job value to the inferred default.

## Cause

The UI had two timing domains:
- live form controls containing the newest user input;
- asynchronous identity/container/font/subtitle probes that can call the global render function at any time.

Replacing editable markup assumes model state is already authoritative. That assumption fails when an async observer wins the race before the normal input-state synchronization path.

## Fix pattern

Before an asynchronous/global rerender replaces editable repeated-row markup, capture the current values from live controls into the owned model state. Then render from that updated state.

Prefer more local rendering where possible, but if a global rerender is retained, it must not treat background readiness as permission to discard foreground edits.

## Reusable implication

Background observation must be monotonic with respect to user-authored state: completing a probe may add evidence/readiness, but must not roll an editable value back to an older inferred/default state.

Do not promote to Canonical from this single bug record.
