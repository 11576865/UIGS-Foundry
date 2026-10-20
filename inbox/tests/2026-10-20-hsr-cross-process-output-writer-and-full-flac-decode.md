# Test / observation — HSR cross-process output writer gate and full FLAC decode preflight

Date: 2026-10-20
Project: `11576865/HSR-Voice-Archive-Builder`
PR: [#196](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/196)
Status: **Candidate/Test — code submitted; exact-head CI in progress; real Android pending**

## Existing defect boundary
Before PR #196, `app/jobs.py` used only process-local `threading.Lock` and in-memory `_JOBS` / `_RESERVED_PROJECT_WRITERS` for same-project async and synchronous writers. A separate HSR Python process did not consult those locks. In parallel, `verify_internal_ass_audio_source` checked FFprobe `codec_name=flac` but not late-frame decoder integrity before the ASS rewrite.

## Proposed repair at tested scope
- Shared `app/project_writer_lock.py` uses persistent lock files keyed by a SHA-256 of the canonical project path, under the same OS user's HSR state directory. POSIX obtains non-blocking `flock`; Windows uses non-blocking `msvcrt.locking`. Lock files stay in place to avoid inode replacement races.
- `jobs.py` holds the OS lock through synchronous writer reservations and asynchronous output callbacks, and cross-process busy checks now query the same lock.
- `app/delivery_artifacts.py` runs FFmpeg with `-xerror` and `-map 0:a:0 -f null -` before rewriting ASS/SRT in the explicit ASS-internal flow, rejecting decode errors, missing FFmpeg, a 1800-second timeout, and stat identity changes.
- Tests: subprocess lock contention and release, background output callback never runs under another process's lock, real FLAC synthesized by FFmpeg with corrupt later bytes that retain an FFprobe FLAC codec but fail full FFmpeg decode, asserting the prior subtitles/receipts are byte-identical.

## Independent local examination
A separate FFmpeg shell experiment on a 2-second synthesized FLAC showed overwriting 200 bytes around 40% of a ~32 KiB file led FFmpeg `-xerror` to exit nonzero with invalid frame sync, while overwriting earlier padding did not necessarily fail. Therefore the committed regression corrupts bytes at 45%, not at an arbitrary offset.

## Evidence scope
- Thread/process output ownership is limited to cooperating HSR processes sharing the user-state directory; not a distributed or cross-user lock. The shared global jobs journal is not yet itself protected against simultaneous writers. External filesystem edits are outside this fence.
- Full decode applies to explicit ASS-internal preflight; a provider authenticity proof, exact PCM-to-manifest identity proof, or proactive scan of every chapter track is not implied.
- Physical Termux, genuine multi-hour media, deliberate power removal, and Windows execution on actual Windows are still Pending.
- No Canonical mutation from one source observation.

Dedup rationale: the existing 2026-10-16 HSR FFprobe Bug captures early invalid stream rejection; this record adds process-to-process writer containment and **late-frame decode evidence**, which differ from codec-only checks.
## Code integration / exact-head CI (2026-10-20)

PR [#196](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/196) merged by squash into `main@78618a84800dda96b553448f92455d714c593ced`, from tested PR head `444dbbc36043b4d8bb741097ebc302a93acedb57`.

The exact PR head passed:
- [Python 3.11/3.12/3.13 + Termux Lite + real libass tests, run 39401140509](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39401140509)
- [Seven ASS requirements, run 39401140422](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39401140422)
- [Chromium/browser subtitle evidence, run 39401140452](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39401140452)

The merged-main workflows are distinct and in progress at writing. `Pending`: real Android/Termux deployment, Windows physical process-lock behavior, multi-hour decode overhead, abrupt power loss, global jobs journal concurrent writes. None are implied by Linux CI. No Canonical modification.
