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
