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
