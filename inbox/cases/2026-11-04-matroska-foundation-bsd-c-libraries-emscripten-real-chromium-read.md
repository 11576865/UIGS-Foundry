# Case: BSD libEBML2/libMatroska2 compiled to WebAssembly and read a real complex MKV in Chromium

Date: 2026-11-04
Status: **Case — reproducible CI proof for one real fixture / prototype only; no production migration and no Canonical change**
Source product: `11576865/MKV-Fast-Muxer`
User/root objective: stop proliferating custom partial EBML code and investigate mature Matroska implementations across the *entire* source-inspection, editing, muxing, validation and batch chain.
Full product issue: https://github.com/11576865/MKV-Fast-Muxer/issues/238
Draft code PR: https://github.com/11576865/MKV-Fast-Muxer/pull/240
Exact passing head: `686ba0444b446ef3029c24d01573faa05f4e2eea`
Exact-head CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41761392996
Artifact: `foundation-matroska2-wasm-actual-build-and-read`, ID `13290427408`
Source upstream: `Matroska-Org/foundation-source@d69761114b79c1dfcb2226ceca84452835e745c3` (BSD-3-Clause; actual C sources Core-C, libEBML2, libMatroska2, mkvtree).
Compiler: Emscripten 3.1.68, CMake; compression/codec helper switches OFF, CONFIG_EBML_WRITING ON.

## Verified steps & failures encountered

1. Experiment started with a real GitHub Actions environment that independently generated a complex MKV with `mkvmerge`/`mkvpropedit`: video+audio tracks, generic attachment, nested Chapters and ChapterUID-targeted Tags. The fixture generator initially failed because the new workflow lacked `python3-fonttools`, not a codec-library issue. Added the real missing dependency rather than bypassing fixture generation.
2. First genuine Emscripten C compilation failed on `Core-C/corec/portab.h`: `#error Platform not supported by Core-C!`; Emscripten was absent from its platform macros. Implemented an **ephemeral test-only** single-guard patch `#elif defined(__EMSCRIPTEN__)\n#define TARGET_LINUX` to probe whether Core-C's POSIX file/character subsystem can run on Emscripten. Saved the exact upstream diff; not a claim that upstream provides a supported port.
3. This compiled the *actual upstream sources* but the first real file call trapped with `RuntimeError: null function or function signature mismatch`. Adding `-sEMULATE_FUNCTION_POINTER_CASTS=1` to the Emscripten link options resolved this specific observed trap for the fixture (potential performance cost; not validated for all ABI layouts).
4. Node WebAssembly actual output report `UPSTREAM_C_MATROSKA_WASM_REAL_FILE_READ_PASS` was confirmed in CI `41760698699`: six Matroska element families observed, source SHA unchanged. This did not itself prove browser execution.
5. Browser probe first failed before reaching Chromium because this product has **no package-lock**, so `npm ci` was incorrect. Switched to `npm install --ignore-scripts` for test dependencies.
6. **Exact-head CI `41761392996` passed** after that correction. Browser report `output/foundation-matroska2-chromium-probe.json` states `UPSTREAM_C_MATROSKA_REAL_CHROMIUM_READ_PASS`, `browserExecuted:true`, Chrome user-agent `HeadlessChrome/156.0.0.0`, all of `ebml,segment,tracks,attachments,chapters,tags:true`, `browserErrorCount:0`, `sourceUnmodified:true`. Node/WASM report also passed in same run. Source ~190,158 bytes; SHA `8c5fa1404490e204c86c8c4187cf29b1614326259bbfb91114027cfecadd7750`, and compiled WASM binary SHA `4fe64111d79fc26871abab566b45f2ad55851f4745c7662728f0b576cafe48c9`. Browser report `elapsedMs:105` is **only this tiny single-file experiment**, not a product performance estimate.
7. Artifact includes compiler logs, temporary compatibility diff, independent mkvmerge -J JSON, Node and Chrome JSON reports, built JS/WASM, and upstream BSD LICENSE.

## Reusable technical distinction

