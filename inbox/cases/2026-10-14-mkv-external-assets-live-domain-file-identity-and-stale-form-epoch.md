# Case: External media asset editor authority needs exact File identity and DOM selection generation

Date: 2026-10-14  
Status: **Case / implementation PR submitted, exact-head CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#133 — bounded external resource live domain](https://github.com/11576865/MKV-Fast-Muxer/pull/133), head `ab11a3488421c14cc1dff1de2a305a8e31afb051`  
Base: merged main `bf75e797700a2f0e14a90a63898e096a94c2ffe8`.

## Gap / specific correctness risk

Earlier P1 source-bound domain Cases moved **existing MKV scanned streams and attachments** into one editable immutable `ContainerProject` with independent SHA rebind and writer safety. External audio and new subtitles, however, were still edited through direct writes to `externalAudioState` / `newSubtitleState`, and a UI refresh copied current DOM form values back to those mutable arrays without an immutable transaction.

The source-neutral `File` selection was reconciled by display metadata `name|size|lastModified`. A different browser File object can have exactly the same display metadata. A replacement File could incorrectly inherit old title/flags from the prior selection, and async probe/UI refresh could copy old mounted control values onto a newly selected task.

## Scoped implementation

PR #133 establishes a distinct **source-neutral immutable ContainerProject v1 domain session** for external audio `title,language,default,original,commentary,hearingImpaired` and new subtitle same fields plus `forced`. Source file and subtitle sidecar object **references** remain exact in-memory bindings; they are not stored in serializable JSON. Edit commands validate every field and all currently bound File/sidecar/format/identity and editable values against the domain, compile immutable project changes first, and only then synchronously project into the already-tested FFmpeg execution arrays.

Selected font File objects appear as source-bound, immutable *inventory* `attachment` objects with names; `preserve|force` font handling is an explicit domain `metadata` policy. This is **not** a new font byte/MIME editor or AttachmentUID writer. All existing external metadata controls, background DOM reconciliation, bulk clear defaults, and font mode toggle route through the domain.

Each form list exposes a local **selection-authority epoch** set at the time it was rendered. Source re-selection and successful subtitle/font resource binding increment the epoch; stale DOM cannot replay form values against the new resource generation. The rebind logic reuses legacy metadata only when the actual File object reference (and subtitle sidecar reference) is unchanged, not when its metadata key happens to match.

Before beginning a normal single-file mux, the current external domain object graph, legacy executor projection, font inventory and mode are checked together. The existing P0 mux writer, independent subtitle witness and frozen batch JobPlan execution remain unchanged.

## Evidence and limitations

- Direct isolated execution of real immutable `ContainerProject` and new module passed combined audio/subtitle edits, rejected invalid mixed actions atomically, updated preserve→force policy, completed 125 title keystrokes with bounded history and refused replaced same-display File reference.
- Node regressions cover field typing, mixed transaction, no-op, long typing, File/sidecar/format drift, font inventory/mode policy, direct legacy bypass and empty source-neutral candidate without false writer authorization.
- Real Chromium scenario submitted: MP4 + external FLAC/ASS/TTF; re-select an external FLAC via a distinct browser File containing identical bytes/name/mtime, assert prior title is not inherited; then author audio/subtitle fields, set font force, actually mux a video-rooted MKV, and independently `ffprobe` delivered track metadata/disposition/font attachment.
- Four modified JS source/test files passed static parser checks. **PR #133 exact-head Node/build/Chromium E2E is Pending**; do not call it integrated green or confirmed all-browser/device behavior before CI.
- This is bounded ownership by disjoint source/external sessions, **not** yet one global atomic project spanning both surfaces. External File grants, subtitle sidecar permissions and persistent source rebind are not portable; resource-only Matroska writing remains unavailable in the present video-rooted browser writer. Complex Chapter/targeted Tag/AttachmentUID #77 guards are not relaxed.

