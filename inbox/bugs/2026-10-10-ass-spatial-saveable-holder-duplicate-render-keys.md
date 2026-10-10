# Bug: Spatial canvas concurrently mounts duplicate SaveableStateProvider keys

Date: 2026-10-10
Status: Bug
Lifecycle: validation-pending
Project: `11576865/ASS-Workbench-Android`
Source: [PR #138](https://github.com/11576865/ASS-Workbench-Android/pull/138), head `ff81f273e7c4c6d9b3ffcaa4cdb80111ab29c96c`
Fix: [product PR #142](https://github.com/11576865/ASS-Workbench-Android/pull/142), merged into active redesign branch at `faf660dd5bff6777aa69b1abe6c6257bebc1a027`

## Reproduced product evidence

Android Emulator Regression [run 38027904104](https://github.com/11576865/ASS-Workbench-Android/actions/runs/38027904104) executed 120 tests, 22 failed. Android CI and the Fontconfig native probe both passed for the same source SHA. Several independent UI flows reported `IllegalArgumentException: Key <session>/<ToolInstance> was used multiple times` from `androidx.compose.runtime.saveable.SaveableStateHolderImpl`.

Specific failures included preview/tool switching, offscreen-media composition, an external tool-focus request, and spatial long-press parameter extraction. This failure class is **not** equivalent to the separate viewport-history assertions, tap injection errors or draft restoration tests within the same run.

## Source mechanism and submitted repair

`InfiniteCanvasHost` reused one `SaveableStateHolder` and `sessionId/entryId` across the board surface, native focused stage, media composition overlay and reference preview. Different presentation instances could thus register the same key concurrently during responsive navigation.

The product correction names saveable providers by their presentation role (`BOARD`, `FOCUSED`, `FOCUSED_LAYER`, `REFERENCE`), and adds an owner discriminator for layered/reference content. A pure JVM test checks uniqueness and identity stability; Android connected regressions exercise the affected UI paths. The `EditorViewModel`, domain ToolInstances, scene geometry and ASS Undo remain single-authority.

## Verification and generalization boundary

**Pending External Validation:** CI was queued for the merged repair head `faf660dd5bff6777aa69b1abe6c6257bebc1a027` (runs 38032991968 / 38032991970 / 38032992080). No emulator PASS, full draft continuity guarantee, device touch acceptance or 240 UI completion is asserted. In particular, distinct saveable keys avoid the duplicate-registration exception but do not prove continuity of ordinary unsaveable `remember` state across board↔focused role replacement.

This is one product's reproducible Bug evidence and candidate implementation test, not grounds for automatically changing Canonical UI policy.
