# Candidate: Compose incompatible mutation engines through private stages; publish only the final verified artifact

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #109

## Observation

Two valid mutations may require different specialised streaming/write paths and therefore cannot always be executed safely in one writer pass. Forcing them into one generalized path can destroy invariants that the specialised path exists to protect.

ASS Workbench encountered this when combining:

- same-slot ASS replacement, which injects regenerated subtitle blocks through a specialised path; and
- external Track import, which merges blocks from several container sources through a k-way streaming path.

The product composes them as private cache-local stages instead of publishing the first stage.

## Candidate rule

When a single user transaction contains mutations implemented by incompatible or independently validated transformation engines:

1. Preserve one **user transaction / plan** even if execution requires several internal stages.
2. Each intermediate artifact is **private implementation state**, not a user-visible saved result.
3. Later stages consume the previous stage's actual output rather than reconstructing an assumed state.
4. Only the final artifact is eligible for publication to the user-selected destination.
5. Run end-to-end verification against the original plan on the final artifact; success of an intermediate stage is not sufficient.
6. If any later stage or final verification fails, do not publish the intermediate artifact as though the transaction succeeded.
7. Keep staging local/ephemeral when possible so internal composition does not create extra user-facing files or identities.

## Implementation evidence

PR #109 uses this rule when dirty ASS replacement and external Track import coexist:

1. write an internal cache `ass-stage.mkv` with the specialised ASS replacement path;
2. import external tracks from that actual staged container into the final cache artifact;
3. re-scan and verify the final artifact against Track, Attachment, Chapter, ASS, and identity invariants;
4. only then copy the final artifact to the user's destination URI.

When no specialised ASS replacement is needed, Track import remains a one-pass remux.

## Evidence boundary

This is one implementation pattern, not a requirement to use filesystem staging. An in-memory pipeline, transactional database, object store, or streaming graph may provide the same semantic boundary.

Do not promote to Canonical from this evidence alone.


## QHE size-ceiling publication test checkpoint — PR #86 (2026-10-10)

A **second project** provides a distinct implementation context for private staging and publish-only-after-verification. QHE PR #86, merged as `7774777b36d57ea8c31f484dad7e8ba6573e70e4`, runs explicitly selected two-pass software H.264 on the real Windows Native Bridge. Pass one creates only private encoder statistics and a null output; pass two produces the staged Matroska. A user-selected **strict** ceiling rejects the *actual completed container bytes* if greater than the declared limit: the job becomes failed, staged output is removed and the existing export operation refuses to publish anything. A Windows synthetic Native API test proved a **1,024-byte strict failure** and a **5,000,000-byte strict success** (73,585-byte output).

This reinforces the Candidate's *private intermediate / only verified final publication* transaction boundary. It is a bounded software CI example, not user GPU/multi-hour/export-dialog field acceptance. The existing Candidate rule is unchanged, not promoted to Canonical. Separate Test: `inbox/tests/2026-10-10-guided-native-two-pass-verified-byte-ceiling.md`.


## QHE stale-success protection — PR #87 (2026-10-10)

