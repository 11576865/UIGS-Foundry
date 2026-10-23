# Bug — FLAC-only standalone delivery can partially retire the last MKV after a filesystem error

Date: 2026-10-23
Project: `11576865/HSR-Voice-Archive-Builder`
Source baseline: `main@f08d91e048b06ba978ce349468c121cd5122435f`
Repair: [PR #208](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/208)
Level: **Bug / source-provable partial cleanup + injected filesystem failure**
Status: **SOURCE FIX IN PR; exact head/main CI and field device verification pending**

## Boundary and distinct failure

PR #207 requires FFmpeg full-stream FLAC decode and identity recheck before the FLAC-only delivery mode retires the previously sealed MKV. That solves **content verification before destructive publication**.

However, the independently callable `app/delivery_artifacts.py:publish_flac_only()` subsequently ran multiple separate filesystem mutations: write replayable background preferences; `unlink` old MKV; `unlink` the verified publication receipt; then `unlink` ASS/SRT/legacy black MKV. An I/O/permission failure after the MKV unlink but before receipt removal could strand the project with its last known MKV absent and a stale receipt. Failure at the last legacy deletion could leave subtitles half-removed and falsely suggest a successful profile change. The outer `preserve_published_archive` safeguards pipeline builds, but the standalone callable function has no own rollback.

## Source repair / safety bounds

PR #208 snapshots all retirement targets `(OUTPUT, RECEIPT, SRT, ASS, LEGACY_BLACK, PREFERENCES)` into a private sibling `.hsr-flac-profile-*` recovery directory **before** the first mutation. Large existing MKVs use hardlinks where the filesystem supports them, and must be fully copied first if hardlinks are unavailable. Existing files are checked for unsafe symlink/nonfile type.

When a normal removal or preferences write fails, the function restores all old artifacts and preferences via `os.replace` before re-raising the original I/O error. If the rollback itself fails, it retains the saved media on disk and marks the output `.build_in_progress` so public status cannot misreport a mixed outcome as current. The full FLAC decode and identity fence from #207 are preserved.

**Limit:** This is best-effort exception recovery, not a multi-file ACID filesystem transaction, synchronized non-cooperating external edits, or tested power-loss recovery. Temporary disk space may be required if the target filesystem lacks hardlink support. An unrecoverable restore leaves its recovery snapshot available for deliberate operator repair; the application does not automatically recover from a hard power cut.

## Tests

Three FFmpeg-backed fault-injection tests in `tests/test_hsr_single_deliverable.py` cover:
1. Success removing MKV followed by a single simulated permission error removing receipt; original verified MKV, byte-identical receipt and prior preferences restored.
2. Failure at the final legacy target after MKV/receipt/ASS/SRT removal; **all** previous outputs recovered.
3. Both commit and restoration fail; previous MKV survives in a retained private recovery snapshot and the build marker makes public state fail-closed.

Existing valid MKV→FLAC→MKV switching still runs.

## Dedup

Foundry search `FLAC profile switch delete MKV receipt rollback`, `publish_flac_only rollback`, `standalone deliverable cleanup partial unlink` found [the earlier PR #207 Bug](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/bugs/2026-10-23-hsr-flac-only-probe-only-retiring-verified-mkv.md) but no specific prior half-cleanup rollback defect. #207 establishes FLAC content provenance; #208 addresses independently failing multi-file cleanup after successfully verified content.

**Pending:** PR-head and merged-main workflow evidence; physical Android/Termux `evanescia` long project; Windows user-device external-error semantics; hard power-loss replay. Do not promote Canonical from this one repair.

## PR #208 initial regression evidence and test-oracle correction

Initial exact PR head `80e05949348b04905d97dbb99b1c74f89af1d28d` passed genuine seven ASS, Windows publisher, pinned historical interop and sustained multi-process checks. Its browser `libass-artifact` job executed real FFmpeg plus new profile-switch tests; two ordinary I/O fault-injection tests passed, while the new *unrecoverable rollback* case expected `bundle_export_status()["state"] == "stale"`. The actual state was `missing`, correctly reflecting that the MKV itself had been removed when the second injected disk failure prevented its restoration. The old MKV was still available in the retained sibling snapshot, and the busy marker existed. This is a **test-oracle error, not a false claim of current/verified**.

Final candidate head `f06530666a4f5817eae26648453cbada52ba7dd8` corrected the assertion to `missing`, explicitly preserving the intended distinction between *retained recovery bytes* and an *installed current deliverable*. A new exact-head workflow set was triggered, still pending when recorded. No production code change was required for this correction.

**Additional safety boundary:** A second I/O failure can make the current main deliverable truly missing even though an intact backup exists. The UI should never call this `current`, and operator recovery must use the retained snapshot deliberately; no automatic field repair was implemented or claimed.
