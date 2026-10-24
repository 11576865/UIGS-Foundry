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

## 2026-10-14 QHE WU-02 recurrence and immediate recovery

QHE initial-version PR #105 had the same cross-language injection hazard while inserting a PowerShell embedded ASS importer through JavaScript String.replace(anchor, replacementString). A regex literal ending in dollar-apostrophe was treated by JavaScript as the replacement token for the suffix after the anchor. The generated windows/native-bridge.ps1 grew from approximately 133 KB to 396 KB, duplicating the old source and corrupting the new function. The temporary faulty commit was 0f8056a03561bb87b13736d02f218555b6325898.

The branch was immediately repaired using the clean pre-change commit 02afa817854822ef0e71f986411e28397d7a09eb and a function replacement (anchor, () => literalSource). Integrity checks required a bounded 139 KB output and exactly one import, original source function and existing Bink2 stage function. Repair commit: 0da4d523966db4f5c4dcd3032825f646808866db.

Status: recurrence fixed at source-shaping layer; focused Windows parser and real media execution CI submitted separately, result initially Pending. This is a repeat of the known Bug, not a new candidate or Canonical rule. Prefer size/sanity checks before every cross-language patch commit.

## 2026-10-24 QHE B21 recurrence: replacement-template duplication of Native Bridge

QHE [PR #136](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/136) repeated this same known cross-language mutation bug. A JavaScript `String.replace(anchor, replacementString)` inserted PowerShell regex source containing the literal `$'` suffix. The JS replacement interpreted it as the *original-string suffix macro* rather than raw PowerShell text, multiplying `windows/native-bridge.ps1` from `main`'s 146,578 characters / 2,562 lines to 405,596 characters / 6,787 lines with three copies of `Handle-Request` and an orphaned partial route. Exact-head Windows WU02 PowerShell parser failed (CI [40079998027](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40079998027), followed by [40080128523](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40080128523)). An attempted in-place restoration of one damaged section was insufficient because the same corruption also duplicated unrelated request handlers.

**Recovery:** QHE `9129089d83e2a91261e05275c0ca9ad281806df3` reconstructed the *entire* PowerShell source from accepted `main@aa466c92ace7aad40209a3f49a77779ec4d18627` and reapplied small B21 additions using callback replacement `s.replace(anchor, () => next)`. Before write, asserted unique anchors, exactly one `Handle-Request`, one original video picker, one new batch picker, one activation function, exactly two batch endpoint routes, original suffix retained, and bounded resulting source length 151,223 characters / 2,658 lines. The repaired preceding-head Windows WU02 [run 40080298563](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40080298563) completed SUCCESS, including two actual file activations/FFprobes and prior WU13 saved-media proof.

**Intake:** This is another occurrence of the preexisting Bug, not a new taxonomy item or Canonical change. Reusable preventive tests must check complete-file size, function cardinality and target-language parser before committing any large cross-language text rewrite. B21's full two-artifact acceptance is a separate QHE Case and remains governed by its own exact-head CI.
