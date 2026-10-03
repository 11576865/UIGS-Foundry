# Candidate: Observational probes must not mutate user policy

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, state-management, media-processing

## Summary

A discovery or inspection operation should populate observed state without silently changing the user's authoring policy.

When software automatically probes a source resource to reveal more structure, the probe result may enable controls, populate an inventory, or refine capability state. It should not by itself switch a non-destructive policy into a selective/removal policy, toggle preservation off, or otherwise reinterpret the user's editing intent.

Observed state and requested transformation state are separate responsibilities.

## Observed case

In `11576865/MKV-Fast-Muxer`, source-MKV track inspection historically had an interaction side effect: explicitly entering the track-scan path switched the workflow away from the "preserve everything + append" behavior so the user could manually select original tracks.

PR #61 restructures this around an observational container inventory:

- selecting a verified Matroska source automatically scans its container structure;
- the scan records streams, attachments, chapters and container metadata;
- automatic inspection does not turn off append-only preservation;
- switching to selective editing requires an explicit user action;
- asynchronous scan results carry a generation/request identity so a stale source scan cannot publish over a newer selection;
- the UI separately renders the observed source inventory and the requested output deltas.

## Candidate rule

For automatic source discovery, inspection, capability probing or inventory scans:

1. Treat the probe as an observational state transition unless the user explicitly invoked an authoring action.
2. Keep observed source state separate from requested mutation policy.
3. Do not infer destructive intent from the fact that the user asked to inspect or reveal details.
4. If detailed controls require a different policy, require an explicit mode/action transition and make its effects visible.
5. Bind asynchronous probe publication to the source/request identity so stale inspection cannot rewrite current state.
6. Present requested output changes as deltas against the observed source rather than rewriting the source inventory itself.

## Provenance

- source repository: `11576865/MKV-Fast-Muxer`
- pull request: `#61`
- implementation branch: `feat/compact-container-inventory`
- evidence: unit/build workflow passed on PR development heads; browser E2E was expanded to cover automatic inventory discovery, non-destructive defaults, source replacement and scan cancellation
- status: PR under validation at intake time

This is a Candidate only. It is not Canonical.