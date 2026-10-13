# Observation: Native task-specific specialist access instead of hiding tools in a global directory

Date: 2026-10-13
Status: Observation / source-level implementation and tests committed; CI/emulator still Pending
Product: 11576865/ASS-Workbench-Android, direct main commits

## Trigger
User asked for direct Kotlin/mainline implementation of tablet-first, compact, low-copy ASS UI. Existing toolbar showed five broad tasks and a global searchable catalog, yet POSITION, VECTOR_CLIP, FRAMES and KARAOKE required directory discovery even after entering their task. Constant tool descriptions also consumed space.

## Product-side source change
- `WorkbenchToolCatalog.kt`: contextualToolsFor derives only from existing WorkbenchTool entries and WorkbenchTask mapping; no new persistence IDs or business state.
- `WorkbenchTaskBar.kt`: task-local selector displays available specialized tools on tablet with current tool name and on compact UI as one accessible icon. Existing main tasks, global directory and preview switch retain their semantics, actions and test tags.
- `ModernEditorScreen.kt`: the directory retains group titles, search and action labels while long-press tooltip owns verbose descriptions instead of repeating them under every tool name.
- `WorkbenchToolCatalogTest.kt`: exact lists for TEXT/EVENT, TIME/FRAMES, TYPESETTING/STYLE/POSITION/VECTOR_CLIP, EFFECTS/KARAOKE and exclusions.
- `PresentationStateSmokeInstrumentedTest.kt`: checks Position and Vector Clip selections leave canonical ASS document and Focus unchanged.
- Mainline commit checkpoint: f22f4499229d518dd51257115266c76caaa5224c; follow-up task record .uigs/tasks/ass-native-ui-minimal-rollout-20261013.json.

## Reusable lesson and limits
Separating a task category from exact specialist tools need not entail a second tool registry: project the already persisted tool catalog into current task context. Prioritize a direct tappable route over an undiscoverable icon-only/help-only action; reserve long-press for *description*, not discovery or required commit. Preserve exact tool, object, scope and draft/commit distinctions. Size the compact selector with OEM touch target testing, not CSS pixel assumptions.

## Evidence status
GitHub file updates and authored JVM/instrumented tests verified as durable pushes. Neither native Gradle build nor instrumented device run was executed in this interaction. GitHub PR-scoped run lookup returned none, classic status empty: **Pending External Validation**, not passed CI. No APK or screenshot evidence claimed.

## Dedupe
Foundry searches included 'ASS fixed contextual specialist switcher discoverability', 'one tap specialist tool current task UI tool directory', 'few words icon only compact toolbar Android', and 'tooltip long press tool directory action discoverability'. Adjacent prior ASS control-grammar Observation covers principles but not this specific mainline implementation pattern and bounded tests.
No Canonical promotion.