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


## Continued Case: direct manipulation of derived subtitle events in a bounded timeline (2026-10-10)

### Observation / implementation

After persistent ASS/SRT-only time overrides were added, numeric start/end controls were functionally correct but did not provide spatial context for neighboring events. A new HSR subtitle event timeline puts the same **derived display data** on a common time scale and delegates pointer and keyboard edits to the existing timing-draft state rather than adding an independent persistence mechanism.

- The editor can pan and zoom through event boundaries (12–300-second windows); cue selection and viewport position are independent states.
- Start/end drag handles change only the selected cue's unsaved draft. An explicit Save still owns the server transaction, project identity and optimistic concurrency. Adjacent cues are never changed implicitly, even when snapping to their edges.
- Snapping is optional and limited to nearby pixel proximity; it is not an assertion of error-free subtitle spacing. Overlap is represented in limited visual lanes and noted as density, rather than silently suppressed.
- A project with many events cannot render an unbounded DOM on each interaction; only items in the current time viewport are considered, with at most 140 displayed. The timeline reports truncated density instead of claiming full visibility.
- The preview playhead is derived from the current ASS trial-time percentage. It is **not** synchronized video-frame playback or a program-wide audio waveform.
- Selected items, source-clock conflicts, unsaved time drafts and source identity constraints remain authoritative in both the numeric editor and the event timeline.

### Evidence / disposition

Implementation: HSR-Voice-Archive-Builder PR #132, integrated HTML/CSS/JS time event timeline beneath the real preview stage; tests/test_subtitle_continuous_timeline.py exercises the production interaction logic with a deterministic project corpus and deferred persistence. Source and functional tests exist; exact-head CI, production-browser visual and device evidence remain independently scoped.

**UIGS Intake:** Deduplicated against the existing preview-identity, async ownership and derived-time Case and the interactive-preview backpressure Candidate. Append to the existing Case; do not automatically promote to Canonical.


## Continued Case: cross-tab text optimistic concurrency and deliberate draft reconciliation (2026-10-10)

Originally cue timing was protected by expected start/end, while the cue
text editor lacked an equivalent expected-current-value check. Two browser
tabs could submit different `final_chs` for the same ID and let the later
request silently overwrite earlier human work. Comparing only the ID
is insufficient when rebuilding archives migrates cue indices.

HSR PR #132 now sends optional `expected_final_chs` and
`expected_source_member_id` from the first-class cue editor. The service
resolves the effective saved subtitle text via the same source-member-aware
override rules as ASS/SRT generation; it compares preconditions and rejects
stale or ambiguous cues before modifying any override/review/export file.
Legacy bulk clients not sending the preconditions remain supported.

The *post-refresh* interaction is equally important. When a server update
arrives and the local cue has an unsaved draft, the editor preserves the
draft, updates its server baseline, blocks Save and offers two explicit
choices: **adopt server text** or **confirm keeping the local draft**.
Only the latter permits an intentional subsequent save based on the newly
loaded text. Without this rebase UI, a warning that says "refresh" can
leave an old cached baseline unchanged and trap the user in repeated
optimistic concurrency failures.

Evidence includes real ASS/SRT writer and overlay tests
(`tests/test_subtitle_integrated_export.py`) plus production-JS
`tests/test_subtitle_cue_editor.py` coverage. This is an instance-level
Case update linked to existing async-save ownership knowledge; Canonical
guidance is not automatically changed.


## Case continuation: explicit source/translation Karaoke boundary (2026-10-11)

The HSR writer could previously apply source-language timing to the CHS target when source_language began with zh. Users clarified the product contract: official source text (English/Japanese/Korean) is read-only; the editorial Chinese translation is the editable field; Karaoke effects attach only to source-language Primary text, not to translated Chinese. Even a Chinese-only archive should not produce CHS Karaoke through the translation layer. The revision removes all CHS Karaoke/clip paths and preserves existing Primary behavior for non-Chinese source languages. It also labels editable Inspector original-language *trial sample* as preview-only, and differentiates immutable archived source from remote third-party index text comparison (while keeping CURRENT/REMOTE tokens).

The validation matrix contains EN/JA/KO × discrete/smooth/clip and Chinese-only fallback, plus event-relative timing compensation. This updates the existing HSR Case about source ownership and preview evidence rather than creating a duplicate user-interface rule. No Canonical promotion or claim of actual speech forced-alignment quality.



## CI evidence for original-language Karaoke role/pre-roll correction (2026-10-11)

HSR PR #133 exact HEAD `83248e831b2440f1b8581d1f82f5dcebfc4a6547` passed [tests run 38119628856](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38119628856): Python 3.11/3.12/3.13 and Termux Lite dependency-surface; and [subtitle evidence run 38119628853](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38119628853): Chromium UI and FFmpeg/libass fixture tests. CI does not establish real official Japanese/Korean forced-alignment accuracy or physical-device acceptance. This PR remains unmerged and dependent on #132. No Canonical promotion.


## Case continuation: source-revision-gated human translation retention (2026-10-11)

