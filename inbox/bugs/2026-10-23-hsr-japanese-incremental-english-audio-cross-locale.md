# Bug — HSR incremental voice application can cross audio locale boundaries

Date: 2026-10-23
Status: **Bug / source-confirmed root cause; user-observed Japanese archive with English incremental voices; field artifact not independently inspected**
Project: `11576865/HSR-Voice-Archive-Builder`
Repair PR: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/209
Severity: **Data integrity / wrong-language audio provenance**

## User symptom and verified code chain

A project created with Japanese source voice audio was incrementally extended with English speech, rather than Japanese. The user's report provides occurrence evidence, but original project files/recordings are not present here for byte-level verification.

On repository main reviewed on 2026-10-23:

1. `app/project.py` default `remote_index_url` points at `Indexs/EN.xlsx`, while check routes in `app/server.py` and `app/lite_server.py` prioritize the persisted URL over the locale-specific provider URL.
2. `app/huggingface_audio.py::resolve_targets()` previously selected primary records only from `English` and `English(US)`, treating `Chinese(PRC)` as optional reference and excluding Japanese/Korean audio as primary candidates.
3. `update_plan.json` did not retain an authoritative primary audio locale, and all locales reused the same `.generated/incremental_audio` directory. Subsequent `apply` could therefore propagate a successfully obtained English WAV into a Japanese combined source/index.
4. The downloader's format and WAV header verification establishes that the result is audio, **not** that the human language matches the project.

The observed problem is therefore a cross-locale **source identity failure**, not a translation or subtitle-display bug.

## Repair checkpoint / bounded claim

HSR [PR #209](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/209), exact proposed head `1468da860d5c57fc536b5b6d36c8377331f70f4f`:

- Requires explicit supported primary audio language; rejects `auto` and divergent source-text language for automatic augmentation.
- Chooses current language's official index when the persisted URL is another official index.
- Resolves HF audio rows strictly within the intended primary language, with no English fallback for `ja`, `ko`, or `zh-CN`.
- Carries `audio_language` in the update plan and rejects stale or locale-mismatched plans before new downloads.
- Separates incremental audio cache by language and validates resolved-row audio language before download.
- Refuses future mutations of projects with old success receipts that imply English audio had been applied to a non-English archive; never silently deletes/rewrites contaminated audio.
- Adds Python regression cases for Japanese/English mixed records, Japanese absence, Korean/Chinese audio, old plan, and legacy receipts.

**Evidence state:** Code and regression additions submitted for review; CI / actual Hugging Face network downloads / physical Termux projects / existing polluted archive remediation are **Pending**. The PR itself is not proof the user's already altered WAVs have been repaired. Canonical norms unchanged.

## Suggested permanent test / case

Create a tiny synthetic HF `result.json` with two different WAV rows for the *same in-game filename*, one in `English/` and one in `Japanese/`. Select Japanese source audio, then assert:
- JP remote index chosen even if older config saves EN; download target points at Japanese row index;
- source primary dataset row and downloaded WAV provenance show `ja`;
- missing Japanese row fails closed; English same-name row cannot substitute;
- repeated check/apply cannot reuse English cache or stale EN `update_plan`;
- preexisting Japanese project with legacy locale-less English apply receipt cannot be silently labeled fixed;
- both FastAPI and Termux route behavior stays parity-aligned.

For actual field closure, inspect original Japanese package, current `.hsr-voice-project.json`, `update_apply_report.json`, `.generated/incremental_audio`, generated index, and WAV samples before rebuilding, preserving backups.

## Dedup

Searched Foundry prior to filing. This is distinct from:
- `inbox/bugs/2026-10-20-hsr-hf-partial-file-false-download-success.md` (partial `.part` or invalid media classified as downloaded);
- `inbox/observations/2026-10-11-hsr-remote-apply-preflight-not-transactional.md` (revision binding, task concurrency, publication transaction).
This bug concerns **which language's otherwise-valid audio is being selected and adopted**. No automatic Canonical change.


## Second engineering pass — row identity and legacy-source audit (2026-10-23)

HSR PR #209 subsequently advanced to head `043b830e2e8d6a81d94a6b33a98137d74925fbd4`. Additional repair slices:

- Read-only `app/incremental_locale_audit.py` examines old incremental apply receipts, current/initial source paths, original Quick Scan metadata and initial index; exposes identical `GET /api/update/locale-audit` in FastAPI and Termux, with an Update workspace button. It cannot infer spoken language or certify current source hashes, and it does not mutate files.
- Critically, a locale-matched `result.json` row number is **not** itself download proof: dataset `/rows` may return a different row if upstream content changes. The downloader now checks row language, in-game path locale and relative file identity before reading `audio.src`.
- Pre-existing WAV files without recorded row provenance are not accepted as valid locale-bound downloads. Stage/publish copies only the successful files from the current download result (not every file in a shared directory), validates extension/header and download-time SHA-256 before source publication.
- Tests cover changed row language, changed row identity, old/unknown cache, staging whitelist and digest tampering, historical English receipt and absence/corruption of the original Quick Scan/receipt. Dataset-level (English/Japanese/Chinese/Korean) metadata is an external API assertion, not proof from a locally executed real download.
- **Validation:** first PR head `1468da8` had successful Python unit (3.11/3.12/3.13) plus Termux, Windows writer, subtitle browser and journal workflows; one Seven ASS workflow was cancelled. Updated head `043b830` workflows were queued when examined. Do not promote this later head as CI green without its exact results.
- Existing contaminated archives are not automatically repaired. Any restoration remains **FIELD-PENDING**, requiring verified original Japanese source and independent rebuilt audio acceptance.

Intake: update existing Bug, distinct from older HF `.part` success and publisher concurrency cases. No Canonical promotion.
