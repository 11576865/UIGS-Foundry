# Bug — HSR Japanese HF metadata probe early exit retains mmap regex exported pointers

Date: 2026-10-24
Lifecycle: validation-pending
Project: `11576865/HSR-Voice-Archive-Builder`
Scope: Python resource lifetime / read-only dataset metadata scanning
Repair PR: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/210
Severity: **Diagnostic unavailable / no audio data mutation**

## Source-confirmed failure

The new metadata parity probe `app/hf_locale_probe.py::probe_japanese_row_identity` used `mmap.mmap(...)` and `ENTRY_RE.finditer(mm)` to sample the first five valid Japanese voice entries in large `result.json` files. Unlike the preexisting resolver (which exhausts the iterator), the probe intentionally exited after enough samples.

When the `with mmap(...)` block ended, live `re.Match` and `re.finditer` references still retained exported pointers to the mmap buffer. The context manager's close failed with `BufferError: cannot close exported pointers exist`. It was not an HF network outage or a wrong-language WAV, and the probe never wrote voice files.

## Evidence

Exact HSR PR #210 head `7f3f731c80ddfcb806523bb8408760a91a8ebe5e` failed Python 3.12 job `unit (3.12)` in GitHub Actions run #40058658836, with three failures in `tests/test_hf_locale_probe.py` all pointing to `app/hf_locale_probe.py` at the mmap context-manager exit. The failure was exposed by synthetic metadata tests, not an actual Hugging Face server call.

## Proposed repair / regression guard

HSR commit `4922d5503aebbf4e6b41d2e0c0d5bff16a6cb8ec` adds a `try/finally` inside the mmap lifetime. The cleanup clears the active `current` and `following` match references and deletes the regex iterator **before** the mmap context exits, including on an exception. The existing three offline tests exercise normal parity success, drifted parity, and fewer than requested source identities; all previously reproduced the BufferError.

**Validation boundary:** This is source-fixed; exact new-head CI remains pending as of filing. Do not mark regression-verified until the new head passes. No actual Japanese WAV content is downloaded or validated by this probe.

## Dedup / reuse

Foundry search for `BufferError cannot close exported pointers exist mmap`, `regex iterator memory map close early exit`, and `mmap finditer iterator release before close` found no existing duplicate. This bug differs from the HSR cross-locale audio provenance Bug: it concerns Python iterator/mmap object lifetimes when *short-circuiting* a read-only scan.

Reusable engineering rule candidate (not Canonical): Python mmap scanners that stop early must release all `re.Match`/iterator references before closing the map, or convert to non-exporting buffer slices after bounded copy. CI should include an early-break test, not only full-file exhaustion.
