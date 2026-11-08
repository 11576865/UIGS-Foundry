# Test: Softmux V3.5 native BatchRunner emits real ASS Group union font and exact Default/Forced dispositions

Date: 2026-11-08
Status: **PASS — exact-HEAD V3 Chromium and independent output probe; full Browser E2E separately pending at write**
Product: `11576865/MKV-Fast-Muxer`; opt-in `?ui=v3&nav=full`, Draft [PR #269](https://github.com/11576865/MKV-Fast-Muxer/pull/269), still dependent on unmerged #267/#268.
Verified HEAD: `c52693da754803981b8f7ff997ff5b1b30ee096f`.
[V3 Pilot #42465477756](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42465477756) **SUCCESS**; [blank MKV #42465477752](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42465477752) **SUCCESS**.
Evidence artifact: [original exact-head #13610994170](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42465477756/artifacts/13610994170).
Related prior Bug (dedup checked): `inbox/bugs/2026-10-13-mkv-frozen-batch-plan-lost-font-identity.md` and `inbox/tests/2026-10-13-mkv-finished-ass-style-semantic-readback.md`.

## Why this is a distinct test

Previous SRT visual/mux tests proved one or two subtitle streams but did **not** independently read actual Matroska Default/Forced dispositions. Previous Group bug proof covered a missing font-identity regression in a single historical case; one UI-selected Group strategy is not proof the output actually contains a **shared reduced font covering the union of all jobs' ASS characters**. This test uses two independent finished outputs and compares their extracted font payloads, not UI button state or arbitrary screenshot counts.

## A. Default/Forced as a product byte invariant

`tests/e2e/v35-batch-multisubtitle-review.e2e.mjs` first imports two true MP4 Files and four SRTs. Two ambiguous SRTs require separate explicit mapping; Start remains blocked until *both* tie selectors are resolved. B's one native inspector contains two original File-and-index-bound subtitle editors. It independently updates the real title/language and native Default/Forced checkboxes (not a synthetic mock):
- English `eng` — `Default=false`, `Forced=true`;
- Chinese `zho` — `Default=true`, `Forced=false`.

After A/B task switching and one actual B-only BatchRunner execution, the independent `ffprobe -show_streams` output confirms **two SubRip streams with exactly these opposite dispositions** (not merely UI checked attributes). Real FFmpeg extracts both original distinct subtitle cues; product native report `audit.ok===true`; output report SHA matches actual downloaded bytes; all six source File hashes stay unchanged.

Final exact-head screenshot + JSON receipt `ui-v35-multisubtitle-review/multi-subtitle-review-evidence.json` has `passed:true`, with actual `subtitleStreams[].disposition` values. Resulting dual-track MKV SHA-256:
`354534656d2804331cba8c8ac054c2f4c31962ad472d069096e07ddbcd572888`.

## B. Actual ASS Group character-union subsetting

`tests/e2e/v35-batch-ass-group-union.e2e.mjs` creates **two independently identifiable short MP4 Files**, pairs each with a valid ASS using the system DejaVu Sans family, and inputs one real source font File. A ASS cue uniquely contains `Ω` (U+03A9); B ASS uniquely contains `Ж` (U+0416). Set native `#batchFontSubsetEnabled=true`, `#batchSubsetScope=group`. Production's existing frozen JobPlan/FontRecognition/Group reducer remains the only business owner; test doesn't simulate generated media.

The original BatchRunner actually produces **2 distinct MKVs, 2 original audited reports, 2 ASS streams**. Independent FFprobe identifies **one font attachment per MKV**; native FFmpeg extracts each attached font to a temporary test-only path; fontconfig `fc-query` parses each extracted font's cmap. BOTH fonts independently support BOTH `Ω` and `Ж`, not just their corresponding episode's character. The extracted font byte SHA-256 is **identical** for A and B:
`5ff036de7040cbf9245f09aa57c688b1884ff5c89cec0428df074fb7fa20f478`.

The sample's source font is **759,720 bytes**; both outputs embed the identical **7,856-byte** `DejaVuSans.subset.ttf` (~98.97% smaller for this specific fixture). Neither attachment matches the original source font hash; two distinct MKV outputs are individually SHA-audited:
- A: `5571581eb4c7527a77c98f578d5230594248b61dca12066e4423b182839cc089`;
- B: `9113a3fd10f8ed6c3d0275281fec8f2193282a3d6a55c37eb831bcebd8fb1fca`.

FFmpeg independently extracts each actual ASS event with its distinct cue text. Both source MP4/SRT sets and reference font SHA are unchanged. Terminal: **2 generated, 2 audited, 0 pending review, 0 failed**. `ui-v35-ass-group/group-ass-evidence.json` reports `passed:true`. Extracted fonts are deleted after assertions; no loose font bytes must be included in user evidence packages.

## Transferable test principle (candidate/case-bound)

A visible `Group` option and passing JS unit metadata do not establish self-contained output. Test the real **frozen resource identities**, actual output attachments, independent byte extraction and cryptographic equality, **glyph union across jobs**, and native mux audit per output. Test Default/Forced independently through finished-stream dispositions rather than UI attributes, and persist raw probe values in the machine-readable receipt. A shared-font Group subset is not equivalent to independent layout shaping or self-contained playback visual parity.

**Hard boundaries:** Fontconfig cmap checks only codepoint coverage and byte identity; no independent HarfBuzz GSUB/GPOS/shaping comparisons, font-face collection variants, adaptive ASS overrides, pix-to-pix libass, all players, tablet hardware, >1GB film performance, or full 55 Figma / 44 legacy feature signoff. This Test is not a Canonical change and is not approval to merge/activate a default UI.
