# Test · Portable external metadata checkpoint requires current byte rebind and revision-bound inverse

Status: **Test Candidate / Product PR Submitted / exact-head CI Pending**. Not Accepted, not Canonical.
Date: 2026-10-15
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/144
Exact submitted product head: `a305dde5486c068f689d45f340dfdd457e02c5b8`
Depends on PR #143 live one-document authority and parent #142 P0 protection.

## Prior knowledge and distinct gap

Foundry already records `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md`: same filename/size/mtime cannot substitute exact browser File reference for **current-session** metadata editing. `inbox/cases/2026-10-14-mkv-verified-source-delta-export-and-atomic-replay.md` covers source-MKV track/attachment replay based on full-source SHA. Those cases do not cover **multiple external audio/subtitle Files plus optional sidecar** across a session restart, with imported checkpoint JSON, explicit consent and revision-bound inverse.

## Submitted scoped regression gate

New `src/portable-external-project-recovery.js` exports only allowlisted per-external-track metadata, current `File` full SHA-256 and optional subtitle sidecar full SHA-256. JSON neither carries browser File grants, writer rights nor outputs. Imported JSON is untrusted, rigidly parsed and inert. Preparing recovery checks each current File name/size, full bytes digest, exact live `File`/sidecar/format/identity references after every await, the unified immutable ContainerProject identity and revision. Mismatched content, changed File inventory, concurrent edits and malformed schema refuse.

A **separate checkbox + Apply click** dispatches the whole recovered external metadata delta through the actual unified transaction. Undo is valid only against the exact Project object revision resulting from this apply; later edits or File changes invalidate it. This is not a generalized persistent Undo journal.

### Required tests

- Node `tests/portable-external-project-recovery.test.mjs`: successful export/parse/prepare/apply/inverse, altered File byte and sidecar byte, same-looking new File, malicious grant key, unknown field, hash-time field mutation, stale plan, no implicit consent.
- Chromium `scenarioExternalCheckpointRecoveryRealMux`: MP4 + FLAC, export/download JSON, change title, inert import, SHA verify, checkbox approval, apply, undo, second prepare/approve/apply, **real finished MKV**, native independent `ffprobe` reads recovered external audio title.
- PR #143's mixed source/external actual MKV scenario and all legacy P0/Batch/P3 regressions must remain green.

**None of these new exact-head CI or native output verdicts is yet confirmed**. This entry is a pending Test, not proof.

## Dedup / limits

Searched `SHA-256 sidecar recovery explicit consent undo`, `external metadata checkpoint`, `rebind exact File digest user confirmation`, `portable project multi source recovery`. Related exact File identity and source-MKV SHA cases are not duplicate of the **external sidecar + cross-session metadata + consent + CAS undo** test class.

Outside scope: source and external changes combined into one all-or-nothing portable replay; font File regrant; serialized browser handles; durable undo after page refresh; new Chapter/Tag writer. No Canonical promotion.

## 2026-10-25 S09: single portable carrier without combined authority (Pending CI)

