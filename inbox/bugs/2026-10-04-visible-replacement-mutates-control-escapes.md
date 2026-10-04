# Bug: Visible-text replacement can mutate control escapes when operating on raw segments

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: structured text editing / search-replace / lossless syntax / control escapes

## Symptom

An editor can label an operation “visible text replacement” while implementing it as regex replacement over raw source substrings outside markup blocks.

In a structured text format, those raw substrings may still contain non-visible control syntax.

For ASS Event Text, text outside `{...}` override blocks can contain escapes such as:

- `\N` / `\n` for line breaks;
- `\h` for hard space.

A raw-segment replacement can therefore rewrite the `N`, `n`, or `h` characters inside the control escape even though the operation claims to own visible text only.

Malformed override syntax can make the problem worse if the damaged tail is treated as ordinary visible text.

## Failure mechanism

ASS Workbench Android's `replaceVisibleSegments` protected `{...}` blocks but otherwise applied `Regex.replace` directly to raw substrings.

That boundary was too coarse:

`override block != non-visible syntax boundary`

The lexical model already distinguished `TEXT`, `ESCAPE`, and `OVERRIDE_BLOCK`, but the replacement implementation bypassed it.

## Mitigation implemented

PR #100 changes visible replacement to:

- run shared ASS lexical analysis first;
- fail closed on malformed override syntax;
- edit only `TEXT` token ranges;
- preserve `ESCAPE` and override syntax byte-for-byte;
- apply replacements from right to left so source token offsets remain stable.

Regression coverage verifies that neighboring visible characters can change while `\N` and `\h` remain untouched.

## Reusable lesson

For structured text, “not inside markup” is not equivalent to “user-visible text”.

A semantic replacement operation should mutate tokens owned by its semantic scope, not ad-hoc raw substrings. Control escapes, embedded expressions, placeholders, markup, and other non-visible syntax need explicit token classes or equivalent structural boundaries.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #100
- evidence level: concrete syntax-corruption path + token-aware correction + regression coverage
- deduplication: searched UIGS-Foundry for visible replacement, control escapes, structured-text token replacement, and markup corruption; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
