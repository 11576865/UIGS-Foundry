# Bug: JavaScript String.replace replacement syntax can corrupt embedded source text containing dollar sequences

Date: 2026-10-04
Status: Bug
Scope: code-generation / repository editing / cross-language source mutation

## Symptom

A repository edit that inserted PowerShell source through JavaScript `String.prototype.replace(search, replacementString)` unexpectedly duplicated or corrupted a large suffix of the PowerShell file. Diff size jumped from a small intended change to thousands of inserted lines, and PowerShell parsing failed.

## Cause

JavaScript replacement strings interpret dollar-prefixed sequences such as `$&`, `$``, `$'`, `$n`, and `$$` specially. Embedded source code can contain such byte sequences accidentally, especially shell and PowerShell code where `$` is common.

The replacement text was treated as replacement-language syntax rather than as opaque source bytes.

## Safe fix pattern

When replacement content is generated code or arbitrary source text:

- prefer index/slice insertion for exact byte-text composition; or
- use a function replacer, e.g. `text.replace(anchor, () => replacement)`, so the returned string is not interpreted as replacement syntax;
- inspect the resulting diff size before committing;
- retain parser/compile gates for the target language.

## Reusable implication

Cross-language source mutation must distinguish host-language replacement syntax from target-language source syntax. A syntactically innocent target-language token can be active metasyntax in the host editing API.

Do not promote to Canonical from this bug record alone.
