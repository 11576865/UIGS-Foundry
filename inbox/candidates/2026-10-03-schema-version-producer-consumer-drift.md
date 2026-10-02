# Bug: Schema-version producer/consumer drift can invalidate a merged cross-platform task format

Status: **Bug / reusable cross-platform contract failure**
Date: 2026-10-03
Project evidence: `11576865/Quick-Automatic-Hardsub-Encoder`

## Incident

The shared media compiler was upgraded to task schema v3 and Web/Android paths accepted v3, but the Windows structured-argument consumer still accepted only v1/v2:

`if ([int]$Task.version -notin @(1,2) ... ) { throw 'Unsupported media task.' }`

The Windows backend simultaneously advertised `taskSchemaVersion=3`. As a result, tasks successfully compiled by the frontend and accepted by the advertised backend contract were rejected at execution with `Unsupported media task.`.

The regression survived the original merge because the Windows smoke test exercised v1/v2 fixtures rather than the current producer version.

## Repair

- update the Windows consumer to accept v1/v2/v3;
- change Windows smoke fixtures to exercise v3;
- preserve older versions only as intentional backward compatibility.

## Reusable lesson

When a versioned task/schema contract changes, update and test all four identities together:

1. producer version emitted by the compiler;
2. capability/version advertised by each backend;
3. version range actually accepted by each backend parser/validator;
4. CI fixtures, which must include the current producer version.

A backend capability advertisement is not evidence that its parser accepts that version. The test must cross the parser boundary.

## Evidence

Repair commits on `main`:
- `8645d596f321b06a7747bd4d63ab66811d92c944` — Windows accepts task schema v3.
- `d7795e6d34dd5732690df8f0b3f60ae315032fed` — Windows smoke exercises v3.
- Windows local smoke passed after repair.

This is a Bug/Candidate record, not Canonical.
