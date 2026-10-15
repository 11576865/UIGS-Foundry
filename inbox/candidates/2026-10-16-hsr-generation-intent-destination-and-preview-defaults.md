# Candidate: Separate parameter-save, internal publication and non-destructive external export

Date: 2026-10-16
Status: Candidate — source changes under review, exact-head CI/field validation pending
Source product: 11576865/HSR-Voice-Archive-Builder PR #186

## User-observed need

In one subtitle workbench, four very different actions had become conflated: saving a changed visual parameter, generating a true FFmpeg/libass *preview*, publishing new internal subtitles into an existing MKV, and exporting a standalone ASS to disk. The user specifically reported surprising automatic builds after parameter changes, and later required distinct actions **生成 ASS（内）** (replace the verified MKV's embedded subtitle track) and **生成 ASS（外）** (new standalone ASS, neither overwriting an old standalone file nor changing the MKV).

This is a durable intent/ownership boundary, not a change to the math of the ASS renderer. An asynchronous job reporting "ASS done" does not prove the requested *container* was updated; conversely, a parameter-save response must not imply that encoded outputs were regenerated.

## Implementation candidate in HSR

- Autosave persists only project parameters and refreshes cheap geometric UI preview. True libass video and final ASS/MKV generation are explicit actions; separate result and progress ownership.
- Internal ASS generation reaches success only after staged MKV subtitle content is extracted, checked against newly generated Style/Dialogue events, atomically published and provenance-certified.
- External ASS export creates `exports/HSR_Voice_Archive_NNNN.ass`, with no-overwrite exclusive publication and a per-project writer slot. No mutation of the user's existing ASS, subtitle receipts, SRT, manifest or MKV is authorized.
- Explicit default background intent: the first MKV uses the *same packaged studio-red-clouds.webp asset bytes* as Layout/Effects. Prior verified project choices (solid color, gradient, user image) remain authoritative. The same asset identity matters more than a visually similar replacement.
- User-authorable source/translation text colors are stored and rendered independently. Temporarily disabled non-Fade motion controls must also be disabled in rendering, not only visually hidden.
- Exact-head CI, real audio duration and rendered opacity timing, and Android/Termux media acceptance remain separate evidence states.

## Dedup review

- `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`: stale asynchronous preview vs saved draft; did not establish the new *internal-vs-external artifact ownership and no-overwrite* distinction.
- `inbox/observations/2026-10-13-hsr-mkv-track-refresh-vs-full-rebuild.md`: source-aware full container replacement vs specialized remux; complementary, not duplicated.
- `inbox/cases/2026-10-15-hsr-studio-red-clouds-browser-ci-acceptance.md`: browser static asset and interaction evidence, not default finished-MKV background authority.
- `inbox/candidates/2026-10-04-imported-resources-fresh-destination-identity.md`: broad destination identity principle; this records product-specific generated-artifact intent and UI trigger distinctions.

Candidate only; **no Canonical change** from one user report and one HSR implementation.
