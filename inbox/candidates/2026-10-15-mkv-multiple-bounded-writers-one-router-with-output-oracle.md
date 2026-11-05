# Candidate / Test · One bounded writer selector must preserve each backend authority and re-audit its completed artifact

Date: 2026-10-15
Status: **Candidate — submitted product head, main-targeted integration CI queued, not Accepted/Canonical**
Product: [MKV-Fast-Muxer PR #145](https://github.com/11576865/MKV-Fast-Muxer/pull/145)
Exact product head: `075679bb2d1cea180ce0892d48afd4fd6ec76ef0`
Full R1–R4 exact-tree CI: [PR #146, base=main](https://github.com/11576865/MKV-Fast-Muxer/pull/146), initially queued workflow runs 38605101216 (Browser E2E) / 38605101157 (Pages). Status must be verified later; no CI success claimed here.

## Distinct reusable finding

Four existing Matroska attachment FileData writers had non-overlapping/partly overlapping structural envelopes: same-length unchanged offsets; enlarged adjacent Void; tail Attachments size updates; and nonterminal indexed Attachments moved via chained SeekHead with separately verified inner/outer CRC. Each had standalone source guards, but the product forced users to choose a technical writer themselves.

**A unified chooser must not become a larger write authority.** It should (1) inspect one current real FileUID/TagTarget graph and requested byte delta, (2) select only from backend-specific accepted plans, (3) refuse on unsupported/invalid metadata and never fall back to an unrestricted remux, (4) keep source bytes and File grants only in one-session opaque references, and (5) re-audit the finished Blob via a separate common source/output oracle. This creates a real usable operation without claiming support for arbitrary EBML, Cues or Chapters writes.

## Product implementation submitted, not verified

- `src/p2-existing-mkv-writer-router.js` routes existing backend prepare/execute functions without replacing their actual EBML algorithms or CRC proofs. Dispatch is based on equal-length or variable-length request and bounded eligibility; all rejected routes are reported as typed refusals.
- The common output pass repeats actual UID, attachment content SHA-256, original source SHA-256, TagTarget relationship and untouched non-SeekHead top-level byte/offset tests after the selected backend's own local geometry checks.
- `src/p2-existing-mkv-writer-router-ui.js` and actual `index.html` provide one opt-in source/actual FileUID/replacement/explicit review/new-copy download path.
- `tests/p2-existing-mkv-writer-router.test.mjs` constructs four positive differently shaped EBML source fixtures, plus referenced UID, unknown element, broken SeekHead, unreviewed and forged/reused plan negatives.
- Complete Chromium `scenarioRoutedExistingMkvNativeOutput` must independently use MKVToolNix-authored original, real UI download, mkvmerge/mkvextract comparison of two FileUIDs, Chapters, Tags, and exact extracted attachment bytes.

These tests are submitted but **no successful exact-head verdict was available** at this intake. Generic format/playback interoperability and source file overwrite are unproven/unallowed; old specific UI paths remain until functional parity and UX review.

## Dedup and related knowledge

Searched `multiple bounded writers one capability router`, `candidate writer selection independent output audit`, `attachment writer route fallback`, `route separate writer safety authority`, `SeekHead routing safe writer selection`. Existing scoped writer Cases `inbox/cases/2026-10-14-mkv-existing-attachment-same-size-filedata-preservation.md`, `inbox/cases/2026-10-14-mkv-variable-filedata-adjacent-void-without-offset-movement.md`, `inbox/cases/2026-10-14-mkv-nonterminal-attachments-native-seekhead-relay.md`, and `inbox/cases/2026-10-14-ebml-crc32-nested-attachedfile-attachments-writer.md` cover individual writer safety, not **selection across disjoint writer envelopes plus completed-artifact common audit**.

The main-targeted CI gate is an independent process issue previously addressed by `inbox/observations/2026-10-04-collapse-stacked-pr-chain-by-retargeting-top.md`; no duplicate Canonical claim is made. The new temporary PR #146 preserves the exact top-of-stack head with base main, without silently merging or closing layered review PRs.

Do not promote this new Candidate to Canonical from one source observation or green CI alone.


## 2026-11-05: S06/S07 actual reviewed-editor native evidence packaging (Pending exact-head CI)

**Dedup Intake:** This existing Candidate covers independently scoped bounded Matroska writers and the post-output oracle. The product has a real reviewed user-facing routed `FileData` replacement editor (S06) *and* a separate reviewed, equal UTF-8 byte-length `ChapString/TagString` editor (S07). Both have existing Chromium tests checking real MKVToolNix-sourced media; nevertheless their **source+actual output+native XML+bytes** were not packaged as dedicated independent acceptance artifacts. No new Writer, authority, Canonical rule or undocumented feature is implied.

**Product work submitted:** [Draft PR #248](https://github.com/11576865/MKV-Fast-Muxer/pull/248), exact head `0455d0cb0b807126ce5fe52f6ebe6095a43a0aba`. Changes only existing `tests/e2e/browser-mux.e2e.mjs` plus existing `.github/workflows/browser-e2e.yml`.
- S06: Existing public reviewed editor replaces an **unreferenced decoy** original FileData in a real two-attachment MKV with an AttachmentUID-targeted Tag for the *other* attachment. New checks compare extracted referenced original FileData source/output exact bytes; archive source MKV, output MKV, original+output attachment bytes, original+output Chapters/Tags XML and bound UID/whole-file/attachment SHA-256 receipt.
- S07: Existing public editor opens a real independently authored audio-only MKA with nested `ChapterUID=510011` targeted by a Tag; a deliberately unequal UTF-8 byte-length edit must produce a browser `blocked` status with disabled save; then approved equal-length `TagString` and nested `ChapString` edits produce intermediate/final MKV. Existing strict native `mkvmerge -J` tracks, `ffprobe` packet bytes/PTS/DTS, extracted XML and unchanged input SHA are retained. Archive original MKA, intermediate and final MKVs, original/final XML and JSON receipt.
- The preexisting external native S06 `mkvpropedit` same-input/ref-UID comparisons and S07 full XML/UID oracle remain separate tests, not falsely described as the result of these user actions.

**Status:** exact-head Browser E2E run [#42015997951](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42015997951) was **in progress** at intake (syntax, units, build green), Pages [#42015998033](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42015998033) SUCCESS. **Pending CI and direct downloaded-archive inspection**. No product release `S06/S07 PASS` or frozen 1.0 candidate until exact scope verified; do not revise the owner approval state or promote Canonical. Evidence gaps should be distinguished from absent capability; never replace the independent oracle with a writer's own success report.


## 2026-11-05: S06/S07 exact 64-bit UID evidence correction

The initial PR #248 `0455d0cb` test retained an inherited `JSON.parse` call for `mkvmerge -J`, which can round `TrackUID/FileUID` values above `2^53−1`. A later test-only correction **`c421a9bb8f16261b7131c6380f38eadea5aefbad`** reuses the already-tested `parseMkvmergeJsonWithExactUids` helper to preserve UID decimal literals as strings before comparison and before receipt creation. Current **exact-head Browser E2E #42016372295 Pending** as of intake, Pages #42016372113 SUCCESS. Superseded #42015997951 is not sufficient to accept the updated UID assertions even if it later passes. This is a test-oracle precision issue; no production code or inferred previous binary corruption. Pending CI/actual ZIP review remains open, no Canonical change.
