# Observation: Remote archive Apply must validate source revision at commit, not only at request

Date: 2026-10-11
Status: Open engineering risk based on source review; runtime race reproduction pending
Project: HSR-Voice-Archive-Builder
PR reviewed: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
Head reviewed: a0d4b95712bf2fa320584224c49099afd0c2c80f

## Findings

- FastAPI `app/server.py` lines ~1351–1375 and Termux `app/lite_server.py` lines ~1232–1254 verify plan Manifest SHA-256 before enqueuing `remote-update-apply`; background closure later downloads and alters combined source/config/index without a second revision guard near publication.
- `app/jobs.py` only enforces one active task for `BUILD_KINDS = {"build", "quick-build"}` when starting a job. The remote-update-apply kind is not covered by that guard. While specific concurrent scheduling scenarios require a runtime test, there is no evident shared per-project mutation transaction encompassing remote apply and archive build.
- `app/server.py` removes existing combined directory before replacing with staging, then writes incremental CSV and changes project configuration. An interruption in the middle can leave an incomplete intermediate state. Source/member basename preflight is useful but not full rollback/atomic publication.
- Existing UI `showPlan(plan)` initializes `selectedRemoteAdditions` to *all* remote `new_logical` rows; subgroup presentation is not proof of chapter-level explicit selection.

## Recommendations for focused follow-up

Bind a committed update plan to archive and input-package revisions; recheck at publication. Introduce a per-project mutation lock covering build and remote apply. Write generated audio/index/report to versioned staging; publish only on success, preserve rollback provenance and a recoverable previous source config. Require explicit selection acknowledgment rather than advertising automatic full-selection as selective review. Validate concurrency, interrupted job, provider data changes and realistic multi-chapter WAV package.

This is a source-based Observation, not demonstrated user data corruption or a production acceptance failure. Canonical unchanged.


## Repair checkpoint — immutable per-update publication (2026-10-11)

HSR PR #133 now defaults to **empty** remote selection, revalidates Manifest and selected candidates *again* inside the asynchronous job before touching persistent source/index, and serializes active build and remote Apply jobs for a shared project root in the existing in-process jobs framework. FastAPI and Termux Lite no longer delete the existing `.generated/combined_audio`; each Apply stages a fresh `.generated/combined_audio_versions/combined-<version>` tree and `quick_index_incremental_<version>.csv`. The new project configuration points at those files only after both exist, keeping previous source resources available following failures. The recovery package also captures the active index.

Synthetic tests cover job concurrency and static publication contracts; exact code/test checkpoint `731b65a65a3c57595a05cb2a45ab34634a6dfeb4` passed [Python](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714940) and [Chromium/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714983).

**Open:** no tested atomic transaction across multiple OS processes or external filesystem mutations; config switch, final user build and provider source revisions are not one atomic commit. Old version directories are not garbage-collected automatically. Crash-injection and large real archive data remain pending. Keep as Observation, not Canonical.


## Journaled two-phase remote publication and guarded rollback (2026-10-12)

The existing HSR source-review Observation has advanced from *versioned
resource staging only* to a bounded recoverable publication protocol on
[PR #133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133):

- `app/remote_update_publish.py` records original project-config, index,
  and Manifest SHA-256 snapshots and validates all three again immediately
  before config publication. Published selected WAVs must match exactly
  one row each in the new index with correct `source_member_id`; the files
  must be present in the new version directory.
- An atomic `incremental_revisions/<uuid>.json` **prepared** journal
  precedes project config replacement, preserving the complete original
  project settings and the hashes of both old and intended new config.
  The later **committed** journal is not itself trusted as evidence:
  read-only inspection compares hashes of the actual disk config.
  If power/process termination occurs between config replacement and
  final journal marking, it reports `applied_unfinalized`.
- An explicit preview→confirmed rollback API/UI action is allowed only
  if the relevant version is still active, its project SHA has not changed
  since preview, the Manifest is unchanged, and the prior source/index still
  exist. It restores the prior config atomically but retains all resources.
  The rollback job is serialized with build and incremental Apply in-process.
- FastAPI and Termux Lite share the same publication helper and
  `/api/update/revisions` plus `/api/update/rollback` routes. Termux
  Lite's incremental CSV now includes the same explicit `source_member_id`
  column and duplicate member protection as FastAPI.

`tests/test_remote_update_publish.py` injects failure before config save
and between config replacement and journal finalization, tests inspection
and guarded rollback, changed Manifest/config/index denial, and incomplete,
duplicate or member-mismatched selected WAV/index combinations. Additional
tests cover same-project rollback/build exclusion and route parity.
Code+tests SHA `3b777564170ea651f373e38be33b7f22198c8d9d` passed
[Python 3.11/3.12/3.13 + Termux surface](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38159748776)
and [Chromium/libass browser evidence](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38159748801).
Documentation-only commit after this checkpoint must be checked separately.

**Still open:** No cross-process commit lock, complete multi-file ACID
transaction, live power-loss test, real large HSR archive integration,
or automatic old-version pruning. Journal metadata does not prove provider
origin content is trustworthy or actual downstream final archive rebuild
success. This is project-specific Observation evidence, **not a new Canonical
rule**.


## Synthetic end-to-end Apply and rollback acceptance (2026-10-12)

Beyond static code checks and helper-level fault injection, HSR PR #133 now
has an end-to-end FastAPI Apply→rollback **synthetic local WAV** regression
(`tests/test_remote_apply_integration.py`). It uses the actual API job,
source directory merge, combined WAV staging, generated index writer,
revision journal publication, revision-status route, and explicit rollback
route, while mocking only external Hugging Face metadata/audio retrieval.
A second path injects publication failure and proves the prior on-disk
project configuration and CSV index remain intact.

Latest exact head `6298f0a1d12fb163b030288efb9adcf35e04c5ff` passed
[Python 3.11/3.12/3.13, Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38160022203)
and [Chromium/libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38160022198)
(six successful jobs total). The Termux Lite API surface shares the
backend helper and passes its surface checks, but a complete live Termux
network-download plus update round-trip was not exercised.

**Unverified**: genuine game WAV corpus, live provider audio, multiple
writer OS processes, abrupt power removal, physical Android/Termux
acceptance, and a comprehensive downstream rebuild after Apply. Keep
Observation level; do not claim full cross-process transaction correctness
or promote Canonical from this fixture evidence.