License suitability and successful CMake compilation are **distinct** from true WASM ABI and runtime correctness. A library can be permissively licensed and buildable yet crash at the first virtual-file parse due to pointer casts or platform macro omissions. Explicitly test a genuine file and a browser runtime, inspect output and error families against a separate native producer, and preserve build errors as engineering evidence. It is incorrect to conclude either "browser support impossible" from the first compile error or "fully supported" from a green compilation.

A bounded platform adapter may be sufficient for an exploratory proof, but it is NOT a robust maintained port. Furthermore a C executable printing a human-readable object tree is NOT a stable machine-readable product API, and running an entire 190 KB fixture in MEMFS is not proof of multi-GB browser feasibility.

## Pending work, no overclaim

- Product UI/production runtime has **not** imported this Wasm, and the four existing Matroska FileData writers have not been removed.
- No real production semantic adapter or browser `File/Blob.slice` streaming I/O, invalid/adversarial container matrix, seek indexes, large-source benchmark, writing-path mutation, performance comparison, player compatibility or security acceptance exists yet.
- `-sEMULATE_FUNCTION_POINTER_CASTS=1` may incur overhead; maintainability and feasibility of the temporary Core-C compatibility adapter require upstream review. No GPL MKVToolNix source was copied into the MIT project.
- Neither one positive read nor bundled BSD LICENSE proves full legal obligations for any future production distribution; verify at release/integration.
- This is one product Case. Do **not** elevate to Canonical or treat Issue #238 as complete.

## Deduplication

Existing candidate `inbox/candidates/2026-10-15-upstream-code-reuse-semantic-contract-license-gate.md` already records considering the BSD Foundation source vs GPL MKVToolNix, without an actual WASM trial. Existing `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` separates browser/platform/FFmpeg virtual FS capability. This Case contributes **first actual pinned-source C-to-Wasm-to-real-Chromium execution**, and records specific ABI/platform failures and necessary temporary adaptations. It does not create a new governing principle.


## Follow-up 2026-11-04: Structured C/WASM read, exact 64-bit UID and parent-range proof

Product Draft PR #240 follow-up exact head `c310fa796ca382230566949bb3e8b85b3662945c`; CI [41765121560](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41765121560) completed **success**; downloaded artifact `foundation-matroska2-wasm-actual-build-and-read` ID `13293110062` and examined `foundation-matroska2-chromium-probe.json`.

The product's research branch now builds a second, separate Emscripten executable around the official libMatroska2 C API:
- `scripts/native/foundation-matroska-json-probe.c` exports `foundation_probe(path)` and `foundation_json()` as C ABI functions, not CLI stdout parsing; it uses upstream EBML element identity, byte offsets/ends, nested master traversal, `EBML_ElementReadData` and `EBML_IntegerValue` for UID scalar values.
- Real Chromium with the generated .wasm enumerated **201 actual EBML elements**; recognized multiple families including TrackEntry, AttachedFile, ChapterAtom, nested Tags, Clusters and Cues. Report `structuredMaxDepth:6`, `structuredParentRangesValidated:true`.
- Two TrackUIDs and one FileUID were output as *lossless decimal strings*, tested against raw `mkvmerge -J` with `parseMkvmergeJsonWithExactUids`; two ChapterUID values and one TagChapterUID had a target-resolving relationship.
- First green primitive experiment uncovered **negative hierarchy depth** in the output: directly reusing the mutable level counter of the upstream `mkvtree` pretty printer is incorrect for a typed object tree. The initial JSON's 202 nodes included a synthetic non-file “Matroska Stream” root. Follow-up changed the wrapper to exclude this synthetic root and reconstruct depth from actual master `EBML_ElementPosition/PositionEnd` ranges. The test rejects negative depth, out-of-range parent relationships and nonmonotonic file offsets. A subsequent C literal escaping error and a JS regex double-escape error caused genuine CI red lights; each was diagnosed from exact job logs and fixed. **Only exact-head 41765121560 is the accepted structured test**.
- Source is an independent `mkvmerge`/`mkvpropedit` fixture (~190KB), original input unmodified. Still uses full-file Emscripten MEMFS staging; the C adapter does **not** implement stream reading, arbitrary MKV editing or product UI integration.