## Deduplication and reusable hypothesis

The previous Case `inbox/cases/2026-10-14-mkv-live-domain-track-authority-with-legacy-mux-projection.md` concerns scanned source streams. This Case covers **external** asset binding and a separate class of async DOM generation leakage, so it is related but not a duplicate.

Transferable hypothesis: use exact input-object identity plus a form-render generation token when an asynchronous resource inspector may rerender or reuse mutable legacy editors. A visual equality key is insufficient to authorize metadata propagation across inputs. A source-neutral semantic domain should remain separate from actual media delivery and File permissions until independent audit proves execution.

Record only as a **Case**, without Canonical promotion from one implementation or unconfirmed CI run.

## Follow-up evidence: stale UI versus actual output plan (2026-10-14)

The first integrated PR #133 run at head `35411ad3`, [Browser E2E 38514430477](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38514430477), had **Node/build pass but Chromium fail** in `scenarioSequentialTasks`: actual second MKV subtitle title was `English · ASS` instead of `Second Task`; cancellation/restart Scenario 10 passed. This is a concrete regression, **not** a passing implementation of the earlier Case.

The unified P1/P3-B PR [#134](https://github.com/11576865/MKV-Fast-Muxer/pull/134) now targets `main` directly. Its branch received one bounded integration patch [3a92e52](https://github.com/11576865/MKV-Fast-Muxer/commit/3a92e52acb439b093d0319b61bd951d68da51249): invalidate prior subtitle form immediately during a newly selected FileList's pending content scan, and preserve authored metadata under inventory-only rebind after validating the exact current File and sidecar references. [7e008c7](https://github.com/11576865/MKV-Fast-Muxer/commit/7e008c7f9030c73fc9f1ce5cff05be4b2d9fa066) adds a browser *pre-execution* assertion: the edited form and actual output plan (`#muxPlan`) must both say `Second Task` **before** invoking the writer; the original independent final `ffprobe` assertion remains mandatory.

**Evidence status:** new integrated PR #134 workflow [38518974530](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38518974530) was queued at checkpoint; no success is asserted. The hypothesis is that separating the form value, actual plan projection, and finished-output observation localizes whether a lost edit originates at the async DOM/domain boundary or later in the media execution. This is a scoped Case update and not Canonical policy.

## Further browser evidence: remount during an otherwise current field edit (2026-10-14)

The integrated [#134](https://github.com/11576865/MKV-Fast-Muxer/pull/134) exact-head [run 38519457650](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38519457650) passed **534/534 Node tests and Vite build**, but real Chromium `scenarioSequentialTasks` still failed **before mux**: after entering `Second Task`, the editable input again read `English · ASS`. The earlier test only detected the incorrect finished MKV; the pre-execution form assertion now establishes that the drop can happen at the UI/editor boundary. Scenario 10 cancellation and restart passed.

A bounded production follow-up in [commit 0772c75](https://github.com/11576865/MKV-Fast-Muxer/commit/0772c75796ad3b498ac598ca23ee1c22e134b39f) changes `renderNewTrackLists()`: asynchronous readiness refresh does not replace existing editor nodes when the **current selection's exact File/sidecar references**, domain selection epoch, total rendered field inventory and canonical input values agree. An actual identity/epoch change, invalid field, or mismatch still forces remount, retaining fail-closed constraints. The aim is to prevent an unrelated async probe from unmounting an input between keystroke/input dispatch and committing an inferred default. The hypothesis is plausible but **not yet validated by Chromium**.

At checkpoint, [run 38520281105](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38520281105) is in progress, and this fix is **Pending External Validation**; no user-facing delivery or Canonical promotion is claimed. Reusable distinction: form **render identity** must be tracked separately from source **authority identity**; harmless readiness updates should not reconstruct a coherent actively edited form, but source-identity changes must invalidate it. This is a refinement of the existing Case rather than an additional duplicate entry.
