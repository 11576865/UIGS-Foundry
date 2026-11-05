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


## 2026-11-05: S06/S07 exact-head native browser proof closed and merged

**Deduplicated closure of the two Pending CI updates in this existing bounded-writer Candidate.** Exact product test HEAD `c421a9bb8f16261b7131c6380f38eadea5aefbad` passed [Full Browser E2E #42016372295](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42016372295) **completed SUCCESS** including syntax/Node/build, real Chromium, no failed steps and all actual artifact uploads, plus Pages #42016372113 SUCCESS. [PR #248](https://github.com/11576865/MKV-Fast-Muxer/pull/248) was squash-merged to `main@d1edba6cbb66f211bf27e0eb3b3795a7934e495c`. The superseded earlier test run #42015997951 was cancelled and is **not** cited as success.

**Independent external evidence examined, not merely browser receipts:**
- S06 actual `s06-existing-mkv-routed-writer-browser-native` Artifact ID `13410535909` includes original MKV **190620 B**, SHA `4a64079f64a746257b0c9b98210d0ae49d6a3e0f0b9aa461bc9bf3f3b489fd33`, delivered MKV **190620 B**, SHA `97eb6d560e9e8aef4416fdae442bb8b8cf1b2acc0121a9adb9e16aa6fc44d13d`, both sides' unchanged referenced attachment FileData SHA `fa7b57ddeea09e347209cca4c51ebb77b9eca97117e1d4fea3126802dee7cc30`, changed decoy FileData SHA `747ea3cd4acc3fb141d85877000abfbbcea68e55340de8a274906fa9b9672a04`, source/output exact equal native Chapters/Tags XML. Local second-pass `ffprobe` validates identical MPEG4/AAC packet hash/PTS/DTS/duration; source/output true 64-bit UIDs are decimal text, never JS precision-rounded.
- S07 actual `s07-chapter-tag-existing-mka-browser-native` Artifact ID `13410605705` contains original audio-only MKA, intermediate and final MKV each **40404 B**. Source SHA `d3a733190548ff4e42ab4c0e72354983af91e7c108a85bf69c781561bc7a3742`, final SHA `d2a511092bc68cf28ed60b0c896b15f8785ad0d6bcdc39e00869807cda5fe36b`. Direct whole-file binary comparison proves `source`→`intermediate` differs **only** in reviewed `TagString`, and `intermediate`→`final` differs **only** in reviewed nested `ChapString`, exactly the approved equal-length UTF-8 bytes. Independent extracted XML changed only those strings; `ChapterUID=510011` remained linked, local `ffprobe` FLAC packet bytes/PTS/DTS/duration untouched. Real Chromium unequal-length edit rejected before any save.
- The second-pass verification receipt `softmux_s06_s07_independent_reread.json` was locally generated from these ZIP input/output artifacts rather than trusting product internal self-report.

**Product release ledger corrected without authority promotion:** docs-only [PR #249](https://github.com/11576865/MKV-Fast-Muxer/pull/249) merged to **`main@6a34061b3771b02e4dbb249587ef352e0695cbbd`** (live main ref and JSON reread verified). S06 and S07 are recorded as `implementationEvidence.scopedAcceptanceEvidence.state=SCOPED_PASS_NOT_1_0_ACCEPTANCE`; all 14 formal scenario statuses/evidence and owner approval remain unchanged, formal S06/S07 `UNASSESSED`, contract `PENDING_OWNER_REVIEW`, release candidate null. No new EBML writer, widened range/CRC/UID grant, product UI changes, Canonical promotion or inferred device/player support.

**Intake state:** The scope-specific proof and CI Pending is now **Closed: scoped PASS / merged**. Broader bounded writer parity and end-user 1.0 release acceptance remain explicit independent tasks; do not re-open these exact scenarios without new contradictory evidence.
