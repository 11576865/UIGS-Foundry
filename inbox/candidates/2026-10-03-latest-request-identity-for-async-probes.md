# Candidate: Async source probes must publish only if they still match the latest request identity

Status: candidate
Date: 2026-10-03
Domains: reliability, interaction-state, native-bridge
Evidence type: code audit plus concrete race path

## Summary

When a user can replace an input while an asynchronous probe is still running, probe completion must be conditional on request/source identity.

A later completion from an older source must not overwrite metadata for the currently selected source.

## Evidence

Quick-Automatic-Hardsub-Encoder starts Native FFprobe work after video selection. Before this stabilization pass, both Windows and Android paths allowed:

1. select video A;
2. A probe starts;
3. select video B;
4. B probe starts;
5. B finishes and updates UI;
6. A finishes later and overwrites B metadata.

The callbacks carried no generation/identity guard.

PR #35 introduces monotonically increasing probe generations on Windows and Android and suppresses callbacks from older generations.

## Candidate rule

- every replaceable-source async probe should carry or capture a request/source identity;
- only the latest still-valid identity may publish state;
- stale success and stale failure must both be discarded;
- changing source identity invalidates older in-flight probe results;
- regression tests should force out-of-order completion and assert that only the newest result becomes visible;
- UI state and logs must not be updated by stale completions.

## Scope

Applies to file/media probes, remote metadata lookup, previews, validation, search/autocomplete, background analysis, device capability reads, and similar async work triggered from replaceable user input.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #35 `Stabilize media workflow state transitions`
- evidence level: code-audited race with deterministic regression coverage

This is a Candidate only. It is not Canonical.
