# Case: Matroska no-edit browser remux requires scoped independent preservation evidence

Date: 2026-10-12
Status: Case / test and code submitted on Draft PR, full CI pending
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/76
Branch: `test/p0-preservation-baseline-20261012`
Initial baseline: `main@7781a4f410a9c6edb9a1f3d056091e6ace333cc4`
Related:
- `inbox/candidates/2026-10-03-preserve-all-must-cover-full-source-domain.md`
- `inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md`
- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md`
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`

## Context / why this case is new

An unchanged input MKV can be re-muxed by browser FFmpeg Wasm into a playable MKV while dropping metadata, attachments, chapters or relationships not inspected by the tool itself. A “no-op remux” is not bytewise no-op. Before general-purpose editing, implement a *negative-preservation oracle* which can falsify an unsupported preserve-all claim.

Draft PR #76 adds `scripts/p0-compare-roundtrip.mjs` and `tests/p0-preservation-audit.test.mjs`, plus a browser real-output E2E scenario against the existing font+note+chapter test MKV. The oracle uses independent `mkvmerge -J` / `mkvextract` to enumerate and extract attachments then hashes their *actual bytes*, and `ffprobe` to compare media types/codecs, applicable flags and titles/languages, chapter start/end/titles and selected global metadata. Failing differences yield a nonzero exit and a machine-readable JSON artifact. Tool failures are reported as CHECK_UNAVAILABLE, not success.

**Explicit coverage limit:** passing checked fields does not mean all EBML is retained. The current fixture itself was generated with FFmpeg and does not stress independent muxers, unknown EBML elements, nested Chapter/Tag targets, UID references, CodecPrivate, packet timestamp identity, playback rendering or player compatibility. Those remain separate P0 tasks. Do not merge or claim full preservation merely because this scoped fixture is green.

## Execution observation (at intake)

At earlier PR head `8cec099537d4d70769274e76f6b7ed23c0cc807c`, both Pages and browser workflows reached Unit tests and failed the same preexisting source-shape assertion in `tests/composition-workspace.test.mjs`: it expected only `roles.needsSourceChoice || roles.unknown.length` while current production `src/main.js` additionally preserves an actively focused source radio using `|| focusedSourceRadio`. The production code was not modified by P0. PR head `7291eb587a309c62a0a82407251a34c45fd24d13` updates the stale regex to match the additional focus-preservation behavior. Pages workflow for that head has passed; Chromium Browser E2E is **in progress** at intake. This is not evidence that the new browser remux oracle has executed successfully yet.

## Proposed cross-project takeaway (Candidate-level only)

A roundtrip test must:
- use the *actual production writer/executor*, not an unrelated CLI simulation, for the system under test;
- independently re-read the resulting artifact;
- compare safety-relevant object facts and extracted payload digests;
- provide explicit `notChecked` coverage and avoid equating scoped success with full preservation;
- keep tool-unavailable and semantic-difference states separate from pass;
- preserve a failing fixture and machine-readable output so a failure changes capability claims instead of being explained away.

This case records a concrete local engineering experiment and pending checks. It is not a generalized UIGS Canonical standard.


## Continued P0 execution: basic green, independent hard corpus in CI

Verified from workflow logs at commit `7291eb587a309c62a0a82407251a34c45fd24d13` (run `38192821478`): Node tests 220/220; existing Browser E2E PASS; `P0 preservation comparison: CHECKED_FIELDS_MATCH` for the FFmpeg-authored unedited input with 2 attachments/chapters. Thus **scoped basic preservation was actually verified** but not all Matroska semantics.

Draft PR #76 now also adds:
- `tests/e2e/generate-independent-matroska-fixture.sh`, independently authoring nested Chapters and a generic attachment with mkvmerge;
- `mkvpropedit --tags all:<file>` injecting an explicit custom `ChapterUID` target, followed by independent extraction and self-checks;
- `scripts/p0-summarize-ebml-xml.py` and `scripts/p0-compare-roundtrip.mjs --deep` to compare hierarchical chapters and scoped `P0_*` tag targets;
- additional isolated unit tests and a real Chromium output test writing `p0-independent-audit.json`.

**Fixture-design observation:** authoritative MKVToolNix docs state that `mkvmerge --global-tags` deliberately removes `Targets` (therefore is not a suitable way to author a chapter-targeted test). Modern `mkvextract` syntax uses explicit XML output paths for chapters/tags. A self-check must independently verify that the fixture actually contains the intended hard structure before any application roundtrip; otherwise a green or red result could be about the fixture generator rather than the product.

At this update, newer E2E `38194692640` is running after correction of an invalid XML test string. Do not misread the older green result as proving this independent corpus passes. All design knowledge stays Case/Candidate, not Canonical.

References: https://mkvtoolnix.download/doc/mkvmerge.html and https://mkvtoolnix.download/doc/mkvextract.html and https://mkvtoolnix.download/doc/mkvpropedit.html


## Positive control: TrackUID-targeted tag semantic preservation (2026-10-12)

Product PR #83: https://github.com/11576865/MKV-Fast-Muxer/pull/83
Browser CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38202212178
Merged test-only commit: `096d3a52b3e828175e9430b2ac41761765335ba3`

An independent MKVToolNix fixture with **flat** chapters and one genuine `P0_TRACK_RELATION` custom Tag targeting the actual video `TrackUID` was authored using the UID read via `mkvmerge -J` with Python 64-bit integer safety, and self-checked by `mkvextract`. The actual browser FFmpeg/Wasm no-requested-edit mux path displays its ordinary `UNVERIFIED_REFERENCES` warning and generates output.

`scripts/p0-audit-track-tag-relations.py` resolves the source and output `TagTrackUID` references to a **logical track identity** (type, codec, ordinal), rather than comparing raw UID numbers, which are legitimately reassignable by container writers. It also rejects a missing Tag and an unresolved/dangling target. At source PR head `c75a68a0b7a614436ec06164f4fa8fec397f3b35`, **228/228 Node tests**, full Chromium E2E PASS and `P0 track-tag semantic relation: CHECKED_RELATIONS_MATCH`; machine-readable `p0-trackuid-target-relation-audit` artifact uploaded.

Interpretation: one **positive control** for correctly linked user-defined TrackUID metadata in a simple independent Matroska source. It does **not** support a blanket TrackUID guarantee, nor negate verified nested ChapterUID-target loss from #77/#76. It supports separating confirmed harmful structures from common-but-not-generally-verified metadata instead of globally forbidding all UID targets. Generalizable methodological insight: independent roundtrip oracles should test **referential semantics** and logical target resolution, rather than false failures from mutable surrogate IDs.

This supplements an existing Case, avoids duplicate Candidate creation, and does not update UIGS Canonical.
