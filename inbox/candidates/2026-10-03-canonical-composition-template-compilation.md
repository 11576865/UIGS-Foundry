# Candidate: Compile composition templates into canonical independent objects

Status: candidate
Date: 2026-10-03
Domains: editor-architecture, authoring-tools, non-destructive-editing

## Summary

A higher-level authoring template can improve usability without introducing a second hidden document model.

For composition effects that expand one source object into several persisted objects, a safe first implementation is:

- compile the template into ordinary canonical document objects in one transaction;
- preserve the source unless the user explicitly requests a source mutation;
- avoid hidden persistent parent/child links when the file format has no native relation for them;
- after generation, let each generated object remain independently editable;
- reject ambiguous source semantics instead of silently choosing one interpretation;
- keep source-to-generated relationships as authoring-time intent unless a durable, portable relation model is explicitly designed.

## Candidate rule

When adding composition/template authoring above a canonical file format:

1. Treat the template as a compiler from user intent to ordinary format-native objects.
2. Make the generation operation atomic in domain history.
3. Do not require proprietary hidden metadata merely to keep the generated output editable.
4. If multiple source semantics conflict (for example two mutually exclusive placement mechanisms), fail with an explicit explanation rather than guessing.
5. If later live-linked templates are desired, design that as a separate project/workspace relation with explicit persistence and failure semantics rather than smuggling it into ordinary source data.

## Evidence

ASS Workbench Android PR #83 introduces a first FX composition slice:

- one source ASS Event can generate an independent reflected companion Event;
- inherited placement is compiled to explicit \pos, while an existing \move path is offset as a path;
- simultaneous \pos + \move is rejected instead of guessed;
- optional flip/stretch entrance changes the source only when explicitly requested;
- the whole operation is committed once through the existing canonical document history;
- no hidden persistent source/reflection link is written into ASS.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #83
- evidence level: implemented vertical slice + domain regression tests; CI/device evidence pending at intake time
- deduplication: searched UIGS-Foundry for equivalent canonical-template compilation and hidden-link guidance; no direct duplicate found
- status rationale: reusable authoring architecture candidate; not Canonical

This is a Candidate only. It is not Canonical.