HSR PR #133 continues the existing source/translation ownership contract
under a more demanding archive-update scenario: the same original source
WAV member is still present after a rebuild, but the archived official
EN/JA/KO transcript has changed. An existing human `final_chs` correction
must remain recoverable without silently being certified as translating
the new source text. The original transcript is still strictly read-only.

The implementation persists a normalized SHA-256 of the official source
transcript **only in newly saved human Chinese override sidecars**. If
the official source changes, the prior Chinese override is retained but
excluded from new derived ASS/SRT, the previous review-confirmed state is
not displayed as confirmed, and the proofreader displays old Chinese text
as read-only comparison evidence with a revision warning. A human can save
a newly reviewed Chinese translation, binding it to the new source text.
Legacy human corrections without old fingerprints remain supported because
prior releases never recorded that evidence.

`translation_override_stale` and previous old human text are computed only
for the API/proofreading view and **never** introduced as Manifest fields.
Tests cover source-change detection, old sidecar byte retention, no
canonical-source modification, stale final-CHS exclusion from SRT, re-review,
whitespace-only normalization, legacy migration and UI warning visibility.

Code+test checkpoint
`f78f27ee79ad4c666af4e0ecf7b4da01e1f7a346` passed
[Python/Termux CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38132938938)
and [Chromium/libass CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38132938954).
Subsequent documentation-only changes must be verified at their exact head.

This case extends previous human-cue optimistic concurrency and data ownership
work; it does **not** define new Karaoke on translated Chinese, editable
official source text, universal multilingual forced-alignment accuracy, or
canonical release acceptance. No UIGS Canonical promotion.


## Audit correction: read-only source is not automatically an officially sourced transcript (2026-10-11)