A second QHE checkpoint strengthens the existing *verify before publication* Candidate: correctness must be bound not only to the stage contents **at encode completion**, but to the same artifact when the user finally publishes it. QHE [PR #87](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/87), merged `3dc38d08e1aad99013be7654e3d17acc8622c692`, revalidates strict staged container bytes at every terminal status query and after a potentially long-running Save dialog; it checks the copied output's actual byte length and source staging status again just before atomic publication. A **real Windows Bridge regression** first completed a strict two-pass H.264 result, then enlarged the private staged file from ~73KB to **5,000,001 bytes** against a **5,000,000-byte ceiling** and verified job failure and export refusal.

This demonstrates a **time-of-check/time-of-use (TOCTOU)** risk in staged publication: a previously successful gate can become stale. The observed test enforces stage-mutation rejection, not arbitrary content-integrity guarantees and not a tested GUI save-dialog mutation race. No Canonical promotion; physical-device/long-form work still pending.


## QHE same-size staged-content mutation guard — PR #90 (2026-10-11)

A new boundary is visible beyond the byte-length TOCTOU failure covered by #87: a staged file can retain the **same byte count** while its contents change after completion. Size checks alone cannot bind the published bytes to the artifact that actually passed stream/packet verification. [QHE PR #90](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/90) (`bfbc6b502d5fe6fe6c297ff55096095cda4bb17d`) submits an opt-in strict-mode SHA-256 fingerprint of the validated final staging file, conditional recomputation on later status when filesystem metadata changes, and an unconditional fingerprint comparison of the **export temporary copy** before publication. Its Windows Bridge regression modifies one byte without increasing file size, checks rejection and verifies export remains blocked.

This is a **submitted Test / Pending CI** checkpoint, not a passed test or a claim that cryptographic hashing removes every last check-to-publish race. Fingerprint generation consumes sequential file I/O for strict jobs; full long-form performance must be evaluated independently. The established Candidate is extended and remains **Candidate**, not Canonical.


## Integration with cancelled long jobs — QHE #88 + #90 (2026-10-11)

QHE [PR #88](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/88) **merged** into main as `5bbc6a81a18694399a9fd3a298e29bd6cdbba117`; its Windows Native real-FFmpeg/Bridge regressions passed. An incomplete long two-pass task no longer relies on further status polling to finalize cancellation/clean its private staging. The request marks cancellation *before* possible pass transition, confirms process exit with a bounded wait, and only then removes private assets. Previously completed output is preserved. Failure to confirm termination retains private files rather than deleting data still owned by FFmpeg.

Original strict fingerprint PR #90 could not be trivially merged after #88 touched the same Bridge and regression file. PR #90 now contains an explicit semantic two-parent merge of #88's mainline and the original digest guard, plus a follow-up correction to preserve the *entire* equal-size mutation fixture. Latest head `56535f5cf5b78fab207c41885fbe813984ac015f` is **Pending CI**; earlier individually green branch results cannot be reused as proof of the reconciled tree.

The reusable candidate observation is distinct lifecycle ownership: a user's cancelled operation has no guarantee that the UI will poll again, so confirmed-stopped native processes must finalize private staging at the cancellation boundary; published user output is a different resource lifetime. Still Candidate, no Canonical promotion.


## QHE PR #90 merged integration evidence

Follow-up to prior Pending CI checkpoint: reconciled PR #90 head `56535f5cf5b78fab207c41885fbe813984ac015f` completed **four successful GitHub workflow runs** (UIGS Evidence Coverage, Frontend, Windows local smoke, Windows Stream Plan v4 runtime). It subsequently **merged to QHE main** as `c1c7872016dbee4d0c199522a5ab7bfcf77d4665`.

This confirms the submitted synthetic tests and mainline integration. It still does not prove physical multi-hour/NVIDIA/HDR/VFR integrity or eliminate all file-system race windows. Maintain Candidate status; no automatic Canonical change.

## QHE Figma v3: static UI projection of the publication gate (2026-10-16)

Design-only observation, not a backend regression: the v2 Figma artifact screen paired pending check text with two visually enabled Save actions. The next design iteration makes those actions Disabled-component instances and states which required check remains incomplete (per-stream preservation difference). It adds Run required checks and Export check report so a disabled Save does not leave a dead end. Optional target-player reopening is explicitly separate from mandatory checks.

Evidence: Figma file FPHdsXxN7xNniLKjZQcVKd, screen node 3:500; structural read confirms save instances 3:582 and 3:629 use QHE/Button/Disabled, opacity 0.55. Visual review confirms the missing-required-check explanation and next action are visible. This does not mean runtime disabled/keyboard semantics, backend gate behavior, or a real output were tested. Existing runtime gate evidence above is independent.

Related design work made output planning the default view, collapsed inactive empty previews, and drew desktop/tablet preview states with 772×434.25 and 596×335.25 viewports (16:9 example). Source display aspect must be derived from actual media, including sample aspect ratio, when implemented. Geometry does not establish usability or device acceptance.

Dedup: this is a static UI projection case attached to the existing verify-before-publication Candidate, not a new universal rule and not Canonical promotion.
