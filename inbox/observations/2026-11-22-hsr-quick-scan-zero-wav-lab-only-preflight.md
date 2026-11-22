# Observation: Quick Scan with no primary WAVs emits both root-cause and dependent index blockers

Date: 2026-11-22
Status: Field observation and source-traced diagnostic; input cause unconfirmed
Project: `11576865/HSR-Voice-Archive-Builder`
Domain: preflight diagnostics, user-visible dependency failures

## Field evidence

The user's mobile screenshot of HSR Quick Scan shows `Generic voice package (none)`, `WAV 0`, `LAB 251`, `same stem 0`, no character/group classification, `source_text_language=en`, no index, and these blockers:

1. `No WAV files were found in the primary audio source`
2. `No reliable local or remote index covers the package WAV names`

Quick Scan correctly prevents launch. No selected source path, package listing, WAV bytes, or prior successful project-source configuration were supplied. The screenshot therefore does **not** prove that WAV files were deleted, that all media is missing, or that a particular wrong package was selected. Some plausible causes: LAB-only text archive chosen as primary, archive containing nested ZIP/7z, or non-WAV audio.

## Production source trace

`app/quick.py::source_inventory` accepts a directory, `.zip`, or `.7z`, enumerates the entries therein, and counts only filenames ending `.wav` case-insensitively. It does not recursively open archive files that themselves appear inside another archive. In `quick_scan()`, `english["wav_count"] == 0` adds the first blocker. With no recognized WAV member, no useful index can be selected and incomplete sibling-LAB coverage means the independent later branch also appends the second blocker. Game profile and character detection likewise have no voice filenames.

## Reusable UX diagnostic consideration

Separate *primary-input corpus absent* from *index coverage failure for a nonempty corpus*; the latter should be labeled downstream/not evaluated if the former is false. A blocking preflight should state which selected input was inspected (source type/path with appropriate privacy), member counts and supported `.wav` requirement, and differentiate text-only package from audio. Do not bypass zero-audio gate or infer the correct file automatically.

## Evidence / status

Source review plus one user-visible observation only. No code edits or tests executed, and root cause of the user's selected source remains unverified. Candidate diagnostic improvement only; **not Canonical**. De-dup search found no prior Foundry record about this exact zero-WAV plus redundant index-blocker case.

## Follow-up user evidence: nested directory contains WAV (2026-11-22)

User explicitly confirms that the extra layer inside the selected-looking package is an ordinary **folder** and that the folder **does contain WAV files**. This rules out an inner compressed archive as their description; it does not independently authenticate the source path passed by the form or provide a member listing.

Source check: `source_inventory()` uses `Path.rglob("*")` on directory inputs, `ZipFile.infolist()` on ZIP and 7z `l -slt` member parsing on 7z. All filter by case-insensitive `.wav` suffix regardless of folder depth. A local nested ZIP path `root/voice/actor.wav` is discovered normally by the same selection logic. Thus the explanation "one extra ordinary folder caused WAV 0" is contradicted by the implemented path logic.

**Next decisive evidence:** the exact primary-audio path returned/sent by the Quick Scan form and the actual member names from the same file (native `7zz l -slt` for 7z, `unzip -Z1` for ZIP, or `find` for directory). Compare that with `source_inventory(path)["wav_members"]`. If raw listing includes WAV while inventory does not, file parser bug; if different paths or names, source selection / stale UI state. Avoid speculative parser modification or bypass of the zero-audio gate without this evidence.

Status **Pending field source identity**. No production change, no Canonical promotion.

## Source capability boundary confirmed (2026-11-22)

User challenged whether the software could accept extracted directories or lossless FLAC instead of WAV. Direct `main` inspection confirms directory input recursively enumerates file paths, plus ZIP and 7z input. However `app/quick.py::source_inventory()` counts voice audio exclusively by suffix `.wav` and sibling `.lab`. `app/builder.py::build_continuous_flac()` resolves WAV paths and parses PCM WAV with `parse_wav_pcm()`; direct FLAC as a *primary source* is not supported, despite FLAC being the output format. Already-extracted directories containing valid WAV members are supported in the backend. UI native folder-picking affordance is an independent question and is not established by the backend check.

