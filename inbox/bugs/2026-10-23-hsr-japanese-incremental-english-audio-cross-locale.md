# Bug — HSR incremental voice application can cross audio locale boundaries

Date: 2026-10-23
Lifecycle: validation-pending
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

## Isolated restoration path — source fingerprint + initial-index verification (2026-10-23)

HSR PR #209 now includes `app/japanese_source_recovery.py`, invoked by an explicitly acknowledged `POST /api/update/create-japanese-recovery` on FastAPI and Termux, plus an Update workspace action. It requires project audio/source text languages `ja`, Quick Scan source text `ja`, exact originally recorded SHA-256/tree content fingerprint, and full agreement between original Quick Scan CSV members and source package WAV members.

The procedure creates a new sibling project with its own original-index copy, isolated output/state paths and no old incremental caches, text overrides or MKV, while preserving the existing project. It does not download Japanese audio, replace existing English WAVs, build FLAC/MKV or claim listening acceptance; it merely creates a source-verifiable candidate for a later independent rebuild.

Regression tests cover original-byte preservation, archive tampering, index mismatch, ambiguous language and FastAPI/Termux parity. The first CI execution of the new recovery test failed because `os.replace(staging, destination)` had been placed inside the post-check rejection branch; source was traced to incorrect indentation and fixed at `f5dcc215fddbfea69a1979d41342f6d8b9026f1a`. Exact-head CI and real-user archive acceptance remained pending at writing. This is a proper source-confirmed new implementation defect, repaired in the same PR before merge. No automatic Canonical promotion.

**Evidence boundary:** source fingerprint establishes identity to the original Quick Scan package, not the correctness of that user's chosen audio language. The candidate references the original package, so deletion of the original path would invalidate it. Existing translation/editing changes require deliberate migration rather than blindly importing records from the possibly contaminated archive.

## 2026-10-24: same-locale row identity gap — subsequent regression in the same provenance chain

The original wrong-language Bug #209 is now **merged** to HSR `main@63cfc2e4e5100ae373b70943a5a7360feafb67bb` after exact-head CI. A further source-level review of upstream `simon300000/starrail-voice/update.ts` and `parquet.py` established that `result.json` stores the source WAV hash key, but the independently published Hugging Face Parquet exposes only `audio`, `ingame_filename`, `transcription`, `language`, `speaker`, `voice_type`. Upstream README dated 2026-07-16 reports **57,869 / 403,437 (14%)** rows without inGameFilename. This metadata is external source evidence, not a locally reproduced spoken-language failure.

**Unclosed guard:** Previously `_verify_dataset_audio_row()` accepted rows where either original or actual `inGameFilename` was blank, as long as `language=Japanese`. An upstream reordering could therefore produce **the wrong Japanese voice line**, not necessarily English, despite the locale guard. Without Parquet's original WAV hash, row number + locale alone is not a robust identity binding.

**Repair proposed in HSR PR #210:** `resolve_targets()` explicitly classifies matching rows without nonempty `.wem` game identities as `identity_unverified` and `unresolved` instead of download targets; `_verify_dataset_audio_row()` requires both source index and live Parquet game identities and exact language-independent relative-path agreement; adds a read-only CLI that compares cached `result.json` with real /rows metadata on device without WAV download or project writes. Regression tests cover incomplete identities, row drift, a valid JP Parquet-schema row and source-output protection.

**Acceptance boundaries:** PR #210 at `74cc3768f1f1fb9f35f6ed156453c8aa21bdb2d2` awaits exact-head CI at time of intake. No live audio, user-device playback or full archive rebuild accepted. The new CLI permits a later independent real metadata parity check; running mocked tests is not that check. Even successful metadata parity does not establish spoken Japanese. Existing Canonical entries remain unchanged.

