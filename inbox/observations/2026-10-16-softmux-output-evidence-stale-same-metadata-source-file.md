# Observation: A passing historical artifact audit must not inherit current-plan authority from lookalike browser Files

Date: 2026-10-16
Status: Observation / mainline correction with targeted runtime proof; full latest-head Chromium E2E not independently confirmed
Product: https://github.com/11576865/MKV-Fast-Muxer
Version: 软封0.1017版本
Exact correction commits: 4d38a3ef8102c8d47632060f70e330ad616b299e, 41a3ae0e55786488693953ac735dd5d497de556c, 7becb46d20fb3fc862e9591465408cbbbac15083, df633e3f31ea1622ca7d6faae3f459e1812bb6d7, bb5f1aaecbaccb19cb849c1fd3e61b6783066359.

## Observed semantic gap

The product already stores the completed mux report, finished MKV SHA-256 and independent ffprobe/attachment FileData evidence, and distinguishes the active editor plan from a previous plan. However the global `projectActualOutputEvidence()` originally computed `current` using `currentSourceKey` (name, size, mtime) and plan equality only. A freshly selected **different File object** with identical display metadata and plan could therefore be labeled as if the old artifact were verified for the current source. The per-object attachment UI had its own exact-File gate; the **global artifact banner** still had a weaker boundary.

This is not a failure of the historical artifact's cryptographic digest. The old report may still be a valid observation about its own output. It is a failure of **applicability to the current user's task**.

## Bounded remedy

- `src/container-workbench-evidence.js`: adds explicit `sourceReferenceCurrent` gate to `projectActualOutputEvidence`, without silently downgrading the historical artifact's own `status`.
- `src/main.js`: both global and per-attachment projections compare the exact current browser File reference against `lastActualOutput.sourceFile`, alongside source key and plan.
- `src/softmux-10.14-workbench.js`: a selected attachment shows that previous artifact audit is stale for a new source or draft, rather than recycling a green per-object status. Styling remains low-glare.
- `tests/container-workbench-evidence.test.mjs`: test with identical display metadata and matching plan but `sourceReferenceCurrent:false`; expects `current:false` while retained old `status:'pass'`.
- Targeted V8 execution reproduced both branches and returned PASS. This is not evidence that the exact latest main head passed complete CI, native Matroska test, or Pages deployment.

## Transferable boundary

Always separate **what a completed artifact audit proves** from **whether that artifact corresponds to the currently authorized source and draft**. Metadata-based file keys are useful for display/reconciliation but cannot grant an independent browser File permission or make a prior artifact current. Do not erase a historically passing independent audit when applicability expires; relabel it as an older artifact and explicitly withhold current-task success. Download/persistence, FFprobe inventory, SHA-256 FileData, UID/TagTargets preservation and player compatibility remain distinct evidence scopes.

## Dedupe / authority

Earlier Foundry `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md` addresses live editable File grant and form drift. `inbox/bugs/2026-10-13-mkv-unknown-header-and-stale-file-preflight-authorization.md` covers preflight authorization. `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md` covers independent preservation evidence. This observation targets the unaddressed **historical-to-current audit applicability claim** in UI. No Canonical change proposed from a single observation.


## 2026-10-24 S12 extension: user-invoked independent real-source/finished-index inspection — Pending CI

Product [PR #200](https://github.com/11576865/MKV-Fast-Muxer/pull/200), first full head `e54e807d8793b857ffa43071b4858dcc60e7c1ea`, based on `main@392b4f591bfd0f100d5a74e8b978365f7d2326ce`. This **extends the existing exact-File/plan evidence-applicability Observation**, rather than creating a duplicate canonical rule.

New product gap: S12 had real Chromium source/output SeekHead, Cues, Block and CueTime scanners, but the modern workbench only presented its existing ffprobe audit. Passing CI alone did not make the additional *optional read-only evidence* accessible in the user-facing actual-output inspector.

Submitted integration:
- A user-invoked “独立检查来源与成品索引” action passes the current exact source File and the actual generated output Blob (not a reconstructed file or declared report) to the existing bounded S12 pointer/Block/timestamp inspections. The result presents per-side scope, reference counts, explicit unverified reasons and limitations.
- It is never a normal mux prerequisite or general preservation/writer grant. In particular, independent pass results for two containers do not prove source→output packet parity, UID graph preservation, playable/decodable media, or persistent user-device save.
- The old output remains separate as a historical artifact when the source or authored plan changes; the action is disabled for stale correspondence. Starting a new accepted mux revokes old URLs and resets the Blob/inspection receipt. A sequence token prevents late scans on retired Blobs from overwriting a new session's evidence. The UI's button-disabled state is also refreshed after `running=false`.
- Added six source-level Node cases and a real browser application E2E invocation after an actual MKV+ASS+font+original-attachment task. The browser scenario **accepts an explicit “unverified” result when the fixture does not contain all S12 required index facts**, rather than fabricating success.

At Foundry intake, [exact-head PR CI](https://github.com/11576865/MKV-Fast-Muxer/pull/200/checks) was queued, not passed. Source-level changes are **implementation submitted / Pending exact-head Node + real Chromium + S12 scoped CI**. This does not satisfy physical tablet / multi-GB field acceptance, and no Canonical change is proposed.

**Deduplication:** This record already specifies historical-to-current output proof scope and exact File/reference gate; the 2026-10-16 per-attachment output Observation covers finer object-level receipts, while the 2026-10-24 S12 independent-proof-budget Case focuses on bounded parser budget rather than actual product UI availability. The current extension adds the missing *user-triggered dual-Blob evidence projection and async output lifetime* without inventing another general rule.
