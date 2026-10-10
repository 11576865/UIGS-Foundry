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
