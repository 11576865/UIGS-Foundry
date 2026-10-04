# Candidate: Separate lexical tag discovery from semantic ownership scope

Status: candidate
Date: 2026-10-04
Domains: parser-architecture, semantic-editing, structured-authoring, diagnostics

## Summary

A lossless lexical scanner and a semantic editor answer different questions.

A lexical scanner may intentionally expose every recognizable tag, including nested tags inside transforms, because syntax highlighting, diagnostics, and raw editing benefit from that visibility.

A semantic operation that owns only direct Event-level state must instead distinguish:

- direct top-level override tags;
- nested transform payload tags;
- later span-local tags;
- reset boundaries;
- malformed or ambiguous syntax.

Using the lexical tag stream directly as semantic ownership state conflates these layers.

## Candidate rule

1. Keep lossless lexical discovery broad enough for diagnostics and source editing.
2. Add an explicit semantic-scope view rather than changing lexical visibility to satisfy one structured editor.
3. Determine top-level ownership with syntax structure such as parenthesis depth, not tag spelling alone.
4. Structured Event-level editors must not treat nested transform targets as immediately active static overrides.
5. When a whole-line property appears in an ambiguous span-local position, prefer an unresolved/ambiguous state over guessed geometry.
6. Downstream consumers should request the narrowest semantic projection they actually need instead of consuming a general-purpose “effective value” summary.

## Evidence

ASS Workbench Android PR #99 found that `AssInlineSyntax` intentionally exposes nested transform tags, while `AssEffectiveInspector`, preview-target logic, Semantic Search, and Style-inheritance cleanup each needed direct top-level semantics.

The correction adds a shared top-level override projection while preserving lexical nested-tag visibility. Preview targeting fails closed for ambiguous late `\an`, `\pos`, or `\move`; Semantic Search sees later direct tags but excludes transform payload tags; Style-inheritance cleanup removes only direct managed tags and preserves nested `\t(...)` payloads.

PR #95 independently hit the same boundary in Batch `HasTag`: using the lexical tag stream caused `{\t(...,\pos(...))}` to match a direct `pos` filter. The Batch filter now uses the same top-level semantic projection while later direct span tags still match.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PRs: #95, #99
- evidence level: repeated parser/semantic boundary defects across Batch, Search, Style inheritance, effective-state inspection, and preview targeting + implementation corrections + tests
- deduplication: searched UIGS-Foundry for lexical-vs-semantic tags, nested transform ownership, and ambiguous preview anchors; no direct duplicate found
- status rationale: reusable parser/editor architecture candidate; not Canonical

This is a Candidate only. It is not Canonical.
