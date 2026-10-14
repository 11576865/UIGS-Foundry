# Bug: JavaScript JSON.parse silently rounds MKVToolNix 64-bit Matroska UIDs

Date: 2026-10-12
Lifecycle: validation-pending
State: **reproduced in independent GitHub CI, fix submitted, exact-head recheck Pending**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/97
Failing head: `164f712068fb82bebd2d3a1fed0477722bc398a0`
Failing non-gating research oracle: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38261195120
Independent JSON artifact: `p2-existing-attachment-edit-fail-closed`, ID `11752461996`

## Reproduction

The independently MKVToolNix-authored `p0-independent-attachmenttag.mkv` source has a target-specific TagAttachmentUID and a decoy attachment, independently enumerated by `mkvmerge -J`. Its `properties.uid` fields are unsigned 64-bit values. `JSON.parse` reads numeric UID literals as IEEE-754 double-precision `Number`, losing integer precision when the value exceeds `Number.MAX_SAFE_INTEGER`. The external-fixture audit compared rounded `String(number)` to the project's exact `BigInt`-derived raw-EBML UID string, yielding `MODEL_SOURCE_UID_MISMATCH`. Report contained rounded display values such as `8607425577185101000` and `2465833630312329700` despite both UIDs being valid and distinct. Overall Node **306/306**, Vite and Chromium E2E passed; CI stayed green because the independent source audit is deliberately non-gating, but the machine oracle reported `INCONCLUSIVE_OR_FAILED`. That red oracle must not be misrepresented as verified.

## Submitted repair and targeted tests

Product adds `parseMkvmergeJsonWithExactUids(raw)`: before JSON.parse, quote raw object fields named `uid` containing unsigned decimal integer JSON literals so that the parser preserves full digits as strings. `exactPositiveUid()` checks string-decimal and `uint64` range, rejecting rounded Number representations entirely. `tests/mkvmerge-exact-uid-json.test.mjs` covers 64-bit values, max uint64, already-quoted UID, non-UID number preservation, invalid inputs. External audit switches to exact-string extraction and prints its own error. New head `7ae0b8895d3bac7e4324708ed22d2a112c98576e` is **awaiting full CI and real independent UID-tag fixture re-verification**.

## Reusable learning and scope

When comparing identity or reference UIDs exported in JSON as potentially >53-bit integer literals, preserve raw digits **before numeric parsing**, then use exact string / `BigInt` identity checks. Exact extraction must be tested against an independently authored real high-UID artifact, not just small-number unit tests. A generic JSON parser's success is not evidence that numeric identity survived accurately.

This is a Bug-level observation, **not** a change to UIGS Canonical. It does not establish any existing-MKV writer or UID reference rewrite safety.

## Exact-head source-oracle revalidation — verified resolved for this script

PR [#97](https://github.com/11576865/MKV-Fast-Muxer/pull/97) was re-run at head `7ae0b8895d3bac7e4324708ed22d2a112c98576e` in [workflow 38262067561](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38262067561). Node **310/310**, Vite and full Chromium E2E passed. Crucially, the previously red independent research audit logged `UID_TAGGED_EXISTING_ATTACHMENT_EDIT_BLOCKED_SOURCE_UNCHANGED`, `error:null`, with both removal and replacement correctly blocked by `SOURCE_UID_RELATIONS_UNVERIFIED`. The repaired exact-decimal UID parsing and regression tests therefore resolve **this specific 64-bit JSON identity precision failure**. Product PR #97 merged `main@b58e5f4101245dc1da567e6d48b5ba1f45ade679`. This does **not** prove arbitrary third-party JSON schema field UIDs safe; continue to preserve exact source numbers before parsing in all such adapters. No Canonical promotion.

## PR #140 recurrence in native source fixture authoring — verified 2026-10-14

This **same historical Bug** recurred during a different engineering feature: a new browser test authored a genuine three-attachment source with one `TagAttachmentUID` intended for the first original FileUID, but obtained that UID via plain `JSON.parse(mkvmerge -J)`. The first full Chromium workflow [38575500069](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38575500069) failed with the UI not disabling the purportedly tagged UID (first there was also an incorrect `TargetTypeValue`, corrected to 20). The next [38576340090](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38576340090) still failed: independent `mkvextract tags` exported an `AttachmentUID` element, but its rounded decimal integer **did not match the actual uint64 FileUID from EBML**, and the source-bound reader properly classified the real attachment as unreferenced.

The final browser scenario **reused the already implemented** `parseMkvmergeJsonWithExactUids` and `exactPositiveUid`, and asserted the exact full decimal UID in native extracted tag XML before starting the UI. Exact-head [CI #38577634115](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38577634115) passed **549/549 Node, Vite, full Chromium and independently native three-attachment output acceptance**; feature [PR #140](https://github.com/11576865/MKV-Fast-Muxer/pull/140) merged at [010e29f](https://github.com/11576865/MKV-Fast-Muxer/commit/010e29f22679ff3e09f91aaca6068a38dff9da10).

**Scope of the reusable defect:** exact UID handling must propagate into *test fixture authoring* and external tools, not only product source scanners and comparison oracles. An XML `AttachmentUID` element existing is inadequate evidence of a **valid target relationship**; verify its **exact numeric identity**. This is the same precision-loss Bug and has been deduplicated here, without Canonical promotion.