Interpretation: if an archive contains FLAC and LAB but no WAV, the observed `WAV 0 / LAB 251` and dependent missing-index warning are expected under current code, not proof of an archive enumeration defect. If actual members have `.wav` suffix, exact selected source and member listing remain needed. No changes to recognition counts without supporting decode, sample-frame timing, source identities and cross-stage provenance. Candidate follow-up: input inventory by real codec, explicit unsupported-format blockers, lossless FLAC decode to scratch PCM with original-source hash, transcript stem matching and no destructive conversion. **No production implementation yet**; do not claim native FLAC support.

## Confirmed Quick Create UI/backend contract gap and bounded repair (2026-11-22)

User corrected the earlier "directory supported" answer: in the **actual Create FLAC / Quick Create interface**, they can only choose archived sources. Source-level verification found the concrete gap in HSR `app/static/index.html`: the primary source is `<select id="quickEnglish">` filled only by `/api/quick/candidates`; `app/quick.py::discover_source_candidates()` previously listed `is_file() and suffix in {'.zip','.7z'}` from known Downloads roots. Its subsequent `quick_scan()`, `source_inventory()`, `ensure_dir_or_extract()` and WAV PCM builder nevertheless accept filesystem directories. Therefore API-level directory support was not an accessible user workflow. This is a distinct **UI capability reachability defect**, not proof of a decoder or content-inventory bug.

