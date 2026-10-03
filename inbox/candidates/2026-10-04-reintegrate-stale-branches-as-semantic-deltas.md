# Candidate: Re-integrate stale feature branches as semantic deltas onto current authority

Date: 2026-10-04
Status: Candidate
Scope: branch integration / long-lived PRs / evolving architecture

## Observation

A long-lived feature PR can become unmergeable even when the feature itself is still valid, because current main has independently changed the same high-authority files.

In Quick-Automatic-Hardsub-Encoder, the Bink 2 adapter branch predated later Windows history, timeline, output verification, bridge endpoint, and capability-contract work. Copying the old feature files wholesale would have reintroduced obsolete versions of those systems.

## Candidate principle

When current main has evolved substantially, treat current main as the authority and replay the stale branch as a **semantic delta**, not as a file-version authority.

A safe integration sequence is:

1. create a fresh branch from current main;
2. identify the stale PR's changed files and intended behavior;
3. apply non-conflicting hunks only where their old context still matches uniquely;
4. resolve changed authority surfaces additively, preserving current-main behavior;
5. verify that both the new feature markers and the newer main markers remain present;
6. inspect the resulting diff for suspicious whole-file replacement or unexpectedly large churn;
7. open a replacement PR and supersede the stale one.

## Why this matters

Textual conflict resolution can be syntactically successful while semantically regressing newer architecture. The risk is highest in central files such as application state, API routers, bridge/server entry points, CI workflows, and shared UI shells.

Diff-size inspection is also a useful guardrail: a feature expected to add a few hundred lines but suddenly showing thousands of additions is evidence of integration corruption even before CI runs.

## Evidence boundary

This comes from one concrete stale-PR reintegration. It should remain Candidate until repeated across projects or independently validated.

Do not promote to Canonical from this single case.
