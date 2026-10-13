# Test: ASS design prototype task layouts, Host separation and long-press safety

Date: 2026-10-13
Status: Test / prototype only; local Chromium evidence, NOT production Android CI or device acceptance
Product: ASS Workbench UI redesign study 02
Relation: inbox/observations/2026-10-13-ass-primary-fixed-vs-spatial-experiment-ui-taxonomy-and-tool-coverage.md

## Subject and source
An offline, dependency-free HTML/CSS/JS prototype was created as a fallback after Figma Starter calls, MagicPath external-agent calls and Lovable project build-fix credits were exhausted. It is distinct from the Lovable project and current Kotlin APK. Owner-directed changes: fixed main editor, experimental canvas as separately routed Host, all 18 catalog keys through searchable directory, task-specific layouts and long-press icon explanations.

## Executed local browser checks
Runtime: Chromium / Playwright, viewport 1440×850 and 390×820.
- Six FIXED tasks (Event authoring, timing, typesetting, effects/Karaoke, resources/QC, batch/delivery) render without JavaScript page errors at both sizes. Each task uses materially different layout composition.
- Command palette lists exactly 18 WorkbenchTool keys; VECTOR_CLIP tool leads to a tool surface explicitly labelled partial support for existing paths.
- SPATIAL_EXPERIMENTAL is accessible through workspace switching but has zero main task tabs when active, and can return to FIXED.
- Mobile initial Event UI exposes preview. A first QA assertion failed because selecting an Event on mobile changed to editing mode but the inspector was never enabled. The prototype was corrected to set the inspector-visible flag alongside mobile editor mode. The subsequent Event row -> Raw editor regression passed.
- A 520ms touch pointerdown followed by pointerup and click shows the explanation and must **not** invoke button Save; a subsequent short click should invoke Save. First QA revealed missing notification persistence because an immediate screen rerender detached the toast. Fixed by preserving short-lived toast state across rerenders; subsequent interaction test passed.
- Mobile studio layout visually initially placed an absolute floating inspector above the video because a later CSS media rule overrode an earlier adaptive column rule. Corrected to a bounded inspector below the preview; browser screenshot reviewed.
- Font display: browser CJK glyphs were verified by screenshot rather than inferred from code.

## Boundaries
The test does not establish a native Android APK, real libass output, validated media decoding, file persistence, actual ASS geometry correctness, VoiceOver/TalkBack behavior, OEM long-press hardware behavior, or all responsive states. The offline demo's save/preview/batch actions are explicitly illustrative.
The Lovable attempt generated source but failed TypeScript build and cannot be presented as a working app. No Figma/MagicPath prior boards were overwritten.

## Reusable testing principle
Visual task diversity and discoverability require more than route snapshots:
(a) correct primary vs experimental Host ownership, (b) complete catalog tool reachability, (c) page-specific spatial composition,
(d) mobile row->editor transition, (e) long-press release does not execute action, (f) native/evidence provenance clearly labelled.
Take actual production or prototype screenshots after mutations. A web prototype check cannot be promoted into Android field evidence.

## Dedupe
Foundry searches 'mobile inspector overlay event list selection acceptance', 'prototype pointer long press suppressed click release', '18 tool directory separate experimental workspace', 'responsive multi-task layout authoring visual acceptance'. Existing Observation of current feedback and MagicPath Pending Bug are distinct: this file records **executed browser test failures and passing corrections for an independent offline prototype**.

No Canonical mutation. Future QA task: port approved UI principles to Android Compose only after user design review and test on specific SHA/device.
