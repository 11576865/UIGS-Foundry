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
