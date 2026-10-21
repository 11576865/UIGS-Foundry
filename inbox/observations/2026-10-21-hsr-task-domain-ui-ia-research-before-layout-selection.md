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
