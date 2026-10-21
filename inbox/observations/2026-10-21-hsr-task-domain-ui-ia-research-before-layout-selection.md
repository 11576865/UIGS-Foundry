# Observation — HSR UI redesign requires separating user tasks, domain objects and evidence states

Date: 2026-10-21
Project: `11576865/HSR-Voice-Archive-Builder`
Source baseline: `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`
Level: **Observation, source-grounded design research; not an approved Target, not Canonical**
Status: **Research complete at task/model level; user validation and UI choice Pending**

## Trigger and scope
The HSR owner explicitly deferred choosing between an audio editor, voice-archive manager or hybrid Studio, requesting fresh research of actual user tasks, information architecture, and interaction model **before** deciding the UI type. This work did not modify the HSR product, create a design PR, or claim user/device test success.

## Actual-source findings
- `app/static/index.html` implements six top-level workspace destinations: `project / review / layout / effects / export / update`. `layout` and `effects` are distinct navigation intents but share a single subtitle canvas, inspector, current cue and project state; this is explicitly asserted in `tests/test_hsr_ui_convergence.py`.
- The six destinations mix **project lifecycle**, **single-cue editorial operations**, **visual authoring tool families**, **publication/output operations**, and **future source maintenance**, rather than a uniform IA axis. This is a classification of the observed hierarchy, **not** proof that real users are dissatisfied.
- Product records and code support distinguishable state owners: source members and fingerprints, resolved sample Timeline, immutable source text vs official/API/hand-final overrides, optional per-word alignment provenance, project style parameters, real libass/video preview evidence, output/MKV publication receipts, cross-process jobs, and update candidates. `tests/test_hsr_navigation_save_gate.py` already protects source-member/project identity and unsaved-navigation constraints.
- Media preview, style save, ASS internal republish vs external copy, validated audio from sealed MKV, and final MKV delivery have distinct side effects/evidence levels. Their states cannot be safely collapsed into one generic `done` status. Product `README.md`, `docs/reliability.md`, `docs/subtitle-style-workbench-v15.md` and attached HSR engineering report dated 2026-10-16 provide scope; latest repository code is authoritative when older text differs.
- Source and test review found no user research data establishing feature frequency, task priority, task completion rates, user roles or optimal navigation count. No new UI screenshot/device acceptance was produced in this research.

## Not-yet-approved model
Organize design analysis into:
1. Global archive-library and job/runtime context;
2. Project-level source, readiness, attention, deliverable/verification;
3. Object/work-level identified voice entries, text provenance, segment time, preview and output-specific editor.

Compare **lifecycle-oriented**, **object-oriented**, and **task-context-oriented** candidate information architectures against the same concrete user journeys (first scan/create, cue proofreading, layout verification and republish, months-later update/recovery). Hold the choice of navigation, page count, visual aesthetics and device layouts pending task evidence.

This is a **product-specific design hypothesis**. It does not authorize unifying or deleting existing workspaces, remapping editors, introducing unconstrained freeform NLE waveform edits, or asserting new backend capabilities.

## Distinct reusable observation / dedup
- `inbox/cases/2026-10-15-hsr-studio-v3-rebuild-after-accepted-v2-rejection.md` already shows a visually validated/CI-green HSR workspace can fail real user acceptance and records concrete pane/navigation issues. This entry does not repeat that Case.
- `inbox/candidates/2026-10-17-source-anchored-actual-target-delta-diagrams.md` already defines source-anchored Actual/To-Be/Delta and a bidirectional UI-capability map, so this entry does not propose or promote a new general architecture method.
- `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md` already warns that simplifying surface controls cannot substitute for the right object/task model.

The new HSR-specific observation is that **the current product navigation combines heterogeneous classification dimensions**; the next redesign should test task paths against the separately owned *archive objects* and evidence/side-effect states before deciding product archetype. This is a falsifiable proposed audit, not a measured usability defect.

## Acceptance and Pending
- Build an As-Is user-action → handler/API → state owner → artifact/evidence table with commit-pinned source links.
- Observe real users or replay five representative tasks with real-scale project data; collect completion/navigation/error metrics, rather than inferring priority from screen appearance.
- Compare candidate IA clickable prototypes under desktop, tablet, and narrow windows without copying current six destinations blindly.
- Preserve real libass vs browser preview provenance, source identity, single editor ownership, and the non-destructive publication boundaries.

**No Canonical promotion. No approved final HSR IA.** No field UI, Android, or user acceptance evidence asserted.

## 2026-10-21 — Experimental native Figma prototype and explicit legacy-essence contract

**User direction:** Create a genuinely new experimental HSR UI in Figma **without losing the old UI's essence**. The owner has not approved a final interface archetype, product implementation or deletion of existing capabilities.

