# Case: ASS native Transform interval handles and exact timing fallback

Date: 2026-10-13
Status: Native main code and tests committed; Pending External Validation
Product: 11576865/ASS-Workbench-Android
Prior: inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md

## Trigger and implementation
Owner requested continuing direct-main Android changes. Native Transform UI had exact Start/End/Accel fields but no touch interval manipulator, and its playhead-range status used persisted times instead of the uncommitted field draft.
- Source now offers a two-handle Material3 RangeSlider for exact in-Event integral-millisecond intervals; the numeric fields remain the authority. Handle drag updates draft and transient ViewModel preview, while only Apply writes source through the existing native domain Edit/Undo path. Live drag previews are throttled and final release flushes the last preview.
- Helper transformTimingHandleRange handles integer-looking domain Double strings such as 120.0, while fractional intervals, shorthand forms, out-of-Event values and long imprecise Float ranges have no slider and remain available as exact text.
- Feedback of playhead position in range is now calculated from drafted times, not only prior persisted transform. Duplicated persistent tutorial text was removed.

## Commits and test additions
724faaaff5eceda3b770c8a802d25d167aea34ed: pure range-eligibility helper.
0ff04ce3f9d38822470bbc3f03844642d4799b14: native Compose two-handle controller and preview.
228f16930942a92925c43ae2e58965ff12a2eec1: accept integer-double input syntax.
beddb37f4d08603ae11dec3ac998ffee34c4328a: JVM test for range/precision exclusions.
5768416cdcc0629a571b3dd93ce1d3672fcc9086: Android instrumentation to verify visibility and fractional fallbacks.
6a5f3c49fbcca45b3257798f3fd3fc1530cd6184: product task checkpoint.

## Evidence limitations
GitHub code and test file commits verified. Commit status check returned no statuses and no PR-triggered runs; build/emulator/native touch verification not established. Do not assert tests passed, user acceptance or libass correctness. Full source preservation remains dependent on existing domain authoring code.

## Reusable principle
Slider representation bounds are not domain validity bounds. A manipulation affordance must disappear rather than silently quantize representable ASS values; always retain exact editable fields, separate preview and Commit, and sample interaction state from draft.

## Dedupe
Foundry searches: Transform RangeSlider exact fractional ASS times native; Compose Transform timing handles preview not commit; ASS UI interval slider keep precise numeric input. Previous v5 HTML case is related but distinct from these native commits.
No Canonical promotion.