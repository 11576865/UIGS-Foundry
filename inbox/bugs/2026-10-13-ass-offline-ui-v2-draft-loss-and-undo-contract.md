# Bug: ASS offline UI v2 prototype violates draft and Undo contracts

Date: 2026-10-13
Status: Bug / confirmed by source inspection and headless Chromium reproduction / OPEN
Scope: OFFLINE prototype `ASS_Workbench_UI_Prototype_v2.html` from this conversation, **not** ASS-Workbench-Android production APK
Relationship: `inbox/tests/2026-10-13-ass-prototype-responsive-task-and-longpress-qa.md`
Severity: design/interaction evaluation blocker; not a production regression claim

## Evidence, reproduction and observed
Using Playwright + headless Chromium with the exact delivered v2 HTML at a 1440×850 viewport:

### 1. Unapplied Raw ASS draft silently dropped on switching Event
1. Open main authoring screen at Event #39.
2. Set `#raw` to `{\\fs60}IMPORTANT UNSAVED DRAFT`.
3. Select Event #40 via `[data-act="select-40"]`, then return to #39.
4. Observed: the raw field has reverted to the pre-edit string `{\\pos(960,720)\\fs48\\c&H80D0FF&}世界は、まだ美しい` with no confirmation or visible conflict.
Source: event select action unconditionally sets `S.draft=null; S.dirty=false` before rendering.

### 2. Apply is not undoable even though UI claims Undo
1. In Event #39 enter `{\\fs64}EDIT TO APPLY` into `#raw`.
2. Activate `[data-act="apply"]`; observe field shows new content.
3. Activate `[data-act="undo"]`.
4. Observed: field is unchanged, notification `当前无可撤销的正式变更`.
Source: `case 'apply'` changes `current().raw` and `current().txt` but never pushes document history; `S.undostack.push` only appears inside delete-event; `case 'redo'` is a notification stub.

## Why important
The user explicitly demands fidelity to the existing ASS engine: document vs draft, transient preview vs Commit, Undo/Redo, separate Focus/Selection/Binding/Write Target. A click-through prototype that renders all tools and screenshots successfully may still encode a destructive interaction contract. A browser smoke test checking tool count and JS errors cannot claim product interaction fidelity.

## Required correction before use as UX acceptance baseline
- Make draft ownership keyed by stable (project/session, event, tool instance) or explicitly block/confirm draft disposal, depending on designed policy; returning to the event must not silently lose edits.
- Push correct single-transaction snapshots for every committed text/time/style edit; real undo/redo should restore exact previous values and focus where applicable.
- Keep `Save` separate from committing dirty inspector buffers; no false promise that "保存" restores forgotten draft.
- Add regression: Raw edit → navigate to another event → return; Apply → Undo → Redo. Add selection/filter / Host switch variants.
- Validate saved screenshot and real gesture evidence; explicitly label demo operations versus native Android guarantees.

## Deduplication/governance
Foundry search phrases 'ASS prototype lost draft event switch undo missing', 'Raw ASS draft lost on changing event', 'demo Apply Undo has no history' surfaced no matching ASS offline prototype Bug. Prior Foundry candidate concerns native Android draft contract, but this is a distinct *delivered prototype* regression. Do not promote to Canonical and do not assert current Android app exhibits this bug.

## Status
OPEN; bug written to Foundry. No prototype modification in this review turn; user asked for assessment.
