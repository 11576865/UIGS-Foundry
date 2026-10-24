# Candidate: Publication of a multi-artifact result requires per-artifact persistence truth

Status: Candidate / implementation-backed, not Canonical
Date: 2026-10-13
Domains: reliability, workflow, interface-grammar, file-output
Source project: 11576865/MKV-Fast-Muxer
Evidence: merged PR #114, https://github.com/11576865/MKV-Fast-Muxer/pull/114
Current-main confirmation: 15ca805db83e640f867bcbc6e36502d89af25f61; browser E2E run 38366667414 succeeded for that main.

## Observation

A single logical export may produce a primary result (MKV) plus a separately persisted audit report (JSON). Browser File System Access does not provide an atomic transaction covering both destinations. Publishing the primary result and then failing to write the report is a *partial publication*, not a failed media generation and not a fully saved artifact set.

In PR #114, a real Chromium batch scenario injected a report-only quota failure *after* the MKV had been committed. It asserted that the MKV remained in the simulated destination, the JSON was absent, in-memory fallback downloads remained available, and UI / terminal summary reported partial persistence.

## Candidate rule

1. Identify every artifact in the logical result set, its destination and independently verified persistence status.
2. Preflight collisions and target identity across all filenames before starting publication; recheck each target at its actual write boundary.
3. Never claim cross-file atomicity when the storage provider cannot guarantee it.
4. If the primary artifact is already committed, do not attempt unsafe rollback or deletion merely because a secondary report fails.
5. Do not create an orphan report if the primary artifact failed to save.
6. Model statuses as a structured outcome (primary persisted, report persisted, review/audit status, failures, unsaved in-memory artifacts), not one boolean success flag.
7. Bind UI and retry actions to the actual artifact identities; preserve valid already-created artifacts.
8. Regression-test success, collision-before-write, primary failure, secondary failure, and late/stale-identity conditions against a realistic storage adapter.

## Boundaries

This is a *candidate engineering pattern*, not proof of an atomic filesystem protocol, crash consistency in every browser, cross-process locking, or real-device directory persistence. The exact CI covers designated Chromium scenarios and synthetic directory failures; broader filesystem/browser acceptance remains separate.

## Deduplication

Existing Foundry Candidate `2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` already distinguishes generated artifacts, optional persistence failure and batch identity, while `2026-10-03-completed-artifact-identity-survives-current-setting-changes.md` separates old artifacts from current UI settings. This Candidate adds the independently testable *multi-artifact partial-commit boundary* (MKV saved while paired JSON fails), rather than restating queue or artifact identity principles.

No Canonical promotion is requested.


## 2026-10-20 validation: save-only retry and frozen failed-job retry

The original candidate's core persistence distinction is now implemented end-to-end in Softmux **0.1022** [merged PR #163](https://github.com/11576865/MKV-Fast-Muxer/pull/163), `main@2368422dd11dabf9f6ef26532505515400ddd531`, exact integration-head [CI #39391267167](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39391267167) **632/632 Node tests, full native Chromium E2E passing**.

The browser test injects a JSON-report-only write failure after the actual MKV has reached a synthetic DirectoryHandle. It confirms partial persistence, preserves the successful MKV and in-memory fallback downloads, refuses to overwrite a report residue until a simulated user explicitly resolves it, and retries **only missing report save**, with the FFmpeg log unchanged. A second real file scenario deliberately fails only the second frozen batch job at the worker boundary, retains the first MKV/Blob URL and its SHA-256, and re-executes only the previously failed Job ID from the frozen plan with actual media. Independent final MKV subtitle packet PTS is `[100,1550]` ms and native `ffmpeg -copyts` recovered cues match the source exactly.

The implementation separates artifact publication retries (no new FFmpeg) from failed-job execution retries (new bounded mux) and keeps the browser permission boundary explicit. **Scope is current authorized browser session and selected fixtures**; this does not demonstrate 20-job real workload acceptance, actual OS disk crash atomicity or durable FileSystemHandle permission across restarts. Continue to classify this as Candidate, not Canonical. Older stacked PRs #150/#151 were closed unmerged when PR #163 proved their integrated semantics on 0.1021 main.

## 2026-10-23 S11 terminal evidence UI correction (Pending exact-head CI)

