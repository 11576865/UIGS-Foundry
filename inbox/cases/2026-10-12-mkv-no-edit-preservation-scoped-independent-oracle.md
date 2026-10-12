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
