# Bug: Programmatic batch execution can race asynchronous input preflight

Status: **Bug / reusable orchestration failure**
Date: 2026-10-02
Project evidence: `11576865/MKV-Fast-Muxer`, PR #53

## Failure

A single-item workflow added asynchronous media-identity preflight on video selection. The preflight correctly placed the UI in a pending state and temporarily disabled mux execution.

The existing batch orchestrator reused the single-item UI path by programmatically setting `videoInput.files`, dispatching the normal change event, and immediately triggering the mux button.

That produced a race:

```text
batch sets input
  -> change handler starts async preflight
  -> execution becomes temporarily not-ready
batch immediately requests mux
  -> request is ignored because mux is disabled
  -> batch records the item as failed
```

The media-identity feature itself was correct for interactive use, but the orchestration contract had not been updated for the new asynchronous readiness dependency. Browser E2E exposed this as two formerly valid batch jobs completing with `成功 0，失败 2`.

## Reusable rule candidate

When programmatic orchestration reuses an interactive workflow that has acquired asynchronous preflight, parsing, validation, probing, initialization, or derived-state work:

- the orchestration layer must await an explicit readiness signal rather than assume that assigning input means the workflow is immediately executable;
- a disabled command control is presentation of readiness, not a synchronization primitive;
- input-change handlers that start asynchronous work should expose a promise/state transition/event that callers can await;
- batch loops should establish a per-item sequence such as `set input -> await preflight -> execute -> await completion`;
- restoration of prior inputs should obey the same readiness contract if restoring them triggers preflight;
- regression tests should cover both the interactive path and a programmatic/batch path after introducing any new asynchronous preprocessing.

## Fix evidence

PR #53 tracks the current media-identity preflight promise and makes the batch loop await it after changing each video input and while restoring the previous input state.

The failure was detected by the existing full browser E2E batch scenario after the new single-item media-identity scenario had already passed, demonstrating why single-item success is insufficient evidence for orchestration compatibility.

## Scope

Applicable to batch processors, import queues, multi-file editors, wizard automation, test drivers, and any architecture where programmatic flows reuse UI event handlers.

Do not promote to Canonical from this single-project failure without broader validation.


## Additional test evidence — font identity preflight

PR #58 added asynchronous structural font preflight to the interactive path. The mux control now remains unavailable while font identity is pending and remains unavailable for structurally invalid fonts; the batch orchestrator explicitly awaits the same preflight after programmatically changing font inputs.

Full browser E2E exposed two useful test-contract consequences:

- an older test that asserted mux readiness immediately after asynchronous subtitle input assignment had to wait for semantic readiness rather than event dispatch completion;
- the malformed-font scenario could no longer click the mux button and expect a late parser failure, because invalid fonts are now correctly blocked earlier by preflight. The regression was rewritten to assert the preflight diagnostic, disabled execution state, absence of stale output, and recovery after replacing the font with a valid resource.

This strengthens the existing rule that asynchronous preflight changes both orchestration and test contracts. Tests should synchronize on the workflow's semantic ready/invalid state, not on the fact that an input-change event has fired.

This remains Bug / Candidate-level evidence and is not promoted to Canonical.


## Additional test evidence — asynchronous batch-plan derivation

While stabilizing PR #59 / #60, Browser E2E scenario 28 exposed the same readiness-contract failure at a different layer. After assigning batch video and subtitle inputs, the test immediately read `#batchPlan` and sometimes observed the temporary state:

```text
正在读取实际视频容器与字幕格式…
```

instead of the derived two-job plan.

The product was behaving correctly: batch identity and pairing are asynchronous. The test incorrectly treated input assignment as equivalent to completed derived state.

PR #60 updates the scenario to wait until the expected jobs and subtitle summaries are present and `batchStartBtn` is enabled before asserting or executing.

Reusable refinement: semantic readiness applies not only to command execution but also to **derived read models** such as plans, summaries, previews, validation panels and computed metadata. Tests must await the derived state they intend to inspect.