**Dedup:** Retained in this Bug rather than creating another record because the failure is a narrower provenance/row-identity subcase of the same Hugging Face incremental-apply chain. Distinct from the older `.part` false-success Bug, which concerns byte validity not target identity. Lifecycle remains `validation-pending`.


### 2026-10-24 Product UI evidence follow-up

HSR PR #210 head `7f3f731c80ddfcb806523bb8408760a91a8ebe5e` adds read-only `POST /api/update/probe-japanese-rows` on both FastAPI and Termux; the Update workspace shows an explicit probe action, metadata parity count and success/failure. It uses a previously cached large `result.json` file and queries Hugging Face row metadata only; missing cache fails explicitly instead of silently downloading WAVs. The `locale-probe` background job fails if sampling is incomplete or any row identity changes, rather than reporting generic task success. The same work improves isolated recovery UI reporting to show the candidate path or failure. Full exact-head CI, live HF metadata checks and actual Japanese listening remain Pending. No Canonical promotion.

## 2026-10-24 CI closure — HSR PR #210 merged

HSR [PR #210](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/210) merged to main as `a0ee60a58a05793701377c4a26095c5e4f10fa3d`, exact proposed head `4922d5503aebbf4e6b41d2e0c0d5bff16a6cb8ec`. The six exact-head GitHub Actions workflows completed `success`: tests (Python 3.11/3.12/3.13, Termux Lite, real-libass ink), subtitle browser evidence (Chromium + libass artifact), Seven ASS requirements, Windows writer and journal safety, sustained concurrency, and pinned legacy interop/process-exit recovery. Source inspection of `main` confirmed `app/hf_locale_probe.py` and strict `identity_unverified` filtering.

Source-level repair is therefore **MERGED / AUTOMATION-VERIFIED** for the same-locale row identity regression. The original end-user Japanese archive was not accessed, so actual WAV spoken language, Japanese remote network parity and archive reconstruction remain **FIELD-PENDING**; keep Lifecycle `validation-pending` and do not modify Canonical.

## 2026-10-24 — recovered source changed after candidate creation

**Confirmed code gap in `HSR main@8d86c83d2b047c74d4f26b67d5f7090bb163ab8a`:** `create_isolated_japanese_recovery` validates the external original archive/ZIP/directory SHA-256 when it creates a new sibling candidate, then leaves `wav_source` pointing at that external file. The ordinary build computes a fresh stage cache input fingerprint from whichever bytes currently exist; it does not compare `ProjectConfig.wav_source_fingerprint` to the original Quick Scan fingerprint. If the external source changed between creation and rebuild, the new candidate could appear rebuilt successfully from a different package. This is a source-confirmed time-of-check/time-of-use loss of recovery provenance, not evidence of a real user's source having changed.

**Repair in HSR [PR #212](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/212):** issue an explicit `.generated/japanese_source_attestation.json` receipt recording original archive bytes/tree fingerprint, initial CSV digest and exact WAV member count. Persist `recovery_source_attestation_required=True` on the candidate configuration; a missing or disabled receipt fails closed, including legacy `*-JP-source-recovery-<hex>` candidates lacking the new receipt. Run source/index/member-fingerprint verification **inside** the FastAPI and Termux Build job before mutating outputs, not only at API request time. Recheck after the build and match `manifest.json` entries exactly against the original Quick Scan `source_member_id` set, including duplicate WAV basenames in separate chapters. The successful job returns a bounded `source-members-verified` statement, explicitly `spoken_japanese_verified=False` and `human_listening_required=True`.

Tests exercise changed original source, changed CSV, diverted project source, missing attestation, legacy candidate rejection, after-build manifest mismatch, and offline ZIP-to-manifest rendering of two distinct chapter WAV/LAB identities with original outputs untouched.

**Acceptance boundary:** HSR PR #212 exact-head CI still pending on 2026-10-24. New proof verifies the originally scanned **bytes and member identities**, not acoustic language or translation correctness. No real archive downloaded/modified, and no automatic Canonical update. Keep this Bug `validation-pending`, distinct from the previously fixed wrong-locale HF download and separately recurrent Termux basename flattener.

### Exact-head verification / merge closure for source attestation (2026-10-24)

HSR [PR #212](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/212), exact pre-merge head `1080c624812b4011b8cef129decd3501acb0f0e7`, passed **all six GitHub Actions workflows**: Python 3.11/3.12/3.13, Termux Lite, real-libass unit evidence, Chromium UI, seven ASS requirements, Windows writer safety, legacy interop/process-exit recovery and sustained concurrent journal tests. Squash merge to `main` was confirmed at `f295acefa8a64deb66fd16e747630744e288f854`.

An explicit `recovery_source_attestation_required` project field prevents deletion of the candidate's receipt from bypassing verification. Old un-attested recovery sibling directories fail closed. The offline full Quick CSV → original ZIP of valid PCM + two identical `same.wav` basenames in different chapters + distinct Japanese LAB → actual `build_project_v02` → source/member-validated Manifest test passed in the CI matrix. Browser displays a separate “source-members verified, still requires listening” status rather than claiming true spoken Japanese.

**Lifecycle remains `validation-pending`:** source-byte and generated-member provenance are automation-verified, but no actual user archive, voice playback or linguistic Japanese verification was performed. No Canonical promotion.

## 2026-10-24 — human listening acceptance pack (field evidence preparation)

After exact-source recovery and membership verification were merged in HSR PR #212, a remaining acceptance gap is that a correct manifest and source fingerprint **do not prove the content sounds Japanese or that the final encoded audio maps correctly to the transcript/time offsets**. Existing archive_audit.py is structural/byte-only and cannot satisfy the missing human voice-language check.

HSR [PR #213](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/213) implements a specific field-evidence instrument: export a finite sample of *paired* original Japanese WAV clips and the corresponding time-positioned **finished FLAC/MKV** clips, requiring an attested isolated candidate and current original/source-member proof. Prioritize chapter-local same-basename collisions, then chapter coverage and distributed manifest samples. An offline HTML review page asks the actual human listener for language identity, spoken-source-text correspondence and source-vs-final sound correspondence, and exports a review JSON. Each evidence row includes member ID, subtitle text, audio timing and short-clip digests. Old/stale packs become invalid if the original source, manifest, or finished media changes. This is not automatic speech recognition, and a sampling PASS must not be elevated to a proof about all archive lines.

**Status at intake:** PR #213 exact-head Python 3.11–3.13, Termux Lite and media unit tests passed (synthetic Japanese-text WAV tone samples; tones do not establish spoken Japanese). Full six-workflow CI and merge still pending. No user source archive or actual Japanese listening review available, so Lifecycle stays validation-pending. No Canonical changes.

**Dedup:** attached to existing HSR Japanese contamination/recovery Bug rather than creating a separate source-audio Bug. Reusable pattern: field-level claims need side-by-side input/output playable evidence and explicit human sign-off, separate from cryptographic structural validity. Treat as observation only until independently applied in another project.

### 2026-10-24 exact-head CI closure and merge — Japanese listening pack

HSR PR #213 final head `bdd3c151095f8b3cc888e94c5372d13370c521d4` passed **all six** exact-head CI workflows, including Python 3.11/3.12/3.13, Termux Lite, actual FFmpeg source/final audio pairing test, non-silent decoded final PCM, browser/libass, Windows safety, Seven ASS, pinned legacy and concurrent journal tests. Merged into HSR `main@b81818331122cadc179dde7c71490a275b1b9c77`.

A stale pack is rejected from the active candidate if its source archive, build Manifest or final media changes. A completed human review checklist remains separate from this automated proof: **NO real user's Japanese WAV was heard, NO human listening decision was collected, and no acoustic Japanese-language acceptance can be asserted**. Keep lifecycle `validation-pending`; no Canonical updates.
