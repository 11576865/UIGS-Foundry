# Candidate: Re-read the authoritative branch head before destructive ref updates

Status: candidate
Date: 2026-10-02
Domains: operations, reliability

## Summary

In multi-agent repository work, a branch/PR ownership check performed at the start of a task is not sufficient before a destructive ref update. The authoritative branch head must be re-read immediately before force-moving or replacing that ref.

Use an optimistic-concurrency pattern:

1. read the authoritative PR/branch head and record the expected SHA;
2. prepare the replacement/rebuild on a separate temporary branch;
3. immediately before updating the public authoritative ref, fetch the PR/branch head again;
4. if the SHA changed, abort the ref update and inspect the new work instead of overwriting it;
5. only move the authoritative ref when the expected head still matches.

## Evidence

While rebuilding ASS-Workbench-Android PR #62 onto a newer main, the UI Contract branch initially had head `fb8898af952655ecb18da9349c0202712206e220`.

A replacement was prepared on temporary branch `rebuild/ui-contract-slice-a-main`. Before updating the authoritative `refactor/ui-contract-boundary` ref, the PR was fetched again and its head had changed to `f67065b6489f153e1a065962d5675d8637cd9fa2`.

That new head already contained the same intended four-file UI Contract rebuild on current main. Because the head was re-read before the destructive update, the replacement was not pushed and another agent's active work was not overwritten.

## Candidate rule

For shared branches controlled by multiple agents:
- treat force-update as a compare-and-swap operation;
- re-fetch the remote head immediately before the write;
- abort on unexpected head movement;
- prefer a temporary rebuild branch so preparation does not mutate the public PR;
- mark abandoned temporary branches as non-authoritative in the coordination record.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#62`
- observed old head: `fb8898af952655ecb18da9349c0202712206e220`
- observed new head: `f67065b6489f153e1a065962d5675d8637cd9fa2`
- temporary rebuild head: `b993762ce4d02f22c433d82669b9df84d4a2eac3`
- evidence level: directly observed concurrent repository state transition

This is a Candidate only. It is not Canonical.
