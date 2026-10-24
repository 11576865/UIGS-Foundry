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


## 2026-10-24 follow-up: make current-artifact evidence inspectable without creating writer authority

Product [PR #200](https://github.com/11576865/MKV-Fast-Muxer/pull/200), merged main commit `7c3ec734e962a719cd5c7001afd886807527eaef`, extends the existing user-visible output evidence inspector. The prior mainline contained independently tested SeekHead/Cues/Track/Block/CueTime read-only scanners, but they were not accessible from the user's current single-workbench delivery. Adding a new standalone scanner page or granting persistence authority from a scanned result would have duplicated the source/project state and overstated an evidence tier.

The product now:
- Retains the exact completed output Blob alongside the existing immutable File reference, report and plan; adds a user-invoked action in the existing finished-output evidence pane. It reads the source File and actual generated MKV Blob separately.
- Checks operation start against exact File reference and current authored plan, disables the control for stale output or a busy task, and discards late results from a superseded mux/output. The stored receipt belongs to one completed output object, never a filename/size/mtime equivalent.
- Displays per-file SeekHead/Cues and Block/CueTime scope, including unsupported/incomplete/contradiction reasons, without turning an independent structure observation into packet parity, UID graph, write authorization, or device-save proof.
- Preserves existing fast mux and batch control flow; no new secondary project or execution state authority.

At intake, PR #200 exact head `4302304f8b7121616c6b34462e14b314495a5817` has successful Node/browser E2E, Pages and S12 real-media specialized workflows. These runs cover a controlled Chromium/CI environment; no user tablet or generalized 1.0 Matroska acceptance is established.

**Transferable elaboration of this existing Observation:** Adding a stronger artifact-check feature to a GUI requires *both* a real user-reachable invocation and the same exact identity/revision fence already guarding historical evidence. A successful read-only probe must be displayed as scoped evidence, not automatically converted into permission to mutate or a durable-save assertion. This supplements (does not replace) the 2026-10-16 observation; no Canonical promotion.
