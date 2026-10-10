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


## Additional case: task-centered subtitle workspace versus parameter-only Inspector (2026-10-10)

A design review of HSR PR #132 exposed that extra provenance labels and responsive CSS did not make a global style form into a functional subtitle authoring environment. A concrete extension now adds a first-class corpus explorer, explicit sample selection, search, sequential navigation, bounded large-dataset pagination, session-level style Undo/Redo, and geometry QA based on the existing solver.

**Source implementation:** `11576865/HSR-Voice-Archive-Builder`, same PR #132, checkpoint `3b30f6cebd8749642e887f1557dc44f1f052bd3d`.

**Design/engineering distinctions retained:**
- Estimated text pressure is an exploration heuristic; it is **not** a verified collision or an actual FFmpeg/libass result.
- The bounded audit reports exact coverage of up to 60 filtered rows per execution; unchecked rows never inherit a checked status.
- Long corpora paginate visible navigation instead of rendering every row to the DOM.
- History for live style controls is not the same transaction as source-text edits, settings persistence, or ASS export.
- On mobile, the preview is promoted above the navigation list; the corpus browser remains available through a collapsed, explicit reveal control.
- This is still style/layout workbench capability, not a fully implemented frame-accurate subtitle timeline.

**Validation boundary:** updated code and tests are committed; exact-head asynchronous CI, production screenshots and target-device runtime acceptance must be tracked separately. Visual-composition fixtures are not production screenshots.

**Intake deduplication:** related to the Foundry Candidates on task-centered workflow continuity, UI resource projections and verified evidentiary semantics. Recorded as an extension to this Case rather than a duplicate Candidate or a Canonical update.


## Case continuation: real cue editing versus simulation affordances (2026-10-10)

### Context

The HSR workbench's earlier three-pane layout provided corpus exploration, global style editing and layout QA, but lacked a clear per-subtitle **source → draft → save → regenerated artifacts** transaction. Adding visual time controls without a capable backend would have advertised a misleading nonpersistent feature.

### Implementation evidence

HSR-Voice-Archive-Builder PR #132 now introduces a first-class stage-adjacent cue editor with:

- Source/target text and immutable source start/end/duration metadata. The segment-relative seek scrubber only adjusts the actual ASS preview timestamp. It is not represented as an editable source-timecode control.
- Per-item, session-scoped draft ownership. Switching corpus rows preserves independent unsaved translations; quick preview text edits detach from the selected project cue rather than implicitly updating data.
- An explicit `final_chs` save to the real backend subtitle override pipeline, with submitted-snapshot identity, single-flight submission, project-root guard and draft preservation on failure or post-submit edits.
- A `persistable` API capability field distinguishing manifest-backed editable subtitles from fallback demonstration rows. The UI disables persistent Save when only examples exist.
- Authenticated source WAV audition with optional browser-decoded wave visualization and positional seeking; a fallback player remains when waveform decoding fails. WAV samples are not falsely presented as synchronized final-video waveform evidence.
- Separate validation: production-JS regression for deferred per-cue save, draft navigation and waveform seeking; FastAPI route coverage for project identity and unbuilt preview-only rows.

### Reusable knowledge and limits

The general failure mode is **false affordance through collapsing model capabilities**: a previewable example is not necessarily writable; a timing scrubber is not necessarily a retiming editor; a source WAV is not the final mixed-media timeline; a successful save request is not proof that newer draft bytes have been saved.

This observation reinforces existing Foundry knowledge on editor ownership and evidence levels and is recorded as an additional Case, not a duplicate Candidate or a Canonical rule. Full production-rendered screenshot testing, browser/device acceptance and frame-accurate timing editing remain separately unverified/unimplemented.

Source: `11576865/HSR-Voice-Archive-Builder`, PR #132, cue editor implementation and tests as of 2026-10-10.


## Continued Case: subtitle-only display retiming as a derived, recoverable layer (2026-10-10)

### New observation

The HSR voice archive's source audio timeline and the exported subtitle display timeline have different data ownership. Exposing a numeric start/end editor directly on source `manifest.json` would conflate them and risk destructive rewrites of sound evidence. The same control may safely become functional if it edits an independently versioned, validated **derived timing layer** consumed only by subtitle outputs.

### Implementation and proof boundaries

- **Derived data:** `subtitle_timing_overrides.json` schema v1, per cue start/end millisecond boundaries + originating source audio member and clock. Original manifest positions and continuous FLAC samples are not rewritten.
- **Output integration:** post-build subtitle artifact refresh uses the overlay to construct ASS and SRT adapters, with all project subtitle GET rows describing both original and effective display boundaries.
- **Validation:** bounded ±5 s movement from each source boundary, finite numeric inputs, ≥100 ms display duration, project-root fence and optimistic expected-current-time precondition. Late edits and concurrent text/timing writes have independent ownership.
- **Stale-source recovery:** rebuilding an archive may change its source sample positions. An old timing override is then held as a conflict rather than reattached to a different source event; corpus navigation still works and explicit source-time Reset clears the derived record. This is not permission to apply the stale result.
- **Alignment provenance:** when the display timing changes, previous word timing is no longer treated as verified for karaoke. The edited cue must be realigned before prior word-level time claims are restored.
- **Tests:** filesystem/SRT/ASS-adapter and production-JS regressions plus FastAPI timing route tests are added to HSR PR #132. Final CI, actual libass render, device visual evidence and human timing audition remain separate proof obligations.

### Intake disposition

Existing related Foundry cases and candidates on preview identity, asynchronous save ownership and evidence levels already describe generic aspects of the problem. This is an **additional concrete Case** on derived-output time ownership, not a new Canonical principle or an automatic policy promotion. It does not claim that full video editing, source-audio retiming, event splitting/merging or timeline waveform dragging is implemented.

Reference: `11576865/HSR-Voice-Archive-Builder` PR #132; `app/subtitle_timing.py`, `app/subtitles.py` and `docs/subtitle-style-workbench-v15.md`.
