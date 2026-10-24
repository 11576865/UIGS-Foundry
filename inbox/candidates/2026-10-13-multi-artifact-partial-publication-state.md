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


## 2026-10-25 S11 single-project publication path reuses batch readback and partial receipt

Product [Softmux PR #201](https://github.com/11576865/MKV-Fast-Muxer/pull/201) extends the existing versioned batch file writer to the **single-project generated MKV + JSON report** user journey, without creating a different file writer. Version candidate 0.1029.0; product main was `7c3ec734e962a719cd5c7001afd886807527eaef` at branch creation. At Foundry intake, code/Node/E2E submitted and exact-head CI **Pending**, not accepted.

Scoped implementation observation:
- Keep the exact generated MKV Blob, report Blob, output SHA and owner as one session-only save grant, independent of current source File picker; old generated files remain downloadable even when the edit plan changes. A new mux retires the prior grant before exposing new output.
- Expose one explicit user-initiated directory picker (File System Access) in the actual single-project delivery surface. Retain browser downloads when the API is absent or permission fails; do not claim that a started browser download was durably saved.
- Reuse the existing `createBatchSaveRetryRegistry` and `writeNewBatchOutput` complete 1-MiB chunked readback for both artifacts. The registry revalidates previously saved exact bytes and does **not rerun FFmpeg** for a save-only retry. Prior destination receipts do not transfer to a different granted directory.
- Distinguish **report refusal before entry creation**, where a second attempt can safely save only the report, from **report write failure after entry creation**, where an empty/partial filename may remain and subsequent same-directory retry MUST refuse. Allow choosing a different directory; never delete or overwrite unknown residual data.
- New PR #201 Node regression fixtures exercise paired success, report-only save retry, collided destination, mismatched post-close byte readback, different directory, stale output-owner revocation, and failure-residue hard refusal. Real Chromium E2E exercises an actual muxed MKV plus report through the user action into an in-memory FileSystemDirectoryHandle with SHA-256 validation; it is not physical device durability evidence.
- A directory close plus observed readback is not power-loss durability, FS atomic exclusive creation, or comprehensive Matroska graph preservation. It proves only observed bytes and the saved-file pair receipt scoped to the tested handle and instant.

**CI fact at intake:** initial head `ec1565f3fed1db12ccece0572e46304077580564` returned 724/725 Node successes and correctly failed one *test assumption* that a report write failure would leave no directory entry. The implementation correctly blocked a dangerous same-directory retry on the residual name. Corrected product test head `224ff2717fa693d8abafece8d4bd8021cd4ba72f` separates pre-create refusal from post-create residue; its Node/build/Chromium and large-media jobs were still running/pending when recorded. Do not claim green from the first red run.

**Deduplication:** this supplements the existing multi-artifact partial-publication Candidate that already covers batch MKV/report partial persistence and exact saved receipt. The only newly exercised boundary is the single-project user-facing grant with an explicit same-directory residue vs permission-before-create retry distinction. No Canonical changes or generalization based on a single job.
