# Candidate: Preserve-all semantics must cover the full source domain

Status: candidate
Date: 2026-10-03
Domains: media-processing, data-preservation, reliability

## Summary

A "preserve all", "append only", or "keep source structure" contract should be defined over the complete source domain, not over a whitelist of source categories the current implementation happens to understand.

A category whitelist can appear non-destructive while silently dropping a valid future, uncommon or currently unmodeled object class.

## Observed case

In `11576865/MKV-Fast-Muxer`, the source container model primarily exposed video, audio, subtitle and attachment streams. Extending it to data streams with a separate `-map 0:d?` reduced one loss boundary but still encoded preservation as a growing category whitelist.

PR #61 strengthens append-only Matroska handling to map the complete source stream set with FFmpeg `-map 0`, preserve source stream order, then append new external streams and attachments. The post-mux audit separately verifies known stream groups and also tracks otherwise unclassified source stream types.

Selective editing remains a different policy: it can map explicit editable groups while preserving verified data streams according to its own contract.

## Candidate rule

When a product promises full preservation or append-only transformation:

1. Define preservation over the complete source object domain.
2. Prefer a full-source pass-through primitive when the execution substrate provides one.
3. Add new objects after the preserved source set instead of reconstructing the source from a known-type whitelist.
4. Audit the output against the complete source structure, including currently unclassified object classes when they are representable.
5. Treat selective editing as a separate contract; do not call it "preserve all".
6. A newly discovered source category should not require a product update merely to prevent accidental deletion under the preserve-all path.

## Scope

The rule generalizes beyond Matroska streams to archive entries, package manifests, document extension records, project resources and other formats where unknown-but-valid content may coexist with modeled fields.

It complements existing unknown-content preservation principles by specifying the implementation boundary for an explicit "preserve all" product promise.

## Provenance

- source repository: `11576865/MKV-Fast-Muxer`
- pull request: `#61`
- implementation branch: `feat/compact-container-inventory`
- execution mechanism: full source stream mapping via FFmpeg `-map 0` before appended resources
- verification: mux-command and mux-audit regression coverage added; browser E2E under validation at intake time

This is a Candidate only. It is not Canonical.