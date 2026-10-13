# Observation — Media viewport fit and reconstruction-evidence attribution

Date: 2026-10-14
Status: Observation / patch inspection and user critique, not compiled UI or field bug
Product: 11576865/ASS-Workbench-Android
Source: user-supplied `ASS_Workbench_Unified_Container_UI_20261014(1).patch` (cumulative six commits), plus the assistant-produced source-reconstruction PNG (not real APK screenshot).
Canonical promotion: prohibited.

## Trigger

The user rejected the previous schematic screenshot: a large explicit “预览” label, several visible frames around the video, and a perceived waste of playable area contradicted the user's stated snug-fit preview requirement. The assistant had presented a source-inspired vector rendering as comparatively close to an actual Native UI despite no installed-build visual evidence.

## Distinguish design drawing from authored Kotlin

1. **Rendering-specific attribution:** the assistant-generated vector image amplified nested decoration and apparent inset margins. Those extra strokes/paddings and illustrated video are not evidence of exact Compose pixels.
2. **Code-grounded attribution:** `TabletWorkbenchPane(title="预览" | "位置 · 字幕 #...")` wraps `WorkbenchPreview` in a dedicated, at-least-48dp heading plus divider and a bordered `Surface`; after patch 3/6 the corner radius is 6dp (not the earlier 12dp). The content layout has an outer 8dp padding. `CompactWorkbenchLayout` also emits a separate “预览” label near its scale slider, creating potentially duplicated visible labels.
3. **Source aspect allocation risk:** `WorkbenchMediaStack` assigns remaining available media stack height to preview by `Modifier.weight(1f)`, and allocates 30% (bounded 180–240dp) to its timeline dock when enabled. The existing `WorkbenchPreview` delegates to `VideoPreview(fillViewport=true)`, which fits the video to its reported aspect ratio into a black `BoxWithConstraints` rather than sizing the parent panel from the media's aspect ratio. A tall panel can therefore contain unused letterbox area despite taking usable editor space. Letterboxing to preserve media pixels is not itself a defect; the unoptimized enclosing panel allocation is the UI question.
4. No native Android screenshot, renderer measurement or real user-device test for this exact patch has been established. Thus this remains a source-derived layout risk and a confirmed reconstruction misrepresentation, **not** a reproduced runtime bug.

## Reusable review practice / acceptance hypothesis

For a media-centered professional editor, test *actual content-to-panel occupancy* and edit-space tradeoffs, not just presence of the video, panel size and non-overlapping bounding rectangles. Distinguish semantic labels (accessibility can preserve them) from visible redundant headers. Prefer video aspect-informed preview sizing and allocating resulting remainder to timeline/editor rather than growing an ornamental background frame. Do not force stretch or crop merely to eliminate bars; the media aspect and true renderer results remain authoritative.

When showing a source reconstruction, tag visuals added for illustration separately from code-backed elements. Never imply a concept rendering proves actual Native screenshot fidelity. A future Android test should sample content bounds, top-level pane bounds, wasted area by viewport configuration, and verify video/ASS alignment.

## Dedupe

Foundry searches for 'redundant preview title panel frame aspect ratio letterbox', 'video view host content fit wasted space', and 'preview semantic label outside video controls chrome' produced no directly matching case or bug. Existing `inbox/observations/2026-10-13-ass-real-android-ui-video-comparison-and-spatial-anchors.md` discusses stable semantic anchors and video primacy; `inbox/candidates/2026-10-03-spatial-canvas-camera-semantic-zoom-gesture-ownership.md` covers zoom semantics, not this aspect-allocated host and screenshot provenance issue. New item recorded as Observation only.
