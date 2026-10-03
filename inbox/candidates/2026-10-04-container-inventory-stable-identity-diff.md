# Candidate: Container inventory diffs should compare stable content identity, not presentation order

Status: **Candidate / reusable UI + verification pattern**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android`, PR #89 (implementation + tests)

## Observation

Container-editing interfaces become hard to understand when they primarily explain the operation in prose while showing only the target track. The user needs to see the container as an inventory of media resources and understand what the planned operation changes.

A second risk appears when before/after comparisons use list position or transient UI ordering. Track order may change even when content identity is preserved, and multiple tracks may share the same codec or language.

## Candidate rule

For non-destructive container editing and remux workflows:

- render the container's detectable contents as a first-class inventory, including all supported video, audio, subtitle, attachment/font, chapter, and other resource classes;
- keep unknown or unsupported resource types explicit instead of dropping them or guessing;
- represent action-heavy operations with compact icons when the action is conventional, while retaining accessible labels/tooltips and textual state for ambiguous domain semantics;
- distinguish baseline scan, planned state, and verified output scan; a planned result must not be presented as an observed container fact;
- compute added / removed / retained / modified resource states from a defined stable identity or matching policy, not from row number or visual order;
- when identity is ambiguous, surface `unknown` / `unresolved` rather than manufacturing a diff;
- after remux/write-back, re-scan the actual output container and compare the verified inventory against the baseline and intended mutation before publish.

A useful conceptual split is:

```text
Baseline inventory (observed)
        +
Planned mutation (intent)
        ↓
Predicted inventory (derived)
        ↓
Actual output inventory (observed)
        ↓
Verified diff
```

The UI should make the verified inventory and diff primary, while moving explanatory prose behind contextual disclosure.

## Why it is reusable

The pattern applies to MKV/MP4 remuxers, archive editors, package managers, project asset bundles, database migration previews, and other tools that modify collections while trying to preserve unrelated members.

## Implementation evidence

ASS-Workbench Android PR #89 implements the pattern in the MKV soft-mux workflow:

- the project surface is now inventory-first instead of explanation-first;
- Matroska scanning exposes all TrackEntry records plus attachments/fonts and chapter count, while editable ASS remains a subset;
- attachment metadata is represented separately from retained payload, so bounded payload reads do not force the whole resource to disappear from the inventory;
- track matching prefers TrackUID; attachment matching prefers AttachmentUID and then content SHA-256;
- weak metadata identities are accepted only when unique; duplicate weak candidates become `UNRESOLVED` rather than being paired by list position;
- source re-scan is compared against the first-load baseline;
- remux output is re-scanned before publish, and the verified inventory is compared to the baseline;
- write-back verification checks track identity/order/metadata, chapter count, original attachment preservation, and ASS persisted semantics before the destination is published.

Tests cover stable-UID track reordering, added/removed/modified resources, ambiguous weak identities, all major TrackEntry classes used by the reader fixture, chapter counting, bounded attachment metadata, and an Android Emulator MKV bridge fixture for modified ASS + added font with no silent source-resource removal.

At intake time Android CI #842 passed. Android Emulator Regression #467 and Fontconfig renderer native probe #742 were still running, so those two evidence levels are not claimed as passed here.

The implementation currently has observed `BASELINE`, source re-scan, and `VERIFIED_OUTPUT` states. A separate pre-write predicted/planned inventory remains a design direction from this Candidate and is not claimed as implemented by PR #89.

## Status

Keep as **Candidate**. This is now implementation-backed in one project, but it has not been validated across multiple projects or by a user study. Do not promote to Canonical from this evidence alone.