A review of `app/builder.py` (primary text can originate in the normalized bilingual index, or the package's same-member .lab for non-English languages) and `app/quick.py::_remote_rows` (provider label can be `AI-Hobbyist EN.xlsx`) shows the UI/source layer's "read-only" contract and its *documented provenance* must be separated. Immutable-within-editor source data can still come from a third-party index, not an independently authenticated official HSR transcript. The assistant's repeated use of “official EN/JA/KO source text” was overbroad. Reusable distinction: authority/provenance flags are independent of mutability; UI should display the real source type and any verification state without granting editing privileges. This is a review observation, not a demonstrated malicious or corrupted source. No Canonical change.


## Case extension: opt-in identity-verified Chinese subtitle backup recovery (2026-10-11)

Further HSR PR #133 work closes a real recovery gap: previous versions could verify and preserve a text-only backup containing `subtitles_overrides.json` and `subtitles_override_history.jsonl`, but could not restore specific proven-current Chinese human edits into a rebuilt project. The added `app/subtitle_recovery.py` defines **separate read-only preview and explicitly selected Apply**. The existing Recovery panel exposes this without creating a second subtitle workbench.

A backed-up current human `final_chs` correction is restorable only when the complete `source_member_id` uniquely identifies a current Manifest entry; the current subtitle item ID is unambiguous; a declared v2 whitespace-preserving source-text fingerprint matches; available backed-up/current WAV hashes agree; and the destination has no existing human override. Missing or legacy v1 fingerprints, duplicated IDs, mismatched audio/source text, previous local corrections, and history-only superseded revisions are **review-only**, not auto-applied. Apply rechecks the backup SHA, Manifest SHA and project root under the subtitle edit lock, archives the original recovery package, writes *only* selected Chinese edits, and forces `confirmed=False` so a previous review receipt cannot be inherited. The immutable original-language transcript, source WAV, Karaoke and unrelated sidecars are not altered.

Synthetic tests in `tests/test_human_subtitle_recovery.py` cover same-basename members in different chapters, reindexing, stale/ambiguous/missing fingerprints, changed Manifest after preview, existing correction rejection, exact backup retention and FastAPI/Termux surface contracts. This **does not** reconstruct all superseded human correction history automatically, guarantee archive provenance beyond recorded fields, or prove cross-process crash atomicity or real HSR archive acceptance. Keep as Case evidence; no promotion to Canonical.


## Opt-in CHS recovery exact-head CI evidence (2026-10-11)

HSR PR #133 exact HEAD `1b57ac02fd4da3422d27124eaef72c809d2f541b` passed [Python 3.11/3.12/3.13 plus Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38138862938) (four successful jobs) and [Chromium/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38138862948) (two successful jobs). Added regression also checks restoration explicitly clears a previously valid review confirmation and refuses recovery when the current Manifest has a duplicated entry ID or incomplete audio fingerprint. These are synthetic fixture and UI-contract tests, not physical-device, crash-injection, real game voice corpus or all-history-replay acceptance. Keep as Case; Canonical remains unchanged.


## Case extension: export-bound rendered evidence, cancellable jobs (2026-10-12)

HSR [Draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact head `14d7293e724aba3724c1efb063e90124de8f1944`, extends existing (not parallel) subtitle style UI and persistent `app.jobs` infrastructure. User-triggered `验证已导出 ASS（抽样）` snapshots the **actual current exported ASS** only when the preexisting `subtitle_export_receipt.json` is hash-current; parses Dialogue time ranges, chooses at most eight distinct distributed subtitle windows (server max twelve), and renders midpoint frames on black/white neutral FFmpeg/libass backgrounds. The result is an atomic `ass_render_evidence.json` sidecar bound to SHA-256 of the exported ASS bytes, export receipt and saved style policy. Reopening the app rechecks all three identities and marks the proof stale after any change. There is no new independent editor, source mutation, or automatic claim of saved style/export equivalence.

The existing persistent jobs API gained an allowlisted cancellable job kind, cooperative cancellation, project-scoped ownership, duplicate-job guard, and progress; the FFmpeg frame reader drains stdout/stderr while enforcing a 12-second per-frame timeout and killing the subprocess on cancellation, with a ~120-second total inspection budget. FastAPI and Termux Lite expose matching start/cancel/status/proof retrieval paths. Any errors/cancellation fail the proof operation; a valid sampled output may still reveal a violation or be inconclusive. `full_interval_verified=false` remains unconditional; `unexamined_unique_windows` is explicit.

New regression and actual FFmpeg smoke tests were added to the Chromium/libass workflow. Exact-head CI was queued/running at submission (tests run `38172664646`, browser/libass run `38172664663`); do **not** inherit green CI from the prior SHA. Also pending: real large-corpus latency, restart interruption under crash injection, physical Android, font parity, and entire exported timeline/frame coverage. Candidate/Case evidence only, no Canonical promotion.


### Save-transaction UI isolation regression caught in CI (2026-10-12)

Initial export-evidence infrastructure head `14d7293e724aba3724c1efb063e90124de8f1944` passed Chromium/libass workflow [38172664663](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172664663), but Python matrix run [38172664646](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172664646) failed one Node VM isolation regression: the pre-existing `saveSubtitleLayoutSettings()` harness intentionally executed a standalone extracted function and lacked the new evidence refresh callback. The optional post-save refresh threw a ReferenceError, making a successful settings commit return false. Follow-up HSR commit `0d35898ca946dda3830cf57af28789874883f5a9` guards this nontransactional presentation refresh behind a runtime feature check. The underlying save's success must never depend on unrelated evidence UI attachment. Exact-head CI [tests 38172787176](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172787176) and [browser/libass 38172787236](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172787236) were in progress at intake; do not claim green until they finish. Case observation only; no Canonical promotion.


### Exact-head infrastructure CI validation (2026-10-12)

The corrected HSR PR #134 head `0d35898ca946dda3830cf57af28789874883f5a9` has both completed GitHub Actions workflows **success**: [tests run 38172787176](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172787176) (Python 3.11 / 3.12 / 3.13, Termux Lite) and [browser / real FFmpeg-libass run 38172787236](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38172787236) (Chromium UI, libass artifact). This supersedes previous Pending CI and initial red test notes for this exact HEAD only. Coverage remains synthetic and sampled, and PR remains Draft. No device or all-timeline safety assertion. Canonical unchanged.


### 2026-10-12: render-policy-at-production provenance gap and fail-closed correction

**Observed from source:** HSR draft PR #134 had a durable `subtitle_export_receipt.json` with input (manifest/text/time) and output (ASS/SRT) SHA-256 checksums. However the receipt did not capture the *effective ASS render configuration when the writer ran*. Its downstream `ass_render_evidence.json` bound an *inspection-time project style* SHA to an existing ASS SHA. A user could therefore save new style settings, skip regeneration, then request pixel verification of **old ASS bytes using the new SafeArea**. Hashes would be internally consistent yet misattribute the style that produced the artifact.

**Implementation submitted:** HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), commit `ffa2739ed307880fbd6443354d3a759e23d48330` adds `render_policy_sha256` to the actual ASS export receipt, computed during successful ASS generation from the effective `SubtitleRenderConfig` and source/target language. Exported raster evidence now rejects a missing (legacy) or mismatching writer-time policy fingerprint and asks for a fresh ASS export. Regular legacy SRT/ASS export-health readability is retained; the strict check applies to *new raster evidence certification*. Tests cover legacy receipts, unsaved-to-export style drift, exact configuration matching, and real-writer receipt integration.

**Transferable Observation:** An inspection-time fingerprint of current settings is not provenance for the *configuration that produced a persistent artifact*. Persist the effective writer inputs at production, then compare with subsequent inspection policy before making artifact-specific claims. This addresses the instance of preview/export policy misattribution; it does not prove the rendering is correct at every time point or on every device. Earlier HSR Case already covered identity and async save; this observation is recorded here after deduplication, without elevating it to Canonical. Exact-head CI [tests](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38194557255) and [Chromium/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38194557267) were running at intake; outcome pending.


### Writer-time render policy provenance: exact-head CI evidence (2026-10-12)

HSR PR #134 head `ffa2739ed307880fbd6443354d3a759e23d48330` completed both workflows successfully: [Python 3.11, 3.12, 3.13 + Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38194557255) and [Chromium + real FFmpeg/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38194557267). The added writer-time render-policy fingerprint regression and actual writer receipt integration were part of this exact HEAD. Supersedes the provisional "CI pending" statement for this SHA; project remains Draft, field/long-corpus acceptance pending. Case level retained; no Canonical promotion.

 
## 2026-10-12: exported ASS dynamic-event sampling and evidence schema break

HSR [Draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), most recent fix HEAD `e1eacbf1d69863ee3a4958e14a08422803d99e99`, replaces **midpoint-only** sampling of actual exported ASS with a risk-aware bounded planner. It parses declared `[Events]` fields and the exported Dialogue text, recognizes animation-event candidates from `\\move`, `\\fad`, `\\fade`, `\\t`, and centisecond Karaoke tags, and allocates a shared maximum of 8 default / 12 server frames across archive-wide windows and selected high-risk event positions. The pixel measurement still comes from one complete composite frame rendered on two backgrounds at each time (not an isolated per-Dialogue mask).

**Claim discipline:** `dynamic_window_count` and `unexamined_dynamic_windows` quantify how many dynamic windows remain without targeted samples. `effect_candidates_truncated_windows` explicitly names cap-induced loss of event candidates. `candidate_count_scope=window_midpoints_plus_targeted_effect_candidates` prevents the restricted candidate tally from falsely standing in for every effect in the full archive. Each frame includes `active_dialogue_count` and `compositing_scope=all_active_ass_dialogues`; overflow may involve overlapping voices and cannot be attributed exclusively to the selected event. `full_interval_verified=false` remains unconditional. Due to materially changed sampling semantics, `ass_render_evidence.json` advances from schema v1 to v2 / `sampling_algorithm=exported-ass-events-v2`; old midpoint-only evidence must be re-run rather than silently accepted as dynamic evidence.

**Regression evidence:** synthetic cases for motion events, multiple Karaoke tags, overlapping dialogue, reordered Events Format, bounded >96-tag candidate handling, and genuine FFmpeg/libass proof that a `\\move` cue beginning beyond SafeArea is detected. Initial head `26139a10...` had a red CI for a truthful budget-exhaustion disclosure bug: scanning 96 tags ended the outer loop before setting the truncation indicator. Follow-up `e1eacbf...` explicitly records that limit before breaking. Exact-head GitHub Actions results pending at intake; no field acceptance yet. This Case is linked to the existing SafeArea rendered-ink Bug, **not promoted to Canonical**.


### Exported ASS risk-aware sampler: exact-head CI outcome (2026-10-12)

Corrected HSR PR #134 HEAD `da02c18ae4461494d54d2e8382a628dc1a0882c1` passed [Python 3.11/3.12/3.13 and Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38195897014) **success** and [Chromium + actual FFmpeg/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38195897012) **success**. All new dynamic events, effect-budget cutoff, composited-overlap, evidence-schema-v2, and real-moving-ASS-outside-SafeArea regression tests were part of the exact checked tree. The intermediate head `e1eacbf...` failed due to an accidental `@patch` decorator placement when adding the evidence-v1 migration test; HEAD `da02c18...` restores proper test ownership. Supersedes prior pending-status claims only for this HEAD; case evidence remains synthetic/controlled, not real large-corpus or Android acceptance. Do not promote Canonical.

 
## 2026-10-12: long ASS synthetic stress, selected-only text ownership, cancellation

HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134) exact HEAD `79e073707b6197f1462526e712be6f48245fd272` introduces a bounded archive planner improvement without changing its sampled-only evidence claim. Previously, every parsed Dialogue was stored with its complete text in a per-window list even though the final budget renders only 8 by default / 12 maximum frames, and every sampled timestamp rescanned all raw intervals to count overlaps. The new two-pass parser preserves only compact time-window facts and recognized effect families in the first pass, then extracts exact override text only for selected dynamic windows in the second pass; sorted start/end arrays with half-open `bisect_right` produce the composite active-dialogue count. The parser checks cancellation/deadline every 256 input lines in both passes. New evidence metrics separate a window that happened to be sampled from a window where an **actual dynamic candidate timepoint** was sampled (`effect_sample_count`, `dynamic_effect_sampled_window_count`, `unexamined_dynamic_effect_windows`).

