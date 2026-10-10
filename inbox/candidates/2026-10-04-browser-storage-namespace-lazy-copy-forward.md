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

## Physical storage reclamation versus logical deletion (2026-10-10)

A deletion tombstone prevents logical reappearance of old data, but it does
**not** prove that dependent media blobs have been physically reclaimed.
In CVR, `removeBook` originally deleted only audio segments referenced by
the book's *current* manifest. After redownloading a revised manifest, audio
for old segment IDs could remain in the IndexedDB `clips` store even though
`getClip` correctly hid the deleted book.

Candidate-level implication: deletion acceptance for revisioned artifacts
needs two different assertions:
1. **Logical fence:** tombstone/ownership checks block reads and stale
   asynchronous writers.
2. **Physical reclamation:** query the actual persisted backing store and
   demonstrate that obsolete or orphaned artifact keys were purged, not just
   that the API no longer returns them. Ensure cleanup excludes neighboring
   owners and is atomic with the logical tombstone when possible.

Evidence: CVR [PR #13](https://github.com/11576865/Character-Voice-Reader/pull/13)
implements `getAllKeys` physical prefix-key reclamation and adds both
in-memory and Chromium real-IndexedDB direct backing-store assertions.
Submitted head `ee8cb6b8bfab853ca301fc440c705aa5fd4adb4e`;
CI **Pending** at intake. Key-prefix matching here relies on the verified
server-side ID contract (`b-` + 24 hex digits; no colon delimiter). This
contract should be reverified before generalizing the algorithm to arbitrary
object keys. Older rollback DB remains untouched.

Dedup: appended to the existing browser-storage migration Candidate, not
a new Canonical rule. No independent product confirmation yet.

## Advisory storage budget and resumable downloads (2026-10-10)

CVR [PR #19](https://github.com/11576865/Character-Voice-Reader/pull/19)
identified an accounting error at the boundary between browser storage
estimates and resumable media synchronization. The Reader previously compared
`navigator.storage.estimate().quota - usage` with
`offlineManifest.totalBytes` and rejected a download if estimated free bytes
were lower. However `totalBytes` includes clips that may already be stored
and SHA-256 verified. The browser estimate is origin-wide and approximate,
not the exact incremental budget for this download.

Candidate implication:
- Do not treat a total artifact manifest as the amount of **new** storage
  required on a resume path. A conservative-looking hard preflight can
  incorrectly reject a fully safe incremental transfer.
- Treat `StorageManager.estimate()` and `persist()` as advisory/best-effort
  interfaces. Unsupported APIs or denied persistence should not themselves
  prevent the actual storage write from being attempted.
- For a real `QuotaExceededError`, preserve committed, verified partial
  artifacts and show an actionable **user-controlled** cleanup/retry path.
  Never automatically delete user-selected offline media to recover space.
- Keep the evidence layers explicit: a mocked estimate with genuine
  browser IndexedDB writes verifies reuse; a deliberately thrown quota
  exception verifies recovery UI; neither creates a real disk-full browser
  nor proves all eviction and quota-pressure behavior.

CVR PR #19 adds an on-demand origin storage estimate display plus actionable
quota-recovery UI, scoped tests, and a Service Worker cache-key bump.
Evidence at intake: head
`deffa31b3002c5d160b7bc503ac30bfa0ef349b9`;
normal Reader and Chromium CI **Pending**. Product behavior and validation
should be updated after completed latest-head CI.

Dedup: this is an extension to the existing browser persistence/ownership
Candidate rather than a new Canonical standard. No automatic promotion.

## Quota recovery verification status (2026-10-10)

CVR [PR #19](https://github.com/11576865/Character-Voice-Reader/pull/19)
was merged to main at
`f5660cc9a1e66a303ac1823e0e7c6b2001c62c10`, after the final head
`deffa31b3002c5d160b7bc503ac30bfa0ef349b9` passed
**Reader tests** and the separate **real Chromium/IndexedDB regression**.
Browser validation confirmed that a low synthetic quota estimate did not
block an incremental download using a valid pre-existing clip, that
StorageManager.persist denial did not abort a download, and that a controlled
QuotaExceededError surfaced manual recovery/retry without erasing the book.

Keep evidence boundaries: the test injected the quota exception rather
than filling actual physical storage. It does not validate all browser
eviction policies, quota exhaustion in other engines or device behavior.
Single-product Candidate remains Candidate; do not promote to Canonical.

## Dependent-record first access during lazy migration (2026-10-10)

CVR [PR #20](https://github.com/11576865/Character-Voice-Reader/pull/20)
uncovered a gap in multi-store lazy migration: its migration strategy
correctly restored an old book on `getBook()` / `listBooks()`, and its
audio migration correctly refused to write clips without a live owning
modern book. But a caller that invoked `getClip()` **before the book
was ever listed or read** could retrieve a valid old audio blob and still
get `undefined` because the required owning book row had never migrated.

Candidate implication: test **every externally available first-access
path** through dependent storage, not just the most common parent-first
user flow. Where migration of a child record requires an owner record,
restore the owner first, with an atomic current-state/tombstone check,
then use a transactional live-owner guard when writing the child.
A deleted legacy owner must not be revived through a child read; orphan
children must not be copied into the new namespace. Keep the old
namespace intact if rollback compatibility requires it.

Product PR #20 adds Node tests and real Chromium two-tab IndexedDB
regressions checking child-first owner restoration, physical clip copy,
cross-tab tombstone rejection, orphan audio exclusion, and untouched
rollback data. Evidence at intake: product head
`0018b86c49ce50752eb2c2d13ad2658d074d5188`;
latest Reader and Chromium CI **Pending** at intake.
No claim of physical mobile-browser acceptance or Canonical change.

Dedup: extended the existing browser-storage namespace lazy-copy-forward
Candidate rather than creating a new overlapping storage rule.

## Clip-first migration verified merge evidence (2026-10-10)

CVR [PR #20](https://github.com/11576865/Character-Voice-Reader/pull/20)
passed its latest-head `0018b86c49ce50752eb2c2d13ad2658d074d5188`
Reader tests and real Chromium IndexedDB regressions, and was merged into
`main` at `ca3582070e4a6df8a15319931ea41558e200ce98`.
This upgrades the prior *Pending CI* evidence for this single-product
migration case to *automated Node and Chromium tests passed*. Real browser
coverage included clip-first migration from the legacy DB and cross-tab
delete-first tombstone safety; it does not establish Safari/Firefox or
physical Android/iOS field acceptance. The Candidate remains non-Canonical.

## Atomic owner-and-media read snapshot across browser tabs (2026-10-10)

CVR [PR #21](https://github.com/11576865/Character-Voice-Reader/pull/21)
found a read-side check/use timing gap: `getClip()` checked a book's live
status in a `books` transaction, then read the related blob in a separate
`clips` transaction. Another browser tab could delete or replace the
book between those operations. Therefore each operation could be correct
individually while the combined authorization/media observation was not
from one coherent IndexedDB state.

Candidate implication: when a dependent media record is readable only
while its owner is live, validate the owner and read the dependent record
in **one multi-object-store readonly transaction**. After a legacy-owner
migration, repeat that atomic current-store read; do not rely on a
stale check made before an awaited migration. Keep a distinct transactional
live-owner fence for legacy media import writes.

Evidence boundary: one readonly transaction gives a linearizable read
snapshot relative to conflicting readwrite transactions; it does not
revoke an audio Blob already returned by a prior legal read or interrupt
an ongoing media element in a different tab. Live revocation/notification
requires an independent cross-tab protocol. Product PR #21 tests native
transaction scope, post-delete read rejection, physical clip absence,
and explicit re-add in Chromium, supplemented by Node scope assertions.

At intake: CVR head `e51d2a7672578093df8fe561728b991944935ab8`,
Reader and Chromium CI **Pending**. This is a related extension to this
existing namespace/migration Candidate, not an automatic Canonical
promotion. Search for multi-store read snapshot and cached-media TOCTOU
found no separate direct duplicate.

## Atomic media read verification and merge (2026-10-10)

CVR [PR #21](https://github.com/11576865/Character-Voice-Reader/pull/21)
passed latest-head Reader tests and the real Chromium/IndexedDB regressions
on `e51d2a7672578093df8fe561728b991944935ab8`. The resulting
main merge commit is `e245d19a44544c077e4eff34bb7dd338433bbffa`.

Evidence: production multi-store readonly transaction plus direct native
Chromium transaction-scope test, cross-tab committed deletion, physically
absent deleted clip, and clean explicit re-add; existing offline migrations,
audio and UI tests remained green. This confirms the tested same-snapshot
ownership guarantee, not invalidation of already returned Blobs or
immediate remote-tab media stopping. No other browser engines or physical
mobile devices were accepted by this regression.

The evidence is recorded at Candidate level without Canonical promotion.

## Committed deletion versus already-acquired media in other tabs (2026-10-10)

CVR [PR #22](https://github.com/11576865/Character-Voice-Reader/pull/22)
extends the atomic owner-and-audio read snapshot in PR #21 to a distinct
life-cycle boundary: one Reader tab may already hold a valid `Blob` and
be playing it when another tab deletes the IndexedDB-backed book.
No database read fence can retroactively pause that pre-existing media
element. Persisted deletion and session/playback invalidation must be
treated as separate concerns.

Candidate-level implementation:
- Publish a same-origin `book-deleted` invalidation event only **after**
  the tombstone and audio purge transaction commits. BroadcastChannel is
  preferred; cross-tab localStorage `storage` events are a fallback.
- On another tab, match the book ID against both the current offline
  document and any **pending async open**. Stop queue playback, release the
  already-created media URL, fence earlier async reads, clear the invalid
  document, disable Start, and refresh the local shelf. An unrelated
  deletion must not interrupt current playback.
- BFCache/pagehide may suspend listeners: reinstall them on pageshow and
  check that an active cached book still exists, so missed messages can
  be reconciled against persistent state.
- Notifications are best-effort for same-origin live contexts and do not
  replace authoritative IndexedDB checks, cross-device synchronization,
  or guarantee revocation of a Blob already returned by a completed read.

Evidence at intake: CVR PR #22, head
`111e41cbf00f17f87612028a9ab2fe639431bb8a`, Reader tests and
real Chromium suite **Pending**; new Chromium cases exercise actual WAV
playback on two Reader tabs, non-matching deletion, delayed stale open,
and localStorage-event fallback.

Dedup: searched Foundry for BroadcastChannel, deletion notifications,
storage-event media revocation, and stale pending offline opening; no
direct entry. Appended to existing browser-storage Candidate rather than
automatically altering Canonical rules.
