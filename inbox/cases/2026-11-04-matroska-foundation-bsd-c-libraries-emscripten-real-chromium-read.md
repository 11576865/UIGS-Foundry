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