**Executable test evidence:** added `tests/test_ass_export_sampling_scale.py`, synthesizing 12,000 unique windows / 24,000 simultaneous-layer Dialogue events with repeated motion, fade and Karaoke. [Python 3.11/3.12/3.13 and Termux CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38212020915) and [Chromium / FFmpeg-libass CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38212020900) both completed **success** for this exact SHA. The latter measured plan-only **1.8753 s**, `tracemalloc` peak **18.592 MiB**; Python 3.11 suite measured **2.6287 s** and **18.864 MiB**. The synthetic report is uploaded with CI artifacts. These metrics exclude source fixture construction and native/process memory, with **zero FFmpeg-rendered frames for this stress fixture**; the separate real FFmpeg moving cue regression remains green. Results are environment-specific, not a device/real game corpus guarantee.

**Critical coverage limit:** despite acceptable synthetic planning time, 11,997 of 12,000 *dynamic* windows were not specifically sampled, and only eight frames were scheduled. Resource boundedness is **not** representative subtitle-safety coverage. This is a reusable Case about honest budget-vs-coverage accounting, not a confirmed cross-project Canonical rule; no promotion.

 
## 2026-10-12: resumable ASS rendered window-pass as incremental evidence, not proof

**Case-level observation** from [HSR draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact SHA `98d09d52fd17441686e8d405fbbaf09fbdcc292d`: an 8-frame risk smoke test offered no way to progressively inspect a large 12,000-window archive. The continuation adds an explicitly user-initiated sequential unique-Dialogue-window batch (8 FFmpeg/libass frames default, 12 maximum), saving the cursor and cumulative counters **only after the whole batch renders and the ASS/output receipt/style identity is rechecked**. A per-run unique ID prevents explicit restart from overwriting older committed receipts; an interrupted operation can leave an orphan batch file, but the checkpoint retains the previous cursor. UI adds `继续覆盖检查（下一批）` and `重新开始覆盖（清除旧进度）`. FastAPI and Termux Lite use the same project-scoped cancellable `ass-artifact-evidence` job type and coverage endpoints. Last batch checksum is checked on read; a full historical chain audit is not yet implemented.

**Evidence:** [Python 3.11/3.12/3.13 + Termux Lite run 38241530911](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38241530911) and [Chromium + actual FFmpeg/libass run 38241531262](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38241531262) both completed **success** at the exact SHA. The real libass runner executed `test_actual_ffmpeg_export_batch_produces_a_durable_checkpoint ... ok`, plus tests for two committed batches, canceled/restarted batches not overwriting old receipts, stale ASS/style identity, corrupted latest receipt and expected-cursor conflict. A 24,000-Dialogue synthetic cursor plan also passed; no real 24,000-Dialogue renderer loop was undertaken.

**Reusable engineering distinction:** workflow coverage (`next_cursor == unique_window_count`) is *not* time-continuous visual coverage. Even a completed pass checks one midpoint (and typically one animation candidate) per window, not the full temporal interior or actual final video/font environment. `full_interval_verified=false` remains mandatory. This is a de-duplicated extension of existing HSR Case and open rendered-ink Bug, not a one-off Canonical change.

 
### 2026-10-12: verification-claims bugs in exported ASS batch evidence

[HSR PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134) at exact HEAD `8b08477525ccff0436e7636a52141e65069035be` corrects three practical defects identified in source review. (1) Earlier checkpoint reader checked only the **latest** saved batch SHA, enabling an older batch receipt to disappear or mutate while `verified=true` / `window_pass_complete` remained displayed. The reader now audits every committed receipt in a backward SHA-256 chain, verifies continuous cursor range from genesis, recomputes sample and finding totals, matches derived coverage counts, and fails closed on changed or absent earlier evidence. New regression tests mutate the first receipt, remove an intermediate file, alter the previous-link SHA while rehashing the latest receipt, and forge counters. This explicit O(batch count) read-time audit may cost latency on huge archives; long-corpus response time is not yet measured. No claim of adversary-resistant authentication against full rewrite.

(2) Unsupported Karaoke absolute-offset `\\kt` was recognized as dynamic, but generic entry/exit probes could be counted as *actual effect-event* coverage. The candidate selector now excludes generic fallback probe reasons when attributing `dynamic_event_examined_window_count`; unsupported `\\kt` still triggers candidate truncation/incompleteness disclosure. (3) Global smoke and sequential batch starts could race between button activation and server response; a synchronous shared UI start guard and disabled peer buttons now prevent duplicate POSTs before a job ID arrives, while the backend project-scoped exclusion remains authoritative. No implementation of independent per-cue effect overrides is asserted.

Exact-head CI: [Python/Termux run 38243027912](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38243027912) and [Chromium/libass run 38243027896](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38243027896), both in progress at initial evidence intake. Deduplicated into the existing HSR Case; no Canonical promotion.


### Bug-fix HEAD exact CI verification (2026-10-12)

HSR PR #134 SHA `8b08477525ccff0436e7636a52141e65069035be` completed both workflows **success**: [Python 3.11/3.12/3.13 and Termux Lite 38243027912](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38243027912) and [Chromium plus actual FFmpeg/libass 38243027896](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38243027896). Historical chain/counter integrity, unsupported Karaoke effect accounting and shared UI start guard are included in this exact checked tree. Evidence limited to automation and controlled fixtures; O(batch count) read-time archive history audit latency, whole-timeline safety and physical device parity remain unverified. Case level unchanged and Canonical not modified.

 
## 2026-10-12: late-cancel-vs-committed ASS proof boundary

**Source-observed race:** HSR `app.jobs` previously set `state=canceled` whenever the cancel event was set **after a cancellable job function returned normally**. The exported-ASS verifier and window-pass commit their durable proof/checkpoint *before* returning their success result. Thus a cancellation request arriving after commit but just before the runner's final state update could report "canceled" even though the persisted cursor/proof had visibly advanced. A misleading canceled state could cause an unnecessary re-run and obscure which evidence was current.

**Fix:** HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), first commit `66ee248e0fdc51eb2c57e7a5bb8c5e08751e821d`, combined head `017b7f640f489e7ec041603e23dd0ebab8f6d593`. The successful return of an ASS evidence writer is now the durable completion boundary. If the cancel flag was set before runner finalization but a committed result was returned, the result stays `succeeded`, `cancel_requested=true` is retained, and the user sees an explicit "cancel arrived after commit" status. Cooperative cancellation before the writer commits still raises and journals `canceled` without new evidence.

