# Bug: JavaScript replacement-string metasyntax can corrupt source-to-source patches

Date: 2026-10-04
Status: Bug
Lifecycle: recorded
Scope: engineering automation / source rewriting / patch orchestration

## Symptom

A text-based integration script used JavaScript `String.prototype.replace(search, replacementString)` to inject PowerShell source that itself contained regex literals ending in `$'`.

JavaScript replacement strings interpret several dollar sequences specially, including `$&`, `$``, and `$'`. As a result, source text from after the matched region was implicitly inserted into the replacement. The generated PowerShell file contained duplicated suffixes and truncated regular expressions, producing a large cascade of parser errors far from the apparent edit site.

## Root cause

The patcher treated the replacement argument as literal source text, but the JavaScript API treated it as a replacement template.

This is especially dangerous when rewriting code that naturally contains dollar-prefixed syntax, regular expressions, shell variables, or other language fragments.

## Fix pattern

For literal source-to-source replacement, use a replacement callback rather than a replacement string:

```js
source = source.replace(needle, () => replacement);
```

The callback return value is inserted literally and does not expand replacement-string metasyntax.

For nontrivial transformations, additionally assert:
- the expected anchor exists exactly once when uniqueness matters;
- known corruption signatures are absent after rewriting;
- the target language parser runs before expensive downstream tests.

## Reusable implication

Code-generation and patch orchestration must distinguish **literal replacement content** from **replacement-template syntax**. When the replacement text is another programming language, callback-based insertion is the safer default.

Do not promote to Canonical from this single bug record.


## Independent reoccurrence and CI prevention — QHE #78 (2026-10-10)
While inserting PowerShell `Invoke-SceneRiskProbe` using a JS string replacement, a generated regular-expression suffix `$'` was interpreted as JavaScript replacement-template syntax, expanding a ~3.2KB intended insertion into over 40KB of duplicated PowerShell. Windows CI immediately failed the PowerShell parser gate. The file was reconstructed from the clean merged `main` version, applying `source.replace(anchor, () => literalPayload)` so dollar-bearing cross-language source was inserted without reinterpretation, and the repaired branch passed Windows parser/smoke. Evidence: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/78, merged `eb84018d2c33344c6c69a965ec48f2c118c99bb3`.

This is a recurrence of the *existing* documented bug, not a new Canonical rule. The regression reinforces performing size/diff checks **before** pushing and retaining parser CI as an independent final gate.
