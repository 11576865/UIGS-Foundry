# Observation: Browser-first container workbench needs a runtime capability envelope

Date: 2026-10-12
Status: Observation / standards-and-source informed architecture proposal; implementation and production acceptance not established
Project: `11576865/MKV-Fast-Muxer`
Evidence source: product `src/main.js` as of `7781a4f410a9c6edb9a1f3d056091e6ace333cc4` (the normal mux path performs `ffmpeg.writeFile(videoPath, await fetchFile(video))`, then executes and audits the output).

## Observation

A browser's ability to represent and edit a media-container project is distinct from the specific embedded encoder/muxer runtime's file limits, memory layout, filesystem capabilities, and background lifecycle. Treating an FFmpeg WASM limitation as a browser-wide impossibility is as incorrect as treating a generally supported Web API as proof that the current FFmpeg mux pipeline is streaming.

For four interoperable capabilities (specialized subtitle delivery; Matroska composition; validation; inspection/extraction), the proposed stable authority is a common `ContainerDocument` model with source provenance, proposed output composition, edit intents, and output evidence. A/B/C/D should be contextual operations/views on that model, not independent mutable copies of the source and output tracks.

## Source-backed runtime distinctions

- `ffmpeg.wasm` upstream FAQ still states a 2 GB maximum input for its ordinary runtime; this is **not** a normative browser or Matroska maximum: https://ffmpegwasm.netlify.app/docs/faq/
- `Blob.slice()` and `Blob.stream()` enable chunked input; success at chunking does not imply the current WASM core, writer or virtual filesystem accepts arbitrary large I/O: https://developer.mozilla.org/en-US/docs/Web/API/Blob/stream
- `FileSystemSyncAccessHandle` supports efficient private-origin file access **in dedicated workers**, but OPFS is not the user's visible filesystem. Direct user-visible save and directory selection APIs remain limited availability; a fallback download is required: https://developer.mozilla.org/en-US/docs/Web/API/FileSystemSyncAccessHandle ; https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker ; https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker
- Browser storage uses per-origin quotas/eviction and may have persistent-storage opt-in; do not promise absolute persistence of staged large files: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API
- Multi-threaded WASM may require cross-origin isolation with COOP/COEP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
- PWA installation/offline support does not guarantee a permanently executing large mux job when UI is closed. Service workers may be terminated/restarted without preserved global state: https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope

## Proposed reusable test boundary

Test runtime envelopes by `operation × file size × container structure × browser × output target`. Each capability is independently declared as supported / expected / unsupported / not verified. Distinguish (1) parsing, (2) planning, (3) mux/edit execution, (4) independent output audit, (5) preview, and (6) output preservation.

When a browser writer cannot safely handle an operation, explicitly report unsupported and offer a separate native execution backend if one is provided. Never replace container semantics with a video-required input just because the current mux command requires `mainInputPath`. Likewise, a PWA or desktop webview may share the same UI code but must not silently advertise platform capabilities it does not have.

## Presentation consequence

A composition-first desktop UI can retain a distinct source-provenance drawer, central output contents and a contextual inspector; tablet/phone project the same domain selection as an inspector sheet/page without reconstructing the editor state. Separate runtime capability states from validation results. Reuse the existing `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` for the UX proposal; this record concerns the *browser-versus-native execution capability envelope*, not a new UX Pattern ID.

## Evidence / limitations

Evidence is product source inspection and official specifications/docs. No multi-browser large-file benchmark, zero-track Matroska writer fixture, or native fallback implementation has been run. This observation is not a product decision, a promise of unlimited web I/O, or grounds for Canonical promotion.

Related existing: `inbox/candidates/2026-10-03-reuse-large-browser-media-staging.md` (reuse of already-mounted source, rather than whole-executor capability).


## 2026-10-20 product decision: advisory size warning vs execution hard limit

