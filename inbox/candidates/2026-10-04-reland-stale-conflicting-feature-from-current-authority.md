# Candidate: Re-land stale conflicting feature branches from current authority

Date: 2026-10-04
Status: Candidate
Scope: long-lived PRs / branch conflict recovery / contract preservation

## Observation

A long-running feature PR can become structurally stale even when its feature implementation is still valid. In Quick-Automatic-Hardsub-Encoder, the Bink 2 adapter branch was based on an older Windows Bridge. Meanwhile main gained compression-history persistence, waveform/keyframe behavior, output-frame verification and authoritative hard-sub reference-frame routes.

Directly forcing or wholesale-copying the stale branch would have made the old branch authoritative over newer mainline contracts.

## Candidate method

When a stale feature branch conflicts with current main and the newer mainline behavior is authoritative:

1. Create a fresh branch from current main.
2. Treat the stale PR as a feature delta, not as a replacement tree.
3. Replay feature-specific changes onto current authority.
4. At every overlap, preserve the newer contract unless the feature explicitly requires changing it.
5. Add explicit guards for the contracts that must survive the replay.
6. Compare the resulting branch against current main and verify the resulting diff is limited to the intended feature surface.
7. Open a replacement PR and close the stale PR as superseded.

## Why this matters

A merge conflict is not only a textual problem. It can represent two different generations of system authority. Resolving it by preferring one whole side can silently regress unrelated capabilities that landed later.

The safer unit of recovery is the feature intent plus its tests, replayed against the current architecture.

## Evidence from this case

The replacement Bink 2 branch preserved current-main:
- compression evidence/history routes;
- no-audio timeline fallback behavior;
- output frame and hard-sub reference-frame verification routes;
- newer Windows Bridge diagnostics.

The final replacement PR reproduced the intended feature-sized diff instead of the stale branch's old authority surface.

Do not promote to Canonical from this single case.
