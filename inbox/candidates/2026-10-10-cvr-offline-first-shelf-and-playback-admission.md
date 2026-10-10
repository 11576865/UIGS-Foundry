# Candidate: Offline-first entry points must not inherit online configuration gates

Date: 2026-10-10
Source: Character Voice Reader (CVR)
Status: Candidate / product PR pending CI and live-device acceptance
Evidence: https://github.com/11576865/Character-Voice-Reader/pull/14
Product branch: `fix/reader-offline-shelf-ui`
Head at intake: `0afb1a656656c50c60375941f32f76121710bba3`

## Problem / observed implementation

The standalone Reader exposed its offline-books list only inside a collapsed
server-oriented library and generation panel. Its `render()` function gated
Start on a selected voice, and `playbackOptions()` rejected any session
without an online voice selection (or with an unavailable engine), even when
`requestAudio()` could retrieve an already-verified clip from local IndexedDB.

Also, opening a local book set `offlineMode = true` only after the document's
initial render, without recomputing the Start-button state. The existing list
deleted a book on one click and used a single paragraph string for all books.

## Proposed solution / current product work

- Separate **local content discovery** from authenticated remote-library
  operations: a directly reachable offline shelf, book-level readiness,
  partial progress, empty/error states and an explicit refresh.
- Decouple playback admission for **cached media** from the online model/voice
  configuration prerequisites needed for **fresh generation**. Missing offline
  audio must still produce a real failure; do not silently regenerate via
  unavailable services or pretend a missing clip exists.
- Re-render controls after completing an asynchronous source/mode transition.
- Use explicit confirmation for destructive removal of local user data, with
  a cancel route that does not delete anything.
- Provide a compact primary action hierarchy on narrow screens, defer
  secondary controls in an accessible disclosure, and respect reduced motion.
- When browser UI tests click an action that awaits IndexedDB, wait for a
  settled UI transition before asserting DOM control state. A synchronous
  assertion immediately after click races against the handler's awaited
  storage reads.

## Evidence and validation boundary

CVR PR #14 includes code plus real headless Chromium UI regression covering
offline shelf access without a CVS backend, no-voice playback admission,
delete/cancel, and closing a deleted in-use offline document. Initial
browser workflow found an immediate Start-disabled assertion; test was
reworked to await the asynchronous UI outcome at product commit above.
Final branch CI **Pending** at intake; no claim of fully resolved browser
acceptance until the latest run passes.

This is a single-product Candidate. Do not promote to Canonical solely from
this evidence. Prior Foundry search for offline-first UI, voice admission,
destructive shelf confirmation and IndexedDB async UI assertions found no
matching reusable entry; storage namespace/physical-blob guidance in
`inbox/candidates/2026-10-04-browser-storage-namespace-lazy-copy-forward.md`
is related but covers persistence, not playback UI admission.

## Cross-source late-completion ownership boundary (2026-10-10)

Continuing CVR UI integration identified a related, separable transition hazard:
the Reader had `importSerial` fencing for file imports but not for remote
book opens or IndexedDB offline book opens. A stale earlier request could
replace a more recent user-selected source, and `loading` could remain true
after a manual override because only the old operation owned its `finally`.
Disabling the manual switch while a file loaded also blocked the escape hatch.

