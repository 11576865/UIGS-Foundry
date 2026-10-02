# Cross-project Knowledge Inventory — Pass 2

Date: 2026-10-02

Second pass adds concrete failure history, test grammar, UI grammar, and reliability mechanisms.

## Added to Bug Museum

- **BUG.ASS.RELEASE_PATH_ASYMMETRY** — tested MKV write-back bridge was absent from the production APK path until release packaging was made symmetric and verified.
- **BUG.HSR.SUBTITLE_AUTOSAVE_RACE** — autosave HTTP writes could race during rapid editing/navigation; write sequencing became single-owner/serial.
- **BUG.HSR.SAME_BASENAME_COLLISION** — basename identity failed for parallel package trees; stable package-relative identity and content evidence replaced filename guessing.

## New reusable reliability patterns

- generation/session/epoch checks for stale asynchronous publication;
- release-path parity between what CI tests and what the final artifact actually contains;
- verify-then-publish staging for long-running output;
- destructive-combination matrices organized around invariants and evidence levels;
- real encoding fixtures for UTF-8 / UTF-16 variants.

## New Interface Grammar patterns

- **Explicit Tool Instance Binding** from ASS Workbench's Workspace migration;
- **Capability Catalog Navigation** from the unified WorkbenchToolCatalog and its regression tests;
- **Preview–Inspector Split** from HSR's adaptive Subtitle Style Workbench.

## Red Reason Registry

An initial CI failure taxonomy now separates policy, build, unit/integration/E2E, runtime-smoke, environment, packaging, release-publication, resource-budget, device-only, infra/flaky, and unknown failures.

## Agent collaboration

A cross-project Candidate records explicit scope/worktree/integration ownership for parallel agents. It remains Candidate because this pass still has conversation-level evidence rather than a located authoritative incident artifact.
