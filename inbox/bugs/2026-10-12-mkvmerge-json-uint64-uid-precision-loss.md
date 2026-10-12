# Bug: JavaScript JSON.parse silently rounds MKVToolNix 64-bit Matroska UIDs

Date: 2026-10-12
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
