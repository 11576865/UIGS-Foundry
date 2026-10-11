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

## Cross-tab playback revocation merged evidence (2026-10-10)

CVR [PR #22](https://github.com/11576865/Character-Voice-Reader/pull/22)
passed Reader tests and real Chromium/IndexedDB multi-tab regression
at final head `111e41cbf00f17f87612028a9ab2fe639431bb8a`,
and was merged to main as `a88eb779859d380fa9b569782c7dc72960bd4f3b`.
Automated evidence includes real WAV playback interrupted after a committed
other-tab book deletion, media source release and disabled playback, matching
async pending-open invalidation, no interruption on unrelated deletion,
and fallback notification through localStorage when BroadcastChannel is
unavailable.

Evidence remains limited to tested Chromium same-origin tabs and
controlled browser scenarios, not Safari/Firefox physical device testing
or cross-device revocation. Candidate only; no Canonical promotion.

## Pending-source reads across BFCache pagehide/pageshow (2026-10-10)

CVR [PR #23](https://github.com/11576865/Character-Voice-Reader/pull/23)
found a remaining cross-tab deletion race outside PR #22's live-book
revalidation. The Reader checked the active offline book on `pageshow`,
but a `getBook()` still pending at `pagehide` had not yet set offline
mode. A frozen page missing a deletion notification could then consume
the old, already-fetched book after restoration and open deleted content.

Candidate-level implication: asynchronous **pending source reads** are
distinct from already established active session state. On suspension,
advance the request-generation fence for pending work, retain only an
identifier for a possible restart, and on restoration **re-read durable
state** before accepting the source. A later explicit user selection
must clear the restoration intent so the old source does not overwrite
the most recent one. The persisted deletion tombstone remains the
authority, not the delivery of a best-effort notification.

Validation planned in CVR PR #23: native Chromium IndexedDB with delayed
old `getBook()` results and synthetic `PageTransitionEvent` callbacks;
cases cover deleted pending book, surviving pending book, and newer
manual-text selection. A synthetic lifecycle event is *not* proof of
true back/forward-cache residency or browser freezing and scheduling
behavior. Real BFCache, Safari/Firefox and mobile remain separate checks.

Evidence at intake: PR #23 HEAD
`f48d5f37d9e02faf42c0f75ab8299a0f70d14cc3`;
Reader/Chromium CI **Pending**. De-duplicated against the existing
storage-migration and cross-tab deletion Candidate. This entry remains
Candidate, with no Canonical promotion.

## BFCache pending-open revalidation verified (2026-10-10)

CVR [PR #23](https://github.com/11576865/Character-Voice-Reader/pull/23)
was merged into `main` as `b56f41768e4457488bc8616f355b2323f8a5dda5`
after final head `f48d5f37d9e02faf42c0f75ab8299a0f70d14cc3`
passed Reader tests and the dedicated native Chromium IndexedDB suite.
The new regression tests source-generation invalidation on simulated
`pagehide`, new durable-state reads on `pageshow`, deletion during
the closed-listener interval, correct reopening of a surviving book, and
priority of a later manual-source selection.

The browser test fires *synthetic* `PageTransitionEvent` callbacks and
therefore does not establish that an actual document was resident in
BFCache or that browser/OS freeze scheduling behaved identically.
Evidence remains Candidate-level; no Canonical promotion.

## Real BFCache admission must be demonstrated separately from lifecycle events (2026-10-11)

CVR [PR #24](https://github.com/11576865/Character-Voice-Reader/pull/24)
adds an additional evidence level beyond PR #23's synthetic `pagehide` /
`pageshow` tests. Standard Playwright Chromium launches disable BFCache
with `--disable-back-forward-cache`; dispatching `PageTransitionEvent` in
a real Chromium page only tests application event handlers, **not**
browser-managed BFCache residency.

Candidate implication: a browser BFCache acceptance test must explicitly
enable the feature in its isolated browser launch, perform actual history
away/back navigation, and assert **both** that the original document
instance survived and that a native `pageshow.persisted === true` fired.
If a navigation produces a newly loaded document, reject it as evidence of
BFCache restoration even if the visible Reader state looks correct.
For failures, record browser cache-ineligibility diagnostics such as
`PerformanceNavigationTiming.notRestoredReasons` when available.

The CVR scenario holds a `getBook()` result pending, navigates away,
deletes the book from a different same-origin tab, and returns through actual
browser history; a second case checks an already-open book deleted while
the Reader is cached. Both complement, rather than replace, controlled
synthetic scheduling tests for pending request precedence.

Evidence at intake: CVR PR #24 head
`3ab0a6b3ca3d36aeb122b177ba52d6a9777f3839`,
Reader + dedicated Chromium CI **Pending**. This is an extension to the
existing IndexedDB/BFCache Candidate, not a Canonical change. Dedup search
found previous synthetic page-transition guidance but no actual BFCache
admission validation entry. Physical device and cross-engine acceptance
remain out of scope.

## Full-Chromium BFCache admission verification and merge (2026-10-11)

CVR [PR #24](https://github.com/11576865/Character-Voice-Reader/pull/24)
was merged into `main` as
`7a29ea0712e7d9cc8c6eb1bccaafd5ed692faadf`
after **Reader tests** and **real Chromium/IndexedDB regressions**
passed on final head `6dee0c021f4a7293e80ec8483a62da77edf9ec8b`.

The first strict BFCache test correctly failed in Playwright's default
Chromium headless-shell configuration: `page.go_back()` created a new
document (`token: null`, no recorded `pageshow.persisted`) and Chrome
reported `notRestoredReasons: [{reason: "masked"}]`.
Do **not** call this a product defect on that evidence. A separate full
Chromium launch with `channel="chromium"` (new headless) and
`ignore_default_args=["--disable-back-forward-cache"]` plus a plain HTML
control page made the test environment's own BFCache capability explicit.
At the final head, the control page and **both Reader** real
away/back navigation cases succeeded with the original document
instance and native `pageshow.persisted === true`: an in-flight offline
getBook rechecked a deleted book rather than accepting its old result,
and an active book removed by another tab was invalidated on restore.

Evidence level now includes actual headless Chromium BFCache admission
on CI, not solely manually dispatched lifecycle callbacks. However,
this is still one browser engine on an isolated CI environment. It does
not assert identical behavior for Safari/Firefox, real Android/iOS or
device-level memory eviction. This remains Candidate evidence, and
does not promote any Canonical rule.

## Cross-engine offline storage and real-media contract reuse (2026-10-11)

CVR [PR #25](https://github.com/11576865/Character-Voice-Reader/pull/25)
extends a previously Chromium-only offline storage/playback evidence
suite with a separate Playwright **Firefox engine** on GitHub Actions.
Rather than recoding loose Firefox smoke assertions, the Firefox runner
imports the same substantive IndexedDB, audio, cross-tab deletion,
and recovery scenarios as Chromium while keeping browser-specific BFCache
admission in its own dedicated scenario/launcher.

Candidate-level design principle: multi-engine compatibility should
reuse a **common behavioral contract** when the expected product
semantics are shared (transactional storage ownership, committed deletes,
media pause/resume and object-URL cleanup). Browser-dependent mechanisms,
such as BFCache admission, autoplay policy, or implementation-specific
headless startup flags, need clearly separated suites with distinct
acceptance boundaries. A successful browser launch is not the same as
successful feature verification.

The PR adds the Firefox workflow to validate real per-origin IndexedDB,
legacy migration and ownership, download resume/cancellation, PCM WAV
HTMLMediaElement playback, local book shelf UX and cross-tab invalidation.
At intake product head `321369d9064eaca88b8ffa3f02f1096831241c50`,
CI **Pending**. Pending Firefox failures are to be diagnosed, not
softened into synthetic success. Tests remain Ubuntu headless only;
not physical Android/iOS or Safari/WebKit acceptance.

Dedup: existing browser-storage Candidate contains only Chromium and
BFCache evidence. Appending cross-engine test-method evidence to that
Candidate, not changing Canonical on one project observation.

## Firefox audio sink versus codec decode evidence (2026-10-11)

CVR [PR #25](https://github.com/11576865/Character-Voice-Reader/pull/25)
initially failed an otherwise passing multi-engine regression on
Firefox 142.0.1 in headless Ubuntu: an offline PCM WAV Blob was valid,
and a separate `HTMLAudioElement` could decode its metadata, but
actual `play()` produced a `MediaError` with `code=3` and
`message="OnMediaSinkAudioError"`. The application's original generic
message incorrectly grouped this with unsupported codecs. The test
environment had no usable Firefox audio sink; an explicit PulseAudio
`module-null-sink` allowed the real media-playback, pause, resume,
cross-segment, and cleanup assertions to succeed while preserving
real media elements.

Candidate-level engineering inference:
- Metadata decoded successfully **does not** prove actual audio output is
  operational. A headless Firefox CI without an audio sink can report
  `MEDIA_ERR_DECODE` for an output-device fault.
- Keep a minimal independent codec/metadata control separate from the
  actual playback test; never mark the latter passing based solely on the
  former.
- If `MediaError.message` reports an audio-sink failure, present an
  output-device remediation message, not a format/corruption message.
- Media error events can be asynchronous relative to source cleanup:
  validate the current media `error` object and its `currentSrc`
  against the active Blob, and do not call `load()` gratuitously when
  no source ever existed.
- In headless browser CI, a silent virtual output sink is an
  **environment fixture**, not a mock of media decoding or playback;
  tests must still assert actual playback time, media lifecycle and
  sound-source release. It does not qualify physical speaker/earphone
  hardware or mobile browser autoplay behavior.

The Playwright Firefox dedicated job passed an intermediate head of
CVR PR #25 with PulseAudio enabled. Final latest-head Reader, Chromium
and Firefox CI pending at this intake; do not report merged or
fully accepted until the final run completes. This extends the existing
browser-storage/media Candidate without automatic Canonical changes.

## Firefox offline/media acceptance verified and merged (2026-10-11)

CVR [PR #25](https://github.com/11576865/Character-Voice-Reader/pull/25)
merged to main at `51f2b54f81259b297c25dc162757956e45c19cec`
after the **final** product head
`bc0bcbe4b26ce851f13d58d04d73a792955ebdba` passed
all three workflows: Reader tests, real Chromium/IndexedDB regressions,
and new Firefox offline regressions.

Firefox CI runs Playwright Firefox 142.0.1 with a PulseAudio
`module-null-sink` as its isolated headless audio-output fixture. The
shared scenarios still test actual PCM WAV play/pause/resume, completion
and URL release plus true IndexedDB ownership/tombstones and cross-tab
deletion. The audio output failure was captured as native
`MediaError.code=3`, `message="OnMediaSinkAudioError"`, while independent
metadata decode succeeded. The product now presents output-device
remediation for this precise sink error and ignores media errors
unrelated to its active Blob URL. The virtual sink is not a substitute
for real hardware speakers, Firefox mobile, WebKit/Safari, or
Android/iOS acceptance.

Evidence level upgraded from planned Firefox CI to **actual tested
headless Firefox and Chromium CI passing**. No Canonical rule has been
changed; the generalization remains a de-duplicated Candidate.

## WebKit cross-engine offline behavioral acceptance (2026-10-11)

CVR [PR #26](https://github.com/11576865/Character-Voice-Reader/pull/26)
extends the previous Chromium/Firefox shared offline behavioral contract
to Playwright's *Linux WebKit* engine. This engine is not the same as
verifying macOS desktop Safari or iOS Safari on a device.

Candidate-level extension: when a product depends on browser
IndexedDB ownership, tombstone deletion, WAV media playback and
cross-tab invalidation, run shared substantive assertions against
independently installed browser engines. Keep browser-specific
environment setup and separately defined BFCache admission tests
explicit. Provide an actual Linux audio output sink (e.g. PulseAudio
null sink) to avoid confusing headless audio hardware absence with
media codec or autoplay-policy incompatibility; retain genuine audio
time progression, pause/resume and media cleanup checks.

PR #26 creates `tests/test_offline_webkit.py` and a dedicated WebKit
CI workflow. At intake final merge **Pending**: do not infer WebKit
acceptance from presence of the harness or earlier Chromium/Firefox
success. Any cross-engine regression must be diagnosed before merge.
The real device background/tab freeze behavior, WebKit BFCache
admission, and macOS/iOS Safari are separate evidence scopes.

Dedup search matched this existing browser-storage Candidate's
cross-engine and virtual-sink guidance. Extended it rather than
creating an overlapping Canonical entry.

## WebKit IndexedDB Blob serialization abort and byte-container fallback (2026-10-11)

While extending CVR to Linux Playwright WebKit in
[PR #26](https://github.com/11576865/Character-Voice-Reader/pull/26),
the native IndexedDB `books+clips` write transaction aborted while
storing the first audio Blob. The browser-reported failure was
`UnknownError: Error preparing Blob/File data to be stored in object store`.
This was observed by attaching native IndexedDB transaction listeners;
without this diagnostic the download Promise appeared simply to hang.
The same WebKit build could not even insert a raw Blob fixture into a
legacy database. Do not infer a defective audio codec from this error.

Candidate remediation in PR #26:
- Serialize new audio as a structured-clone-safe record containing
  `ArrayBuffer` bytes, MIME type and a format tag; reconstitute `Blob`
  at the public read boundary. Retain raw Blob reads for old records.
- Perform asynchronous `Blob.arrayBuffer()` conversion **before**
  opening IndexedDB transactions. Retain owner/token/tombstone checks
  inside the single atomic readwrite transaction so a deletion during
  conversion cannot silently resurrect data.
- Keep raw legacy Blob migration tests on engines that can actually seed
  old Blobs (Chromium/Firefox); in this WebKit CI, use a separately
  identified byte-container fixture for ownership/tombstone invariants,
  not an unsubstantiated claim that historical raw Blob migration passed.
- Record storage representation, browser engine, observed transaction
  abort reason and test fixture deviations. Avoid turning a single
  Linux WebKit-specific error into a universal Safari compatibility claim.

Evidence status: production patch + Node tests submitted; WebKit full CI
**Pending** at this intake. This extends the existing cross-engine
browser storage Candidate after deduplication; not Canonical.

## Shared localStorage without cross-tab storage events in WebKit (2026-10-11)

CVR [PR #26](https://github.com/11576865/Character-Voice-Reader/pull/26)
exposed a second Linux WebKit compatibility gap when deliberately disabling
`BroadcastChannel`: the sender committed its IndexedDB deletion, wrote
an invalidation message to `localStorage`, and the receiving same-origin
tab could read the same value, yet that receiver observed **zero native
`storage` events**. This is a notification-delivery difference, not
evidence of failed IndexedDB or localStorage persistence.

Candidate-level recovery: keep native storage-event handling but
supplement it with low-frequency comparison of the localStorage message
value when BroadcastChannel is unavailable. Also recheck on
`focus` / `pageshow`, initialize the observer from the current value
to prevent replay of older deletions, and release polling/listeners on
unsubscribe. Background throttling means eventual reconciliation,
not real-time delivery. Persisted IDB ownership/tombstones remain the
source of truth; notification never substitutes for transactional checks.

At intake this fallback was submitted to CVR PR #26; latest WebKit
and cross-engine CI are **Pending**. One controlled Linux WebKit finding
does not justify a universal claim that Safari never delivers storage
events. Dedup: extension to the existing cross-browser storage Candidate,
no Canonical modification.

## WebKit storage/audio and cross-tab compatibility verified (2026-10-11)

CVR [PR #26](https://github.com/11576865/Character-Voice-Reader/pull/26)
merged into `main` at
`f25b14b811c78fd068e4f0223f04f3aed3bc322d`,
after **all four required workflows** passed on final product head
`9bf6d6fba9968b2942227ad9977b9e67ec0cd06b`:
Reader tests, real Chromium IndexedDB regressions, Firefox offline
regressions and the new real Linux WebKit offline regression.

Confirmed browser evidence:
- WebKit first failed on native IndexedDB `Blob` serialization abort;
  ArrayBuffer byte container + MIME restored reliable commit and the
  same public Blob contract. Existing legacy raw Blob read code retained
  and independently tested with Chromium/Firefox; WebKit's old-book
  fixture uses a distinct binary container because the CI browser
  cannot persist a raw legacy Blob at all.
- When BroadcastChannel was disabled, WebKit could read the shared
  localStorage deletion message but emitted no native storage event.
  Low-frequency message polling plus focus/pageshow catch-up preserved
  invalidation; test also verifies observer unsubscription stops
  delivery and releases the poll loop.
- Real stored audio playback, ownership/migration, deletion tombstones,
  download cancellation/recovery and shelf UI completed on the
  current Ubuntu headless WebKit regression, with virtual PulseAudio
  output for actual media progression.

Evidence scope: verified three headless browser engines plus Node,
not macOS Safari, iOS/Android browsers, physical speaker hardware,
or WebKit actual BFCache admission. Store this as Candidate evidence
only; a single product finding is not an automatic Canonical change.
