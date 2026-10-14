# Test — FLAC quality-mode completed mux must be audited even without sizePlan

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `c54a81912db7d06724fa7b7a6f7649165c364ce4`
Status: product implementation pushed; new Windows Native HTTP job acceptance in progress; external PASS not yet claimed.
Requirements: B16 partial. B01–B25/A01–A10 full theoretical initial version remains open.

## Scope and dedup
Prior Foundry B16 Tests address full-source, isolated copy, FLAC preencode and already completed packet observations. The new defect specifically concerns linking **the real compiled Manual task and Native completion path** to the same evidence, not the standalone preflight's correctness. Searches for `FLAC quality mode completed packet audit no sizePlan`, `outputPlan subtitle all mapped ordinals source identity`, `QHE Native FLAC HTTP ledger invalidation mixed output`, and `B16 finished FLAC mux packet evidence` returned no direct duplicates.

## Defect found after real Windows runtime passed
- Exact-head `0bd2381c...`: `Windows B16 runtime acceptance` run `38513613921` succeeded with actual PowerShell 5.1 and FFmpeg FLAC full+trim dual-audio plus separate softsubtitle copy; frontend and UIGS evidence gates succeeded.
- But `Get-CompletedTrimPacketEvidence` required `task.hasTrimRange && task.sizePlan.copiedTrimReserveBytes>0`. A valid FLAC **quality/bitrate** Manual job deliberately has no predictive `sizePlan`, so would never emit completed-mux packet evidence, making the new preflight-vs-final parity report forever unavailable.
- `src/media-stream-plan.js::createOutputPlan` projects subtitles as `{sourceOrdinal,action}` objects while `src/auxiliary-mux-reconciliation.js` incorrectly used `indexOf(sourceOrdinal)` on that object array. The symbolic default `['all']` likewise lacked concrete per-track IDs even when the source stream count was known.

## Regression contract
1. Any completed Native Manual job with an explicitly selected FLAC audioPlan track must trigger bounded FFprobe post-output packet auditing even if it has no sizePlan. Existing copy/trim post-output audit remains intact; quality-mode behavior must not invent a predictive cost.
2. When `compileTask` contains a known subtitle/attachment count, its reporting-only outputPlan must explicitly enumerate `all` into source ordinals while leaving actual FFmpeg optional `-map 0:s?` / `0:t?` behavior unchanged. Unknown count must not produce fabricated ordinals.
3. Reconciliation must map actual subtitle outputPlan objects to source ordinals, detect ambiguous, unknown, stale, or reordered provenance; output status remains only `single-completed-job` with `canReplaceFormalBudget:false`, `canCertifyFutureMux:false`.
4. Workbench status/report exposes measured pairwise per-stream payload equality/delta only after the current task's completed FFprobe receipt is independently available, and must never present it as a budget authorization.
5. `scripts/check-flac-native-http-lifecycle.ps1` actually starts Windows Native localhost server, measures full-source packets, launches/reads FLAC async preview, then **remeasures the same file** and requires prior receipt revocation by measurement ID. It next starts a real Manual Native video + dual-FLAC quality-mode job **without sizePlan** and compares returned `completed-artifact` audio packet bytes to an independent FFprobe scan on staged mixed output. Test is run by Draft-capable `.github/workflows/windows-b16-runtime.yml`.

## Evidence
- Product code: `windows/native-bridge.ps1`, `src/media-stream-plan.js`, `src/auxiliary-mux-reconciliation.js`, `src/media-workspace.js`, associated JS tests, new Windows Native HTTP fixture and focused CI.
- 17 isolated behavior tests PASS on retrieved *actual* repository implementations, including real `compileTask` data structures and expanded all subtitle/attachment mapping. The UI module parsed successfully.
- Prior real Windows focused test run `38513613921` SUCCESS; **new exact-head** `c54a8191...` Windows B16/Node/frontend/UIGS were in progress at the one initial workflow read. Do not claim Native HTTP pass until completed CI provides that evidence.

## No Canonical promotion
This remains a Test entry, not an automatic Canonical update. Future strict-budget FLAC admission requires matching/owned encoded packet artifacts or a justified executable budget contract, independent real browser/long-form/PTS/media fixtures and complete final-output validation. One matching mixed-mux outcome does not prove another job's bytes.


## Exact-head hosted acceptance — confirmed

On product commit `c54a81912db7d06724fa7b7a6f7649165c364ce4`:
- `Windows B16 runtime acceptance`, run `38515635165`, job `115693681408`: **SUCCESS**. The individual PowerShell 5.1 parser, Node JS receipt suite, real FLAC full+trim packet oracle, real multi-audio/subtitle trimmed-copy oracle, and **Native HTTP FLAC preview/source-ledger invalidation + formal quality-mode dual-FLAC completed-artifact audit** steps all concluded success.
- `Test frontend`, run `38515634868`: **SUCCESS**.
- `UIGS Evidence Coverage`, run `38515635024`: **SUCCESS**.

This upgrades the new native source-ledger and finished-mixed-FLAC packet-chain acceptance from Pending to PASS for the bounded synthetic Windows fixture. **Remaining Pending:** real interactive browser/workbench UI, long/VFR/complex formats and source ownership under crash/restart, cross-platform Android/Web and reusable strict-budget FLAC cost authority. No Canonical promotion.
