# Test — completed mixed-mux codec packet byte accounting must not label residual as pure container overhead

Date: 2026-10-14
Source product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `9a503bfc437619822f3a80d8d4418771fb34d73a`
Requirement: QHE B16 partial. Full B01–B25 / A01–A10 release matrix remains open.
State: code submitted, isolated behavior/wiring checks passed; exact-head hosted Windows, full Node and browser acceptance **in progress / Pending**, not PASS.

## New test boundary and dedup

Prior Foundry `inbox/tests/2026-10-14-qhe-b16-flac-quality-mode-completed-packet-audit-and-explicit-all-stream-mapping.md` covers actual final FLAC audio packet observation and explicit subtitle/attachment source/output mapping. This new Test is distinct: **the verified finished container's byte accounting must include video + audio + subtitle codec packet payloads and the unassigned residual**, with current job/FILETIME identity and fail-closed unsigned safe-integer behavior.

Do not treat `artifactBytes − measured videoPacketBytes − measured audioPacketBytes − measured subtitlePacketBytes` as a pure `muxOverheadBytes`: residual can include attachment files, chapter/data payload, index, codec extradata, metadata, headers, padding and non-A/V/subtitle streams. Reusing that number to predict a future container or waive FLAC unknown cost would be unsupported.

## Test obligations

1. Windows short completed-mux Native path scans FFprobe `-select_streams v`, `a`, `s` independently within a bounded timeout. Long output / >512 MiB uses the existing isolated FFprobe worker for all three classes. Streams must retain output ordinal ordering; missing packet cost returns unavailable, never zero.
2. Worker receipt includes `videoPacketBytes` alongside audio/subtitle arrays, plus original real staged file `sourceLength` / `sourceWriteTicks`. Native attaches its own `artifactJobId`, `artifactBytes`, losslessly serialized `artifactWriteTicks`, and invalidates reused output receipts if the artifact changes.
3. `src/completed-mux-byte-ledger.js` requires verified completed task, exact job ID and artifact bytes, valid Windows tick text, actual output-plan track cardinalities, nonnegative safe-integer sizes, and total codec bytes no larger than actual container bytes. It computes actual video/audio/subtitle totals and `otherAndMuxBytes`; no forecast or strict budget authority (`canPredictFutureBytes:false`, `canAuthorizeStrictBudget:false`).
4. Shared media task JSON report and visible UI include the four classes after short output and following a long asynchronous completed artifact audit; labels communicate the residual's non-equivalence to pure mux overhead.
5. Independent Windows FFprobe oracles remeasure video packets on Native short and real **182-second async** output, and on a distinct actual **1 video + 2 FLAC audio + 1 softsubtitle** Matroska. Packet sums cannot exceed actual total file bytes. No API may accept a success certificate by extrapolating a source duration or previous movie.

## Evidence so far

- `windows/trim-packet-audit.ps1`, `windows/native-bridge.ps1`, `src/completed-mux-byte-ledger.js`, `src/media-planning.js`, `src/media-workspace.js`, `src/completed-mux-byte-ledger.test.mjs`.
- Windows real tests extended in `scripts/check-flac-native-http-lifecycle.ps1`, `scripts/check-b16-long-async-output-identity.ps1`, `scripts/check-flac-encode-preflight.ps1`; Draft-fast/full front-end Node and Windows B16 focused runtime workflows wired.
- Eight isolated actual JavaScript behavior tests PASS and static Native/worker/UI wiring checks PASS; modified JS modules parsed after removing ESM imports. Prior exact product head `7c0ddf0c` Windows B16 run `38518876660`, Test frontend and UIGS coverage SUCCESS, including actual 182-second FLAC source and artifact mutation.
- At the new exact head the Windows B16, Test frontend, and UIGS coverage were **in_progress** on the one immediate status read. New video packet scanning / mixed-mux residual fixtures cannot be claimed Windows PASS until that run completes.

## Promotion and remaining acceptance

Test-level implementation observation only. No automatic Canonical update. Even a fully measured completed mux is one observed current artifact, **not** a predictive coefficient or certificate of a future strict byte ceiling. True B16 closure needs reusable actual FLAC bitstream within the same formal mux task (or stronger constructive equivalence), container reserve and mixed AVS+attachment proof, complete field media/Android/Web acceptance and authenticated final delivery.
