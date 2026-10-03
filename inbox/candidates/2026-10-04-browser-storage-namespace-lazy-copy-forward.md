# Candidate: Split-project browser storage should migrate by lazy copy-forward without deleting the legacy namespace

Date: 2026-10-04
Status: Candidate
Domains: browser storage, localStorage, IndexedDB, project split, backward compatibility

## Problem

When a browser application is split from a parent project, continuing to write parent-prefixed local state preserves hidden coupling. Renaming keys or databases outright, however, can make existing progress, bookmarks, preferences, cached catalogs, or offline assets appear lost.

## Candidate rule

For a project-namespace migration:

1. all new writes use the new project's namespace;
2. reads check the new namespace first;
3. if absent, read the legacy namespace and copy the value forward when it is actually used;
4. keep the legacy record during a defined migration window rather than deleting it immediately;
5. apply the same policy across both localStorage and IndexedDB;
6. cover every currently persisted preference/state key, not only the most visible one;
7. test at least one real legacy-to-current migration path plus a static namespace contract.

Lazy copy-forward limits migration work to data the user actually accesses and preserves rollback compatibility.

## Evidence

Character Voice Reader PR #7 migrates:

- reading progress;
- bookmarks;
- cached voice catalog;
- font size, line height, reading width, paragraph gap, theme, and prefetch depth;
- paragraph audio variants;
- offline library books and clips.

New writes use `cvr.*` / `character-voice-reader-*`; legacy `cvs.*` / `cvs-*` records remain readable and are not deleted during the migration window.

## Provenance

- project: `11576865/Character-Voice-Reader`
- replacement PR: #7
- revision: `beabc794dcf3d197d3f94b76f48b5aa81e3ce07c`
- evidence at intake: implementation + migration tests authored; asynchronous CI pending
- deduplication: searched Foundry for localStorage/IndexedDB namespace migration and lazy copy-forward equivalents; no direct duplicate found

This is a Candidate only. It is not Canonical.
