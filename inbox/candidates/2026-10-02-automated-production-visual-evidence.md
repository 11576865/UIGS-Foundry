# Candidate: Automated Production Visual Evidence Capture

Status: candidate
Date: 2026-10-02
Related:
- OPS.UIGS.SHOWCASE_EVIDENCE_LADDER
- OPS.UIGS.SOURCE_OWNED_UI_INVENTORY
- OPS.UIGS.PRODUCTION_REALIZATION_PROVENANCE
- OPS.UIGS.CROSS_LAYER_EVIDENCE_RESOLVER

## Problem

Production Visual Evidence must not depend on the user manually sending screenshots. Manual screenshots and recordings are valuable field evidence for transient/device-specific bugs, but they are not a scalable baseline collection mechanism.

## Candidate mechanism

Each UI-bearing source repository declares a source-owned visual capture contract, for example:

`.uigs/ui-visual-capture.json`

A capture state binds:

- stable Surface ID;
- source revision;
- platform/runtime;
- route, Activity, test entry, or fixture setup;
- viewport/device geometry;
- theme, font scale and locale;
- deterministic fixture/state;
- selector or capture region;
- evidence level;
- output identity.

Foundry orchestrates capture from the real product repository at an immutable source revision and records the resulting image with a manifest and content hash.

## Evidence levels

Keep at least these levels distinct:

1. `production-rendered` — real product UI code rendered from a pinned revision with deterministic fixtures; backend/native dependencies may be simulated if declared.
2. `runtime-backed` — real product UI with the actual backend/native bridge/renderer active.
3. `field-capture` — screenshot/recording from a real user/device/session; useful for environmental and transient failures.

Reference Demo and Visual Baseline remain separate Foundry evidence classes and must never be relabeled as production evidence.

## Platform strategy

### Web

Use Playwright against the checked-out production repository. Start the product's real development/preview server, seed deterministic state, navigate to the declared state, wait for an explicit ready condition, then capture the target Surface or viewport.

### Android

Use an emulator/instrumentation capture path. Build the real app, launch a deterministic fixture/project, navigate through a test entry, wait for idle/renderer readiness, and capture via instrumentation/UiDevice or adb screencap. Device profile, density, theme, locale and font scale must be declared.

### Web UI with native host/bridge

Capture fixture-backed UI states separately from runtime-backed states. A Windows runner can start the real native bridge and browser frontend for bridge-dependent evidence.

## Orchestration

Prefer Foundry as the control-plane runner:

1. read source-owned capture contracts;
2. determine which source revisions/states changed;
3. check out the relevant repository at the pinned revision;
4. execute only affected capture states;
5. hash screenshots and manifests;
6. compare with previous evidence;
7. commit/index changed evidence;
8. expose evidence through the cross-layer resolver and coverage reports.

Routine project builds should not require Foundry to be online.

## Storage

Do not upload routine screenshots as transient Actions artifacts and call that durable evidence.

For the initial implementation, store current deterministic captures plus provenance manifests in Foundry. Preserve historical images only when needed for a known regression/case or when the capture contract explicitly requests history. If scale becomes material, move binary storage behind a content-addressed object/release store while keeping manifests and hashes in Git.

## Failure semantics

A capture failure is not a visual difference.

Report separately:

- capture environment failed;
- state fixture failed;
- target Surface not found;
- screenshot changed;
- screenshot unchanged;
- runtime dependency unavailable.

Do not silently regenerate/accept a visual baseline after failure.

## User screenshots

User-provided screenshots/recordings remain optional `field-capture` evidence. They are especially useful for device/browser states CI cannot reproduce, but the normal coverage path must be automated.

## Validation work

- add schema for visual capture contracts and evidence manifests;
- implement a Playwright adapter on MKV-Fast-Muxer or Quick-Automatic-Hardsub-Encoder;
- implement an emulator adapter on ASS-Workbench-Android;
- connect evidence to Surface IDs and the cross-layer resolver;
- add change/failure reporting;
- validate storage cost before expanding to all 62 current Surfaces.

This candidate does not change Canonical guidance.
