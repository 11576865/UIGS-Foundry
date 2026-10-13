# Case: ASS UI v6.3 minimal-copy correction, NOT design freeze

Date: 2026-10-13
Status: Browser-tested prototype Case / NOT final / NOT Android implementation
Related: inbox/cases/2026-10-13-ass-ui-design-freeze-rc-prototype-honesty-and-handoff-gates.md
Related: inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md

## User correction
The user explicitly said '差不多该结束' did not mean approval to freeze. Serious UI problems remain, especially persistent verbose wording violating the user's '少字主义' requirement, under which explanations belong in long-press tooltips.

## Artifact
Offline HTML: /mnt/data/ASS_Workbench_UI_Prototype_v6_3.html; ZIP /mnt/data/ASS_Workbench_UI_Prototype_v6_3.zip; actual Chromium screenshot collage /mnt/data/ASS_Workbench_UI_v6_3_实际预览.jpg. No Android source edits.

## Evidence-grounded changes
- No more frozen/final status. Global chrome, Event draft and revision states are much shorter; mobile demo is visible and not duplicated with footer.
- Persistent tutorial/duplicate copy removed from inspector, Karaoke, effects, batch and preview. Core object identity, numeric parameters, units, write target and explicit destructive/commit verbs remain visible.
- Simulated video and audio are marked SIM, with detailed provenance in long-press help rather than a permanent paragraph.
- Karaoke's redundant half-width summary panel replaced with continuous proportionate timing/selected exact values and a simulated audio waveform aligned to the same cursor/time ruler.
- Animation submit changed to review-first flow: '审核修改' opens before/after Raw ASS modal; only explicit modal confirmation calls effect-commit.
- Tablet/compact spacing rebalanced; grip pointer targets widened. Full 18-tool directory and separate experimental infinite canvas host retained.

## Tests
- Local headless Chromium: 48/48 targeted checks across 1280x800, 800x1280, 390x820 and 360x780; 18 tools, draft A→B→A, modal before/after, no accidental click on long press.
- 50/50 supplemental checks: all six tasks, responsive overflow, separate host and review guard.
- Exact reports in /mnt/data/ASS_UI_Minimal_Iteration/test_report.json and extra_checks.json. Actual screenshots captured. Source JavaScript syntax check passed. No page errors observed.
- These are 98 overlapping browser checks, not independent product criteria or production Android/ASS results.

## Boundaries
Still a prototype. Real audio wave and scene are simulations; not decoded audio, actual libass, native Android Compose, real file persistence or OEM touch evidence. All complex ASS tag preservation remains native/domain scope. The design must not be called approved or frozen.

## Dedupe/governance
Foundry searches: 'ASS user minimal UI remove repeated labels show tooltip', 'Karaoke wave simulation prototyping title visibility', 'icon only tablet UI explanations long press duplicate status', 'ASS prototype text-dense frozen candidate correction'. Existing related items did not record this owner correction and tested v6.3 change. No Canonical promotion.