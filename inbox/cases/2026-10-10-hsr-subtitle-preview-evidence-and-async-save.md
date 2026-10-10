# Case: HSR subtitle workbench separates rendered evidence from editable drafts

Date: 2026-10-10
Status: Case / Implementation evidence, validation pending
Domain: subtitle authoring, responsive UI, asynchronous media preview, browser state ownership
Source project: `11576865/HSR-Voice-Archive-Builder`
Source branch: `feat/subtitle-style-workbench-evidence-v15`
Source implementation checkpoint: `02012fc13ffa5eb3e7dddab248f83e41e81ec285`

## Situation

The HSR subtitle style workspace offers two previews of the same trial configuration:

- browser geometry solving, which exposes safe-area and collision diagnostics;
- on-demand FFmpeg/libass rendering, which provides an actual rendered frame.

Neither is equivalent to a persisted project setting or verified published ASS artifact. Both involve asynchronous behavior; the user can edit trial controls or switch projects while prior previews/save calls are still in flight.

## Risk and observed code boundary

Code review of the pre-change request handlers found no source/generation guard before a returned renderer image was installed, and no generation guard before a returned geometry preview updated UI status. Thus out-of-order completion could publish a result belonging to a previous edit. This is a *code-level risk analysis*, not a claimed independently reproduced field failure.

The save action also applied `fillProject()` after the request completed, which reloads saved style controls. If a user changed settings during the POST, the reload could overwrite that new draft. Recording `subtitleSettingsPayload()` only after the POST could then incorrectly mark the newer draft as saved.

## Implementation response

- Persistent provenance bar displays `geometry`, `rendering`, `libass`, `stale`, or `failed`.
- A request generation number **and** identity of project + submitted payload guard real-render preview publication.
- A geometry request generation rejects older asynchronous layout results, including those that complete during a debounce interval.
- Manual switch back to geometry invalidates earlier actual-render requests.
- Save captures the submitted snapshot before sending. A newer live draft is not reloaded from the older response, is left unsaved, and prevents Save & Generate ASS from misrepresenting the prior saved version as the current edit.
- The UI keeps one responsive workbench and the same domain/API IDs, while adding declared desktop/tablet/phone production visual capture states.

## Validation contract

Source tests:
- `tests/test_subtitle_style_workbench_ui.py` — hierarchy, responsive layout, evidence modes, identity guard and save contract.
- `tests/test_subtitle_style_preview_races.py` — Node VM with delayed response completion using production JS.
- `tests/test_uigs_visual_capture.py` — layout capture contracts.

Evidence at intake:
- Production JS syntax evaluated successfully in V8 for both inline scripts.
- Branch commits exist.
- Full repository CI: **Pending**.
- Registered production visual evidence for the *new* captures: **Pending**.
- Real FFmpeg/libass runtime and device acceptance for v15: **Not claimed**.

## Relationship to existing Foundry knowledge

This is a concrete cross-concern case; do **not** duplicate or promote the broader candidates:
- `inbox/candidates/2026-10-03-interactive-preview-backpressure-stale-results.md` — request identity, stale results and backpressure.
- `inbox/candidates/2026-10-04-interface-as-evidence-system.md` — operational versus interpreted state.
- `inbox/bugs/2026-10-04-async-rerender-can-clobber-live-editor-values.md` — asynchronous rerender versus live drafts.

The case does not establish server-side FFmpeg backpressure or any canonical universal UI rule. No Canonical file is changed.


## Continuation observation / follow-up implementation (2026-10-10)

A continuation of the same HSR PR #132 adds concrete evidence for three already recognized state boundaries; this is an extension of the existing Case, not a new Canonical rule.

1. **Automated sample selection versus manual foreground authoring.** Navigation to the layout workspace previously triggered an asynchronous corpus sample lookup that could replace the Chinese/source trial text with a late response. The added request-generation, project-root and text-revision checks prevent that replacement; manual trial text is explicitly identified and a direct sample reload action is offered. Word timings from an auto-selected sample are discarded when the sample text is manually changed.
2. **Transport success versus actual decoded image.** Returning HTTP 200 and a nonempty blob does not prove that the browser can decode/show the corresponding libass frame. The UI now defers success evidence until image decode/load has completed and surfaces failures separately. Outdated requests are aborted at the presentation boundary, with no claim of server-side job cancellation.
3. **Project-scoped save commit.** A UI single-flight guard prevents repeated Save/Generate submissions while one POST is pending. Both the FastAPI and Termux-lite settings endpoints accept `expected_project_root` and fail closed when supplied but inconsistent with the current active project, while old clients lacking that field remain compatible.

Added regressions exercise the production sample-loader JS with delayed responses, decoded-image success/error, concurrent save attempts, and backend project identity acceptance/rejection. The source-level V8 simulations passed; full updated CI, registered visual evidence and runtime/device acceptance remain separate validation statuses.

Source: `11576865/HSR-Voice-Archive-Builder`, PR #132, development checkpoint `9a70dabe02b6e9927913fa8963fc8c1575efb5dc`.

**Deduplication:** Continues the existing HSR case, consistent with the Foundry preview/backpressure Candidate and live-editor-rerender Bug. Does not overwrite those records or promote Canonical.
