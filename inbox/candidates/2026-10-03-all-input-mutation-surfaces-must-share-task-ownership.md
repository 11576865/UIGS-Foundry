# Candidate: All input mutation surfaces must share the active task owner

Status: candidate
Date: 2026-10-03
Domains: reliability, interaction-state, workflow
Evidence type: state audit plus implementation regression

## Summary

When a task assumes a stable set of inputs, every UI surface capable of mutating those inputs or their effective dependency set must respect the same task lifecycle owner.

Locking only the obvious file inputs is insufficient if alternate pickers, resource libraries, bindings, or other side channels can still change execution inputs.

## Evidence

In Quick-Automatic-Hardsub-Encoder, `runWebTask` disabled the ordinary video / ASS / font file inputs while analysis, preview, tests, or encoding were active.

However two mutation paths remained outside that lock:

1. Windows Native uses separate system-picker buttons for video / ASS / fonts.
2. The browser saved-font library can remove or clear fonts that participate in ASS font resolution.

This allowed the effective input universe to change while an existing task still assumed the old one.

PR #43 now:
- locks Windows Native picker buttons under the same operation owner;
- rejects picker starts while `operationBusy` or a Native job is active;
- locks saved-font delete / clear actions during active tasks;
- invalidates analysis when the saved-font dependency set changes.

## Candidate rule

- identify the complete effective input set of a task, not only the most visible form controls;
- enumerate every mutation surface for that input set, including alternate/native pickers, dependency libraries, mapping controls, and indirect resource management actions;
- while an operation owns the input snapshot, competing mutations must be rejected, queued, or explicitly versioned;
- changing a dependency that participates in derived analysis invalidates that analysis even if the primary source file did not change;
- UI busy-state tests should assert all mutation surfaces, not just canonical inputs;
- lifecycle ownership should be enforced in the mutation function itself as a backstop, not only through disabled presentation.

## Relationship to existing Foundry knowledge

Related:
- `REL.SINGLE_OWNER_LONG_JOB`
- `REL.CHECKPOINT.ROUTE_AND_INPUT_IDENTITY`

This Candidate narrows those broader reliability ideas to the interaction-layer problem of multiple mutation surfaces targeting one effective task input snapshot.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #43 `Stabilize input lifecycle and native picker identity`
- evidence level: code-audited input mutation paths plus regression contracts

This is a Candidate only. It is not Canonical.
