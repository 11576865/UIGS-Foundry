# Bug: QHE multi-clip verified result cannot be retried from the queue after Native Save failure

- Date: 2026-10-11
- Product: `11576865/Quick-Automatic-Hardsub-Encoder`
- Status: **Source-confirmed bug / product repair committed / exact-head CI Pending**
- Repair PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/100
- Initial repair head: `6ecfbe59c03b28833389c7c3a9766335eae27ff8`
- Related proposal: `inbox/candidates/2026-10-11-single-clip-to-lightweight-batch-segment-queue.md`
- Severity: Incorrect UI recovery workflow; risk of redundant re-encoding or lost native verified output.

## Source evidence

Merged QHE PR #99 processes each clip through the existing `hooks.run` and `hooks.save` and waits for the matching Native export event. In `src/media-workspace.js`, a failed `saveQueuedResult(completed)` is caught and the row is marked generic `failed`, while the existing verified `completed` result remains available. The queue's next `导出剩余` entry point refuses processing when there is an unsaved verified artifact (correctly avoiding overwrite), but the queue row offers only `载入` and `删除`, not a route to retry saving the verified result. The ordinary task Save button may still work, but its result does not update the originating clip row; the next queue operation can re-run that already-verified interval unnecessarily. This is distinct from a failed encode, where a fresh run can be necessary.

## Correct bounded behavior

Keep the verified output and its Native jobId and attach it to the failing queue row. Show `待重试保存` and a row-level `重试保存` action which uses the **same** existing `#taskSave` export path. On confirmed success for the correct Native jobId, mark the original clip `已导出`, unblock processing of remaining clips, and **do not** call the encoder again. On another failure/cancel, keep it pending. Refuse accidental deletion, queue clearing, task switching or new runs while the verified output has not been saved. A changed source must not silently discard a pending verified result. Do not clone encode/download code.

## Reproduction/acceptance

Source-based diagnosis at QHE main `2c4ee1db6513a9778a6a4b08228cc9b93088b910`. New Playwright test appended after the successful two-clip queue: compile a third 125-second clip, emit a jobId-matched Native `ok:false` export result, verify `待重试保存`, confirm Start/bulk export are disabled, click `重试保存`, prove unrelated jobId cannot complete it, then emit matching success. Assert `window.taskRuns` count is unchanged across save retry. This is **simulated Native UI-contract evidence**, not physical system-dialog or SAF device acceptance.

## UIGS Intake boundary

Dedup queries `QHE multi clip save failure verified retry`, `QHE Native save dialog queue jobId failed output`, `无损剪切 多片段 保存失败 重试` found the prior design Candidate and general QHE Case but no bug specifically covering failed per-clip Native Save recovery. Record as Bug; do not promote to Canonical based on this single source-backed case. Latest-head Frontend, Windows smoke and UIGS acceptance remain **Pending External Validation** at intake.


## First CI evidence and bounded repair

PR #100 first head `6ecfbe59c03b28833389c7c3a9766335eae27ff8` completed Windows local smoke `38143033963` SUCCESS and UIGS Evidence Coverage `38143033965` SUCCESS. Frontend/Playwright `38143033916` entered the new failed-save workflow, then failed with **Failed Native save lacked recovery guidance**. The product defect was that the outer catch replaced the specific save-only instruction with a generic message after `clipAwaitingSave` had already been set; the test correctly exposed real user-facing copy drift. It did not reach the subsequent save-only retry assertions.

The bounded follow-up `7b26c4fd2242b6de234287fa771b00ef4ea22c6d` preserves explicit **重试保存，无需重新剪切** text when a verified copy job's save fails. It also blocks a programmatic `form.requestSubmit()` while verified output is pending, supplementing disabled buttons. Browser smoke includes an assertion that this direct submit does not start any new encoder job. **Latest-head Frontend, Windows and UIGS CI Pending External Validation**. Do not merge on prior success or promote to Canonical.
