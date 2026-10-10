# Candidate: Shared file journals need synchronization at the shared-resource scope

Status: candidate
Date: 2026-10-02
Domains: reliability, architecture

## Summary

Method-level or instance-level synchronization is insufficient when multiple object instances operate on the same fixed filesystem journal or staging paths.

If two instances both use names such as `latest.tmp` / `latest.meta.tmp`, one instance can clear, replace, or overwrite staging files between another instance's stage and read-back verification even when every public method is individually `synchronized`.

Synchronization must be scoped to the shared resource, not merely to the object instance that happens to access it.

## Evidence

ASS-Workbench-Android uses multiple `RecoveryStore` instances that share the app recovery directory. Its staged recovery write uses fixed paths:

- `latest.ass.tmp`
- `latest.meta.tmp`
- `latest.ass`
- `latest.meta`

Android Emulator Regression for Edge Bookmark integration #63 failed independently in the existing destruction regression:

```
java.io.FileNotFoundException:
.../recovery/latest.ass.tmp: ENOENT
at RecoveryStore.write(RecoveryStore.kt:48)
```

The staged ASS file had already been written, but disappeared before read-back verification. The pre-fix methods were `@Synchronized`, which only locked each RecoveryStore instance and therefore did not serialize another instance's `clear()` / `write()` against the same directory.

A product-side fix is under validation in ASS-Workbench-Android PR #64: all journal IO operations use one process-wide monitor, plus a multi-instance write/write/clear instrumentation stress test.

## Candidate rule

For a shared file journal with fixed staging or target paths:

1. Identify the actual shared-resource scope (directory/path/process/database), not just the object scope.
2. Serialize stage, verify, publish, read, and clear operations at that shared scope.
3. Do not treat instance-level `synchronized` as sufficient when independent instances can address the same files.
4. Keep the entire stage → verify → publish transaction inside the shared critical section.
5. Add a multi-instance concurrency test that exercises write/write/clear or equivalent conflicting operations.
6. If cross-process access is possible, a process-local monitor is insufficient; use an OS/file/database coordination mechanism appropriate to that authority boundary.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- source PR exposing failure: `#63`
- failing workflow: `36986759434`
- failure test: `EditorRegressionInstrumentedTest.repeatedActivityRecreationDoesNotMutateDirtyDocument`
- product fix under validation: `#64`
- fix head at capture: `48fb34a7c90046aebce2f502e1046ed641ab49e4`
- evidence level: observed emulator failure + code-level shared-resource analysis; fix CI pending at capture time

This is a Candidate only. It is not Canonical.


## Follow-up: cross-process Model Registry lost-update boundary — CVS PR #20 (2026-10-10)

In `11576865/Character-Voice-Service`, [PR #20](https://github.com/11576865/Character-Voice-Service/pull/20) advances the same shared-resource synchronization principle from in-process recovery journals to a Model Registry that can be written by independent service/CLI processes.

- A uniquely staged, fsynced and atomically replaced `model-registry.json` prevented partial JSON reads, **but did not prevent Lost Update**: two processes could load the same old snapshot and then overwrite each other's independent lifecycle mutations.
- The repair holds an advisory OS exclusive file lock over the **entire read-modify-write transaction** for `scan_model_root`, `set_status`, `promote_model` and `retire_model`; the scan includes directory discovery and weight verification, not merely its final save.
- The lock identity is the canonical registry path, and its `.lock` file persists on disk rather than being deleted/recreated. Linux uses `flock`; Windows uses a byte-range lock. Cross-process regression tests use separate Python interpreters and force overlapping model status updates.
- Lock ownership is cooperative. A direct low-level whole-snapshot overwrite with stale data, an external writer ignoring the lock, or uncoordinated edits to physical model artifacts remain outside this protection.
- Evidence is **source+test implementation submitted, Pending CI**, not a verified production incident or a passing Linux/Windows workflow. Source PR is stacked on CVS #19; merge reconciliation remains outstanding.

Dedup assessment: this is implementation evidence for the existing shared-resource-scoped synchronization Candidate, not a new generic lock rule. It also relates to the [CVS Model Registry Bug](../bugs/2026-10-10-cvs-model-registry-promotion-identity-integrity-gaps.md) as a concrete project repair. **No Canonical promotion.**
