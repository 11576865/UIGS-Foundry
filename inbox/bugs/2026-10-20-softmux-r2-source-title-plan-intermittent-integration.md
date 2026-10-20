# Pending Bug: R2 source-track title disappeared from executable plan in two integration CI runs

Date: 2026-10-20  
Status: **Bug / intermittent repro, root cause unverified; monitoring / Pending**  
Product: 11576865/MKV-Fast-Muxer  
Affected integration: [PR #162](https://github.com/11576865/MKV-Fast-Muxer/pull/162) (merged after exact-head green)  
Prior validated main: [PR #161](https://github.com/11576865/MKV-Fast-Muxer/pull/161), WU-01 0.1020.

## Actual observed evidence

- [CI #39297140664](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39297140664) on WU-02 re-integrated candidate passed the new exact-file Chapter/Tag safe-navigation scenario, then failed at existing `scenarioSharedContainerProjectRealMux`: `#muxPlan` had original source audio title `Japanese AAC`, not expected authored title `R2 Original Source`, while `R2 Added Audio` and `R2 Added ASS` were present.
- [CI #39297923622](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39297923622) repeated after adding a 12-second wait for the exact authored source title plus external audio and ASS in the current executable plan. Timed out. Therefore do NOT label this as a proven short async delay or weaken the executable-plan assertion.
- [CI #39359223974](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39359223974), exact head `11c17fdde26b31f29a28fae0080d447325458876`, passed all 620 Node tests and complete real Chromium/native scenarios after moving the same R2 case immediately after metadata navigation and adding diagnostics. Diagnostic snapshots after source-title fill and after external changes each showed `sourceInput: "R2 Original Source"`, `planHasOriginal: true`, and source title retained. There was **no corresponding production data-authority fix** between these runs.

## What can and cannot be concluded

The two red exact-head runs are repeatable symptoms in the tested CI order, but the green run after instrumenting/reordering does **not establish the trigger**. Potential event-loop scheduling, stale source-track session, focus/re-render, late probe/authority refresh or test order should be considered hypotheses, not claims. PR #162's merged source code is scoped to observed read-only Chapter/Tag → independent P2 tool navigation and does not directly modify `changeSourceTracks`, so causal attribution to that feature is unproven.

Keep the E2E expected exact title and finished MKV/ffprobe checks. Add recurrent multi-seed ordered Chromium runs or precise source-domain transaction/re-render tracing before classifying fixed. If reproduced independently in main, prioritize a source-domain state/authority fix, **not** an assertion removal.

## Dedupe

Pre-existing `2026-10-02-batch-execution-async-preflight-readiness-race.md` covers old batch UI event/readiness timing, while `2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md` addresses external resource editor epoch behavior. This record uniquely concerns **source-track title → shared executable plan** disappearing in a combined R2 regression after Chapter/Tag UI changes. The 2026-10-20 WU-01 hidden-warning / file-picker-test bug covers false assertions; the present executable-plan discrepancy was a real failed business invariant in a CI run, not proven false assertion.

No Canonical rule changed. Evidence is Pending root-cause determination, not Pending record-writing.
