# Bug — ContextVar build-ownership can outlive its publisher, nested publisher may clear active marker

Date: 2026-10-23
Project: `11576865/HSR-Voice-Archive-Builder`
Source base: `main@d5eaf369b241ba9def9e41e4050aaf3369742cc5`
Fix: [PR #206](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/206)
Merged main: `16a81eb9ce68c0a9aa2f6a6113e3da1aedfff548`
Classification: **Bug / source-provable reproduction + regression; not Canonical**
Status: **SOURCE-FIXED / PR-CI GREEN / MAIN-CI PENDING / DEVICE FIELD-PENDING**

## Trigger / failure boundaries

A follow-up review after PR #203/#204 found two distinct correctness risks in `app/publishing.py`'s scoped `.build_in_progress` protection.

1. **Copied context authority survives transaction exit.** Original `_OWNED_BUILD_OUTPUTS: ContextVar[tuple[Path,...]]` saved exact output paths and `owns_published_build` checked membership. `contextvars.copy_context()` (also the mechanism used when launching Python asynchronous child tasks) captures the old tuple. The parent `ContextVar.reset(token)` on exit does not invalidate that copy, so a dormant child/saved context could subsequently call `bundle_export_status(output,_owned_build=True)` and incorrectly discount the `.build_in_progress` marker of a *new* independent build on the same path. This is a source-derived capability lifetime defect, not an allegation that an HSR user exploited it.
2. **Nested same-output publication can prematurely clear marker.** A nested invocation of `preserve_published_archive(output,state)` would commit and unlink the marker when the inner call finishes, while the outer protected build remained active, making a partial output appear externally idle. Existing product source did not intentionally call nested guards; this is a tested defensive boundary.

## Fix / design contract

- Replace immutable path-based ContextVar tokens with shared mutable per-transaction `_BuildLease` objects (`output`, `active`). All copied contexts refer to the **same** lease. In `finally`, revoke `lease.active = False` before resetting the local ContextVar. `owns_published_build` requires a live matching lease, so reset cannot be bypassed by copied child contexts.
- Reject a nested protected build for the same output **before** touching output files or marker.
- Keep external queries' build-busy markers strict. Continue to validate receipt, source, subtitle and MKV integrity on the internal path; no “current” or “verified” shortcuts added, no media implementation changed.

## Reproduction / exact CI

Three new `tests/test_owned_build_mkv_seal.py` cases exercise:
- `copy_context` produced within a live transaction can validate then becomes unauthorized upon exit; during the *next* build on the same output its `_owned_build=True` request raises rather than exposing current.
- Copied authority revoked after exception/rollback.
- Nested same-output guard refused while outer marker stays present until outer finishes.

Exact PR head `7075e6e8a73f7d924b53abf9e52c873dbebcb896` passed all five triggered workflows:
[Python 3.11–3.13, Termux Lite, real ink `tests` #39907888369](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39907888369),
[seven actual ASS contracts #39907888415](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39907888415),
[native Windows files and journal #39907888366](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39907888366),
[legacy/current process interop #39907888431](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39907888431), and
[sustained progress stress #39907888459](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39907888459).

The earlier HSR main `d5eaf369...` seven ASS [run #39896683223](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39896683223) initially timed out in dependency preparation (cancelled, no product tests) but **rerun attempt 2 succeeded**. This is a CI environment incident, not evidence of a product regression.

## Dedup and acceptance limits

Foundry searches on ContextVar copy, inherited HSR build marker lease, and nested publisher marker return no equivalent prior Bug. The earlier `inbox/bugs/2026-10-23-hsr-build-marker-vs-mkv-seal-verification-deadlock.md` concerns owner marker erroneously blocking *its own* final seal; #206 concerns stale ownership still valid after it should expire.

Pending: exact merged-main independent CI, a genuine parent/child asynchronous HSR production load, physical Termux user archive `evanescia` rerun, and hardware abrupt power interruption. Unit tests prove the copied-context mechanism; not all deployment failure modes have been accepted. Do not alter Canonical based on this one repair.
