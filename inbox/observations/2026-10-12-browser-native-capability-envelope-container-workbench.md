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