This is additional evidence for the existing Bug candidate and is not promoted to Canonical.


## Additional test evidence — ten-sequential source UI readiness (2026-10-10)

While expanding UI-first MKV source container editing in Draft PR #69, existing Chromium `scenarioTenSequential` intermittently wrote the **inferred subtitle title** (`中文 · ASS`) instead of the test's `Loop 1`. Workflow `38023294968` had already passed the new tree-order, disposition and artifact E2E scenarios; the failure arose in the older 10-task loop. The test set video/subtitle/font input files and immediately filled `data-new-sub-field="title"` without ensuring current asynchronous subtitle identity and mux readiness had converged. This was a **test orchestration race**, not proof of a newly introduced mux failure.

The scenario now waits for the active `subInput.files[0].name` to match the requested current subtitle, the title field to exist/enabled, and `muxBtn` to be enabled before filling title and executing. Subsequent latest-head Chromium workflow `38023534205` passed this scenario, all remaining browser cases, and **169/169 Node tests**.

Reuse the existing contract: a change event or populated input control is not proof that asynchronous identity/derived track editors are ready to accept programmatic edits. Tests must synchronize on the current *task identity* and semantic readiness, not arbitrary delays or a stale previous-row selector. This evidence **adds to**, and does not create or promote, the existing Candidate.


## P0 stale batch snapshot review — 2026-10-12

Source product review: `11576865/MKV-Fast-Muxer` `main@9c49af8b32bc0b0926a07dfc1bad700627d60787`
Tracked issue: https://github.com/11576865/MKV-Fast-Muxer/issues/79

The merged Matroska EBML source gate added asynchronous `await sniffFileContainer(job.video)` / `await inspectMatroskaPreservation(job.video)` before `batchRunning = true`. The earlier output-directory check uses `batchPlanGeneration` to invalidate stale approval, but the **new preflight loop has no generation recheck** before committing the batch. While it awaits, inputs/rules are editable, so the old local `pairing` can become stale. A second start click may enter the preparation window. This is a code-reviewed transaction-boundary risk; a controlled browser interleaving has not yet been executed.

Distinct refinement of existing readiness bug: **awaiting readiness is necessary but insufficient**; the approved document/job snapshot must remain valid after every `await`, or the UI must lock its identity for the entire prepare→commit phase. Batch execution must acquire an explicit start lock before asynchronous preflight, reject stale plan-generation/destination changes, and test delayed file reads plus mid-preflight edits. Do not auto-promote to Canonical.


## Verified atomic batch-start mitigation (2026-10-12)

Source project: https://github.com/11576865/MKV-Fast-Muxer/issues/79 (now closed)
Merged PR: https://github.com/11576865/MKV-Fast-Muxer/pull/81
Main commit: `df7720e3b2d889776df8526ecb0678b8264877dc`
Head Chromium CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38200486406
Main Chromium CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38200756917

Confirmed by source review: the initial P0 batch EBML preflight ran async without `batchRunning=true`, without a preserved `batchPlanGeneration` check after source reads; old local `pairing` could outlive changed inputs/rules.

PR #81 adds `batchStartPending` prior to the first `await`; locks the interactive start/source inputs; exposes cancellation; captures plan generation, output directory identity, source/subtitle/font identities and batch rule snapshots; checks these after all awaited preflight operations and immediately before committing `batchRunning=true`; retains earlier result links on refusal; and re-derives button readiness after cancellation/stale rejection.

Real browser E2E deterministically delays a `File.prototype.slice().arrayBuffer()` read during batch startup. When source/subtitle inputs are replaced programmatically, no stale job executes, the plan is invalidated, and the new plan becomes ready. A separate delayed-read cancel scenario verifies no job/output is created and readiness recovers. PR head and postmerge main CI passed all legacy Chromium E2E and 226/226 Node tests.

This adds **post-await snapshot validity and transactional commitment** as a refinement of the already documented async readiness contract, not a new Canonical rule. It does not remove the older UI-driven batch executor or establish generic Matroska preservation.
