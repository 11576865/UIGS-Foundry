# Candidate: Parameter semantic identity should be independent from control presentation

Date: 2026-10-04
Status: Candidate
Domains: UI architecture, parameter projection, custom tools, interaction contracts

## Problem

When users can extract parameters from existing tools and compose their own workspace controls, directly copying a slider/text-field implementation creates multiple accidental authorities:

- control identity becomes presentation identity;
- local draft state can escape its original owner;
- changing a slider into a dial or XY pad appears to create a different parameter;
- preview/commit/cancel semantics become coupled to one Compose widget.

## Candidate rule

Represent custom/extracted controls with separate layers:

1. **Parameter descriptor**: stable semantic identity — what is being edited, context, arity, unit, source capability.
2. **Presentation**: how that descriptor is shown — numeric field, slider, angle dial, XY pad, etc.
3. **Address/binding**: which workspace projection and target binding are active.
4. **Intent**: PREVIEW / COMMIT / CANCEL plus revision and values.

Changing presentation must not change descriptor identity or target authority.

The intent boundary should validate descriptor existence, binding compatibility, value arity and finite numeric values before a future mutation router reaches canonical editor state.

## Evidence

ASS Workbench Android PR #114 establishes the first contract-first slice:

- stable descriptors for Position XY, Rotation Z, Scale XY and Shear XY;
- one Rotation Z descriptor supports numeric, slider and angle-dial presentations;
- Event parameter addresses reuse FollowFocus / PinnedEvent and reject selection binding;
- preview/commit/cancel intents are typed and revisioned;
- the 240 ledger moves items 109/110 from Planned to Partial rather than claiming implementation of extraction UI.

Drag-to-extract UI, persisted parameter instances and EditorViewModel routing remain deliberately outside this first slice.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #114
- revision: `13e54473d93babf98d4b6488e671a3d473a48c88`
- evidence at intake: contract + unit tests authored; asynchronous CI pending
- deduplication: searched Foundry for parameter semantic identity / visual presentation / custom-control intent contract equivalents; no direct duplicate found

This is a Candidate only. It is not Canonical.
