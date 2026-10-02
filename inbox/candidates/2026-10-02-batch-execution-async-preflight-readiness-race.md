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
