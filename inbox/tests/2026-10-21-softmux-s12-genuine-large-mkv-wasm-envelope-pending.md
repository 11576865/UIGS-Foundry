# Test · S12 genuine large Matroska byte-volume execution envelope

Date: 2026-10-21
Status: **Test submitted / Pending corrected fixture CI; not S12 PASS; not Canonical**
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/170
First PR head: `171682e302f7b92ae3d5166271b6842bb22419a9`
Corrected fixture/test head: `ef932a3241e68ed164407f343bf959b0a7cbcf08`
Product baseline: main softmux `0.1025.0` after PR #169.
S12 contract: `docs/softmux-1.0-product-acceptance-contract-20261020.md`.

## Deduplication
- `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` already distinguishes soft size-risk threshold, confirmed FFmpeg/Wasm limit, native writer/parser constraints, empirical per-device capacity. This Test implements the proposed *operation × size × structure × runtime* envelope rather than inventing another general rule.
- `inbox/candidates/2026-10-03-reuse-large-browser-media-staging.md` already covers avoiding repeated whole-media staging but warns that identical File metadata must not substitute exact source identity. No staging implementation change is claimed in this PR.
- Existing product `scenarioGigabyteSourceAdvisory` checks only the 1,000,000,000 B and 1,000,000,001 B UI advisory boundary with sparse test sources. It does NOT create or execute an actually large MKV.

## Submitted test path
- Native script streams **actual random bytes** to disk, uses mkvmerge to attach them to a valid independently generated MPEG-4/AAC source. Three separate real-source tiers: 512 MiB, 1,000,000,128 B and 1,200,000,000 B. No file truncation or mocked browser File.size.
- Chromium/Wasm script records source byte length, genuine native `ffprobe` stream inventory, public UI warning/readiness, actual source scan, real mux, browser download, final native stream inventory, original payload round-trip `mkvextract` + SHA-256 and unchanged source digest, when successful.
- Browser/runner operating system and versions, staged operation and approximate child process RSS samples are emitted in an incremental machine-readable receipt. A crash or failure remains a **red job**, not reinterpreted as a green S12 performance success.
- Separate GitHub Actions matrix jobs hold each tier, with deadlines to prevent a stalled browser from blocking normal release CI. Each run uploads bounded JSON receipts; >1 GB raw media/output are intentionally not GitHub artifacts and are ephemeral CI files.

## Observed first attempt: native parser fixture cap, not WASM proof
- Initial S12 matrix run [39552836794](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39552836794): all three tiers **failed before browser execution**, in native `ffprobe` input validation. The logs reported `Invalid length 0x20000000 > 0x10000000 for element with ID 0x465C` at 512 MiB and equivalent invalid length for larger FileData. These are ffprobe reader failures for a *single huge attachment element*, not observed ffmpeg.wasm maximum or app behavior.
- Corrected fixture shards the **same true total payload** into individually valid 64 MiB FileData attachment elements, retaining per-piece and aggregate ordered SHA-256 validation. Native output audit uses a single mkvextract invocation to avoid O(number_of_attachments × file_size) rescanning.
- Until the corrected head [CI 39553162552](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39553162552) completes, the browser's true success/failure envelope is **unknown**.

## Explicit limitations
- The valid MKV has a real 2-second video/audio track but bulk byte volume comes from original binary attachments. It stresses browser/Wasm large byte I/O and MKV preservation, **not** realistic sustained high-bitrate video packet throughput.
- No target physical tablet, user-visible filesystem save, all-browser parity, general 2 GB runtime cap, or large-file output longevity claims.
- The full S12 contract requires 512 MiB, ~1 GB, >1 GB, near-real engine hard-limit, realistic long-video and actual tablet/desktop observations. This PR is a diagnostic test harness toward those outcomes.
- No Canonical change and no artificial 1 GB writer rejection. If a tier fails, classify its exact stage (fixture/parser, UI, source scan, Wasm ingestion, mux, audit, browser download) rather than treating all failures as one "size limit".

## 2026-10-21 interrupted test-run classification and latest head

- Corrected head `ef932a3241e68ed164407f343bf959b0a7cbcf08` [run 39553162552](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39553162552) generated/validated all three native large MKV fixtures and entered browser execution, but was **cancelled by a newer PR head before terminal browser verdict**. Neither PASS nor FAIL for the real Wasm path is established by those jobs.
- Test harness follow-up `bb2948ed29a0d895cb447d9c9a9c55ef26179a88` adds an `if: always()` post-step that marks still-IN_PROGRESS receipts as `INTERRUPTED_OR_TIMEOUT`, or records `NOT_RUN_OR_SETUP_FAILED` when no browser receipt was ever written. A deadline/OOM must not look like a successful or completed operation.
- Latest [actual tiered run 39553878527](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39553878527) is in progress for 512 MiB, decimal >1GB and 1.2GB tiers at this update. **Outcome Pending**. No product engine code is modified in the research branch.

## Final four-tier diagnostic run (partial verdicts as of 2026-10-21)

- Latest pressure PR head `ca7f6d14dc62c0ae080b14b44f237869b0d422ef` adds a **64 MiB true output control**, stricter no-zero-stream assertions and browser status/RSS progress sampler. Run [39557148027](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39557148027).
- **64 MiB PASS** in actual Chromium/FFmpeg.wasm: source was native-validated (video/audio/one 64 MiB original attachment), browser scanned three streams, muxed and downloaded an MKV of 67,153,682 bytes; native ffprobe observed video, audio, the new subtitle and preserved attachment, and full native mkvextract SHA-256 of attachment passed.
- **1,000,000,128 B FAIL in browser source-scan phase**: native ffprobe sees valid video/audio + 15 original 64 MiB attachments, but browser shows `轨道扫描完成：0 个流 · 0 个附件`. The test now rejects this immediately, rather than treating the text as a valid scan or waiting eight minutes.
- **1,200,000,000 B FAIL in browser source-scan phase**: native ffprobe sees video/audio + 18 original 64 MiB attachments, same false-success zero-stream state.
- **512 MiB** was still in browser mux at time of these observations; do not assign terminal PASS/FAIL without updated exact job result.
- Separate production fix [PR #171](https://github.com/11576865/MKV-Fast-Muxer/pull/171) raises `SOURCE_PROBE_EMPTY_STREAMS`, suppresses automatic unbounded same-source retries, and invalidates any earlier bound track editor when a manual rescan fails. It **does not** make 1GB runnable. Its exact head `e1e8181700626b76a59596754503ef7525a08547` Pending CI.
- S12 release contract **remains BLOCKED/PARTIAL**, not PASS. Valid physical/tablet 1GB+ media output, source-size/performance envelope and save evidence are still absent. These four tiers' long byte volume is intentionally original attachments, not real long-form video packets.