Product [PR #15](https://github.com/11576865/Character-Voice-Reader/pull/15)
uses one source-change generation counter across all entry paths, checks
ownership at each async result-to-state boundary, and resets old loading and
poll timer state when a new source is chosen. Tests inject explicitly delayed
remote response, IndexedDB lookup, and File.arrayBuffer, with a newer user
choice in between.

Candidate extension, not Canonical:
- Treat all UI entry points that select the same logical resource as one
  cancellation/ownership family. Separate per-entry counters leave holes.
- Enforce *latest user intent wins* on each awaited result before state/DOM
  mutation; cleanup/finally paths must also be ownership-checked.
- Do not disable the user's alternative source actions solely because a
  prior source import is pending, unless cancellation/switching is otherwise
  clearly provided.
- Async background job/history results need the same identity fence.

Evidence: branch commit `a015f0099a0fff3d28e2c4bf01e1f0c8d43094a9`,
PR #15 submitted, Reader and Chromium CI **Pending** at intake.
Do not claim verified live-device acceptance.
Dedup: appended to existing CVR offline-first UI Candidate rather than
creating a competing UI Canonical or redundant Candidate.

## Browser media acceptance beyond button admission (2026-10-10)

The earlier PR #14 Chromium UI check proved that opening an offline cached
book could enable the Start button without an online voice catalog, but that
assertion by itself was not evidence of actual audio decoding, time
advancement or lifecycle completion.

CVR [PR #16](https://github.com/11576865/Character-Voice-Reader/pull/16)
adds a distinct real-media acceptance tier: generate valid 16 kHz mono
16-bit PCM WAV blobs, persist them through the production IndexedDB adapter,
and initiate playback via the real Reader UI. Assertions cover duration,
increasing HTMLAudioElement.currentTime, pause-hold/resume, two-segment
auto-advance, completion/progress, and media source release on Stop.
A separate Chromium simulated 360px touch viewport checks horizontal
overflow, manual-source selection and auxiliary playback disclosure.

Observations/Candidate distinctions:
- A button becoming enabled is **input admission**, not playback acceptance.
  Real media should be tested with a playable file and the browser's actual
  decoder/HTMLAudioElement, not only fake player APIs and dummy media blobs.
- Error copy should not silently identify a single codec when the service
  supplies multiple formats: the prior AudioPlayer error incorrectly claimed
  every decoding failure was a WAV problem despite CVR downloading MP3.
- Headless Chromium playback and touch emulation add runtime evidence, but
  are not a physical Android/iOS device test or a guarantee against mobile
  autoplay policies; retain that boundary explicitly.

Evidence at intake: CVR PR #16, latest head
`92a6cb2abc9fff42212b5510546a31727929257e`,
both dedicated Chromium and Reader CI **Pending**. No Canonical promotion.
Dedup: extended existing CVR offline-first UI Candidate after searching for
real audio decoding, HTMLAudioElement testing and codec-neutral diagnostics;
no directly matching prior Foundry entry was found.

## Recoverable media resume rejection must be visible (2026-10-10)

CVR [PR #17](https://github.com/11576865/Character-Voice-Reader/pull/17)
identified a user-observable gap after real media tests were added: the queue
already retained `paused` and `snapshot.error` when a browser rejected an
explicit `HTMLMediaElement.play()` resume (for example `NotAllowedError`),
but the Reader's paused state copy always said only “已暂停”. An actionable
retry existed but the user could not tell why Continue had failed.

Candidate-level implication: UI rendering must distinguish **intentional
pause** from **paused after failed resume**, even if both share a recoverable
state in the playback machine. Preserve media position, display the actual
error with a retry path, and clear the transient error only after a successful
resume. Verify this using both fake-player state tests and browser
HTMLAudioElement-backed tests where the next `play()` is rejected once.
An injected browser error proves the UI state handling, not any particular
real-device autoplay policy.

Related rollout issue: changing cached reader script behavior requires
updating the HTML asset revision *and* Service Worker cache key together.
Product PR #17 advances both to v8 and retains Reader namespace version
contract tests.

Evidence at intake: PR #17 head
`fcab6dc03ea00087d6a53f2e6f78d9c46bd3df1d`,
normal Reader CI and real Chromium CI **Pending**. This extends existing CVR
UI Candidate rather than changing Canonical. Dedup searched Foundry for
media resume, autoplay NotAllowedError, playback retry and Service Worker
revision; the earlier async playback abort/revision Candidate covers stale
writes, not this paused-error UX.

## Shelf discovery versus asynchronous persistence (2026-10-10)

CVR [PR #18](https://github.com/11576865/Character-Voice-Reader/pull/18)
adds title/author search, downloaded/partial filter, sort and clear-filter
recovery to an IndexedDB-backed offline library with asynchronous refresh.
The key interaction distinction is between fast **view projection** of the
most recently loaded library snapshot and an explicit **persistence refresh**
that may await disk/legacy migration: filtering should not perform a database
request per keystroke, nor should Refresh blank the entire book list while
a new asynchronous result is pending.

Related recoverable-state checks:
- Distinguish an empty underlying library from a non-empty library with zero
  matches for a search/filter, including a one-click reset.
- Show visible/total counts so the user understands why cards disappear.
- Preserve the last completed view on a failed refresh and explain that its
  contents may be stale; version/fence concurrent list requests.
- For a two-step destructive confirmation, support `Escape`/Cancel without
  persistent mutation and restore focus to the initiating control. Guard
  refresh-control reenablement if deletion invalidates a pending list read.

Evidence at intake: CVR PR #18 head
`9dce0d8ccdb8023d6536f7ce111805637d31bbc8`, implementation and
Chromium test submitted; final CI **Pending**. The candidate has not
been validated on physical mobile devices or screen readers.
Dedup: extended the existing CVR offline-first shelf Candidate rather than
creating a competing Canonical rule. Prior Foundry search found related
destructive confirmation and async rendering records but no exact shelf
search/async-refresh combination.

## Post-CI implementation evidence: recoverable resume and shelf discovery (2026-10-10)

The previously pending candidate extensions are now supported by completed
automated checks and main-branch merges in the source repository:

- CVR [PR #17](https://github.com/11576865/Character-Voice-Reader/pull/17)
  was merged at `f6b90c3121c9366cf1808cff87679c26ab249dc8`.
  Final test head `565d54aad19891c8335aa669aa7072726c8a2fc6` passed
  normal Reader tests and actual Chromium media regressions.
  During validation an initial browser assertion read the stale error
  message immediately after the media element resumed; the UI queue state
  had not yet completed its asynchronous transition. The final regression
  waits for both playing state and cleared error message, rather than
  weakening the functional check.
- CVR [PR #18](https://github.com/11576865/Character-Voice-Reader/pull/18)
  was merged at `1bbb3074c751b3350e3268e55e4826224703ad62`.
  Final test head `9dce0d8ccdb8023d6536f7ce111805637d31bbc8`
  passed Reader tests and the dedicated Chromium/IndexedDB workflow.
  Browser regression covers search/sort/filter, no-result recovery,
  delayed refresh without flashing old cards, Escape cancellation of
  deletion, and confirmed deletion.

Evidence level: source implementation + headless Chromium regression,
not physical Android/iOS UX or assistive-technology acceptance. These are
still Candidate-level examples, not grounds for automatically altering
Canonical standards.
