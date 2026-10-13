# Case: Native ASS Fade preview/Apply parity and malformed source fail-closed

Date: 2026-10-14
Status: Android main source and tests committed; Build/Device Pending
Project: 11576865/ASS-Workbench-Android
Related: inbox/cases/2026-10-14-ass-native-fade-blur-draft-commit-guards.md

## Trigger
Following the per-Event Fade/Blur session draft changes, Fade had only a formal Apply action and no source-bound transient preview. Review also found a dangerous no-op acknowledgement path: unsupported/malformed Raw could produce no source modification but still clear a dirty draft. Preview and Apply originally computed their proposed Raw changes separately.

## Implementation
- Added pure proposeEventFadeSource backed by the existing AssAnimationSemantic patchers. It rejects unsupported Fade modes, invalid numeric ranges and malformed leading override structures. Preserves non-Fade and unknown Raw tags as supplied by the domain writer.
- Reused the same proposal for ViewModel previewEventFadeIfSourceMatches (changes previewDocument only) and applyEventFadeIfSourceMatches (canonical Event text transaction and document history only if the Event source still matches). The UI offers compact Preview / Apply actions; both become disabled on malformed input or a stale source.
- Fade/Blur UI now acknowledges the draft only after a meaningful accepted transaction; no-op or failed writes no longer silently discard dirty input.
- Source-aware Blur preview/Apply also fails closed on malformed leading ASS override blocks. UI shows a concise Raw warning instead of an always-clickable write button.
- Added JVM plan tests and native Android instrumented assertions including Preview Raw equals subsequent committed Raw, stale source, invalid values, Undo, malformed source and disabled controls.

## Repository commits
91e26596e1df37b6774c9b563a473a74253cb478 shared proposal.
8e41f995db3c467a60f49e2219a98c153a72979b preview/ViewModel integration.
dffaa2d438d8d37e6aaeaaba11e35c4a54452628 compact Fade preview UI.
f06d4f7c47f19cfe1820be50aa41f2b6ff8cb2cf JVM tests.
43f42b5b90e3ba15d0f29bee547c1ffacff5c86d Android preview/commit test.
834ac7fa123027448504d47837eee3f145091bbb invalid source guard.
77214ab61173573e670538b473d97d1d87896def do not acknowledge failed no-op.
8b58119e192d67f7e3269d5b4858b86b11a50312 ViewModel Blur source guard.
aa91fe97302a61a319626821b95a646576c564a9 UI disable invalid Raw edits.
30740f8cb79fd2789da6e450e038e754e491276f Android malformed Raw test.
918c577e7b6f483dae97cdd4e1937295cfe03d6e product checkpoint.

## Evidence boundary
Source and tests exist on main, but no Gradle build, actual JVM run, native instrumented pass, emulator screenshot, media decoding, renderer PTS or .ass save/reopen pass has been verified. The repository has an Android CI workflow triggered on push to main, but current connector only exposed empty legacy commit statuses and did not confirm any workflow outcome.

## Reusable observation
Preview and Apply must consume a single semantic patch plan; not merely similar input values. Unchanged or refused writes must not implicitly discard dirty UI state. Malformed source cannot be safely treated as an empty override into which a typed editor may insert arbitrary new tags.

## Dedupe/governance
Searched native Fade preview and Apply shared proposal, malformed ASS override blocks, and Android transient document preview. The earlier v5 HTML prototype Case is adjacent but not equivalent to this native implementation. No Canonical promotion.