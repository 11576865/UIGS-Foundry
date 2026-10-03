# Candidate: Rebuild a stale feature on current main when semantic ownership has drifted

Date: 2026-10-04
Status: Candidate
Domains: git, long-lived branches, integration, semantic conflict resolution

## Problem

A long-lived feature branch may remain syntactically mergeable or individually tested while the target branch has accumulated substantial changes in the same ownership surfaces.

At that point, a mechanical merge or broad file overwrite can reintroduce old architecture and silently erase later capabilities even when textual conflicts appear manageable.

## Candidate rule

When a feature branch is far behind current main and overlaps files whose semantics have materially evolved:

1. identify the capability that the stale branch was meant to deliver;
2. treat current main as the authoritative semantic baseline;
3. port or rewrite only the still-valid capability onto a fresh branch from current main;
4. directly reuse old files only where current main has not changed them since the stale branch's merge base;
5. integrate overlapping files by semantic intent, not by taking either side wholesale;
6. add regression coverage for the rebuilt boundary;
7. close the stale PR as superseded rather than pretending it was directly merged.

## Evidence

Character Voice Reader PR #4 had diverged by dozens of commits while current main added Reader library, generation history, paragraph generation, playback preferences, and related state.

Its useful standalone stabilization capability was rebuilt as PR #7 on current main instead of hard-merging the stale branch.

Direct file reuse was limited to files unchanged on main since the old merge base (for example the CVS client and storage modules). High-overlap files such as `reader.js`, `app.py`, `index.html`, tests, and CSS were integrated against current-main semantics.

## Provenance

- project: `11576865/Character-Voice-Reader`
- stale PR: #4
- replacement PR: #7
- replacement revision: `beabc794dcf3d197d3f94b76f48b5aa81e3ce07c`
- base main includes PR #6 at `5588c580fc6426a3da3997f15d708e6a5bcd5d08`
- evidence at intake: branch + PR + regression coverage authored; asynchronous CI pending
- deduplication: searched Foundry for stale-branch/rebuild/semantic-drift equivalents; no direct duplicate found

This is a Candidate only. It is not Canonical.
