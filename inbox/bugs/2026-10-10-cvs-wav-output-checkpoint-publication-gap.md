# Bug: CVS voicebench WAV publication could outrun its durable checkpoint

Status: **Bug / repair submitted; CI Pending**
Lifecycle: validation-pending
Date: 2026-10-10
Project: `11576865/Character-Voice-Service`
Source PR: https://github.com/11576865/Character-Voice-Service/pull/17
Parent implementation PR: https://github.com/11576865/Character-Voice-Service/pull/16

## Failure mode (source review, simulated; not a reported production incident)

The first voicebench runner wrote final `audio/<sample_id>.wav` bytes and only
**afterward** committed the `run.json` entry containing its SHA-256 and
`status=ok`. A power loss or process termination between the operations
could leave a valid final WAV and a stale `pending/failed` checkpoint.

On `--resume`, the old validator would then reject this WAV as an
untracked artifact that must not be overwritten. The runner could neither
reuse the legitimate generated result nor safely retry it. This is a
**publication/checkpoint atomicity gap**, not evidence of actual user data
loss. Protecting against overwrite alone did not provide crash recovery.

## Submitted repair

The stacked CVS PR #17 implements a two-stage per-sample protocol:

1. Exclusively write and fsync `<id>.wav.part`.
2. Durably checkpoint `status=prepared` with the output digest and metrics.
3. Publish the staged bytes as `<id>.wav`, then durably checkpoint
   `status=ok`.
4. On resume, **first** revalidate frozen original corpus, live reference
   bytes and serving model/generation identity, then validate the recorded
   prepared output's bytes and finish the interrupted publish without
   rerunning inference.
5. Reject mutated, duplicate, missing or unjournaled artifacts. Never silently
   discard an unknown file.

The generalizable failure pattern is that a side-effecting file artifact and
its persistent metadata have separate durability boundaries. A single final
file write followed by a metadata write is not an atomic logical operation.

## Tests, current confidence and limits

The source-derived local isolated pytest suite reported **21 passing tests**
for the runner, including three failure-injection regressions:

- interruption after staged WAV and prepared journal but before final publication;
- interruption after final publication but before `status=ok` journal;
- changed prepared WAV hash prevents recovery.

An additional 15 offline A/B audit cases also passed in the local harness
(36 combined). **Full repository CI and actual runtime-backed acceptance
are Pending**. No private original role-speech corpus was accessed here.

A crash **before** journaling `prepared` can still leave an untracked staged
file and must fail closed pending operator inspection. Multi-writer directory
races are not supported by this v1 protocol; tests assume exclusive run
ownership. These limitations should not be erased by a generic claim of
complete transactional durability.

## Dedup check and knowledge boundary

Foundry search on 2026-10-10 for two-phase publication, checkpoint crash,
atomic artifacts and journaled output found nearby artifact identity and
derived-evidence candidates, but no exact entry for the crash window
**between artifact publication and metadata checkpoint**. Those adjacent
records concern configuration/input identity rather than interrupted
publication. Record this as a concrete Bug, **not Canonical**, pending CI
and separate cross-project confirmation.