**Deterministic test:** `tests/test_jobs_cancel_commit_boundary.py` pauses a worker immediately after a durable checkpoint write but before returning; cancels during that pause; verifies success status and checkpoint identity. A complementary test cancels before write and verifies no receipt appears. A separate new Foundry Bug records the related long-archive in-memory Job journal leak, deduplicated from this Case.

**Evidence / limits:** exact-head [Python/Termux CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245248441) and [Chromium/libass CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245248555) were in progress at initial intake. The narrower ordering assertion is a controlled thread interleaving, not physical-device crash injection. It does not claim unconditional cancellation atomicity across filesystem writes or whole-timeline pixel safety. Case level only; Canonical unchanged.


### Final CI: late cancellation after durable ASS proof return (2026-10-12)

Latest HSR PR #134 exact head `7e3577d5f4ef170ff01b6f1b680e6f324383a1be`: [Python 3.11/3.12/3.13 + Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245706504) **success**, [Chromium / actual FFmpeg-libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245706585) **success**. Actual libass job executed both `test_late_cancel_cannot_disguise_committed_evidence_as_canceled ... ok` and `test_cancel_before_persistence_is_canceled_and_does_not_write ... ok`. The prior workflow file update accidentally omitted the dedicated late-cancel test invocation; final head restored both dedicated tests and reran CI successfully. These are controlled thread-barrier cases, not OS crash injection; existing whole-timeline rendered-ink Bug remains open. Case remains Case, Canonical unchanged.

 
## 2026-10-12: single-byte-snapshot audit and post-scan identity revalidation

