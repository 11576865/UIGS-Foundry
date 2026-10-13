# Case: ASS Transform draft survives task/Host switching and fails closed on external Raw source changes

Date: 2026-10-13
Status: Native Android main source and test additions committed; Pending External Validation
Product: 11576865/ASS-Workbench-Android
Prior: inbox/cases/2026-10-13-ass-native-transform-time-handles-exact-fallback-pending.md

## Observation and trigger
Follow-up to the native two-handle Transform time editor found that Start/End/Accel/Tags lived only in local remember(transform.rawValue) state. Navigating tool/Event/Host could destroy or reinitialize the local component and discard dirty input. Re-rendering after a Raw source change could also overwrite stale transform index if write intent were based on a previously selected index without source identity validation.

## Actual native implementation
- Added session-owned TransformDraftStore keyed by Event ID and transform index, with baseline source text, baseline fields and exact current string drafts. The UI shares the store via CompositionLocal in both FIXED and SPATIAL_EXPERIMENTAL, and serializes entries with Compose rememberSaveable. Session replacement isolates drafts; deleted Events are pruned. This is UI/session state, not a change in ASS syntax.
- Native InlineTransformCard reads/writes its fields from the session store. A change to the whole Event ASS source when the draft is dirty retains the draft, shows a concise conflict, disables Apply and disables stale preview; explicit Discard reloads canonical values. Clean drafts rebase onto current source.
- Transform panel keys no longer include raw-value strings, preventing recreation from being treated as an implicit draft reset.
- Added setEventTransformIfSourceMatches in EditorViewModel. The existing domain parser/patcher is invoked only when current Event text matches the expected source in the document edit transaction, preventing stale index patching. Undo remains owned by the original document history.
- Native UI acknowledges a committed draft only after guarded ViewModel acceptance; no independent HTML/source writer is introduced.

## Evidence commits
6d58a081c14055afea2b1bbf9a29e64ebf066613: session draft store and save/restore.
2a1511c1568b970358ac349c15fd26e2c345c706: UI draft and conflict handling.
b4e571e6f6161ee811afb9e24328d6b5d01e6f80: JVM state/conflict/serialization tests.
6c87fc71db3cbd347cc54c96b33fa803d5fd5ab7: block previews on conflict.
72f3e53c6ded79d0aa4d7990bf6591fbf859cf52: source-guarded ViewModel write.
05e55f1f41925f77f9e13521e43d39fdbb310c32: UI apply handshake.
fe85ede904d859c6f57fe2804f21e9aa1c2297db: stale-source/Undo instrumented test.
f4843ea3642ca6690db05bdf33ae0c94d4201ccc: cross-tool/Host/Raw-conflict instrumented test.
8f675389049e327e75c9f0acf7667e364f523fa1: durable product checkpoint.

## Validation boundary
GitHub commits verified. One immediate combined-status read returned empty statuses, as did the PR-only workflow lookup on a direct main commit. No native Kotlin compilation, JVM test run, emulator screenshot, IME, stylus or real libass pass has been observed. Tests are committed but their passing status is unknown. Do not promote to project complete.

## Reusable knowledge
For index-addressed source editing, the editing draft must track baseline **source identity**, not just Event ID and token index. A session store retains dirty fields across navigation. External changes to that source should preserve the user's draft but forbid both preview and Commit until deliberate reconciliation. Guard final write inside the canonical ViewModel transaction, not only a previously rendered UI frame. Persistent UI state should be scoped to project/session to avoid cross-project leakage.

## Dedupe / governance
Foundry searches for Android Transform draft session source guarded stale write owner conflict, ASS Transform draft persistence Host switch Raw edit conflict ViewModel, and Transform time sliders exact preservation native test found no matching native implementation Case. Prior HTML draft Case and native timing slider Case are adjacent but distinct.
No Canonical promotion.