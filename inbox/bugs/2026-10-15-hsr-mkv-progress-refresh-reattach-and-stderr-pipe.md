# Bug: Browser reload loses active MKV progress subscription; unread FFmpeg stderr can stall

Date: 2026-10-15
Project: `11576865/HSR-Voice-Archive-Builder`
Source: [PR #166](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/166)
State: **Proposed fix committed; CI, Android/Termux and true failure causality pending**
Classification: Bug + portable engineering observation, no Canonical promotion

## Direct user evidence

User reported that while generating a background-image MKV on Android/Termux, reloading the web UI recovered an old progress value but it never advanced, seemingly requiring a new export. The same user supplied two screen recordings of portrait and landscape Layout/Effects workbenches showing the experience: extremely long floating-point cue start/end fields, extensive vertical navigation separating the current preview from parameter changes, dense bilingual stage content and overloaded Inspector operations.

Screen recordings: `Screenrecorder-2026-10-15-03-49-46-4.mp4` (~20.5 s, 1282×1920) and `Screenrecorder-2026-10-15-03-53-57-228.mp4` (~18.4 s, 1920×1282). Review is observational only; no device process traces or live user project artefacts were available. Product workbench follow-on task is persisted in `.uigs/tasks/hsr-workbench-evidence-rework-20261015.json`.

## Confirmed software defects (do not conflate with proven runtime root)

**Frontend liveness defect:** `refresh()` fetched `/api/status`, called `renderJobs(s.jobs)` and stopped. `watchJob(id)` was only invoked after an explicit new task launch. A browser reload destroyed the previous JavaScript timer and did not attach another one for an already running backend job. Thus recovered progress appeared static even if encoding continued.

**Backend potential deadlock:** `ArchiveBundleExporter.export` created FFmpeg with `stdout=PIPE` and `stderr=PIPE`, then consumed `stdout` until EOF before draining `stderr`. If FFmpeg wrote enough diagnostics to fill its stderr pipe, FFmpeg itself could block waiting for the parent, never close stdout, and leave the job apparently frozen. Without direct FFmpeg logs, we cannot claim this second defect definitely caused the reported device freeze.

**Precision/UX defect:** cue start/end inputs used `String(rawFloat)` and exposed values such as `40.48533333333333` instead of bounded display precision.

## Proposed repair

[PR #166](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/166) adds page-load reattachment to existing job ID (without new export), guards against duplicate active pollers, warns if encoding progress does not advance for >90 s, redirects FFmpeg stderr to temporary file instead of an unread pipe, and bounds displayed cue time to milliseconds without changing authoritative raw values until the user edits them. Regression checks assert these cross-layer contracts.

## Reusable lesson (candidate only)

**Lifecycle ownership:** persistent server jobs outlive page JavaScript state. Reloading a client must re-subscribe by stable server job identity, not merely render a one-time snapshot; the UI must not automatically enqueue duplicate writes. **Subprocess liveness:** if one of two child output pipes is not drained concurrently, a full output buffer can deadlock the producer; use concurrent draining or a bounded-lifecycle non-pipe sink. **Precision:** format display values separately from internal timing state, avoiding unintended persisted edits on read.

## Evidence status / next gates

- Source-level issue: confirmed.
- PR source fix: committed.
- CI: pending.
- Android/Termux reloading mid-encode: pending.
- Full Layout/Effects workflow redesign: separate durable task, pending.
- Exact backend process freeze causality: unknown pending device logs.
- Canonical promotion: **not performed**.

Dedup: queried Foundry for `page reload job polling`, `FFmpeg stderr pipe deadlock`, `browser refresh job progress`, `HSR studio cue time precision`; only neighboring lifecycle/background design observations found, no duplicate for this failure.
