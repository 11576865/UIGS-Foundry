# Foundry Operationalization — Baseline Implementation

Date: 2026-10-02
Status: implemented baseline

## Implemented

- Five active product repositories now expose .uigs/project.json.
- Each repository has a UIGS Intake Adapter.
- Tracked CI failures automatically produce a Pending intake packet.
- Manual workflow dispatch can emit Observation, Candidate, Bug, Case, Test, or Lesson packets.
- Packets are persisted to a repository-local uigs-outbox branch using only that repository's GITHUB_TOKEN.
- UIGS-Foundry has a collector, receipt ledger, dedupe handling, Pending directory, packet schema, and collector unit tests.
- The collector runs on a six-hour schedule, manual dispatch, and collector-code/source-list changes.
- Foundry validation and report smoke tests run after collection.

## Durability boundary

This design survives a ChatGPT-GitHub connector outage for events generated inside GitHub, because source Actions and source outbox branches continue to exist independently.

It does not magically persist a fact that exists only in a chat while every external write path is unavailable. Those cases remain explicitly Pending until an external durable write succeeds.

## Current automation scope

Automatic: tracked CI failure/timed-out/startup/action-required runs.

Explicit source-side dispatch: semantic Observation/Candidate/Bug/Case/Test/Lesson.

Chat-side: UIGS Intake Check remains governed by project instructions and can write directly when the GitHub connector is available.

## Next expansion

- triage pending packets into Red Reason / Bug / Test / Case records;
- add project-side adapter schema validation;
- add selected PR/issue/release signals only where noise can be bounded;
- generate cross-project Red Reason and release-readiness reports from Pending + structured records.
