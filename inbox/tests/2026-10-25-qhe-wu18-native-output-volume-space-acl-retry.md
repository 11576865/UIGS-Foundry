# Test: QHE WU18 output-volume capacity and NTFS write-denial recovery

Date: 2026-10-25  
Project: `11576865/Quick-Automatic-Hardsub-Encoder`  
Status: **Hosted Windows WU02 verified; whole PR exact-head gate pending**

## Distinct problem from WU15–WU17

Existing WU15–WU17 output-safety cases prove authorized-input protection, file-identity equality, temporary SHA verification and reuse of a completed Native Job after failed publication. The destination **storage volume** could still have insufficient space for the new verified copy; source/staging volume space is NOT evidence for output-volume capacity. The user may also select an existing read-only output or lack rights to create a temporary file in its parent directory.

This is a NEW storage-delivery test, not a duplicate of `inbox/bugs/2026-10-25-qhe-native-save-overwrites-authorized-source.md` and not a Canonical revision.

## Implementation / oracle

[QHE PR #145](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/145), last witnessed exact head `54874081d2f5f9eb4d5f11ff10668b1d0a206864`.

- Actual Windows `GetDiskFreeSpaceExW` reports bytes available for the **chosen destination folder**, using `UInt64` values. Refuse in `Assert-NativeOutputVolumeSpace` if available bytes are below the **complete staged output byte count + 8 MiB**; do not subtract old output size, as it must coexist until atomic replace. This is a **preflight, not space reservation** and not proof that a later disk-full event cannot occur. Full-job and Native sample both call it before the same-volume temporary copy.
- Existing target carrying Windows `ReadOnly` attribute is rejected fail closed; user's existing bytes stay unchanged. WU17 selected-destination identity/leases and Save-only UI remain the same.
- Standalone `scripts/check-wu18-native-storage-delivery.ps1` performs a real Win32 call on the runner's temporary filesystem, boundary-checks a **6,000,000,000-byte** hypothetical stage using UInt64 without writing a giant file, checks a deterministic low-space decision without filling the runner, uses a real read-only file, and **denies CreateFiles on a real NTFS destination directory** for the runner identity. It then executes the same temporary-file Copy-Item that Native Export-Job uses, requires an access-denied result and old-file/stage SHA unchanged, restores ACL, and publishes the original verified stage without a re-encode. This is a real NTFS permission-denied test, not an HTTP mock.
- Production Chromium / Native Bridge / actual FFmpeg B21 batch test `capacity-recovery`: first Save cancelled; old target sentinel created; runner-gated `disk-capacity-low` invokes the PRODUCTION insufficient-space check before any copy; old SHA unchanged, no orphan temp and initial Job still completed; click same-job Save-only retry, then separately execute and save second source. Requires **2 actual encodes, 4 Save attempts, 2 independently FFprobe/FFmpeg-decoded MKVs + SHA receipts**.

## Actual CI sequence and important Windows rights observation

The first WU18 exact head failed [WU02 run 40191038543](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40191038543) before Native export because the implementation had used `[ulong]`, not a Windows PowerShell 5.1 type alias. Fixed by changing every type annotation to `[UInt64]` (correct PowerShell syntax), rather than relaxing the capacity check.

The next exact head passed earlier WU13–WU17 and actually reached the WU18 independent permissions oracle, where a test asserting that an NTFS **Delete Deny on the destination file** blocks `File.Replace` failed: Windows still allowed the replacement ([WU02 run 40191194716](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40191194716)). File-level Delete denial alone is **not a safe substitute for the actual CreateFiles permission needed for temporary output**; directory-level `DELETE_CHILD` may explain Windows' effective delete ability, but this possible mechanism was not independently established. Accordingly, the test was corrected to deny `CreateFiles` on the real destination directory and exercise the production `Copy-Item` write boundary.

At exact head `54874081d2f5f9eb4d5f11ff10668b1d0a206864`, [WU02 Windows run 40191481288](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40191481288) **SUCCESS**, with explicit `WU18 REAL WINDOWS STORAGE DELIVERY PASS` (real free space, 64-bit deterministic refusal, readonly, real NTFS directory CreateFiles denial, same-stage recovery) and `WU18 REAL NATIVE STORAGE RECOVERY PASS` (two real Native Job outputs with exact failure/retry semantics). Earlier WU13 through WU17 regression gates remained PASS.

## Acceptance boundary

- **Evidenced:** real Windows available-space measurement; output-volume rather than input-volume authority; simulated insufficient-space branch in production logic; actual read-only + directory CreateFiles ACL denial; same-stage retry; full Chromium/Native double-source delivery.
- **NOT evidenced:** real disk exhaustion mid-copy, cross-physical-volume or network/USB test media, 4 GiB+ actual encoding and transfer, concurrent external disk consumption, user-operated Save dialog on a physical device.
- **No Canonical modification** from this first independent case. As of log entry the full PR's separate Windows VVC runtime CI remains in progress and PR is **not merged**.

## Final exact-head CI and merge closure

At QHE PR #145 exact HEAD `54874081d2f5f9eb4d5f11ff10668b1d0a206864`, **all 10 applicable GitHub Actions workflows completed SUCCESS**, including [real Windows WU02 run 40191481288](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40191481288), Windows Local Smoke, required VVC runtime and Windows codec/stream plan checks. PR [#145](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/145) was **squash-merged** into `main@15d97b4f64441c4f0c135541d81346f99b9d7c6b`.

The exact production `main` source was re-read after merge, confirming one `Assert-NativeOutputVolumeSpace`, Win32 `GetDiskFreeSpaceEx`, PowerShell `[UInt64]` numeric capacities, a reject-on-readonly output guard and **two actual calls** to the volume space authority (full Native Job + sample exports), along with the checked-in independent Windows storage test.

**WU18 bounded confirmed behavior**: actual destination-volume free-space preflight; deterministic low-capacity refusal without touching old bytes, stage, or other queued jobs; 64-bit six-billion-byte numeric safe path; Windows read-only target refusal; genuine Windows NTFS **directory CreateFiles deny** actually blocked temporary output copying; restoring directory ACL and same staged bytes succeeded without re-encode. Shipping V3 Chromium Native batch completed two separate FFmpeg jobs and two saved artifacts through an injected space-insufficiency failure and Save-only retry (four save attempts). WU13–WU17 regressions also passed.

**Explicit NOT VERIFIED:** actually exhausting an output disk while copying, cross-physical-volume or removable/SMB/cloud destinations, multi-gigabyte genuine exports, selected OS dialog on physical user workstation, arbitrary third-party file lock behavior and cross-process adversarial races. A capacity check does not reserve bytes. No Canonical promotion; the standalone Test is kept distinct from WU15–WU17 output-identity Bug.

**UIGS Intake**: found no existing corresponding QHE WU18 test in Foundry prior to initial write; kept one dedicated Test rather than duplicating the original-source-protection Bug. Status now `EXACT_HEAD_CI_VERIFIED_AND_MAIN_MERGED`; not Pending.
