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