**Reusable takeaway (Candidate-level interpretation, case-evidenced):** Parsing a container with a mature library is not enough to assert stable machine-readable semantics. CLI presentation depth and language-runtime numeric conversion can silently corrupt structural or identity information. Use the library's physical element ranges for ancestry, expose uint64 UID values as strings, independently verify source relations and output boundaries, and fail closed on inconsistent trees.

Dedup: this is a follow-up to this *same* Chromium/WASM Case; older `2026-10-15-upstream-code-reuse-semantic-contract-license-gate` Candidate covers choosing mature source and license, not a specific C ABI and lossless numerical/original parent relation issue. No new overlapping Case or Canonical change.

Pending: the main product Browser E2E job for exact head is still in progress at last observation, full diverse real-file matrix, streaming File/Blob random read (required for multi-GB recordings), error/ABI stability, security, production integration and replacement decision. Do not infer general Matroska preservation or write capability from this one read experiment.


## API integration review 2026-11-04: direct call is licensed, but production API is not yet safe to ship

Trigger: user explicitly challenged whether using the library through direct interfaces is acceptable **technically, legally, architecturally and operationally**. Reviewed the actual PR #240 head `c310fa796ca382230566949bb3e8b85b3662945c`, `scripts/native/foundation-matroska-json-probe.c`, `scripts/probe-foundation-matroska2-browser.mjs`, GitHub workflow, product MIT LICENSE, pinned upstream BSD LICENSE and official API headers. No additional product code changes made for this review.

**Verified positive controls**
- Official BSD-3-Clause C libraries, with Matroska upstream LICENSE, are compatible with keeping the product MIT-licensed *provided third-party notices remain in the shipped package*. A CI artifact retaining upstream LICENSE does not by itself cover future production distribution. No GPL MKVToolNix source was copied. The custom C adapter's traversal explicitly acknowledges derivation from upstream BSD sample.
- Official public C functions (EBML element read/position/value/context, MATROSKA_Init) are invoked by a **product-authored ABI bridge**, `foundation_probe(path)` and `foundation_json()`, via Emscripten `ccall`. These symbols are not a stable interface promised by upstream; it is the product's responsibility to version and test that ABI.
- Input stream is opened `SFLAG_RDONLY`; test runtime has no actual end-user source-file overwrite. Exact 64-bit UID and parent-range proof succeeded for the one pinned independently authored fixture in Chromium.

**Concrete pre-production blockers / code-review observations**
1. The exact workflow relies on `-sEMULATE_FUNCTION_POINTER_CASTS=1` and an upstream Core-C platform-guard patch. Emscripten documentation cautions function-pointer cast emulation adds runtime overhead, does not cure the underlying incompatible function signatures, and prefers correctly typed adapters. Temporary experimental compatibility is not maintained upstream portability.
2. `foundation_json()` points to a **static 1 MiB C global output buffer**; node count and maximum hierarchy depth are hard-coded to 8192 and 32; current bridge is stateful and non-reentrant. It is adequate for an isolated demonstration, not concurrent production calls or all large/complex MKVs. Fail-safe numeric return codes exist but errors lack detail; `DebugMessage` currently discards diagnostics.
3. Browser script transfers entire fixture as base64 into the page and copies the decoded bytes separately into two Emscripten MEMFS modules; this proves neither memory efficiency nor large-file processing. For multi-GB files a worker-scoped `File/Blob.slice` random-access bridge with bounded cache/seek and no whole-file staging is needed. `FileReaderSync` is available in dedicated worker contexts, not the main thread (MDN); memory and latency must be measured separately.
4. The bridge identifies UID element kinds through **string class names** and reads only selected scalar values. It does not guarantee complete EBML element semantics, unknown-element preservation, CRC/Cues/SeekHead mutation compatibility, or lossless output; the independent oracle currently compares only particular IDs/counts and valid hierarchy on one file.
5. Real malformed/hostile MKVs, out-of-memory/CPU limits, cancellation, input truncation/unknown-length segments, multiple module instances, browser security controls and dependency security review have not been validated. WASM sandboxing is defense-in-depth, not proof that parsing untrusted files is harmless.
6. Third-party source provenance and notice requirements must be preserved for every linked component at distribution, separately from the upstream BSD-3-Clause + product MIT license check.

