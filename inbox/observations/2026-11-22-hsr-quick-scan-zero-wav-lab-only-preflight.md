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