HSR [PR #224](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/224), head `92c28b4131c9e14eb449972ece0a83274a9f3d96`, adds bounded no-hash nested-WAV-directory discovery from existing roots, labels directory candidates, offers manual local Termux directory/ZIP/7z path entry, and routes both Quick Scan and Quick Build to the same effective source. Source changes invalidate the previous scan eligibility. Regression tests cover nested unpacked WAV+LAB corpus, local package-lab Quick Scan and UI binding. No input file modifications. Primary FLAC input remains **unsupported**; do not infer it from output FLAC support.

**State:** Product code and test committed to review branch, PR open. First immediate PR-head workflow-run query returned no runs yet. **Pending External Validation** for exact-head CI and actual Android/Termux FLAC generation from an extracted folder. No Canonical promotion.

## FLAC as primary voice clips — implementation candidate (2026-11-22)

The user expressly requested implementing FLAC as *input*, not merely scanning the filename. A narrow product implementation now exists as stacked HSR [PR #225](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/225), head `04e2b3b261f9f89ac2b64f3fc8152826e80c6bce`, on Quick Create directory-input PR #224. The original observation that production main had WAV-only input remains historically correct; PRs are **not yet merged**.

Implementation: source inventory recognizes FLAC inside extracted directories, ZIP and 7z via unique virtual WAV member IDs, preserving sibling LAB matching and blocking WAV/FLAC same-stem collisions. The build worker stages real FFmpeg lossless decode into isolated PCM WAV files; checks codec, original bit depth, channel/rate, exact STREAMINFO frame count and source stability, with bounded decoded sizes. The manifest carries the original FLAC member path and SHA-256 as separate from decoded PCM SHA-256. Resumed builds authenticate both original container identity and derived PCM. Source-byte audits compare original FLAC rather than the derived WAV. Original voice audition decodes single FLAC clips into a source-hash-bound local cache. UI lists WAV and FLAC independently and preserves manual local source path. Tests exercise real FFmpeg FLAC folder, mixed 24-bit ZIP, collisions, corrupt input, source identity and resume.

Reusable design distinction: **format aliases for index compatibility must never replace persisted source identity or decoded PCM integrity evidence**. Source bytes, decode parameters/sample count and derived bytes need separate provenance fields; a foreign WAV index hash cannot be asserted about FLAC bytes. This remains a source-backed, bounded **Candidate/Observation**, not a promoted Canonical rule.

Validation status: PR #225 feature branch open; exact-head GitHub Actions first read showed jobs queued or in progress. Physical Android/Termux end-to-end source acceptance and production merge **Pending External Validation**. PR #224 had a previous UI-contract test failure (global textual assertion) and a Playwright 1.55 Chromium installation failure on Ubuntu 26.04; the assertion was narrowed and browser job runner pinned to supported Ubuntu 24.04, with new CI pending. Do not claim feature shipped or complete until merge + device rerun.

## 2026-11-22 correction: green CI hid skipped real-FFmpeg FLAC acceptance

User observed that FLAC still cannot be detected after PR #225 was drafted. A fresh live repository check showed both HSR PR #224 (folder picker) and #225 (original FLAC sources) **still open and unmerged**, while main `app/quick.py` recognizes only `.wav` and main Quick Create only offers the ZIP/7z candidate selection. Thus pulling main will not expose the feature.

Also found a **test-coverage weakness**: all six workflows of prior PR #225 head `04e2b3b261f9f89ac2b64f3fc8152826e80c6bce` were green, but `tests.test_flac_quick_source` was `skipped 'Real FFmpeg and FFprobe required'` in regular Python matrix, so green CI had not established real FLAC ingestion. Added mandatory `python -m unittest tests.test_flac_quick_source -v` step to a media-evidence job that installs genuine FFmpeg/FFprobe. This exposed four genuine positive tests and a fifth test error due to the *test's* incorrect `来源成员路径` field rather than the generated quick CSV's `source_member_id`; fixed on the PR #225 branch at `f9c805426c08379438a89a054f27e9d8fd4b8347`. Await the fresh exact-head CI before promoting any acceptance claim.

Reusable principle/candidate: a skip-tolerant test matrix can show an all-green PR while a newly required codec's **entire end-to-end acceptance suite never runs**. Guard codec features with an explicit media-tool-equipped required job and verify individual test results, not only workflow conclusions. This is an **Observation**, not Canonical. Physical Termux field acceptance and merge remain **Pending External Validation**.

## 2026-11-22 release verified — original FLAC source support merged; device acceptance pending

Following the mandatory real-FFmpeg acceptance correction, **both dependent PRs are merged** to HSR main:
- [Quick Create directory chooser PR #224](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/224), merge commit `def0efcf3d5412086fd26f129df363ecffcd5663`.
- [FLAC voice-source PR #225](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/225), merge commit `f0d1ee9072480912af7bbcba577b0c671339659d`.

Each PR-head had six GitHub workflow results success. Crucially the FLAC PR's `tests` workflow included actual `ffmpeg` and `ffprobe` installed, and its dedicated `real-libass-ink-evidence` job (137259424502) executed **five of five real `tests.test_flac_quick_source` tests successfully with no skips**, as shown in job logs. Cases cover extracted FLAC-only folder full build and resume, ZIP mixed sources, original manifest hashes/source audit/reference preview, duplicate FLAC basenames with LAB, corrupted FLAC and same-stem WAV/FLAC conflict.

Independent **post-merge main readback** confirmed virtual WAV member inventory with separate `flac_count`, `app/flac_source.py` decoder/provenance, `builder.py` private PCM staging and original source identity, `app/static/index.html` directory/manual path selector and WAV/FLAC separate preflight count, and workflow's mandatory FFmpeg acceptance step. This resolves the initially observed **released-main path missing** issue. No Canonical promotion.

**Evidence level:** merged product code + PR-head CI (with real FFmpeg) + main source readback. **Actual Android/Termux build of user's own media package still Pending External Validation**; front-end may need Termux `git pull`, service restart, and a fresh reload. Auto-folder candidate discovery is bounded to common roots; manual source path is intentional fallback for nested/external locations. Do not treat user's earlier failure as physically resolved until an on-device build succeeds.
