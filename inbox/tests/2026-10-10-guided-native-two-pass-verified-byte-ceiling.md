# Test: User-selected two-pass size strategy and fail-closed Native container byte ceiling

Status: Test; Windows Native synthetic CI passed, physical user-device acceptance pending  
Date: 2026-10-10  
Domains: media-encoding, UI policy, byte-budget acceptance, staging, native job state machine  
Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/86  
Merged QHE main: `7774777b36d57ea8c31f484dad7e8ba6573e70e4`  
Related QHE Issue: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/85  
Related older Test: `inbox/tests/2026-10-10-guided-cq-versus-full-vbr-budget-accuracy.md`  
Related Candidate: `inbox/candidates/2026-10-04-private-staged-mutation-publish-only-final-verified-output.md`

## Distinct acceptance question

The existing Foundry CQ→VBR test identified **size and quality model prediction error** from real encoding. This Test adds **end-user execution contract evidence**: a Windows Native guided budget request can choose an explicit two-pass software encoder and, for a declared **strict** byte ceiling, refuse publication of the output when the **actual container bytes** exceed that user limit.

Do not conflate statistical likelihood of hitting a budget with post-output **pass/fail verification**. A strict ceiling strategy can produce no successful output.

## Implementation and invariants

QHE PR #86 implements:
- An explicit, default-preserving selector with `best-effort` (original one-pass possibly NVENC), `two-pass` and `strict-ceiling`. Opt-in software modes only accept Windows Native **H.264/libx264**, **not** silently substituting codecs when a different user codec was selected.
- The first and second software passes derive from the **same source, ASS/font/scale video filter, preset and target bitrate**. First pass is intentionally nonpublishable, and has no audio. The second produces the real container with the requested audio settings. Both stages count toward progress, and stage transition failures are terminal.
- Strict success checks the number of bytes of the **actual final container** (not a VBR target or projected sample size) against `sizeCeilingBytes`. On overshoot, the staged file is deleted, the terminal state is `failed`, and the existing `Export-Job` precondition forbids saving it. A previous user export is not touched. **No auto-retry or guarantee that the target is achievable.**
- Since CQ samples may be obtained from the preferred hardware NVENC rather than the explicit two-pass software encoder, the chosen-plan summary suppresses incompatible CQ SSIM and historical speed extrapolations. One separate measured R-D chart remains, labeled according to its evidence context.

## Real Windows Bridge execution fixture

Windows GitHub CI runs `scripts/check-guided-budget-native.ps1`: starts the actual PowerShell localhost Native Bridge and FFmpeg with a two-second 320×180 lossless FFV1 testsrc2 source and a real ASS cue, and calls the production `/api/encode` and `/api/jobs/{id}` endpoints.

Observed outcomes on the Windows runner:
- Software two-pass strategy: **completed**, staged Matroska **73,585 bytes**, encoder **libx264**.
- Strict `1,024`-byte ceiling: task terminal **failed**, error identifies strict container limit; repeat query stays failed and cannot pass `Export-Job` precondition.
- Strict `5,000,000`-byte ceiling: **completed**, **73,585 bytes**, repeat query remains completed.
- The runner saw stage 2 progress. A 2-second **stage 1** can finish before the first HTTP polling result, so requiring both transient states be sampled would be a race-sensitive *test flaw*. Complete two-pass output and recorded second stage are the stronger acceptance evidence on this tiny fixture.
- Frontend policy/unit/UI tests, Windows Native smoke, Windows Runtime and UIGS Evidence Coverage all passed at PR #86's merged head.

## Boundaries

The test uses synthetic **software** H.264 on a CI Windows runner. It is **not** real NVIDIA NVENC, HDR/VFR, 4K60, multi-hour content, complex subtitles, multiple audio tracks, OS crash recovery or full export/reopen UI acceptance. Strict mode checks **container byte bound**, not a guarantee of acceptable full-film visual quality or an exact-byte encoder. Extra retries/quality adjustment are not implemented. For real footage, ensure cancellation, crash-safe cleanup, post-encode decode validity and performance receive independent field Cases; QHE #85 and #77 remain open.

This evidence supports an existing staged-publication Candidate but must **not** promote Canonical from one controlled fixture.


## Post-completion strict-size revalidation regression — QHE PR #87

Source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/87  
Merged: `3dc38d08e1aad99013be7654e3d17acc8622c692`  
CI: Windows Native smoke, Windows Runtime and UIGS Evidence Coverage passed.

A completed two-pass task can remain in private staging before the user saves it. The initial byte-ceiling check in PR #86 did **not** guarantee that a later staged artifact was still within that limit. A stale `completed` response could remain exportable after the staged file changed.

PR #87 introduces `Test-GuidedStrictBudget` and calls it both immediately after native encode finalization and on **every subsequent completed-job status query**. The export path also rechecks status after the modal destination selector, then rechecks source status and actual **copied private-temp bytes** (positive, ≤ strict ceiling, equal to the freshly checked source size) before `Publish-VerifiedOutput`. Failure cleans up the unpublished private temp file. This avoids publishing an oversized file merely on the authority of a previous success.

**Actual Windows Bridge mutation test:** a synthetic software H.264 two-pass output first completes under an explicit **5,000,000 byte** limit. The test then expands the completed staged MKV to **5,000,001 bytes**. A new production localhost `GET /api/jobs/{id}` must return `failed`, delete the oversized stage, and the subsequent `POST /api/jobs/{id}/export` must reject before save dialogue. This ran successfully in Windows CI.

**Evidence limits:** the real Bridge test covers post-completion stage tampering and rejection at export precondition. It does **not** exercise a graphical Windows Save File Dialog or a mutation occurring between post-dialog copy and publication; those protection checks are implemented but lack a GUI timing/fault-injection acceptance. A byte ceiling is not a cryptographic integrity or visual-quality guarantee. Owner-closed QHE #85 remains closed; hardware/long-form field work remains #77.
