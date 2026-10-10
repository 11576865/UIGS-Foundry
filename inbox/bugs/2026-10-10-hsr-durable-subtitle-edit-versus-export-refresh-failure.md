# Bug: Subtitle override committed but ASS/SRT refresh failure reported as a failed save

Date: 2026-10-10
Status: Implemented fix on unmerged HSR PR #132; real writer and browser fixtures exercised
Categories: state ownership, durability, async transaction, error recovery, output provenance

## Observation

The HSR voice archive exposes separate human subtitle text and derived ASS/SRT
display-time overrides. Previously the edit endpoint first atomically wrote its
override JSON, then regenerated SRT and optional ASS. If subtitle export failed
after that write (e.g. disk write exception or ASS layout rendering problem),
the API could return an error interpreted by the UI as **subtitle save failed**.
That was objectively false: the human edit had already persisted. Retrying
would either unexpectedly hit a newer timing state via optimistic concurrency
or encourage repeated submissions of a committed text change.

A related risk was that re-rendering would write the Manifest and CSV before
checking source-bound timing overrides for conflicts from a new archive build.
An intentional empty final Chinese subtitle could also fall through to an old
original text via truthy-or fallback, resulting in incorrect export content.

## Fix / execution boundary

- Separate `saved` (durable override commit) from `artifacts_current` and
  `artifact_error` (derived ASS/SRT refresh status), preserving success for the
  already committed edit even if export later fails.
- Expose a distinct API and UI command **重试生成 ASS/SRT**. The retry only
  rebuilds derived outputs, keeps the project-root fence, and never resends
  the text/timing edit or its old optimistic timestamp.
- Serialize cue text and display-timing mutation/refresh with a **per-output,
  in-process reentrant lock**; block editing during active project build jobs.
  This does not claim cross-process locking or multi-file atomicity.
- Fail source clock validation **before** touching Manifest/CSV derived metadata;
  avoid writing override/review files on unknown subtitle IDs.
- Preserve deliberately empty `final_chs` as an explicit user override.

## Evidence

- HSR PR #132: `app/subtitle_timing.py`, `app/subtitles.py`,
  `app/server.py`, `app/lite_server.py`, `app/static/index.html`.
- `tests/test_subtitle_integrated_export.py` uses real ASS/SRT writer output,
  validates timing/source invariance and blank text, injects an SRT export
  error **after** durable commit, and retries to rebuild exported files.
- `tests/test_subtitle_timing_editor.py` runs actual frontend JavaScript,
  confirming partial success, retry affordance, independent API call and
  no accidental resubmission.
- A dedicated FFmpeg/libass CI job rendered the produced ASS at 0.6, 2.0
  and 5.0 seconds and passed pixel-presence/pixel-absence assertions in
  GitHub Actions run 38034755036. These are real libass pixels over a
  deterministic synthetic manifest and black source video, not production
  archive footage or device screenshots.

## Intake disposition

This is a verified code-level Bug with a concrete repair and regression proof.
Generic asynchronous save ownership and UI evidence distinctions already exist
in HSR-related Foundry Cases; this adds the **durable edit vs. derived export**
failure boundary. No automatic Canonical rule change.