**Observed source-level defect** in HSR [Draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134): the existing historical ASS-coverage receipt auditor opened each batch receipt to hash its bytes, then opened the same file again to parse JSON. This doubled I/O across a potentially long history and allowed a time-of-check/time-of-use gap in which hashed bytes and interpreted contents could differ. Furthermore, the coverage status API only verified exported ASS/receipt/style identity **before** iterating the historical chain. A replacement of ASS or advancement of the checkpoint during this potentially long audit could cause the status response to display a stale snapshot as `verified=true`.

**Mitigation:** HSR HEAD `6b9511b0d43c96b85d757c1c1848ca30ed7f8f22` hashes and JSON-decodes the **same bounded byte snapshot** (max 256 KiB per batch receipt), instead of reopening each file for two independent reads. It bounds checkpoint parsing (1 MiB), rehashes the checkpoint and revalidates current exported ASS/export receipt/saved style **after** historical audit, returning `state=stale`/ `verified=false` if either changed. An initial CI failure on `b3d79752388ffae866abab772a0782bf1272b83e` was an error-classification regression: an ASS replacement during scan correctly failed closed but returned the generic invalid-record reason instead of the specific in-audit identity-change reason. HEAD `6b9511b...` classifies it specifically, without broadening acceptance.

**Regression tests:** `test_ass_change_during_full_history_audit_fails_closed`, `test_concurrent_checkpoint_advance_during_audit_is_not_reported_verified`, `test_receipt_audit_reads_each_hashed_json_blob_once`, `test_oversized_historical_receipt_is_rejected_before_json_decode`. Exact-head [Python/Termux run 38248075070](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38248075070) and [Chromium/real libass run 38248075086](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38248075086) were in progress at intake. Earlier CI is NOT evidence of this exact SHA.

**Limits:** The two snapshot checks do not provide an OS-level transaction across multiple files, nor authenticate against adversarial full-chain rewrite. Historical chain audits remain O(committed batches) per verification and repeated appends still have cumulative O(n²) cost. This is a de-duplicated extension of existing HSR provenance/async-save Case, not a new Canonical standard.

 
### Single-byte receipt snapshot and post-scan identity: exact-head green CI (2026-10-12)

HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact head `6b9511b0d43c96b85d757c1c1848ca30ed7f8f22`, passed [Python 3.11/3.12/3.13 and Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38248075070) **success** and [Chromium plus actual FFmpeg/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38248075086) **success**. The real libass runner confirms all four new tests (`test_ass_change_during_full_history_audit_fails_closed`, `test_concurrent_checkpoint_advance_during_audit_is_not_reported_verified`, `test_receipt_audit_reads_each_hashed_json_blob_once`, `test_oversized_historical_receipt_is_rejected_before_json_decode`) as **ok**. The intermediate red head only misclassified a correctly stale outcome; fixed before final green CI. This supplants initial Pending CI for this SHA; no user-visible Foundry Pending write remains. Scope remains project-level Case, not Canonical, with unresolved large historical-chain scan cost and field/device proofs.

 
## 2026-10-12: output-scoped cross-process ASS coverage writer transaction boundary