Product [PR #202](https://github.com/11576865/MKV-Fast-Muxer/pull/202), head at intake `cc7f1a7dacaf9628d07811af76ace61b0ddb5a37`, adds one `softmux-workspace-recovery-bundle-v1` JSON containing an inert detached source-track/attachment draft and an optional inert external-audio/subtitle/sidecar checkpoint. This addresses the real user burden of separately exporting/importing two checkpoint files for a single workbench session. The bundle delegates parsing of each nested component to its **existing strict standalone parser**, rejecting unknown top-level keys, invalid nested schema, forged SHA/metadata, over-budget content and malformed JSON. Only after BOTH validate does the UI replace either pending-review draft.

**Crucial limit:** A single delivery package is not a single authority or transaction. The actual source File and external File/sidecar objects must be freshly granted after refresh, verified against the nested full-byte hashes, reviewed and explicitly applied **separately** using the pre-existing recovery paths. Neither bundle import nor complete nested parser validation changes the executable mux plan, applies edits, restores fonts, grants writer permission or simulates atomic rollback.

Node regressions cover valid dual packaging, optional external content, malicious unknown fields, false nested SHA, malformed nested content, size and JSON rejection. A real Chromium mixed source+ASS+font workbench scenario exports the bundle, imports it and asserts both scopes remain awaiting independent consent and cannot alter the actual plan; invalid nested external metadata rejects the whole import and retains the prior staged checkpoints. **Exact-head Node/build/Chromium CI is pending at this intake, not accepted evidence.**

**Deduplication:** This extends this existing Test because it composes the same already-recorded external checkpoint with the existing source verified-delta restore; it does not assert or introduce a universal `multi-domain atomically restorable project` rule. No Canonical promotion.

**2026-10-25 S09 identity/UI correction:** Product head `32dabe2dab2a984b436c37ebfb1713e1ce3b02a6` avoids clearing existing *applied* source/external undo receipts when merely importing another inert bundle. Existing revision/source guards continue to control eligibility. Latest exact-head CI pending. Foundry Validate was already red on dozens of unrelated historical Bug records lacking required Lifecycle metadata, so this Test proposal must remain Pending rather than being mislabeled accepted or altering Canonical.\n
## 2026-10-25 S09 browser acceptance blocker and remediation under review

Product PR #202 exact head `96996afc4a073777bce0c7a92158141c4b62fc6b`: Node tests and Pages/S12 scoped CI passed, but full Chromium E2E failed at the new real-workbench combined-export action because no download was emitted. Diagnostic exact-head `901d7df581e1c00a230bf5fc869bed0cb19528f5` confirmed the output's real MKV mux had already succeeded, yet a click produced neither a download nor a changed bundle-status line. A possible busy/preflight guard prevented a visible result; the evidence does **not** by itself identify which guard fired. Product follow-up `ceb20ffa37862b03c15b131d796835cd79a4caac` moves potentially failing plan evaluation inside an error-reporting boundary, surfaces busy rejections to the user, disables bundle export while the source is unready or other workbench tasks are active, and declares the busy flag before shared UI rendering.

**New regression concern:** A newly added UI control may be enabled while its handler has silent early returns, making a real user click look inert and causing the browser download evidence to time out. Keep user-visible disabled readiness synchronized with execution guards; retain an explicit status for genuinely rejected actions. Verify under the **full actual media workflow**, not just Node parser tests. The latest product head's browser CI is **pending at this record update**, so the candidate remains Pending and no canonical principle is promoted.

The Foundry's own validation remains red on unrelated existing Bug intake records missing valid `Lifecycle` fields; no attempt was made to bypass the validator.

### Root-cause correction: closed recovery disclosure, not a worker or disabled-button error

Product CI head `3c9338d9e6b8b43fb97630f59b2b7ae3970215e3` added a real Playwright trace on the new export button: `pointerdown=0`, `click=0`, while the button's `disabled=false`, source mux status was successful and the element remained connected. Source inspection confirmed existing modern workbench `src/softmux-10.14-workbench.js` moves `.composition-header-tools` into `<details id="sf14Recovery">` **closed by default**. The browser test had attempted to click the hidden disclosure content without opening the visible summary; the export handler had never been invoked. This is a **test interaction-path/visibility mistake**, not confirmed source File corruption, failed SHA, or bad bundler JS.

Product follow-up head `207d088817aaf4ffc7de9bde36aa4513478f60c4` corrects the full browser scenario to **open the user-visible recovery disclosure before clicking**; the modern UI also relocates bundle status inside the disclosure and automatically opens it after a combined file is selected, with copy explicitly preserving separate recovery authority. The early-return state feedback and disabled readiness checks remain useful safeguards but must not be mislabeled the sole proven root cause. **Exact-head full Chromium result is pending**, so the regression remains Test/Pending, not accepted.

Transferable test oracle: for current production UIs that rehost controls inside progressive disclosures, asserting a DOM ID exists or `isDisabled() === false` is insufficient evidence that the control is reachable by an actual user interaction; the test must navigate the visible disclosure first, then verify `isVisible()` and execution effects.