Product: [Softmux PR #183](https://github.com/11576865/MKV-Fast-Muxer/pull/183), head `e984e02aa7cc7e8d6f2c6fe178093eb21189248a`, derived from main `585f4e8e8473e09d0a4c7fa63d66368d9a9f9870`.

The product's batch executor already distinguished generated Blob, independent audit warning/unavailable and save-to-directory receipt in per-job states. However `formatBatchTerminalStatus()` still counted every `item.ok` as user-facing **“批量完成：成功 N”**, even when the independent audit was unavailable or the result had not been persisted. This is an aggregate **presentation and evidence-semantics gap**, not a discovered FFmpeg mux or file corruption defect.

Bounded proposal submitted in PR #183:
- Count **generated outputs**, **auditStatus === pass**, **unverified audit (including absent auditStatus)** and **per-job execution failure** separately in the terminal summary.
- Report fully persisted MKV+JSON directory pairs only for rows with a real directory attempt and `savedToDirectory === true`. Do not equate a browser download URL or an MKV-only partial save with complete directory persistence.
- Preserve per-result download fallback, separate MKV/report partial-save warnings, cancellation and fatal-interruption precedence.
- Add Node regressions for warning audit + saved directory, passing audit + failed save, missing audit status and report-only save failure. The new PR does not change the actual mux engine, file writer, audit verifier or version.

**Incremental CI correction (same day):** Initial PR head `e984e02aa7cc7e8d6f2c6fe178093eb21189248a` ran Node/build successfully but stopped the S10 real browser proof before native audit: a historical assertion still required the old aggregate string `成功 20，失败 0`. Product commit `8b0ba3b94d7324f9ac2cbf83df9ad7178e26dea3` updates the real 20-job E2E to require separate generated/audited counts and to reject inferred directory persistence. This is a **test-oracle wording migration**, not a confirmed S10 media failure. Latest exact-head full browser result remains pending at update.\n\n**Evidence boundary:** Product code and tests submitted; exact-head Node/build/Chromium results and real hardware/durable FS proof are not available at intake. This note is **Pending CI / Candidate extension**; no claim of complete S11 acceptance, no change to Canonical. Related Foundry queue Candidate already distinguishes generated and audit per job; this extension records the still-problematic **aggregate user-facing success wording**. No duplicate Candidate or Observation was created.

## 2026-10-23 accepted S11 terminal projection evidence

Product [PR #183](https://github.com/11576865/MKV-Fast-Muxer/pull/183) was **squash merged** to main at `f33b8e3b89f0c71dd7dda47a7e8e532b16685d52` after exact-head `1bc923e9e8bb71f74c9c6e707a122683b10b63d8` passed [Node/build + real S10 20-MKV browser/native audit + full Chromium E2E](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39896403596) and [Pages build workflow](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39896403594). The earlier historical terminal-text assertion was migrated without weakening actual final-media or native audit oracles. This confirms the scoped user-visible distinction among generated, audited, incomplete audit and directory-persisted paired MKV/JSON artifacts for the tested browser cases, **not** physical-device durable storage or universal S11 1.0 acceptance. Remains Candidate; no Canonical promotion.

## 2026-10-25 scoped reuse in single-project user delivery (Pending exact-head CI)

The S11 real single-project workbench previously exposed browser download links only, while its batch job path already had independent `FileSystemDirectoryHandle` readback and save-only retry. Product [PR #201](https://github.com/11576865/MKV-Fast-Muxer/pull/201), head at this intake `5cf99ab6d2990f7d4eef935a2880180f4604aa4a`, reuses the **existing batch save-only registry and byte-readback writer** for a distinct exact generated single-output MKV+JSON pair rather than introducing a second persistence implementation.

The present product branch binds that pair to the actual completed Blob/report and an exact in-session generation owner. A directory picker is user-initiated; the UI distinguishes both saved, MKV-only saved, save failure, and downloaded-without-save claims. Existing download links survive failure. A follow-on mux retires the prior directory-save grant, while the existing browser output and report remain until the next accepted mux operation. The save-only retry revalidates the previously saved MKV before writing only the missing JSON, uses a fresh write boundary for each destination, and refuses to overwrite pre-existing or failed-write residue.

**Concrete new failure-matrix detail:** The Node mock initially simulated a report writer failure *after* creating a report destination and incorrectly expected a successful retry without removing the residue. Codex review on PR #201 correctly identified the contradiction: the real writer must reject the residual name instead of treating it as empty. The corrected tests separately cover (a) report creation denied **before** an entry exists, allowing a save-only retry, and (b) report failure **after** an empty entry exists, which must be refused until the user clears the collision or chooses another directory. The extended Chromium E2E exercises the actual public UI with an actual generated MKV and simulated DirectoryHandle: initial two-file byte readback, report-only retry without rewriting MKV, and external modification of a previously verified MKV causing save receipt rejection. Browser E2E mocks the filesystem adapter; it is not an actual physical OS device durability test.

The earlier precise PR head `224ff2717fa693d8abafece8d4bd8021cd4ba72f` passed Node/build/full Chromium and the S12 large-media workflows. **After adding browser negative cases at head `5cf99ab6d2990f7d4eef935a2880180f4604aa4a`, exact-head CI was still running at this intake**; do not silently carry earlier green evidence forward to the new head. This remains an implementation-backed Candidate extension and does not update Canonical.

**Deduplication:** No new Candidate was created because this is a concrete single-project application of the existing 2026-10-13 per-artifact persistence/partial-publication rule, not a new or conflicting universal invariant.

### 2026-10-25 browser picker cancellation follow-up

The same S11 product PR #201 adds a distinct UI receipt safeguard: after a successful verified save to directory A, opening and **cancelling** a second directory picker must not replace the existing truthful success message with “not saved.” The prior implementation cleared `singleDirectoryStatusMessage` before calling the picker and ignored `AbortError`; it now restores the prior display receipt on user cancellation. A real public-workbench Chromium test asserts this, in addition to report-only retry and changed-MKV refusal. Latest product head after this correction: `1b119d654f7b3067cbcaebd874ed9998e147ec7e`. **Its exact CI is pending**; do not claim success from older commit runs. This is another scoped instance of preserving truthful *historical outcome* through a failed/no-op attempt, still not a new Canonical rule.