**Candidate-level reusable interpretation:** public API access, permissive license, compilation, browser execution, semantically correct parsing, stable host ABI, efficient I/O, and production safety are **independent acceptance gates**. Using a mature parser can reduce custom code while leaving adapter maintenance, unsafe legacy ABI assumptions, and file I/O integration as real long-term obligations. Never treat a green 190KB read fixture as a cross-product production replacement decision. No Canonical change or product code merge. Status remains **Case evidence + production Pending**.

Official references: https://www.matroska.org/downloads/libraries.html ; https://spdx.org/licenses/BSD-3-Clause ; https://emscripten.org/docs/porting/guidelines/function_pointer_issues.html ; https://emscripten.org/docs/porting/files/file_systems_overview.html ; https://developer.mozilla.org/en-US/docs/Web/API/FileReaderSync .


## Follow-up 2026-11-04: Foundation C/WASM reader with real browser WORKERFS lazy File input

Product Draft PR #240 exact head `6fb13cada85d633f282220fade6fa1ffa2f99940`; pinned official BSD Foundation C sources + Emscripten 3.1.68. [Dedicated WASM/Chromium CI 41768079485](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41768079485) **passed**; downloaded actual evidence artifact `foundation-matroska2-wasm-actual-build-and-read` ID `13293880793`. Product full Browser E2E at same head `41768079408` remained in progress at last review. No production code, UI, original writer or official source was modified by this experimental mount.

**Precisely scoped new evidence**:
- Compiled only the new Foundation structure-probe WASM target with Emscripten `-lworkerfs.js`, `WORKERFS` exported and `-sENVIRONMENT=web,worker,node`.
- A genuine Chromium dedicated Worker received the exact user-supplied `File` through a file input and structured clone, mounted `FS.mount(WORKERFS,{files:[file]},'/source')`, and called **the same official `foundation_probe(path)` C ABI** as the existing MEMFS fixture. The 201 structural nodes were exactly equal as JSON. This does not use the user's media bytes for remote HTTP requests; only the local compiled WASM/JS is served.
- Observed `FileReaderSync.readAsArrayBuffer` calls in that worker via temporary instrumentation: for 190,158-byte MKV, 613 reads totaling **642 bytes**, max one slice **8 bytes**; input SHA unchanged.
- An independently `mkvmerge`-authored 100,854,018-byte valid MKV including 96MiB original attachment was passed from the Chromium file selector as a real File (not loaded with Node `fs.readFile`, nor staged into WASM MEMFS). The Foundation C reader enumerated 238 nodes, 2 tracks and 1 attachment, matching native `mkvmerge -J` track/attachment counts. 730 FileReaderSync calls totaled **771 bytes**, max slice 8 bytes; stream-hashed original file remained byte-identical.
- This is proof of **observed bounded Blob-slice reads for structural inspection** of these two fixtures, not proof of all browser memory consumption, code heap use, attachment payload extraction, video decoding, malformed input robustness, device performance, multi-GB/300GB compatibility or writing/editing.
- Official Emscripten docs explicitly describe `WORKERFS` as a read-only File/Blob-backed filesystem usable only inside Workers, separately enabled by `-lworkerfs.js`. This was a library-supported adapter, not a new home-grown EBML reader.

**Dedup and prior art correction (important):** The Softmux main branch **already used WORKERFS in 0.1027** in `src/ffmpeg-browser-source-staging.js`, with tests `tests/ffmpeg-browser-source-staging.test.mjs` and S12 browser/native large File evidence. Foundry `inbox/candidates/2026-10-22-softmux-large-original-attachments-media-only-wasm-byte-lane.md` and `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` already described that capability. Thus this Case **must not claim WORKERFS is newly introduced to Softmux**. The new, distinct result is compatibility of the separately sourced **BSD libMatroska2 C/WASM typed-reader** with the same browser-native read-on-demand model. `scripts/workers/foundation-matroska-worker.js` is a research entrypoint only; actual production integration should reuse shared File identity/cleanup behavior and not fork a parallel user-facing source staging system.

