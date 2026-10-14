# Bug: Valid reviewed FileUID falsely rejected because target UID and selection epoch were passed in reversed order

Date: 2026-10-14
Status: **fixed in merged product / regression verified in real Chromium**
Classification: Bug, not Canonical
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Issue scope: [PR #137](https://github.com/11576865/MKV-Fast-Muxer/pull/137), UI readiness before launching a real EBML writer.

## Observed symptom and independent evidence

Multiple exact-head complete Chromium workflows with green Node/unit and Vite build, including [38538687371](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38538687371), [38539535736](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38539535736), [38540246954](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38540246954), [38541032760](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38541032760), and [38541845779](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38541845779), failed *before the writer began*. Real browser UI showed source file, single replacement file, unreferenced selected UID, explicit review and inventory all valid; the prepare button remained disabled with `EXACT_FILE_OR_SELECTION_EPOCH_CHANGED`.

The final per-predicate diagnostic (last red run) explicitly showed `inspectionSourceMatches:true`, `userReviewed:true`, `sourcePickerHasOne:true`, `replacementPickerHasOne:true`, `targetUidExact:true`. Other attempts attributed this to unstable browser `FileList` and `File` wrapper identities, but this was not the root cause of the false result.

## Root cause

The guard signature is:

`current(sourceFile, newFile, target, token)`

The UI refresh invoked:

`current(source, substitute, epoch, row.fileUid)`

The **third and fourth positional arguments were reversed**. The gate was asking whether a string FileUID equaled an integer selection epoch. The valid authoring path was therefore always blocked. The generic rejection name misleadingly suggested a source security fault when the fault was call-site integration.

## Fix and regression evidence

[Commit bfa1be0](https://github.com/11576865/MKV-Fast-Muxer/commit/bfa1be00b670c92bd572b73957c4a1191a06c53c) corrected the guard invocation to:

`current(source, substitute, row.fileUid, epoch)`

It did **not** remove review, source, UID, File identity, hash, source generation, or output audit requirements. The final [exact-head workflow 38551049217](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38551049217) passed 542/542 Node, Vite and complete Chromium, including a real downloaded variable FileData MKV independently verified by MKVToolNix and `ffprobe`. The entire product PR merged as [2e56a85](https://github.com/11576865/MKV-Fast-Muxer/commit/2e56a856f2dc2f58c291e532cb251833b3f54b91).

## Reusable, evidence-limited conclusion

When all *individual* source/UID/review predicates are true but their aggregate guard returns false, inspect the exact function signature and call-site argument order **before** changing the underlying security policy. A named/object argument contract or targeted test can make this class less likely; such an architectural recommendation is a **candidate**, not an automatic Canonical requirement. The real test must include gate readiness **and** a final independently verified artifact, so falsely permissive changes do not masquerade as fixes.

Dedup check searched `wrong positional argument order FileUID epoch guard readiness` and `UI guard all predicates true but positional argument mismatch false` in UIGS-Foundry with no matching existing Bug. Related [P0/P2-V Case](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/cases/2026-10-14-mkv-variable-filedata-adjacent-void-without-offset-movement.md) contains the bounded writer evidence; this record isolates the cross-project UI predicate defect. Never auto-update Canonical from this single product event.
