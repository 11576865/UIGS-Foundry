# Bug — PowerShell automatic $args shadowed FFprobe child argv in Windows Native B16

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Failing product head: `83a37a10f1ea10b3fa4f2669c628478e94d29025`
Fix submitted: `a38fc79187d81f2c90d1edbb0675e6080b7391d2`
Severity: runtime blocker of B16 Native packet-cost preflight; not the actual FLAC codec.
Status: fixed source submitted; exact-head Windows rerun Pending at time of recording.

## Real evidence, not a hypothetical bug

GitHub Actions focused `Windows B16 runtime acceptance` run `38510258959`, job `115676894500`:
- PowerShell 5.1 parser PASS; Node JS receipt tests 19/19 PASS; Chocolatey FFmpeg 9.0.2 installed successfully.
- Actual FLAC worker failed during first FFprobe stream inventory call. FFprobe stderr states: `You have to specify one input file.`
- Relevant code in `windows/flac-encode-preflight.ps1` passed a PowerShell function parameter named `$args` to `System.Diagnostics.ProcessStartInfo.Arguments`. In PowerShell, `$args` is also an automatic variable for unbound positional arguments; this name is not a safe explicit process command string parameter. A similar `Run-Preflight` design existed in the isolated trimmed-copy worker but could not run in this workflow because FLAC stopped the job first.
- The failure is **not** evidence that FFmpeg FLAC encode is unavailable. The source-level code and JS tests cannot establish that PowerShell actually delivered the desired commandline.

## Change and regression boundaries

- Both Windows pre-encode workers now name the ProcessStartInfo input `$Arguments` and script-local FFmpeg argument list `$muxOptions` (no `$args` auto variable usage).
- Windows parser and real FFmpeg FLAC/trim-copy packet fixtures remain in a focused Draft-eligible workflow. The exact-head Windows real execution is the required acceptance, not static syntax, matching text, or generic local FFmpeg.
- In the same product work unit, `src/auxiliary-mux-reconciliation.js` adds a *completed-artifact only* FLAC/copy per-track packet comparison against output FFprobe evidence; source-ledger ID, FILETIME, range, actual seek start and output mapping must match. Equality cannot be propagated into the next formal budget or claim exact mux size. One Linux synthetic 3-second dual-FLAC video+subtitle run yielded audio totals 39,300 and 27,599 bytes in both isolated and mixed mux; this is a case observation, not a general equality law.

## Proposed regression rule — Test level only

For scripts that invoke subprocesses via PowerShell, avoid reserved automatic variable names for parameters and argv buffers, and exercise a true shell/runtime fixture before marking the subprocess path accepted. On a failure, retain exact stdout/stderr, distinguish external dependency failures from argv construction bugs, and fix all equivalent call sites together. Do not automatically promote to UIGS Canonical based on this single incident.


## Windows follow-up: production FFmpeg succeeded; expected-failure test harness was red

At product head `a38fc79187d81f2c90d1edbb0675e6080b7391d2`, focused Windows B16 run `38513290671` showed the FLAC preflight succeeded, independent packet audit succeeded, and the **final video + two FLAC audio + soft subtitle** Matroska mux was encoded successfully. Actual auxiliary packet deltas were both zero bytes on that limited three-second fixture. The job nevertheless exited red on the deliberately invalid duplicate-source-track request because stderr `Invalid or repeated FLAC source stream` from a child PowerShell process triggered a terminating `NativeCommandError` in the **parent test harness** with `$ErrorActionPreference='Stop'`. This is not a production FLAC failure.

Fix head `0bd2381c3f0a85195410e610a3cde89ca033daac`: the FLAC and trim-copy **negative test** subprocesses now use bounded separate `Start-Process` invocation (15s), redirect stdout/stderr to separate files, and assert the *actual child* exit code is nonzero and no receipt was created. Exact-head Windows rerun was in progress when recorded.

Reusable test lesson: a negative-process assertion must treat expected stderr as evidence, not as an unhandled failure of the test harness. Differentiate positive-path runtime regression from harness handling of expected rejection before diagnosing the codec or system. Maintain Test/Bug status; do not promote to Canonical from one fixture.


## Final exact-head validation

The third focused Windows B16 run, `38513613921`, on product head `0bd2381c3f0a85195410e610a3cde89ca033daac`, is **SUCCESS**. PowerShell parser, Node evidence suites, real FLAC full/trim dual-track packet oracle, real mixed video/FLAC/softsubtitle mux and real trimmed copy audio/subtitle packet oracle all PASSED. Separate `Test frontend` and `UIGS Evidence Coverage` were SUCCESS. The earlier argv defect and negative stderr harness defect are now **fixed and host-verified in the bounded synthetic fixture**, with long-form and all-platform behavior expressly outside this result.