**Remaining Pending gates**: exact-head full product E2E, cancellation, worker lifecycle/parallel isolation, stable reentrant C ABI (current static 1MiB buffer), C function pointer compatibility maintenance, cross-version legal notices and supply chain, output semantic oracle beyond nodes/UIDs, multiple adversarial MKVs, multi-GB device memory and streaming workloads. No Canonical update, no new product release claim, no generalized Matroska rewrite.


## Follow-up 2026-11-04: Optional production-reader boundary and lifecycle tests

Product Draft [PR #240](https://github.com/11576865/MKV-Fast-Muxer/pull/240), exact submitted head `0b3561120b4282e6d42c923229d6e3a6c65cd93a`, introduces a **bounded, optional verification hook into the existing product reader**, rather than a parallel UI or a second source manager:

- `src/foundation-structure-observation.js`: fail-closed, source-bound adapter around the proven dedicated Worker/WASM `foundation_probe` JSON contract. Validates nested real byte ranges, 64-bit UID decimal strings, node limits and genuine WORKERFS source-size/read evidence. Each request owns a Worker, terminated on success, parse failure, abort, timeout or explicit cancellation. An independent read observation never grants a writer permission.
- `src/matroska-attachment-reader.js`: existing `createMatroskaAttachmentReader()` accepts an **optional** injected `foundationWorkerFactory`, exports `inspectFoundationStructure(inventory)` and `cancelFoundationInspection()`, uses the existing `createSourceAssetSession()` asset identity, requires the same live inventory, refuses stale/reinspected results, compares official Foundation FileUIDs with existing bounded-reader attachment UID inventory. No previous extraction or editor path is redirected; no external WASM is shipped at this stage.
- `tests/foundation-structure-observation.test.mjs`: positive identity/read-only contract plus no-runtime, UID-mismatch, invalid tree, fake WORKERFS evidence, re-inspection cancellation, abort, timeout and same-reader concurrency denial tests.
- `scripts/probe-foundation-matroska2-browser.mjs`: actual Chromium serves and imports the new product adapter and the existing `matroska-attachment-reader.js` plus dependencies; calls that integration with an actual MKV and the already-proven Foundation C/WASM Worker; compares resulting official FileUIDs to current attachment inventory. Keeps the earlier 100MB WORKERFS fixture test.
- Experimental worker filename rules now align with existing `src/ffmpeg-browser-source-staging.js`: preserve spaces/Unicode in original names while rejecting paths, separators and NUL. New browser test explicitly uses a selected filename with Chinese characters and spaces.

**Evidence boundary:** At this Case update, latest exact-head CI `41769727767` (Foundation C/WASM) and `41769727751` (full product Browser E2E) are **pending/in progress**. Do not declare these integration tests green or a production reader replacement until the exact-head runs finish. Existing mainline behavior and UI remain unchanged; the binary is CI-only and runtime factory absent by default, therefore no user-visible execution path is enabled. Existing 2026-10-22 Foundry WorkERFS Candidate and product `src/ffmpeg-browser-source-staging.js` already cover WORKERFS for FFmpeg; this Case's distinct finding is bridging the mature library into the existing Matroska source asset and inventory authority with bounded cancellation/lifecycle semantics.

**Potential reusable invariant (provisional):** a successful library parse must be attached to the same exact source object and revision as the product's active inspection, must not outlive cancellation or a newer inspection, and must not by itself change writer authorization. Reuse existing source authority rather than inventing a second viewer state machine. Record as a Case follow-up only; do not revise Canonical from a single product branch.


### Acceptance update — exact HEAD C/WASM product reader interface validated in Chromium

Product PR #240 exact head `0b3561120b4282e6d42c923229d6e3a6c65cd93a`; dedicated [Foundation CI #41769727767](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41769727767) **completed SUCCESS**. Downloaded artifact `foundation-matroska2-wasm-actual-build-and-read` ID `13293678440`, read actual `output/foundation-matroska2-chromium-probe.json`:
- `existingProductReaderFoundationIntegrationPassed:true`, `existingProductReaderAttachmentCount:1`, `productAdapterInvokedInChromium:true`, `productAdapterConsistentWithNative:true`.
- Existing **product** `src/matroska-attachment-reader.js` module and dependencies were served as ES modules into genuine Chromium. It generated the current source inventory, invoked its optional `inspectFoundationStructure` with exact File source identity and official WORKERFS WAsm worker, then independently matched its FileUID inventory and the WASM's UID list. No output/write path was authorized or redirected.
- `workerFSUnicodeFilenamePassed:true`, including test `作品 第1话 中文字幕.mkv`; the Worker no longer imposes a false ASCII-only filename policy and follows existing FFmpeg WORKERFS source filename safety boundary, rejecting traversal/path separator/NUL.
- 201 structured nodes and all existing hierarchy/UID checks passed. Dedicated large 100,854,018-byte MKV read 771B with max 8B slices to inspect 238 nodes; reference count matched; original source SHA unchanged. Browser error count 0.
- Product Node unit tests in the full browser CI reached green unit stage; tests cover no-runtime rejection, bad tree/UID, cancel/reinspection/Abort/timeout, concurrency isolation; S12 scoped large media workflow for this head passed.
- At this Case update **the full product Browser E2E workflow #41769727751 was still in progress**, so it is distinct from the exact-head dedicated WASM acceptance; PR #240 remains Draft and unmerged. This does not place a packaged third-party WASM runtime in product distribution or replace production reader/writer implementation.

**Revised lesson:** for a mature-parser runtime to augment an existing model, bind it to the *existing inventory instance* and File object, cross-check a source identity it cannot invent, and terminate its Worker on any cancellation or re-inspection. Positive readback is bounded evidence, **not** a writer permission or general conformance certificate. This extends an existing Case; no Canonical changes.


## Follow-up 2026-11-04: Versioned native allocation and reproducible licensed Vite bundle

**Scope:** same existing Case as the official Foundation C/WASM browser read; no new parallel Candidate or Canonical. Product Draft [PR #240](https://github.com/11576865/MKV-Fast-Muxer/pull/240).

**Concrete prior defect addressed:** the experimental C ABI formerly declared a fixed `static char output[1024*1024]`, implicitly retained result memory and had no documented release/version checks. It could not support explicit lifecycle auditing. The product bridge now uses a growable `realloc` buffer (hard cap **16 MiB**, not unlimited), `foundation_abi_version()`, `foundation_json_length()`, `foundation_release()`, and resets/clears output for every probe. `src/foundation-wasm-json-abi.js` centralizes version assertion, UTF-8 byte-length evidence, parsing, schema check and native release in `finally`; the same helper runs in classic Chromium Worker and the standalone research runner. Node regression tests cover success, failure, version mismatch, invalid/oversize/truncated UTF-8 output and guaranteed deallocation.

**Exact tested evidence:** product commit `588031021283bee1a8ab8b2931c4ebb22c6374e7`, [Foundation CI #41791278593](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41791278593) **SUCCESS**, archived artifact `foundation-matroska2-wasm-actual-build-and-read` ID `13303451629`, whose actual ZIP was inspected:
- `.e2e/output/foundation-matroska2-chromium-probe.json` confirms `structuredCAbiVersioned:true`, `structuredCAbiReleaseChecked:true`, `structuredCAbiFailureRecoveryChecked:true`, `existingProductReaderFoundationIntegrationPassed:true`, browser error count 0.
- New opt-in `scripts/stage-foundation-wasm-runtime.mjs` verifies the exact upstream Foundation commit, actual WASM magic and generated Emscripten runtime, copies generated C/WASM + the classic Worker + versioned product JS ABI module + upstream BSD-3-Clause LICENSE to `public/vendor/matroska-foundation`, writes byte-count/SHA-256 provenance manifest and refuses overwriting existing staged packages. `npm run build` is then executed in CI; staged `dist/vendor/matroska-foundation` checks byte-for-byte before a **separate real Chromium smoke** actually imports the staged JS/WASM/Worker assets, not merely CI temp `mkvtree.wasm`.
- `.e2e/output/foundation-staged-runtime-chromium.json`: `result:"PACKAGED_FOUNDATION_WASM_CHROMIUM_READ_PASS"`, exact TrackUID 2 / FileUID 1, 201 nodes on small real MKV; 100,854,018-byte large MKV yields 238 nodes, 730 read calls and 771 bytes of observed FileReaderSync slice reads; browser errors 0, source unmodified.
- Distributed manifest `bridgeAbiVersion:1`, `upstreamCommit:d69761114b79c1dfcb2226ceca84452835e745c3`, `readOnly:true`, `productionActivation:disabled-by-default`, per-file SHA-256, BSD LICENSE bundled. The new `foundation_json_probe.wasm` in that artifact is 270,129 bytes (specific build binary only).

**Additional continuation pending as of this record:** commit `9164a7b10004261f41166d92ca68b998ae031b92` also stages a product-authored same-origin Worker factory with Vite/GitHub Pages BASE_URL handling and tests explicit activation; exact-head CI [Foundation #41791948115](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41791948115) plus product E2E [#41791947833](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41791947833) had not yet completed at update. Do not promote this additional step until direct evidence is collected.

**Boundaries:** A license-bearing and verified opt-in Vite bundle is NOT automatic production deployment. The normal product build does not invoke the specialized pinned-source compiler nor include a bundle unless explicitly staged; `main.js` does not activate it; project UI and four existing writers remain unchanged. 16MiB output and 8192-node / 32-level caps remain deliberate fail-closed limits, not full conformance. Core-C POSIX patch and Emscripten function pointer emulation remain technical debt; upstream C ABI is still a product-owned experimental bridge. No one-file proof is valid for 300GB media and no actual mkvmerge/mkvpropedit editing path was migrated.

**Reusable knowledge:** test native allocation/ownership at ABI boundaries, *then* test the exact bytes shipped by the package manager/build, with a separate browser smoke and legal/provenance manifest. These are distinct gates; static JSON output parsing in a CI scratch module is insufficient proof that the licensed runtime actually loads after a Vite release build. No Canonical change.


### Final opt-in Worker factory packaging acceptance for this turn

Exact product head `9164a7b10004261f41166d92ca68b998ae031b92` — [Foundation CI #41791948115](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41791948115) **SUCCESS**. Downloaded, inspected artifact `foundation-matroska2-wasm-actual-build-and-read` ID `13304250397`:
- `.e2e/output/foundation-staged-runtime-chromium.json` returned `PACKAGED_FOUNDATION_WASM_CHROMIUM_READ_PASS`, `explicitProductWorkerFactoryPassed:true`, `productUIActivated:false`, `writerEnabled:false`, `browserErrors:0`, `sourceUnmodified:true`. Manifest SHA256 `68fab19deeaffe5552175a9577d3dadcdf12126b3938b21789d690b5fdaad3c3`; files include actual generated Wasm/JS, experimental Worker, ABI helper, Worker factory and BSD LICENSE.
- Published `src/foundation-runtime-worker-factory.js` is opt-in and same-origin, uses caller-specified/Vite `BASE_URL` to support GitHub Pages paths, checks path traversal and does not allocate a Worker until invoked. A Node unit test covers root/subpath/invalid/cross-origin and lazy construction; separate Chrome test **imports its staged ES module** and constructs actual Worker from it, not an invented absolute path.
- Vite distribution is staged only via the pinned-source explicit script and verified per-file against SHA-256 manifest, with BSD LICENSE retained. It is still a **test distribution**, not automatically deployed to the product's default UI. This is importantly different from merely compiling the C library or having a test-only research worker.

Related exact-head workflows: [S12 real large media #41791947768](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41791947768) SUCCESS and Pages #41791947815 SUCCESS; product full Browser E2E #41791947833 still running at this observation. No Canonical changes, no production default, no MKV editor/writer migration; upstream portability work and real untrusted-file safety gates remain.

Dedup: this is the same source-of-truth Case recording successive gates of the same Matroska Foundation reuse experiment, not a new Candidate or unsupported generalized reuse principle.
