# Bug: QHE Guided Native completed-job recovery drops the size-budget receipt

Date: 2026-10-14 (Asia/Shanghai)
Status: Implemented in Draft QHE PR #105; exact-head final platform CI pending
Area: QHE / Windows Native Bridge / persisted job monitor / budget provenance
Classification: Bug, not Canonical

## Source observation

The original Guided ASS Windows Native UI kept a byte target, predicted whole-container bytes and policy only in the ephemeral `state.nativeJobProjection` created when `runNativeEncode` started. At completion, the live monitor used that object to calculate predicted-vs-actual bytes. After a page reload, `recoverNativeJob()` recovered only the job ID and actual bytes from `GET /api/jobs/<id>`, not the budget. The same completed artifact therefore lost its budget comparison when recovered. A strict-check label sourced from the cached plan would also be insufficient evidence of backend verification.

The Native Bridge itself still owns the completed job's request, actual stored output and strict-gate validation after a browser reload; it must be the source for a durable receipt.

## Implemented correction

- QHE `1298b79ca98dcd16fcd9e95032544ae660941272`: pure normalization/formatting with origin distinction `native-status` vs transient plan; recovered strict proof requires `budgetProjection.strictVerified===true` and actual bytes <= target.
- `008236f6f8d2b65ad229d4bbd1975c03a78aac59`: Guided Native request supplies planned full-file bytes and cost-basis annotation; live completion and `recoverNativeJob` render the same completed budget receipt and keep it on the recovered artifact.
- `929e963969e49cea3d24c33fc71d1cf4d23f8ae4`: Windows Bridge's two completed status paths return the job-owned byte-budget projection, policy and strict evidence only after the existing strict output gate.
- `12123c55344c0fce44a67b6d52ffa569d6f8d0e5` and `4e69d1fd30366aaed37458339098f4f185e54563`: pure checks, status wiring and actual vm-driven page-reload path.
- `40fe91f899afd9c261c17a75c57d2ea66dd47bfe`: Windows localhost smoke verifies non-null durable completed receipt and repeated status consistency after completed two-pass and strict-ceiling jobs.
- `8724a80e794e99f5fa32c5516c39e1d4b9124493`: retire a legacy `ui-shell` source-text assertion on the transient-only `sizeError` path; assert the recovery receipt instead.

Initial frontend CI saw a red **legacy source assertion** at `src/ui-shell.test.mjs` after the behavior changed; the pure recovery tests were green. The current exact-head full set of workflows was queued/in progress at intake, so no final current-head green claim.

## Reusable rule (provisional)

Persist an authoritative result receipt at the runtime/owner of a long-running job, not solely in a browser-memory projection. After reload, return the same prediction basis, actual result and independent strict acceptance status. An actual-output result may be within a user target without a formal strict-ceiling certificate; never elevate a planned target or transient UI memory to a verified delivery contract. Guard incompatible, absent and other-job receipts.

## Dedup and limits

Related `inbox/bugs/2026-10-13-qhe-guided-native-copied-audio-cost-receipt-not-validated.md` deals with **source measurement authorization before execution**; this Bug is **completed-result evidence survival during recovery**. Neither addresses restarting the Native Bridge process, long-form physical playback or real-user movie acceptance. No Canonical change, main merge or release.