**Defect observed in HSR source:** the existing `app.jobs` per-project concurrency guard applies only to one Python process. Independent standard/FastAPI or Termux Lite service processes can both read a matching `ass_render_coverage_checkpoint.json` cursor, render a batch, pass their own optimistic read checks, then race to replace the same persistent checkpoint. Re-reading an old cursor just before write is *not* a compare-and-swap transaction. This can silently overwrite the other's progress or leave mismatched batch receipt provenance.

**Mitigation:** [HSR Draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact code SHA `f03c0369ed7cb825e46a1b9723aa9a8a74cd331a`. New `app/ass_coverage_lock.py` acquires a **stable, output-directory-scoped OS file lock** across the *entire* next-batch operation (read old checkpoint → render FFmpeg/libass frames → revalidate exports/history → commit receipt and checkpoint). Nonblocking `fcntl.flock` on POSIX/Termux and `msvcrt.locking` on Windows fail with a clear busy condition rather than waiting and overwriting. The lock file is never unlinked; symlinks/nonregular files fail closed; canceled requests do not acquire the lock. OS lifetime releases locks on process death without PID guessing. Lock key is the resolved output directory, not the caller's project-root string.

**Regression evidence:** `tests/test_ass_coverage_writer_lock.py` starts an **independent Python subprocess** while the parent holds the lock, asserts busy, then asserts that a subsequent process acquires after the parent releases. Also tests same-process exclusion, cancellation and symlink refusal, and an application-level test ensures lock contention does not advance the coverage cursor. [Python/Termux run 38249293484](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38249293484) passed at initial intake; [Chromium/real libass run 38249293524](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38249293524) was in progress. No Windows-native runner was used.

**Boundaries:** only **cooperating sequential ASS window-pass writers** acquire this lock. It does not serialize independent ASS exporters, arbitrary external writes, the global non-window evidence proof sidecar, or full project asset mutations. Reliable OS locking on unusual network filesystems is unverified. Full historical receipt-chain auditing remains necessary and still has O(committed batch count) per read and O(n²) cumulative progression. This is a de-duplicated extension of the existing HSR evidence transaction Case, not a one-off Canonical rule.

 
### Cross-process ASS output writer lock: exact-head CI (2026-10-12)

HSR PR #134 exact head `f03c0369ed7cb825e46a1b9723aa9a8a74cd331a` completed [Python 3.11/3.12/3.13 + Termux Lite 38249293484](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38249293484) **success** and [Chromium + actual FFmpeg/libass 38249293524](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38249293524) **success**. The real-libass job ran independent subprocess OS-lock contention (`test_two_independent_processes_cannot_own_one_coverage_output ... ok`) and no-checkpoint-advance while output lock is owned (`test_another_process_output_lock_rejects_batch_without_changing_cursor ... ok`). New cross-process lock mechanism is code/test verified for that CI POSIX environment only. Windows native and unusual network FS are unverified; exporter/coverage shared lock and full batch history performance remain pending. No Canonical promotion.

 
## 2026-10-12: defer **writer-only** early chain audit, strictly revalidate before new ASS evidence commit

**Source-observed performance issue:** HSR's resumable exported-ASS window-pass writer performed a strict O(committed historical batch count) validation twice on each requested new batch: first at cursor preflight, then again immediately before publishing a receipt/checkpoint. The public status endpoint also performs a strict audit. The full-chain requirement matters because old mutable JSON receipt bytes can change without changing the newest checkpoint's digest. A shortcut cannot honestly claim `verified=true` when it has not actually read all historical records.

**Mitigation:** [HSR draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact head `88bb91ec38559d672ffa4b0c2111cdc5b81f4550`, introduces a writer-internal `_defer_history_audit=True` mode only for the *initial* cursor candidate while the writer holds the output directory OS lock. It checks checkpoint structure, exported ASS/receipt/style identity and the latest receipt SHA-256, but marks `verified=false` and `history_audit=deferred`. After rendering, and **before** a new record is written, the normal strict full history audit is mandatory. Public reads never request deferred history. A historical corruption caught after rendering fails closed, even if it means some FFmpeg work was wasted.

**Controlled regressions:** one strict chain scan per resumed-batch commit; a candidate is never verified; a nonlatest historical receipt corrupted **before** render is caught at final commit; a receipt corrupted **during** rendering likewise blocks the checkpoint; a damaged latest receipt fails at fast preflight. The intermediate CI head `8b3df328...` failed because the initial regression fixture corrupted the *only/latest* batch yet expected post-render failure; expected production behavior was a correct **early** rejection. The final test uses three batches to distinguish historic/nonlatest corruption from latest-receipt preflight.

**Synthetic performance evidence:** 256 linked batch receipts (no video rendering) yielded provisional candidate read `0.0021 s`, strict all-receipt audit `0.0349 s`, traced Python peak `1.033 MiB` on one GitHub Actions runner. These times validate **different strengths** and are not a direct same-workload speedup comparison. [Python 3.11/3.12/3.13 and Termux Lite run 38251403315](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38251403315) and [Chromium plus real FFmpeg/libass run 38251403216](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38251403216) both completed **success** at the exact head. The real libass runner executed the scale audit test and both before-/during-render old-receipt tamper tests.

**Reusable distinction:** `progress cursor available` is not equivalent to `evidence history fully verified`. An internal provisional snapshot may accelerate planning, but cannot be represented as an externally certified status, and the authoritative integrity boundary is strictly before durable commit. This extends the existing HSR Case after de-duplication; no promotion to Canonical from this one implementation. Residual historical audit complexity remains O(n) per strict read and O(n²) over many appended batches, and real-world long-game-corpus / Android acceptance is pending.

 
### 2026-10-12: multi-batch audit count and failure-path regression reinforcement

The original writer-side deferred-history architecture and corresponding Foundry Case entry at HSR `88bb91ec...` remain authoritative: provisional cursor reads must expose `verified=false`, latest-receipt preflight is hash-checked, and the complete SHA-256 historical chain is audited immediately before publishing any new ASS window-pass checkpoint.

HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact head `f76e1d816940fdf3902e886e212707c3907ba67c`, adds **three deterministic tests** as a de-duplicated extension rather than introducing a new unreviewed optimization. (1) Sixteen successfully committed two-window batches must produce exactly **15 strict historical audits inside the writer** (one per append after the first); externally verified final status still checks the complete chain. (2) Rendering errors must not trigger a strict historical scan or advance a checkpoint. (3) A tampered newest receipt must be rejected by the bounded preflight SHA before FFmpeg work or historical traversal.

**Exact-head CI:** [Python 3.11/3.12/3.13 and Termux Lite run 38263410963](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38263410963) **success**, and [Chromium plus real FFmpeg/libass run 38263410949](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38263410949) **success**. The actual libass CI job explicitly logs all three tests `... ok`. Its separate, **synthetic non-rendering** 256-receipt audit recorded provisional pointer check **0.0030 s**, strict audit **0.0514 s**, `tracemalloc` peak **1.033 MiB** on that runner. Different read modes provide different assurance; these numbers do **not** represent a guaranteed speedup or real HSR archive render throughput.

**Remaining:** strict reads and successful pre-commit audits still cost O(committed batches), repeated end-to-end progression is O(N²), and external/uncooperative filesystem writers are not globally transacted. `full_interval_verified=false` persists. This remains existing Case-level evidence, not a Canonical promotion; no Foundry Pending entry.

 
### 2026-10-12: explicit ASS coverage restart bypasses discarded chain, preserves provenance boundary

**Identified inefficiency:** HSR sequential coverage's `restart=true` starts a brand-new independent `run_id` and does not inherit any earlier sampled evidence, but the post-render gate still invoked a full strict audit of the previous run's receipt chain, wasting O(previous batch count) time for historical data that will not be used. This inefficiency was present even after the one-strict-audit-per-normal-resume improvement at head `f76e1d8...`.

**Implementation:** [HSR Draft PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134) exact head `8d9d2e10e5cfc47d14ea83461cde44069f02f879`. Explicit restart now snapshots the old checkpoint's SHA-256 and rechecks the same bounded checkpoint bytes at the pre-commit boundary; externally replaced, appearing/disappearing, symlinked, or oversized old checkpoint files prevent an unsafe commit. **No old receipts are audited or inherited** by a new run. Previous run's receipt files are preserved and newly named receipt files start with a distinct run identity. Ordinary `restart=false` continuation STILL requires a strict audit of the complete historical chain before durable commit; public `verified=true` reads remain unchanged.

**Reproducible controlled tests:** `test_explicit_restart_skips_discarded_history_without_claiming_old_coverage` corrupts prior receipts and proves a fresh run is independent while old data remains untouched; `test_restart_aborts_when_old_checkpoint_changes_during_render` injects a checkpoint rewrite mid-render and ensures no new receipt is published; `test_restart_fails_closed_if_checkpoint_is_symlink` rejects a dangerous symlink. Exact-head [Python 3.11/3.12/3.13 and Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38266173097) **success** and [Chromium with real FFmpeg/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38266173400) **success**. The real libass runner explicitly logged all three new tests as `ok`.

**Evidence limitation:** restart-path O(N) historical audit was removed where the old run is discarded. Normal continuation and external strict status still cost O(N) per audit and remain O(N²) over many batches. No cross-process uncooperative ASS-export transaction, Android/Windows-native field acceptance, or full continuous-frame safety proven. De-duplicated into existing HSR Case, no Canonical promotion and no Pending write.
