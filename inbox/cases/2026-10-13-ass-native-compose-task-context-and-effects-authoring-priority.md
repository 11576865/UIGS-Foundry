# Case: Native ASS Compose task-context specialist discoverability and effects priority

Date: 2026-10-13
Status: Case / source committed to Android main; **Pending External Validation** (CI, emulator, device)
Product: 11576865/ASS-Workbench-Android
Related: inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md
Related: inbox/cases/2026-10-13-ass-v6-3-minimal-ui-revision-not-design-freeze.md

## Trigger
User requested direct changes on main rather than continuing HTML mockups and then asked to continue. Owner's strict minimum-copy rule, tablet-first multi-pane workflows and all-18-professional-tools reachability remain priorities.

## Native implementation evidence
On main:
- Persisted WorkbenchTool identities remain unchanged. New contextualToolsFor(activeTool) projects the actual catalog onto task groups; row-level FIXED UI offers a drop-down with domain tools (TEXT+EVENT, TIMELINE+FRAMES, STYLE+POSITION+VECTOR_CLIP, EFFECTS+KARAOKE), while the complete directory remains available. Commit a41644dab1642fc652f1703fa50f3cd97fa584c1. This switcher is a projection, not a new domain registry or separate document state.
- ModernEditorScreen's InlineEffectsEditor put FxCompositionPane before the ordinary Blur/Fade/Transform editors, causing oversized advanced templates to push common task operations out of view. Commit b1ea4700b5c23f91d34d2ff72b16fdf1a44db841 moves advanced composition below the direct editors, shortens duplicated visible instructional text, and initializes \\t editing as expanded when existing transforms are present. Original ViewModel commit functions and ASS semantics are unchanged.
- Commit 3004d0888f96de8b7df907c48d2c3303e58934e2 introduces stable accessibility/test tags for Blur numeric control, Fade heading and Transform entry.
- Commit 0b1d197d6ddede7ba9d76f16f097c45ee41447c9 extends native EditorRegressionInstrumentedTest to assert all these are reachable and FxComposition remains accessible.

## Distinction between source and validation
GitHub source commits are confirmed; latest task checkpoint: .uigs/tasks/ass-native-ui-minimal-rollout-20261013.json, on main. One immediate commit status check returned empty statuses (not success). No Gradle build or Android emulator/device screenshot is proven by this record, so do not claim passing instrumentation. No native arbitrary ASS effects parser, new real libass writer or protocol migration is claimed.

## Reusable principle
For dense native creative tools, the location/order of interactive operations is a first-order feature-discoverability factor: direct daily edits precede advanced recipes. Short copy can reduce clutter without hiding safety or typed parameter meaning. Always couple UI hierarchy changes with stable semantic test tags and at least test cases, then seek real-device visual evidence. Specialist menu content should derive from an authoritative catalog and never silently add independent editing state.

## Dedupe/governance
Searches 'ASS Android fixed task contextual specialist switcher', 'native animation advanced FX composition below Fade Transform', 'ASS Compose minimal UI task tool discoverability', 'native effects form-first vs time editor' returned no existing exact native case. Previous observations covered the recommendation, not the committed native source and pending device outcome.
No Canonical promotion; external CI remains pending.