Source: [softmux PR #160](https://github.com/11576865/MKV-Fast-Muxer/pull/160), documentation commits through `6999fcaf85f095c4a17529b71dd9ca4860afa556`. Status: **user-approved project-specific product boundary / reusable Observation**, not automated implementation/Canonical authority.

The product owner explicitly corrected an assistant-invented 1 GB admission ceiling: **1 GB is a non-blocking triangle warning threshold**, not a maximum MKV size. Ordinary ffmpeg.wasm muxing should remain attemptable after the warning until the **actual configured FFmpeg/Wasm input constraint**; the upstream official FAQ currently lists **2 GB maximum ordinary input size** ([official FAQ](https://ffmpegwasm.netlify.app/docs/faq/)). No separate artificial 1 GB output limit, no mandatory confirmation dialog, no automatic rejection for merely >1 GB. Affected file rows show a `triangle-alert` icon and accessible caution text; batches judge per source rather than sum across jobs.

**Reusable distinction:** risk-notification threshold (soft warning), confirmed engine admission limit (hard gate), stage-specific writer constraints (e.g., P2 60 MiB/64 MiB), and empirical device success capacity **are four distinct values**. Never turn a performance benchmark or risk threshold into an undocumented admission refusal. Conversely, a documented engine maximum is not evidence that memory-intensive `fetchFile`/MEMFS/`readFile` processing will succeed near it. Expose concrete runtime failures accurately; unsafe Matroska operations must still fail closed for structural reasons independent of size warnings.

**Evidence limitation:** the owner approved this product behavior; the product PR changes specifications only. The >1 GB warning UI and 1.2–1.5 GB real file capability have **not** been confirmed implemented or passed on target devices. Do not promote to Canonical from one project decision.

## 2026-10-21 S12 empirical counterexample: native reader element-size cap ≠ browser media size limit

- New bounded test harness: [softmux Draft PR #170](https://github.com/11576865/MKV-Fast-Muxer/pull/170), initial head `171682e302f7b92ae3d5166271b6842bb22419a9`.
- First tiered actual-input runner [CI #39552836794](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39552836794), genuine mkvmerge-authored Matroska with 512 MiB, ~1 GB or 1.2 GB **single attached FileData** failed **before reaching browser**, because host ffprobe reported `Invalid length 0x20000000 > 0x10000000 for element with ID 0x465C` (and analogous larger lengths). This is evidence of the test runner's ffprobe/Matroska **single element** read constraint in these exact builds, not a general Matroska cap, full-file size limit, or a discovered FFmpeg/Wasm 1 GB limit.
- Corrected source preserves actual byte volume, writes 64 MiB independent FileData elements with per-part + ordered aggregate content SHA-256 and uses native mkvmerge. This avoids the specific reader failure without falsely truncating/replacing file content.
- Corrected PR head `ef932a3241e68ed164407f343bf959b0a7cbcf08`, [CI #39553162552](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39553162552): all three input fixtures have reached real Chromium/Wasm browser execution; **output verdict still Pending at this intake**.
- Reusable classification refinement to the existing capability-envelope Observation: distinguish *source container overall byte size*, *single EBML element byte size*, *individual attached resource*, *ffprobe parser support*, *FFmpeg/Wasm memory*, *output storage* and *real device capacity*. One parser rejecting one EBML element cannot be used to assert an artificial source-size hard limit. Not a new Candidate/Canonical change.

## 2026-10-21 controlled Matroska geometry evidence — total bytes alone are not the capability envelope

- S12 experimental [PR #170](https://github.com/11576865/MKV-Fast-Muxer/pull/170) uses *real native-generated data*, not a forged browser `File.size`. Same `WORKERFS` browser source strategy and Ubuntu/Chromium/FFmpeg.wasm runner, with explicit source checks and native finished-output oracles.
- A 256MiB MKV whose size is dominated by four real 64MiB original Matroska FileData attachments failed at **FFmpeg output header construction** (`Could not write header ... Out of memory`), while a >256MiB MKV whose size is dominated by real 177-second multichannel PCM timed audio packets **succeeded**, producing a 274,100,042-byte output. Thus the total declared source size was **not** a sufficient explanation even at that exact tier.
- Long valid PCM-packet input of **1,012,768,569 bytes** later passed [S12 exact experimental CI #39587026817](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39587026817): actual WORKERFS source, FFmpeg/Wasm append soft-subtitle mux, browser download **1,012,769,255-byte MKV**, ffprobe video/audio/subtitle + 654s input/output matching duration, original SHA-256 unchanged. The 1GB nonblocking advisory appeared; independent safety preflight completed before mux authorization. Sampled Chromium summed process RSS peak `4,218,472 KiB` in that run, **not** real physical-device peak memory or a general minimum hardware requirement.
- The same runtime still failed on original-attachment-heavy **512MiB** and >1GB source variants. A media-packet positive result **must not override an attachment-preservation negative result** or be marketed as unlimited ≥1GB Matroska support. It is also not a typical compressed feature film sample: repeated MPEG-4 video track and 7.1/32-bit generated PCM audio.
- Product [PR #172](https://github.com/11576865/MKV-Fast-Muxer/pull/172) isolates the bounded exact-File read-only staging change from the intentionally red large-attachment research. Its [S12 scoped exact-head CI #39587924233](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39587924233) passed all three scoped 128MiB attachment, 512MiB PCM and >1GB PCM cases. Full ordinary Browser E2E CI remained Pending at this observation. **No S12 aggregate PASS / no Canonical rule changes.**
- Reusable conclusion: evidence for a browser media engine should be indexed at least by **payload geometry (original attachment FileData vs media packets), chosen source staging, operation stage (probe vs header writer vs actual output), native result, runtime/hardware**. Do not infer a global admission threshold from a single workload or a single parser failure. This augments existing capacity-envelope Observation; no duplicate Candidate.
