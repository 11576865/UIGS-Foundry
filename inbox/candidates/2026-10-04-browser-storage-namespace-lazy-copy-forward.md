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

## Negative-state boundary: deleted records must not be lazily restored (2026-10-10)

A lazy copy-forward migration has a second, distinct edge case: when the old
namespace is deliberately retained for rollback, deleting a migrated record
from the new namespace makes it appear *absent*, so a later fallback can
resurrect it from the old namespace. Absence cannot represent both “never
migrated” and “explicitly deleted.”

Candidate extension:

1. Persist an explicit negative state (for example, a tombstone) in the new
   namespace for a user-requested deletion while the legacy namespace remains
   readable.
2. Make legacy restoration conditional on that negative state, including a
   recheck inside the destination write transaction; merely checking before an
   asynchronous migration is susceptible to delete/import races.
3. Apply the same rule to dependent assets (e.g., clips associated with a
   deleted offline book), and exclude tombstones from normal user inventories.
4. Permit deliberate re-add through an explicit write, rather than treating
   legacy fallback as a user-authorized restore.
5. Keep rollback behavior explicit: an older application reading only the
   legacy database may still display the old record. This is different from
   guaranteeing that the *new* application respects deletion.

### Additional provenance and evidence boundary

- Project: `11576865/Character-Voice-Reader`
- Code PR: [#10](https://github.com/11576865/Character-Voice-Reader/pull/10)
- Submitted revision: `f877c115b3b1bfe7dade2b75b832cbeb06b26f9d`
- Changed code: `web/js/offline.js`; Node regression: `tests/test_offline.mjs`
- Evidence at intake: static code finding + implementation and regression submitted; asynchronous CI and user-browser acceptance **Pending**
- Deduplication: extends this existing lazy-copy-forward Candidate instead of introducing a separate generalized migration rule. The observation is not independent cross-project validation.
- Status remains **Candidate**, without Canonical promotion.

## Async commit-time ownership boundary (2026-10-10)

The same CVR migration family revealed a second failure mode beyond a legacy
read resurrecting a tombstone: a long-running offline download can acquire a
book row, await network/cryptographic operations, and subsequently write a
stale snapshot over a newer deletion or download.

Candidate extension (not yet a cross-project invariant):

- Cancellation alone is insufficient because network requests may ignore
  AbortSignal or complete after cancellation. A persisted operation token
  must be checked against the current destination record *inside the same
  transaction* that commits the produced artifact and its progress metadata.
- Deletion should fence outstanding writes and clear associated data
  atomically when the storage engine supports multi-store transactions.
- A newer operation for the same destination may supersede an older one;
  stale completions must be rejected rather than presented as success.
- A visible cancel control and source-switch cleanup improve immediate UX,
  but do not replace cross-tab durable ownership checks.
- Test delete-vs-late-result, overlapping writes, and cancellation with an
  upstream operation that ignores AbortSignal; retain partial verified work
  for explicit retry when safe.

Evidence at intake: implementation and regression tests submitted in
[CVR PR #11](https://github.com/11576865/Character-Voice-Reader/pull/11),
with test-fixture repair at `80f5823129365ade19ead6b5ca3927c3e8a45a66`.
Initial CI exposed a simulated IndexedDB aborted-upgrade rollback defect;
the repair is committed, final asynchronous CI **Pending**. This is one
project's implementation evidence, not independent confirmation or a reason
for Canonical promotion.

Scope exclusion: this record does not assert that all browser engines,
cross-tab UI updates, or every cancellation timing have been field-tested.

## Real-browser transactional evidence boundary (2026-10-10)

A simulated IndexedDB adapter is useful for controlled scheduling and
failure injection, but it does not itself validate browser-native transaction
lifetimes, versionchange rollback, or same-origin cross-tab ordering.
Treat emulator/unit tests and real browser IndexedDB tests as distinct
evidence levels.

CVR [PR #12](https://github.com/11576865/Character-Voice-Reader/pull/12)
introduces a path-filtered headless Chromium + Playwright runtime regression,
with production `web/js/offline.js` executing against actual browser storage:
cross-tab delete during an in-flight download; newer write superseding an
older one; cancellation and verified partial-download resume.

- Head SHA at intake: `59a2c9bae301f0ea7dd4e0e4fa31c175fc68fde1`
- Status: implementation submitted; external browser CI **Pending**
- Scope: this constitutes an added validation method, not yet a claim that
  the cases passed in Chromium, and not a substitute for mobile browser
  field acceptance
- Dedup: scoped extension to this existing migration candidate, rather than
  a new standalone principle; no Canonical authority change
