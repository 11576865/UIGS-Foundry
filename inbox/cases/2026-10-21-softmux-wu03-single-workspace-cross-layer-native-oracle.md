# Case: one browser workspace delivery requires independently joined UI, container, payload and save-state evidence

Date: 2026-10-21  
Status: **Case / scoped implementation verified; not Canonical and not full product 1.0**  
Project: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)  
Merged work: [PR #165](https://github.com/11576865/MKV-Fast-Muxer/pull/165), `main@8a16d1473dc167a56b51ef581889bf3300d67bee`  
Exact PR-head: `2173b16b966d03628d85009fdbaa367c2c48706c`  
CI: [Browser/native E2E #39461812972](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39461812972)  
Artifact: `wu03-fa-modern-workspace-actual-mkv-native-evidence`, ID `12282354353` (actual MKV + product report + independent JSON); artifacts have finite retention.

## Trigger and scope

The approved Softmux 1.0 plan B PDF identifies WU-03 as **a real single-project longitudinal task** (user UI → source/domain authority → execution → actual MKV → independent output → truthful save). Earlier individual browser tests verified attachment edits, source stream edits, font payloads and ASS audits separately, but could still allow an under-covered combined task if the test only trusted FFmpeg exit code, names in a report or an object inspector.

The merged WU-03 test extends the existing **public modern workbench** scenario rather than creating a second test-only writer/state owner:
- Import an actual MKV carrying chapters, global metadata, and two attachments plus an external ASS and DejaVu TTF, in the same authorized source inventory;
- Through the real source-container tree, exclude one original attachment, retain/rename the other and change its MIME; update new subtitle title/language; actually mux and download output MKV + report;
- Independent `mkvmerge -J` source+target reader checks the output inventory and exclusion; `mkvextract attachments` re-opens both source and produced MKV and validates the renamed `notes.txt` `FileData` SHA-256 is unchanged, and the newly attached external DejaVu font has exactly the original file bytes;
- Independent native `ffmpeg -c copy -f hash -hash SHA256` compares **compressed video and audio packet payload streams** between source and final MKV; source MKV entire-file SHA remains unchanged, and downloaded report's output SHA binds the actual downloaded MKV;
- Existing in-app independent ASS/attachment audits and the real source-object inspector must still pass. `download.saveAs()` proves runner file persistence, **not** browser app knowledge of user-side durable-save receipt; `savedToDiskVerified=false` remains truthful.
- Machine-readable `.e2e/output/wu03-fa-single-workspace-independent-evidence.json` is CI artifact; this is a **2-second, scoped, simple chapter/tag fixture**, not a feature-film load test.

## Exact observed result and validation

Exact PR head `2173b16` [#39461812972](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39461812972) passed **632/632 Node**, build, separate **20 actual browser jobs** S10, and full Chromium/native E2E. Log contains: `WU-03 F-A single public source + ASS/font + attachment edit + native packet/bytes/hash PASS`, `Scenario 2 PASS`, and `All browser E2E scenarios PASS`. The proof artifact was independently seen in the Actions artifact listing with size 574001 bytes and not expired at intake. Merged `main@8a16d147` through PR #165; exact main CI was awaiting invocation at entry creation, so the PR-head CI evidence is the claim.

## Reusable gate

A single-project feature acceptance needs one **joined provenance chain**: authoritative scanned source File identity and preserved input hash; actual user editing intent; executable plan; actual output bytes; independent stream/payload/original-attachment checks; product report hash parity; and precise differentiation between **generated**, **verified**, **download initiated**, and **durably saved**. Separate component tests can each be green without establishing that combined chain.

Prefer augmenting a proven real UI fixture to spawning a parallel writer, mock or duplicate global state. Per-element audit receipts can only establish their scoped integrity (FileData/name/inventory); they do not prove arbitrary EBML UID/TagTargets linkage or general remux structural equivalence.

## Deduplication and limits

Foundry search identified `inbox/tests/2026-10-16-softmux-attachment-finished-proof-receipt-consistency.md` (malformed receipt and live UI evidence), `inbox/observations/2026-10-16-softmux-source-attachment-result-identity-freshness.md` (evidence freshness), and `inbox/cases/2026-10-20-softmux-20-real-browser-batch-execution-and-independent-output-proofs.md` (per-Job 20 outputs) as adjacent but not duplicate. This Case uniquely checks **one simultaneous mixed-object modern workspace operation**, output stream-copy packet hashes, external native FileData and save-status separation.

Still pending for overall WU-03 / release: more varied F-A multi-track inputs, #77 F-B cross-path denial/structural proof, F-C layout variants, precise device and >=1 GB stable mux/save results, and other S01–S14 MUST cases. No Canonical promotion from this one scoped Case.
