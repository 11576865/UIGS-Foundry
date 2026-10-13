# Test: QHE heterogeneous audio plan and source-owned UI

Date: 2026-10-13
Status: Test / local compiler + actual FFmpeg acceptance; hosted runtime Pending
Source: QHE draft PR #105, code bba86515185d6d204ae653453244a27b5798b9e5

## Dedup
Existing Candidate inbox/candidates/2026-10-12-qhe-per-output-audio-track-intent-and-encoder-capability-layers.md covers the design hypothesis. This records scoped implementation and actual output evidence, not a duplicate design or Canonical promotion. The existing rational-FPS Bug inbox/bugs/2026-10-13-qhe-windows-compression-history-rational-fps-parser.md is referenced; its implementation fix remains pending Windows acceptance.

## Observed implementation / proof
One normalized audioPlan maps source ordinals to contiguous output audio indices; actions copy/AAC/Opus/FLAC/drop, explicit channel/sample-rate/range changes. A legacy global policy applies only when no per-track override exists. Task outputPlan records retained and dropped source tracks. Subtitle and attachment ordinals map separately. Restricted indexed FFmpeg arguments are bounded to 32 output tracks; no shell/path option was added.

Local suite: 196 PASS, 6 conditional skips, 0 failures. Four real FFmpeg integration tests pass: heterogeneous retained codecs are FLAC+AAC or Opus+FLAC; copied FLAC packet SHA256 sequences are unchanged. Output audio codec/channel/sample-rate assertions are independent from task compilation. Build passes. No claim of subjective quality or player support.

Independent review found global-policy leakage in Android count/duration, stale UI defaults/config rows, incorrect known-rate size refusal, false calibration audio costs and missing Android auxiliary counts. These were addressed. Browser fixture covers source reset/default/config ownership; Windows executable tests cover indexed argument rejection and output validation; Kotlin compile/runtime checks are registered but Pending external CI. They are not counted as local runtime passes.

## UI mapping and limits
Intent -> per-output audio intent -> existing authoritative form -> one hidden audioPlan JSON -> expected source-specific transforms -> compiler/actual-output checks. Manual rows use one field; source changes reset it. Guided hard-sub still uses global audio policy and hides this editor. Unknown copy/FLAC budgets remain unknown; complete-file accounting belongs to the next work unit. Old material/report repetition is not independent confirmation. Do not change Canonical.


## Round-four task review projection (Case/Observation, 2026-10-13)

QHE PR #105 adds a read-only source/checked-plan/artifact view in the shared manual editor. Checked rows derive from compiled outputPlan; artifact records retain executed source, original task and backend report. Editing or changing source invalidates current plan while keeping previous saveable output; frame-comparison source ownership clears on actual identity change. Browser download handoff and Native save completion are distinct. Missing backend verification receipts, actual bytes and external-player/device compatibility are not inferred.

A visible product defect from frontend run 38341203285: saved-state CSS hid plan inspection after switching mode/source. Visibility now depends on whether completed output belongs to the unchanged plan; the existing browser fixture asserts new-source inspection remains reachable. Source/plan/artifact and 390px layout checks added. Pure model lifecycle and unknown-evidence checks pass, local total 211 passed/7 conditional skips, actual FFmpeg 5 passed, Vite build passed. Browser execution/screenshots and physical devices Pending. This is same-project implementation evidence, not independent usability confirmation or Canonical promotion. Scope: manual workbench, guided hard-sub remains existing presentation.


## Final scoped acceptance, 2026-10-13

Exact QHE head 95fc86dee63585493818f9c452b69649dd68fc1c: all eight hosted workflows completed successfully. Frontend 38342175981; Windows smoke 38342175973; Android emulator 38342175961 with independent output report 8/8 and instrumentation OK (2 tests). Production desktop and 390px VVC phone PNGs visually inspected; no visible clipping in reviewed object-review region. The standalone task-review fixture lacks full app styling and must not be used as evidence for production colors. Vertical editor length and duplicate overview content remain refinement debt; no usability-study inference.

VVC artifact 11786973192 explicitly reports structuredTaskTests PASS but actual status UNSUPPORTED, reason libvvenc not included. Green workflow conclusion does not establish actual VVC runtime support; do not promote or collapse these states. Artifact IDs frontend 11787053015, Android 11787875629. Product-side acceptance manifest carries exact-head/run/PNG-hash provenance. Local final Node 211 pass/7 skip, real FFmpeg 5/5 and build pass. Scope remains synthetic/emulator/browser; physical/GPU/long-form/provider/player Pending. Same originating project lineage, no independent corroboration or Canonical promotion.
