# Bug: HSR archive rebuild aborts on Android/Termux when Python omits os.link

Date: 2026-10-15
Project: `11576865/HSR-Voice-Archive-Builder`
State: **Fix submitted to main; exact-head CI and physical Termux rebuild pending**
Area: cross-platform filesystem capabilities; last-known-good archive preservation
Evidence level: user screenshot + source-level diagnosis + submitted commits (not a completed runtime acceptance)

## Observed failure

A user's Android/Termux HSR Voice Archive Builder instance failed the `dahlia` project's archive build with:

```text
AttributeError: module 'os' has no attribute 'link'
```

The screenshot identified `app/jobs.py` task runner line 175 and `app/lite_server.py` around line 1170, which delegates to `build_project_v02`. It does not show every lower stack frame; the precise matching source defect was then found in `app/publishing.py`.

The pre-build preservation context tries `os.link(path, saved)` for large published audio/video files and `os.link(src, dst)` for chapter audio tree files. Both fall back to `shutil.copy2` **only** for `OSError`. If the Python build does not expose `os.link` at all, evaluating/calling that missing module attribute raises `AttributeError`, bypassing the fallback before the archive rebuild proceeds.

The previously available regression test injected only `OSError("unsupported")`, so it could not detect the unavailable-attribute failure.

## Product-level repair (main)

- [`801155cf13f5650a6698b7f6d5206d2d0edc14d2`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/801155cf13f5650a6698b7f6d5206d2d0edc14d2): both hard-link attempts now catch `(OSError, AttributeError)` and use `shutil.copy2` when linking is unavailable.
- [`36500ea871b316cdb0ce47bab3df4d2b440564ca`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/36500ea871b316cdb0ce47bab3df4d2b440564ca): added a missing-link regression covering both the large archive audio file and nested chapter file, rollback after a simulated build failure, and marker cleanup; existing `OSError` mock now allows the attribute to be absent.
- [`5a5563effe146020064d269d590523ae4d8da011`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/5a5563effe146020064d269d590523ae4d8da011): corrected the new test's mocking strategy. `patch.object(os, "link", create=True)` followed by `del os.link` breaks patch teardown on platforms that initially lack the symbol. The revised test injects `SimpleNamespace(replace=os.replace)` at `app.publishing.os`, deliberately omitting `link` without mutating the process-global `os` module.

## Verification and explicit limits

The code and test commits were confirmed via GitHub source reads. **No successful actual pytest/unittest run, exact-head CI result, or on-device re-build was observed during this repair.** An earlier assistant answer asserted “3/3 tests passed” without an executed-test artifact; that assertion is withdrawn. Source existence or a commit is not equivalent to runtime pass evidence.

The real-world screenshot confirms a failed build, not voice-record corruption. Falling back to `copy2` can require free disk capacity proportional to the existing large audio/video archive; insufficient space and rollback under copy failure are separate test subjects. On-device application also requires updating the local Termux checkout and restarting the service.

## Reusable scope and relation

A fallback is incomplete if it catches only the errors produced by an **existing** platform API. Optional or platform-dependent Python APIs can be **absent**, not merely fail after invocation; test both cases. For a snapshot/rollback workflow, cover large-file and directory-tree branches, rollback cleanup, and the platform where the symbol is originally unavailable. Do not globally monkeypatch foundational modules to simulate missing capabilities if a module-local dependency replacement suffices.

Related existing Foundry record: `REL.LAST_KNOWN_GOOD_ROLLBACK` (experimental). This Bug is a concrete compatibility failure inside that existing pattern, **not** a new independent Canonical rule.

Intake dedup: searched Foundry for `os.link`, `AttributeError`, `Termux` and hard-link-related cases. Found an adjacent CVS `os.link` discussion and the existing rollback pattern, but no matching HSR Termux missing-symbol bug.

**Intake:** Bug / source-level repair submitted / Pending CI and device. No Canonical promotion.