**Design artifact:** [HSR Voice Studio — Experimental UI / Preserve the Core](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx), new independent Figma Design file. HSR source baseline `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`, plus the task/domain report from 2026-10-21.

**Native editable frames:**
- `2:41` — Archive overview: Quick Scan and project choice, source health, actionable attention, separate trustworthy artifact state and global job context.
- `2:42` — Subtitle Studio: stage-first 807×454 (~16:9) frame, separate Layout/Effects intents, approximate vs true libass evidence, stage-owned Preview/Render/Save commands, current cue/PCM timing, separate Inspector. Red-cloud style is deliberately a **native editable abstract placeholder**, not the original reference photograph or a verified ASS preview frame.
- `2:43` — Proofreading: single final Chinese subtitle editor and human draft state, original voice playback waveform, immutable source/official-text comparison, stable entry identity.
- `2:44` — Delivery & update: one MKV with audio/video/subtitle verification and receipt, independent external exports, explicit subtitle staleness, conservative added/changed/conflicted update review.
- `10:14` — Legacy essence / migration contract: six old functional destinations mapped to four experimental contexts and explicit non-negotiables.

**Verification:** Figma screenshots of all four screens and the inheritance map were visually reviewed; the 16:9 studio's reference composition was toned down after inspection. Structural Figma read-back reports 176, 174, 181, and 110 native scene nodes in the four respective screens plus 37 in the inheritance map; no image-filled/UI-raster nodes; 15 local semantic color tokens and 3 editable reusable local components (`HSR / Button / Primary`, `Neutral`, and `Badge / Good`). These counts establish Figma document structure, not browser/runtime implementation or user acceptance.

**Essence preserved as a proposed interaction contract, not mere style:** authoritative source/cue identity; one final-CHS editor; real original WAV context; stage dominant and no layered nested viewport traps; approximate/true libass/on-audio preview must be distinct; save settings ≠ regenerate ASS ≠ republish MKV; last verified deliverable stays available when edit draft is newer; jobs visible across workspaces; update deltas require evidence before acceptance. A redesigned navigation is a **candidate organization**, not a claim that the original six activities were removed.

**Unverified / Pending:** the mock has no wired backend, no production interaction handlers, no responsive tablet/mobile variants, no user-approved visual direction, no Figma click-through prototype behaviors, and no on-device acceptance. Sample cue counts/percentages and media states are illustrative, not claims from an actual archive. Product GitHub code remains unchanged.

**Dedup:** this extends the present HSR domain/IA Observation. The pre-existing 2026-10-15 HSR V3/V4 Case already owns the historical user rejection/viewport defect, and the 2026-10-17 Actual/Target/Delta Candidate already owns the general method. No new Canonical; first get owner review of the editable Figma artifact, then use task walkthroughs to test navigation before implementation.

## 2026-10-21 — Native Figma Motion MP4 walkthrough of the experimental HSR UI

**User request:** Produce a demonstration video from the previously created HSR experimental Figma design, not a backend-enabled screen recording.

- Source design: [HSR editable experimental UI](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx), frames `2:41` archive, `2:43` proofreading, `2:42` subtitle studio, `2:44` delivery/update, `17:14` icon grammar, `10:14` old-to-new essence map.
- New native top-level Figma Motion timeline: [54.5-second video source node `26:168`](https://www.figma.com/design/UwCJi7ioyIUZbOBN13Z1bx?node-id=26-168), 1600×900 / 16:9. Each scene contains a cloned, editable Figma source screen, a separate Chinese explanatory side rail and manual opacity keyframes. Animated focus frames draw attention to task-specific operations; opening and closing cards are explicitly labeled as an experimental concept demo.
- Timeline duration 54.5 s; export invoked via Figma `export_video` at 18 FPS and medium quality. The server returned an MP4 `downloadUrl` and `availableUntil: 2026-10-28T06:49:34Z` (time-limited link), rather than permanent storage. Original Figma Motion timeline persists and can be re-exported after URL expiry.
- Motion verification: `get_motion_context` returned native per-scene opacity tracks, timing percentages and scene transition curves for `26:168`. A separate 3.5-s native Figma animation was successfully exported before composing the full tour.
- Scope disclosure is mandatory: animated UI frames demonstrate *intended navigation and feature semantics*, but they do not exercise actual HSR APIs, media files, real libass rendering, backend task execution, subtitle writes, or verified MKV output. No narration or actual user interactions. Desktop-only illustration; usability/device acceptance still Pending.
- Reusable production observation: retain native editable UI frames, create a standalone animated tour frame with Figma Motion tracks, and explicitly label speculative interactions. Figma MP4 exports use temporary signed URLs; the persistent source is the editable timeline file, not the generated asset link. No Canonical update.

Dedup: existing HSR Observation above governs domain and visual IA; separate HSR icon-density Candidate documents semantic role distinctions; this is evidence of an animated design communication output only, not new product functionality.
