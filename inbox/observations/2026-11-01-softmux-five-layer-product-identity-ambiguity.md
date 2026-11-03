# Observation — Softmux product identity remains ambiguous after bounded-scope and release-evidence expansion

Date: 2026-11-01
Status: Observation / owner-reported conceptual uncertainty; proposed model unvalidated; no Canonical change
Project: `11576865/MKV-Fast-Muxer`
Product main snapshot: `36f71dc9ae80a4e0b463de51d2f3aa2edae64c02` (`0.1032.0`)
Pending product PR: [#205](https://github.com/11576865/MKV-Fast-Muxer/pull/205) (`0.1033`, release evidence gate, open and unmerged at inspection)

## Trigger and evidence boundary

The owner stated: “我已经越来越搞不懂这个项目是什么，现在是什么，要成为什么，可能成为什么和应该成为什么了。” This is owner feedback about *understanding and product direction*, not permission to narrow scope, remove working features, freeze a new strategy, or rewrite Canonical contracts.

Source-grounded milestones:
- 2026-10-12 strategic decision D-01—D-10: a Matroska-centered workbench with reliable subtitle/font delivery as flagship; inspection, composition, verification, bounded editing as distinct roles.
- 2026-10-20 approved scope B and nonblocking >1GB warning; details S01—S14 remained proposed, not explicitly approved one by one.
- On 2026-11-01 repo `main` was development version 0.1032, with implemented source/external metadata recovery, batch delivery, bounded source/output inspection and output-save evidence; proposed 0.1033 PR #205 encoded a fail-closed release gate, while its readiness report still marked all 14 release tasks short of formal full acceptance.

## Distinction potentially reusable across projects

Do not collapse five different questions into one “product status”:
1. **What it is**: historical reason for the tool and its primary user job.
2. **What it currently is**: verifiable implemented behavior, runtime envelope, and evidence level, including legacy vs research-only paths.
3. **What it intends to be**: user-approved strategy and bounded proposed first-release contract, tracked separately.
4. **What it could be**: alternative technically possible directions and their separate costs, not inferred obligations.
5. **What it should be**: normative product judgment requiring user task evidence, competitive comparison, limitations and owner decision.

Matroska's general document ontology (Tracks, Attachments, Chapters, Tags, Cues, EBML) does not itself authorize a general-purpose writer. Read/inspect, remux, bounded in-place edit, independent verification, saving and player compatibility are separate operations with separate proof burdens. A growing chain of deeper verification tasks can be technically useful without by itself settling user-facing product purpose.

**Causal caution:** this is an interpretive risk mechanism, not a demonstrated root cause. Prior [QHE product-identity Observation](../observations/2026-10-12-qhe-feature-growth-and-unresolved-product-identity.md) records the owner's explicit correction that lack of first-principles domain understanding can precede identity ambiguity; do not replace that with an unproven simplistic “feature creep alone” explanation.

## Proposed next test (not an authorized scope change)

- Explain underlying format objects, remux versus bounded EBML mutation, and evidence promises before recommending a product form.
- Select three real user jobs (quick subtitle/font delivery, multi-source Matroska composition, inspect/safely alter existing MKV); compare actual artifact and error experience with mature alternatives.
- Explicitly distinguish: flagship capability, supporting subsystem, restricted experimental operator, release gate, and out-of-scope future possibility.
- Ask owner to evaluate tradeoffs before declaring a newly worded “should become” sentence as project authority.
- Confirm a concrete task-to-artifact path in the actual app, not only PR count, CI green or matrices. Treat test effectiveness as pending.

## Dedupe / links

Reviewed these existing Foundry records:
- [2026-10-20 scope vs executable release contract](2026-10-20-softmux-scope-vs-executable-release-contract.md): separates strategy, bounded release contract and evidence; does not capture this later five-question owner feedback.
- [2026-10-12 MKV tool scope correction](2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md): format validity and existing ecosystem.
- [2026-10-12 orthogonal product dimensions](../candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md): A/B/C/D are not competing navigation sections.
- [2026-10-12 QHE product identity](2026-10-12-qhe-feature-growth-and-unresolved-product-identity.md): comparable owner experience and epistemic correction.
- [2026-10-14 agent next-unit drift](../candidates/2026-10-14-agent-generated-next-units-goal-drift-guard.md): self-generated work queue may displace root goals.

This Observation preserves a **new dated owner report in the MKV product** and the five-layer distinction, without creating a competing Canonical principle or copying existing release-gate guidance.

## State

Recorded as Observation. Product strategy, prioritized user jobs, any reduction in scope, and first-release acceptance remain **Pending owner validation**, not automatically changed.


## 2026-11-01 owner follow-up: user acceptance is not an invisible-defect oracle

Owner correction: treating **“make it immediately usable”** as the next optimization may produce fast apparent progress but little explanatory understanding, repeat the HSR project’s owner-as-tester burden, and worst of all assume the owner can detect errors whose existence is not visible. This does **not** authorize pausing all usability work or choosing research over delivery in perpetuity.

Sharper distinction: user task acceptance verifies discoverability, interaction suitability, and observable outcome; it cannot by itself verify hidden state, omitted container objects, media timestamps, preservation relations, stale artifacts or deep semantic equivalence. A green implementation test or self-authored output report may share assumptions with the code under test. The general **test oracle problem** is documented by Barr et al. (IEEE TSE 2015, doi:10.1109/TSE.2014.2372785); independent reference readers, negative controls, property-based / metamorphic relations and real artifact readback reduce but do not eliminate this blind spot.

Specific supporting local cases already in Foundry (do not duplicate them):
- `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`: playable no-edit remux may silently lose attachments/chapters/relationships;
- `inbox/bugs/2026-10-13-mkv-ffmpeg-wasm-ass-mux-timestamp-shift.md`: real browser mux passed existing track/attachment checks, while added independent ASS-event comparison revealed +2 centisecond offset;
- `inbox/bugs/2026-10-11-hsr-incremental-same-basename-and-stale-download-merge.md`: source identity/session errors can carry wrong audio into archive without immediate visible warning.

Candidate improvement to test, not a new Canonical rule: require a **claim → expected invariants → independent oracle → mutation/failure counterexample → limits/notChecked** record for any high-risk operation. The developer/agent is responsible for proactive error discovery, independent finished-artifact examination and unverified-claim labeling. Owner's role is product-purpose and subjective usability judgment, not serving as the only acceptance oracle. Build an explanatory map from format semantics to operations and observable claims, as an enduring companion to runnable tests. Evaluate success by both independent defect-detection power and owner comprehension, not PR count or whether a demo appears to work.

This extends the **same current Observation**, avoiding a duplicate Candidate or premature Canonical promotion. It is a hypothesis about better product governance; no test of the proposed workflow has yet been executed.


## 2026-11-01 owner direction: prioritize an actual usable product, defer hard non-core capabilities

After the previous discussion about the ideal operator workflow and its implementation difficulty, the owner stated: “困难的可以先搁置，重要的是我们需要做一个实际的”. The sentence is incomplete, but in context it expresses a **priority preference for a concrete, usable delivery rather than treating advanced Matroska generality as a prerequisite**. It is not yet a fully approved replacement of Plan B / S01–S14, nor an instruction to weaken safety or erase prior capabilities.

Proposed bounded first usable path (assistant inference, NOT product Canonical):
- one normal user journey: import supported real video/MKV, subtitles and fonts → inspect intended output tracks/attachments → apply supported attributes → preflight & execute real stream-copy mux → independently inspect actual output → download or safely save;
- then reuse the same authority and actual-artifact verification in batch matching/queue/retry;
- defer arbitrary EBML editing, broad unknown-structure retention and repair, universal attachment-only writing, and unconditional multi-GB/device guarantees;
- keep bounded fail-closed preflight, exact source/output identity, observed-artifact verification and explicit unchecked claims as nonnegotiable guardrails. “Defer advanced correctness” is NOT permission for silent loss.

Next validation: map existing main implementation and user-visible entry paths to this specific task, collect actual real-file/browser evidence and negative controls without making the owner the sole bug oracle; separately get owner approval for any change to the 1.0 release contract. No code, PR or Canonical scope change is authorized by this note.

Intake status: updates this existing Observation rather than creating a duplicate Candidate. **Release scope approval / runnable slice definition: Pending owner review.**


## 2026-11-01 owner clarified original product intent and cause of drift

Owner’s own initial requirement restatement (paraphrased, not a new approval): the original subtitle muxer accepted video + subtitles + fonts, made one MKV, and did not expose other concerns. The intended “generic upgrade” would instead accept arbitrary resources *where Matroska supports them*, including image attachments; start a new Matroska with just loose files and **no video** when appropriate; inspect existing MKV contents; subsequently allow editing the observed content. The owner asks why such an apparently direct product expansion produced today's large, difficult project.

Important exact semantic clarification: “generic inputs” are not all playable tracks; an image can be a generic Matroska attachment (FileData) without being converted to video. Under RFC 9559 §6.1, Info alone is top-level REQUIRED; Tracks + Cluster are needed for *playable* Matroska, not every Matroska document. This original project requirement was already in Foundry `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`; do not mislabel it as a newly invented user request.

Verified repository-specific divergence:
- Issue #68 content-first intake retained “one user-selected main source that has a usable video stream for the current engine” as a compatibility adapter; this was an implementation restriction, not the user's generic product semantics.
- Current `src/mux-command.js` `buildMuxCommand({mainInputPath,...})` begins with `-i mainInputPath` and `-map 0:v?`, preserving a video-rooted executor. `src/output-composition.js` itself declares composition a view projection over legacy state, not a new generalized writer.
- Independent P0 issue #77 reproduced nested ChapterAtom and ChapterUID-targeted Tag loss under real browser FFmpeg remux, which correctly requires honest scope or fail-closed behavior; it does *not* entail writing an arbitrary full EBML editor before delivering generic attachments.
- In contrast, RFC and existing MKVToolNix attachment editor semantics support bounded generic attachment operations. Different write lanes (track remux vs no-track Matroska creation vs property edit) should be separated, not treated as one ever-expanding FFmpeg code path.

Tentative root cause hypothesis: the team continued extending video-rooted execution and then compensated with richer domain projection, safety instrumentation, deep structure research, release tracking and fragmented follow-up tasks instead of first delivering an end-to-end minimal generic container writer and inspector. Some research is genuine and valuable (issue #77); the *ordering and elevation to product acceptance* are questionable, not the existence of safeguards. Do not attribute all elapsed work or all errors to this mechanism absent a dated end-to-end issue/PR audit.

Suggested falsifiable corrective test (not an authorized scope change): four independent working product paths (new video+ASS+fonts; add JPEG/PNG as attachment to MKV; create valid no-track attachments-only Matroska from PNG/document with native independent readback; open existing MKV, enumerate/extract attachment and perform one supported modification into a separate valid output). Compare their code paths to legacy engine gating and actual UI entry points; if not supported, report precise missing adapter/writer rather than expanding a universal editing contract. Keep exact-original preservation risks explicit. No direct product repository mutation or Canonical promotion here.

This is appended to **the same** dated Observation to dedupe the existing Oct 12 original-intent entry; new explicit owner restatement strengthens source rationale while final architectural recommendation remains proposed and **Pending owner validation**.


## Owner rejected superficial legacy-feature inventory answer (2026-11-01)

When asked "原始版本已经有的功能怎么处理", the assistant replied by enumerating 44 `L-001–L-044` historical features and proposing three separate entry modes (“快速封装 / 通用容器工作台 / 批量封装”). The owner explicitly rejected the answer: “完全没说到点上。”

Correction to the interpretation (**assistant hypothesis; owner has not yet confirmed this new reading**):
- `L-001–L-044` is a mixed migration ledger containing later enhancements, old UI/pipeline descriptions and original behaviors. It is not an inventory of the *original* video+subtitle+font tool alone; using it to answer the conceptual question confuses provenance and scope.
- The primary design question may instead be **how the original tool's specialized, content-aware actions fit naturally into the same generic Matroska composer**, with one authoritative document, not whether to run three segregated application modes. Eg a single content-based import of video, ASS, TTF and PNG should yield media/subtitle tracks and font/image attachments, retaining triggered font identification, ASS matching, font subsetting, subtitle preview, and supported track options. With only attachments, a no-track container path should exist (once verified); no video placeholder.
- Task-specific presets or batch job matrices can be convenient projections over the same composition authority; do not elevate them to separate product identities, data models or non-interoperating editors.
- Preserve proved **behavioral invariants**, distinguish legacy input widgets and implementation detail from user-value capabilities, and individually test specialized operations without letting old video-root restrictions define the generic domain.
- This is substantially covered by `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md` (specialized ASS recipe on one composition domain) and `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` (behavioral inheritance and batch job identity). No new Candidate or Canonical promoted.

Status: **Observation of owner dissatisfaction and assistant framing failure**, deduplicated as a continuation of this identity Observation. The exact intended question is not proven until corroborated; do not silently claim owner endorsement of this interpretation.


## Owner's minimal interaction contract clarified (2026-11-01)

After rejecting the prior assistant's legacy feature inventory and separated three-mode recommendation, the owner explicitly specified a much smaller product interaction invariant: **“用户必须拖入某些文件，而最终的输出仍然一定是mkv，当然，用户也可能只是想看看mkv的内容，因此不一定有输出。”**

Source-faithful interpretation:
- Entry is resource-first: user supplies some file(s), not a prior choice of application mode or mandatory primary video.
- If the user elects to export, the output format is **Matroska**; export is **optional**, not a prerequisite to inspection.
- A user may import an existing MKV just to inspect its contents, with no mutation and no produced artifact.
- Subtitle/font specializations, attachments, existing-container viewing and editing, and batch output are contextual operations on imported content rather than independent product identities. An input video is not required for a non-playback attachment-only Matroska creation where a verified writer exists.
- Do **not** silently conflate “imported” with “modified”, “viewed” with “approved for writing”, or “valid Matroska attachment” with “playable media stream”. Do not auto-generate outputs just for viewing.
- For a single export task, no output or a Matroska artifact; batch may result in multiple Matroska artifacts.

This is a simpler *user-level grammar* than project architecture, and must be kept separate from implementation detail. The owner did **not** authorize replacing the entire UI, removing legacy functions, adopting a particular writer, or modifying the 1.0 Canonical acceptance document.

Deduplication: `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md` and `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` already cover content-first and one composition authority; the **optional-export invariant** and the owner's direct correction are appended here as dated Observation, not a duplicate general UX Candidate.

Status: owner-confirmed user behavior statement; proposed implementation implications **Pending validation**, no Canonical promotion.

## 2026-11-01 reappraisal after report: 0.1035 genuine domain bridges, but execution remains split

Owner requested “重新审视软封” after asking for a detailed PDF reconstructing November 1 conversation. Reappraisal source: PDF 软封_本次聊天完整讨论与决策溯源报告_2026-11-01.pdf (20pp), owner-approved Oct12 D-01–D-10 and Oct20 scope B, live product main README `0.1035.0`, `src/asset-intake.js`, `src/container-document.js`, `src/output-composition.js`, `src/mux-command.js`, `src/container-target-draft.js`, merged product PR #207/#208/#209, release evidence/readiness and Foundry case `2026-11-01-softmux-candidate-membership-capture-output-identity.md`.

Important time correction: the 20-page PDF captured **0.1032**; main later advanced to **0.1035**, including #207 external subtitle/audio candidate membership independent of preview with actual browser/FFprobe output, #208 ordinary-workbench **PNG/PDF-only 1–8 attachment zero-track output** bounded to 16MiB individual/32MiB aggregate with native MKVToolNix readback, and #209 per-exact-File source-side A/B draft retention and two verified separate outputs. This narrows prior gaps **without proving** complete cross-source object reuse, media+general attachment combined write, universal arbitrary files/large attachments, independent per-target external font/subtitle state, all-source ASS/font self-dependency, or comprehensive complex Chapter/Tag semantic fidelity. Existing legacy `buildMuxCommand({mainInputPath})` and one-`video` document projection still govern ordinary media output. S14 release gate and 14/44/57 ledgers are non-PASS and contractApproval PENDING_OWNER_REVIEW; pending #205/#206 research ≠ production acceptance.

**Interpretive product analysis (candidate, not a new owner decision):** Softmux currently has a verified specialist mux core, increasingly real content-first browser interactions, separate bounded structural writers, and a sophisticated safety/evidence envelope. The architecture is not yet one seamlessly composable general container executor. A tempting design mistake is treating each independently verified capability as a product-end-state and expanding research forms/modes or release bureaucracy while the everyday seam remains missing. This is a *hypothesis*, not proof that rigor itself is wasteful. Matroska real format complexity (UID references, timestamp semantics, unknown structures), inheritance complexity (ASS/font/batch), and assistant-generated hypothetical workflow complexity should be explicitly separated.

Specific next execution proposal pending owner approval: prioritize a genuinely useful cross-boundary job **existing MKV with audio/video + arbitrary generic non-font attachment → new MKV**, preserving all unmodified semantic contents and independent readback (Complex Chapter/Tag negatives must not silently succeed). This is a missing product seam because #208 explicitly blocks media+generic attachments; prefer capability-routed writer reuse plus output oracle rather than inventing a new full-document UI. Next investigate using an existing embedded attachment from MKV A in a proposed B output (without pre-extracting as a requirement), retaining exact provenance; later finish existing/source ASS–font closed-dependency output audit, without automatically applying all new operations to batch. All 1.0 scope changes remain separate explicit owner decisions. Avoid asserting global success from only bounded fixtures, and keep the accepted browser-only cost ledger (memory, rereselect permissions, interruptions, save friction, unsupported writer paths).

**Epistemic boundary:** This reappraisal is based on inspected repo source, PR descriptions/reports and the earlier conversation; no new full real-device or independent artifact run performed during this assessment. Do not modify Canonical or product code from this observation alone. New knowledge is the **concrete 0.1035 gap topology and priority hypothesis**; dedup with existing owner-source candidate and November 1 integration Case. 

## 2026-11-03 updated executable planning baseline: 0.1047 after MKVToolNix product-value challenge

Owner asked “那软封存在的意义是什么”, then “照这个方向列一个完善计划”. Approved baseline not changed: pure browser/local, generic Matroska document, inherited ASS/font professional depth and batch retained; benchmark against mature free Chinese-language MKVToolNix instead of asserting novelty of generic mux/edit.

**Critical new live source correction:** On Nov 3 product main README announces 0.1047; older line in README still labels 0.1044 (minor documentation drift). Earlier Nov 1 observation identifying mixed media+ordinary attachments as a missing functionality is **outdated**: merged #224/0.1046 does write ordinary attachments with audio/video alongside fonts/subtitles (8 included, 16MiB/item, 32MiB aggregate, source-image FileData recovery and exact final output SHA), #223/0.1045 handles audio-only without invented video, #222/0.1044 exports original source audio/subtitle tracks into independent reusable media, #213/0.1035 previews embedded ASS/attached fonts, #219/0.1041 adds bounded unified undo history, #226 supplies 20-task combined failure recovery and #227/0.1047 fixes canonical-composition glyph preservation with real output font-shaping checks. These are scoped completed PRs/CI descriptions, not blanket S01-S14 acceptance. `docs/softmux-1.0-release-evidence.json` still shows S01-08 UNASSESSED; S09-11 IMPLEMENTED_NOT_ACCEPTED; S12-14 BLOCKED; owner detailed contract approval PENDING_OWNER_REVIEW. 14/44/57 crosswalk not auto acceptance.

**Remaining seams requiring evidence:** cross-MKV direct inclusion of an A track/attachment into B's planned target (existing #222 can export track to standalone but UI operation may still require manual extraction; no proof cross-target membership and timebase), complete recursive Chapter/Edition/Tag UID semantically equivalent remux/edit beyond fail-closed #77, font self-dependency closure across all source/target/result, support beyond 0.1046 bounded mixed files, browser memory/save/tablet realistic device envelope, and user-experienced differentiator compared to MKVToolNix.

**Candidate phased approach, not owner-approved product contract:**
- Baseline: measure actual 0.1047 3-5 end-to-end real jobs vs MKVToolNix, not feature names or fake previews; log duration/steps/error/semantic deltas and runtime cost;
- Preserve current user-facing no-special-mode import, candidate preview vs output membership and native quick flow. Define cross-source provenance and an ExpectedSemanticManifest from real source+edit intents, independent output oracle. Prefer one high-value cross-source attachment job before arbitrary audio multi-source timebase mergers.
- Extend browser capability-route FFmpeg.wasm/media, attachment-only writer, P2 bounded editor by verified *operation*, avoiding speculative general writer or backend modes in UI.
- Deepen output ASS/font closed-dependency check, real audio/video/subtitle byte+PTS and nested chapter/tag UID preservation, cross-device memory/saving;
- For every new scope item, distinguish benefit versus MKVToolNix, incremental engineering cost, user inconvenience, rollback, evidence, and owner authorization. Do not import candidate-only goals automatically into 1.0 S01–S14, don't retire verified legacy batch, don't assert all 44/57 failed because UNASSESSED.

**Evidence boundary:** This is a planning assessment grounded in live GitHub default branch README, latest merged PR descriptions and existing scope B; current assistant did not run new native/browser tests. Does NOT promote Canonical or change release contract; decision of thresholds/feature scope remains with owner. Dedup against existing Nov1 five-layer identity Observation, Nov1 UX-domain Candidate and 2026-10-12 browser-runtime Observation.
